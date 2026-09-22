"""Retail-media monetization benchmark across three listed Indian marketplaces.

The core discipline of this script: compute an implied ad-revenue figure ONLY where
a company has disclosed ad revenue (not ad spend, not a blended take rate) as a
distinct percentage of GOV/GMV. Where that disclosure doesn't exist, output
INSUFFICIENT_DISCLOSURE rather than estimate one — the gap in disclosure quality
across these three companies is itself the finding.
"""
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = ROOT / "data" / "raw" / "marketplace_disclosures.csv"
OUT_PATH = ROOT / "outputs" / "tables" / "monetization_benchmark.csv"


def load(path: Path = SRC_PATH) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_benchmark(rows: list[dict]) -> list[dict]:
    by_company_segment: dict[tuple, dict] = {}
    for r in rows:
        key = (r["company"], r["segment"])
        by_company_segment.setdefault(key, {}).update({r["metric_type"]: r})

    results = []
    for (company, segment), metrics in by_company_segment.items():
        gov_row = metrics.get("gov_gmv")
        ad_pct_row = metrics.get("ad_revenue_pct_of_gov") or metrics.get("ad_revenue_pct_of_gov_TARGET")

        if gov_row is None:
            continue  # no scale figure at all for this company/segment — skip, don't guess

        row = {
            "company": company,
            "segment": segment,
            "period": gov_row["period"],
            "gov_gmv_inr_crore": gov_row["value"],
            "gov_source": gov_row["source"],
        }

        if ad_pct_row is None:
            row["ad_revenue_pct_of_gov"] = "INSUFFICIENT_DISCLOSURE"
            row["implied_ad_revenue_inr_crore"] = "INSUFFICIENT_DISCLOSURE"
            row["basis"] = "No standalone ad-revenue-as-%-of-GOV disclosure found in sources reviewed this session"
        else:
            pct = float(ad_pct_row["value"])
            is_target = ad_pct_row["metric_type"].endswith("_TARGET")
            implied = round(float(gov_row["value"]) * pct / 100, 1)
            row["ad_revenue_pct_of_gov"] = f"{pct}% {'(forward target, not current actual)' if is_target else '(disclosed floor, >=)'}"
            row["implied_ad_revenue_inr_crore"] = implied
            row["basis"] = ad_pct_row["notes"]

        results.append(row)
    return results


if __name__ == "__main__":
    rows = load()
    benchmark = build_benchmark(rows)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["company", "segment", "period", "gov_gmv_inr_crore", "ad_revenue_pct_of_gov",
                  "implied_ad_revenue_inr_crore", "basis", "gov_source"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(benchmark)

    print(f"{len(benchmark)} company/segment rows with a disclosed GOV figure.\n")
    for row in benchmark:
        print(f"{row['company']} — {row['segment']} ({row['period']}): "
              f"GOV INR {row['gov_gmv_inr_crore']}cr | "
              f"Ad revenue: {row['ad_revenue_pct_of_gov']} "
              f"{'= INR ' + str(row['implied_ad_revenue_inr_crore']) + 'cr' if row['implied_ad_revenue_inr_crore'] != 'INSUFFICIENT_DISCLOSURE' else ''}")

    n_disclosed = sum(1 for r in benchmark if r["ad_revenue_pct_of_gov"] != "INSUFFICIENT_DISCLOSURE")
    print(f"\n{n_disclosed} of {len(benchmark)} company/segment rows have a usable standalone ad-revenue disclosure.")
    print(f"Written -> {OUT_PATH}")
