# Data Dictionary

## `data/raw/marketplace_disclosures.csv`

| Field | Description |
|---|---|
| `company` | Swiggy, Nykaa (FSN E-Commerce), or Eternal (Zomato/Blinkit) |
| `segment` | Business segment, where disclosed separately |
| `period` | Fiscal period the figure covers |
| `metric` | Plain-language name of the disclosed figure |
| `value`, `unit` | The figure and its unit (INR_crore, pct) |
| `metric_type` | The field that drives the benchmark logic — see below |
| `source` | Citing report/press outlet |
| `notes` | Scope, caveats, or why a figure was excluded |

### `metric_type` values

| Value | Meaning |
|---|---|
| `gov_gmv` | A directly disclosed scale figure — usable as the benchmark's denominator |
| `ad_revenue_pct_of_gov` | A disclosed, current, standalone ad-revenue-as-%-of-GOV figure — the only kind used to compute an implied revenue number |
| `ad_revenue_pct_of_gov_TARGET` | Same, but explicitly a forward-looking target, not a current actual — used, but always labelled as a target |
| `ad_SPEND_not_ad_revenue_EXCLUDED` | The company's own advertising *spend* — recorded to document the distinction, never used in the benchmark calculation |
| `bundled_revenue_not_ad_only` | A revenue line that bundles ads with other services — not usable as a pure ad-revenue figure |
| `blended_take_rate_not_ad_only` | Commentary attributing take-rate growth partly to ads, without a standalone figure — directional only |
| `revenue` | Company/segment revenue, not the same as GOV/GMV |

## `outputs/tables/monetization_benchmark.csv`

One row per company/segment with a disclosed GOV/GMV figure. `ad_revenue_pct_of_gov` and
`implied_ad_revenue_inr_crore` are either a real computed figure or the literal string
`INSUFFICIENT_DISCLOSURE`.
