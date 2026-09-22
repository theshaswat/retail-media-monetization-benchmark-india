# Retail Media Monetization Benchmark, India — The Number Two of Three Don't Disclose

> Benchmarking retail-media ad monetization — advertising revenue as a percentage of
> GOV/GMV — across three listed Indian marketplaces, built entirely from their own public
> disclosures. Only one of the three discloses it. The other two disclose a number that
> looks like it and is its mirror image.

## Question

Retail media is the margin story attached to every Indian marketplace right now. What does
the ad take actually look like as a share of platform volume, and can it be benchmarked
across Swiggy, Nykaa and Eternal from what each company publishes?

## Findings

| Company / segment | Period | GOV / GMV | Ad-revenue disclosure | Implied ad revenue |
|---|---|---|---|---|
| Swiggy — Food Delivery | Q4 FY26 | ₹9,005cr | **≥4%** (disclosed floor) | **≥₹360.2cr** |
| Swiggy — Quick Commerce (Instamart) | Q4 FY26 | ₹7,881cr | **6.5%** (forward target, 6–7% range) | **₹512.3cr** at midpoint |
| Nykaa (FSN E-Commerce) | FY26 | ₹19,963cr | `INSUFFICIENT_DISCLOSURE` | — |
| Eternal (Zomato / Blinkit) | Q4 FY26 | Revenue ₹17,292cr | `INSUFFICIENT_DISCLOSURE` | — |

**The benchmark has one clean row because only one company supplies one.** Swiggy
discloses advertising revenue as a standalone percentage of GOV. Nykaa and Eternal do not
— and both disclose a figure that is easy to mistake for it: their own advertising
**spend**, the money they pay Google, Meta and others to advertise themselves. Nykaa's
₹995cr (FY25) and Eternal's ₹936cr (Q4 FY26) sit on the opposite side of the transaction
from ad revenue, which is money brands pay *them* for placements on their platforms.

Both figures are recorded in the source register and **excluded from every calculation**,
with the reason stored in the data rather than only in the prose. Two further figures are
excluded on the same principle: Swiggy's FY26 platform services revenue of ₹11,927cr
bundles order facilitation, delivery income, advertising, onboarding and service charges
into one line, and Eternal's 31% FY25 take rate is blended across the business with ad
revenue never broken out.

A three-row table built by treating advertising expense as advertising revenue would have
looked complete and been wrong by construction. This version is less tidy and states what
is not known.

Also note the Instamart row is a **forward target Swiggy set for itself, not a current
actual**, and is labelled that way in the output file, not only here. Blinkit's segment
revenue of ₹13,232cr reflects an inventory-led model adopted from Q1 FY26 — it captures
the full value of goods sold rather than a commission, so it is not comparable to a
GOV-based ad-take metric without adjustment this pass does not make.

Full reasoning: [`reports/01_RECOMMENDATION_MEMO.md`](reports/01_RECOMMENDATION_MEMO.md).
One-page version: [`reports/00_EXECUTIVE_SUMMARY.md`](reports/00_EXECUTIVE_SUMMARY.md).

## Method

`src/benchmark.py` loads the disclosure file, groups by company and segment, and computes
an implied ad-revenue figure **only** where an `ad_revenue_pct_of_gov` row — or an
explicitly labelled `_TARGET` row — exists for that segment. Every other case is written
out as `INSUFFICIENT_DISCLOSURE`. Nothing is estimated, interpolated from a peer, or
inferred from a blended metric.

The discipline is carried in the schema rather than in the analyst's memory: every row in
`data/raw/marketplace_disclosures.csv` carries a `metric_type`, and the values
`ad_SPEND_not_ad_revenue_EXCLUDED`, `bundled_revenue_not_ad_only` and
`blended_take_rate_not_ad_only` make the exclusions explicit in the data itself. A later
reader cannot pick up the ad-spend figure and use it as revenue without overriding a field
that says not to.

## Structure

```
retail-media-monetization-benchmark-india/
├── data/raw/          # marketplace_disclosures.csv — 11 rows, each with
│                      # metric_type, source and exclusion rationale
├── src/
│   ├── benchmark.py   # groups disclosures, computes implied ad revenue
│   │                  # only where a clean disclosure exists
│   └── build_pdf.py   # renders reports/*.md to PDF
├── outputs/tables/    # monetization_benchmark.csv
├── dashboards/        # dashboard.html — GOV scale vs. disclosure quality
└── reports/           # executive summary, memo, data dictionary,
                       # source register, limitations (.md + .pdf)
```

## How to run

```bash
pip install -r requirements.txt
cd src
python3 benchmark.py     # -> outputs/tables/monetization_benchmark.csv
python3 build_pdf.py     # -> reports/*.pdf
```

## Data and sources

`data/raw/marketplace_disclosures.csv` — 11 rows drawn from each company's own results
disclosures (press releases, investor materials and shareholder letters), and from
reputable secondary reporting of those same disclosures where the primary document could
not be parsed. Every row records its source and, where applicable, why it was excluded.

Full register: [`reports/03_SOURCE_REGISTER.md`](reports/03_SOURCE_REGISTER.md).
Field definitions: [`reports/02_DATA_DICTIONARY.md`](reports/02_DATA_DICTIONARY.md).

## Limitations

Full detail in [`reports/LIMITATIONS.md`](reports/LIMITATIONS.md). Headline items:

- **One usable company.** With only Swiggy disclosing cleanly, this is a benchmark with a
  single clean observation plus one forward target — a finding about disclosure quality
  across the sector, not a peer-group rate table.
- **Two primary PDFs could not be parsed** in this build (Nykaa's and Eternal's Q4 FY26
  investor materials), so those companies' figures rest on press releases and shareholder
  letters as summarised by financial press rather than on directly re-parsed primary
  documents.
- **The Instamart figure is a company target, not an actual**, and the Food Delivery figure
  is a disclosed floor (">4%"), not a point estimate.
- **No CPM rate card or media proposal is derived**, because none of the three companies
  discloses impression or traffic volume — the denominator a CPM requires simply is not
  public.

## Author

**Shaswat Sharma** — [GitHub: theshaswat](https://github.com/theshaswat)

## License

MIT (see [`LICENSE`](LICENSE)).
