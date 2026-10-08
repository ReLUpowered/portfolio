# Booking Flow Demo — Web app sample (portfolio demo)

A complete multi-step booking flow in a single self-contained `index.html` — the kind of widget a service business (plumber, salon, repair shop) embeds on their site to take appointments without phone tag.

## The flow

1. **Details** — name, phone (validated), service picker
2. **Pick a time** — 7-day picker (skips Sundays) + time-slot grid with "full"/"open" states
3. **Review** — summary of everything before committing, optional notes field
4. **Confirmation** — booking reference number, recap, "book another" reset

## Techniques demonstrated

- **Multi-step state machine** — a single `state` object carried across panes; back-buttons never lose data
- **Client-side validation** — inline errors on name/phone, slot selection enforced before review
- **Deterministic demo data** — "full" slots derived from the date so the demo is stable (not random each load)
- **XSS-safe rendering** — user input escaped before being injected into the summary
- **localStorage persistence** — last booking saved locally (shows awareness of real-world needs)
- **Simulated async submit** — loading state on the confirm button, then a confirmation screen (in production: swap the `setTimeout` for a `fetch()` to any booking API)

## To preview

Open `index.html` in any browser — no server, no build, no dependencies.

## For clients

This is the front-end half of a real booking system. The back-end half (slot availability API, SMS confirmations, calendar sync, no-show reminders) is a natural fixed-price follow-on project — which is exactly how small demo builds turn into bigger contracts.

*Fictional business, fictional data — built as a portfolio sample.*
