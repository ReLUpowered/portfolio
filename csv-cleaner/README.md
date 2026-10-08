# CSV Cleaner — Python data-cleaning utility (portfolio demo)

A command-line tool that cleans the messy CSV exports small businesses actually deal with: duplicate rows, invalid emails, inconsistent phone formats, mixed date formats, stray whitespace, wrong casing.

## What it does

| Problem | Fix |
|---|---|
| Exact-duplicate rows | Dropped (configurable: dedupe on all columns or key columns like `email`) |
| `"  alice "` / `"SMITH"` | Whitespace stripped; optional lowercase / title-case per column |
| `ALICE@Example.COM` | Lowercased for consistency |
| `bob AT example.com` | Invalid emails detected and dropped (configurable column) |
| `(828) 555-0142`, `18285550142` | Normalized to `8285550142` |
| `2026/10/01`, `Oct 3 2026` | Normalized to `2026-10-01` (unparseable ones reported) |
| Fully-empty rows | Dropped |

## Try it

```bash
pip install pandas
python csv_cleaner.py sample_messy.csv \
  --dedupe-cols email --email-col email \
  --phone-col phone --date-col order_date \
  --lower-cols email --title-cols first_name,last_name,city \
  --report
```

`sample_messy.csv` → `sample_cleaned.csv`, with a printed report of everything changed:

```
--- cleaning report ---
rows_in                  7
invalid_emails_dropped   3
unparseable_dates        3
duplicates_dropped       1
rows_out                 3
```

## Techniques demonstrated

- **pandas** for real-world data wrangling (not toy examples)
- **argparse CLI** — 10 options, sensible defaults, `--help` text
- **Defensive I/O** — clear errors for missing/malformed files, never a traceback for user mistakes
- **Composable transforms** — each cleaning step is a small pure function, easy to extend
- **Reporting** — every run can print exactly what changed, so clients can audit the output

## For clients

Typical engagements this maps to: cleaning a mailing list before an email campaign, deduping a CRM export after a merger, normalizing supplier catalogs, prepping sales data for reporting. Fixed-price or hourly — the script is the deliverable *and* the proof I can build it.
