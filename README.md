# Retail Media Monetization Benchmark, India

**Status: Phase 1–4 complete** for the benchmark itself. Data sourced, engine built, reports
written and available as both Markdown and PDF, dashboard built (`dashboards/dashboard.html`).
Resume-ready line is in `reports/00_EXECUTIVE_SUMMARY.pdf`. **Not done:** the CPM-based rate card
and media proposal template — see Limitations for why (no company discloses impression/traffic
volume).

## What this is

A benchmark of retail-media ad monetization (ad revenue as a % of GOV/GMV) across three listed
Indian marketplaces — Swiggy, Nykaa (FSN E-Commerce), and Eternal (Zomato/Blinkit) — built entirely
from each company's own public disclosures (annual reports, investor presentations, shareholder
letters, and reputable secondary reporting of the same).

## Headline finding

**Of the three marketplaces reviewed, only Swiggy discloses advertising revenue as a clean,
standalone percentage of GOV.** Nykaa and Eternal do not — and, critically, both of them *do*
disclose a number that is easy to mistake for ad revenue but isn't: their own **advertising spend**
("AdEx" — money they pay Google/Meta/etc. to advertise themselves), which is the opposite side of
the transaction from ad **revenue** (money brands pay them for placements). This project deliberately
records those ad-spend figures in the source register and **excludes them from the benchmark
calculation** rather than mistaking one for the other.

**Usable result (from Swiggy's own disclosures):**
- Food Delivery, Q4 FY26: GOV ₹9,005cr × ≥4% (disclosed floor) = **≥₹360.2cr implied quarterly ad revenue**
- Quick Commerce (Instamart), Q4 FY26: GOV ₹7,881cr × 6.5% (Swiggy's own **forward target**, not
  current actual) = **₹512.3cr implied**, clearly labelled as a target-based projection

Nykaa (GMV ₹19,963cr, FY26) and Eternal (revenue ₹17,292cr, Q4 FY26) appear in the source register
with their real scale figures, but their ad-revenue line is marked `INSUFFICIENT_DISCLOSURE` rather
than estimated.

## Data

`data/raw/marketplace_disclosures.csv` — 11 rows, each tagged with a `metric_type` that forces the
ad-spend/ad-revenue distinction to be explicit in the data itself, not just in prose. Two primary PDF
sources (Nykaa's and Eternal's Q4 FY26 investor materials) could not be parsed this session — see
Limitations — so this benchmark relies on the companies' own press releases/shareholder letters as
summarized by financial press, not on directly re-parsed primary PDFs.

## How it works

`src/benchmark.py` loads the disclosures, groups by company/segment, and computes an implied
ad-revenue figure **only** where a `ad_revenue_pct_of_gov` (or explicitly-labelled `_TARGET`) row
exists — every other case is written as `INSUFFICIENT_DISCLOSURE`, never estimated.

## Reports (Phase 3–4)

`reports/00_EXECUTIVE_SUMMARY.{md,pdf}`, `01_RECOMMENDATION_MEMO.{md,pdf}`,
`02_DATA_DICTIONARY.{md,pdf}`, `03_SOURCE_REGISTER.{md,pdf}`, `LIMITATIONS.{md,pdf}`. Dashboard:
`dashboards/dashboard.html` (GOV scale vs. disclosure-quality badges).

## Note on this rebuild

`data/`, `src/`, `outputs/`, `.git/`, and this README were found missing from disk partway through
this build session — `reports/` and `dashboards/` (the most recently written folders) were still
present. Cause unconfirmed; possibly iCloud Desktop-sync eviction, since this whole portfolio lives
under `~/Desktop`. Everything above was reconstructed from this session's own record and re-verified
(`benchmark.py` re-run, numbers match exactly). **Worth checking iCloud Drive sync status for
`~/Desktop/Profile Projects /`** if files go missing again elsewhere in the portfolio.

## Author

**Shaswat Sharma** — [GitHub: theshaswat](https://github.com/theshaswat)

## License

MIT (see [`LICENSE`](LICENSE)).
