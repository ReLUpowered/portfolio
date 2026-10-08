#!/usr/bin/env python3
"""
csv_cleaner.py — Clean, dedupe, and normalize messy CSV files.

A practical data-cleaning utility for small businesses: sales exports,
mailing lists, CRM dumps, supplier catalogs. Handles the real-world mess —
duplicate rows, inconsistent casing, stray whitespace, junk characters in
phone numbers, and mixed date formats.

Usage:
    python csv_cleaner.py INPUT.csv [options]

Options:
    -o, --output FILE     Output path (default: INPUT_cleaned.csv)
    --dedupe-cols C1,C2   Columns that define a duplicate (default: all columns)
    --email-col COL       Column holding emails (validates + drops invalid)
    --phone-col COL       Column holding phones (normalizes to digits)
    --date-col COL        Column holding dates (normalizes to YYYY-MM-DD)
    --lower-cols C1,C2    Columns to lowercase (e.g. email)
    --title-cols C1,C2    Columns to title-case (e.g. name, city)
    --report              Print a cleaning report to stdout
    -q, --quiet           Only print errors

Examples:
    # Basic: trim whitespace, drop exact-duplicate rows
    python csv_cleaner.py customers.csv

    # Mailing list: dedupe on email, validate emails, title-case names
    python csv_cleaner.py leads.csv --dedupe-cols email --email-col email \\
        --title-cols first_name,last_name,city --report

    # Sales export: normalize phones and dates too
    python csv_cleaner.py orders.csv --phone-col phone --date-col order_date \\
        -o orders_clean.csv --report

Requires: Python 3.8+ and pandas (`pip install pandas`).
"""

import argparse
import re
import sys
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    sys.exit("pandas is required: pip install pandas")


def clean_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from every string cell."""
    return df.apply(
        lambda col: col.str.strip() if col.dtype == object else col
    )


def normalize_case(df: pd.DataFrame, lower=(), title=()) -> pd.DataFrame:
    """Lowercase / title-case the given columns (skips missing cols)."""
    for col in lower:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().replace("nan", pd.NA)
    for col in title:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title().replace("nan", pd.NA)
    return df


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def validate_emails(df: pd.DataFrame, col: str):
    """Return (df, dropped_count): drop rows whose email is invalid."""
    if col not in df.columns:
        return df, 0
    mask = df[col].astype(str).str.match(EMAIL_RE, na=False)
    dropped = int((~mask).sum())
    return df[mask].copy(), dropped


def normalize_phones(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Strip non-digits; drop a leading US country '1' on 11-digit numbers."""
    if col not in df.columns:
        return df

    def _norm(v):
        digits = re.sub(r"\D", "", str(v))
        if len(digits) == 11 and digits.startswith("1"):
            digits = digits[1:]
        return digits if digits else pd.NA

    df[col] = df[col].apply(_norm)
    return df


def normalize_dates(df: pd.DataFrame, col: str):
    """Coerce mixed date formats to YYYY-MM-DD. Returns (df, failed_count)."""
    if col not in df.columns:
        return df, 0
    parsed = pd.to_datetime(df[col], errors="coerce")
    failed = int(parsed.isna().sum() - df[col].isna().sum())
    df[col] = parsed.dt.strftime("%Y-%m-%d")
    return df, failed


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean and dedupe messy CSV files.")
    ap.add_argument("input", help="Input CSV path")
    ap.add_argument("-o", "--output", help="Output CSV path (default: INPUT_cleaned.csv)")
    ap.add_argument("--dedupe-cols", default="",
                    help="Comma-separated columns defining a duplicate (default: all columns)")
    ap.add_argument("--email-col", default="", help="Column with email addresses")
    ap.add_argument("--phone-col", default="", help="Column with phone numbers")
    ap.add_argument("--date-col", default="", help="Column with dates")
    ap.add_argument("--lower-cols", default="", help="Columns to lowercase")
    ap.add_argument("--title-cols", default="", help="Columns to title-case")
    ap.add_argument("--report", action="store_true", help="Print cleaning report")
    ap.add_argument("-q", "--quiet", action="store_true", help="Suppress progress output")
    args = ap.parse_args()

    def log(*a):
        if not args.quiet:
            print(*a, file=sys.stderr)

    try:
        df = pd.read_csv(args.input, dtype=str, keep_default_na=True)
    except FileNotFoundError:
        sys.exit(f"error: file not found: {args.input}")
    except Exception as e:  # malformed CSV etc.
        sys.exit(f"error: could not read {args.input}: {e}")

    rows_in = len(df)
    stats = {"rows_in": rows_in}

    df = clean_whitespace(df)
    df = normalize_case(
        df,
        lower=[c.strip() for c in args.lower_cols.split(",") if c.strip()],
        title=[c.strip() for c in args.title_cols.split(",") if c.strip()],
    )

    if args.email_col:
        df, dropped = validate_emails(df, args.email_col)
        stats["invalid_emails_dropped"] = dropped
    if args.phone_col:
        df = normalize_phones(df, args.phone_col)
    if args.date_col:
        df, failed = normalize_dates(df, args.date_col)
        stats["unparseable_dates"] = failed

    dedupe_cols = [c.strip() for c in args.dedupe_cols.split(",") if c.strip()]
    before = len(df)
    df = df.drop_duplicates(subset=dedupe_cols or None, keep="first")
    stats["duplicates_dropped"] = before - len(df)

    # drop fully-empty rows that add nothing
    before = len(df)
    df = df.dropna(how="all")
    stats["empty_rows_dropped"] = before - len(df)

    out = args.output or re.sub(r"\.csv$", "", args.input, flags=re.I) + "_cleaned.csv"
    df.to_csv(out, index=False)
    stats["rows_out"] = len(df)
    stats["output"] = out

    log(f"done: {rows_in} → {len(df)} rows → {out}")
    if args.report:
        print("\n--- cleaning report ---")
        for k, v in stats.items():
            print(f"{k:24} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
