# Retail Media Monetization Benchmark, India — Recommendation Memo

## Why this project

Built for the Tata CLiQ Monetization Intern application (retail-media reporting and brand-pitch
market research) and directly relevant to equity research roles, where ad monetization is a live
theme for Indian internet-platform coverage. The question: how much ad revenue does an Indian
marketplace extract per rupee of GOV, benchmarked against comparable listed companies.

## Methodology

1. **Source three listed marketplaces' own disclosures** — annual reports, investor presentations,
   shareholder letters, and (where primary PDFs didn't parse) reputable financial-press summaries of
   the same filings.
2. **Tag every disclosed figure by `metric_type`** in `data/raw/marketplace_disclosures.csv` —
   `gov_gmv`, `ad_revenue_pct_of_gov`, `ad_revenue_pct_of_gov_TARGET` (forward-looking, not current),
   `ad_SPEND_not_ad_revenue_EXCLUDED`, `bundled_revenue_not_ad_only`, `blended_take_rate_not_ad_only`.
   This forces the ad-spend/ad-revenue distinction into the data itself, not just into prose that's
   easy to skim past.
3. **Compute an implied ad-revenue figure only where both a GOV figure and a standalone ad-revenue-%
   figure exist for the same company/segment** (`src/benchmark.py`). Every other case is written as
   `INSUFFICIENT_DISCLOSURE`, never estimated.

## Results

Swiggy is the only company with a standalone ad-revenue-as-%-of-GOV disclosure: ≥4% in food delivery
(a disclosed floor — the real figure could be higher), and a forward target of 6-7% in quick
commerce (explicitly described as an expectation, not a current achieved figure — used at the 6.5%
midpoint and labelled as a target throughout). Applied to real Q4 FY26 GOV (Food Delivery
INR 9,005cr, Instamart INR 7,881cr), this implies ≥INR 360.2cr and INR 512.3cr respectively.

Nykaa's GMV is well disclosed (FY25 INR 15,604cr, FY26 INR 19,963cr) but no standalone ad-revenue
line was found — only its own INR 995cr FY25 marketing/ad *spend* figure, which is the wrong side of
the transaction and was excluded. Eternal's revenue is disclosed (Q4 FY26 INR 17,292cr, Blinkit
INR 13,232cr) but not a GOV/GMV figure comparable to the other two — and Blinkit's move to an
inventory-led accounting model from Q1 FY26 makes its revenue figure not directly comparable to a
GOV-based metric without further adjustment not attempted here.

## What broke

Two primary-source PDFs (Nykaa's Q4 FY26 investor presentation, Eternal's Q4 FY26 shareholder
letter) were fetched but didn't parse: one returned only its digital-signature certificate metadata,
the other exceeded the fetch tool's size limit. Rather than guess at their contents or fall back to
unreliable numbers, this project relies on financial-press summaries of the same underlying filings
and documents the limitation plainly — see `LIMITATIONS.md`.

The more consequential "what broke": an early read of the search results nearly used Nykaa's and
Eternal's disclosed "AdEx"/ad-spend figures as if they were ad-revenue figures, which would have
produced a clean-looking but wrong three-company table. Re-reading the source context (these are
figures about money the companies spend advertising themselves, not revenue they earn from brands)
caught the error before it reached the data file.

## What this demonstrates for the role

The habit the JD actually tests for — read a company's own disclosure carefully enough to know what
it does and doesn't say, rather than pattern-matching a plausible-looking number into a benchmark
table. This is the same discipline as the RTO revenue-basis catch and the RBI ECL reconciliation
elsewhere in the portfolio.
