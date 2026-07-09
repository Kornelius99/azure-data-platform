# Data Quality Framework

The platform includes a reusable PySpark data quality module (`src/data_quality/checks.py`) used as a gate between medallion layers. It is intentionally dependency-light (pure PySpark) so it can run inside any Databricks cluster without extra libraries, alongside heavier tools like Great Expectations if adopted later.

## Checks implemented

1. **Completeness** — percentage of nulls per configured column against a threshold; fails the batch if a mandatory field (e.g. `order_id`, `customer_id`) exceeds the allowed null rate.
2. **Uniqueness** — verifies primary/business keys have no duplicate values after silver deduplication.
3. **Referential integrity** — confirms foreign keys in a fact/child table exist in the corresponding dimension/parent table (e.g. every `product_id` in sales exists in the product dimension).
4. **Freshness** — checks the max ingestion timestamp in a table against an expected SLA window, flagging stale data.
5. **Row-count anomaly detection** — compares today's load volume against a trailing average and flags loads that deviate beyond a configurable percentage, catching silent upstream failures.

## Output

Each check returns a structured result (check name, status, metric value, threshold) which is aggregated into a single quality report per run. In this repo the report is printed/logged; in production it would be written to a monitoring Delta table and surfaced through Log Analytics/Power BI alerts, and a failing report can block promotion to the next medallion layer.

## Why a custom framework alongside ADF monitoring

ADF monitors pipeline/activity-level success or failure (did the copy/notebook run complete). This framework checks the *content* of the data itself, which is a different and complementary concern. Together they give both operational monitoring and data trust, which is what supports the "data quality and lineage" and "stakeholder trust in reported metrics" responsibilities on the CV.
