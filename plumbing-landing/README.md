# FlowRight Plumbing — Landing Page (portfolio demo)

A complete, mobile-responsive small-business landing page built as a single self-contained `index.html` (no build step, no dependencies, no frameworks).

## What's inside

| Section | Detail |
|---|---|
| Sticky header | Logo, nav links, CTA button, mobile hamburger menu |
| Hero | Headline, subhead, dual CTA, trust badges |
| Emergency strip | 24/7 banner with tap-to-call |
| Services grid | 6 services with "from" pricing, hover effects |
| How-it-works | 3-step process cards |
| Reviews | Testimonial cards with star ratings |
| Quote form | Validated lead-capture form with inline error/success states |
| FAQ | Accessible accordion |
| Footer | Contact, service area, license info |
| Floating call button | Sticky tap-to-call on mobile |

## Techniques demonstrated

- **Pure HTML/CSS/JS** — zero dependencies, loads instantly, works anywhere
- **Mobile-first responsive** — hamburger nav, stacking grids, tap-friendly targets
- **Form validation** — required-field + phone-format checks in vanilla JS
- **SEO basics** — semantic markup, meta description, descriptive headings
- **Conversion patterns** — sticky CTA, social proof placement, urgency strip, single clear ask per section

## To preview

Just open `index.html` in any browser — or serve it:

```bash
cd plumbing-landing
python3 -m http.server 8000
# → http://localhost:8000
```

## Customization notes (for clients)

- Phone number, license #, service area, and pricing are placeholder content — swap in real details
- Colors live in `:root` CSS variables — rebrand in under 5 minutes
- The quote form currently validates client-side only; wire the `submit` handler to any endpoint (Formspree, Netlify Forms, or a backend API)

*All business details on this page are fictional — built as a portfolio sample.*
