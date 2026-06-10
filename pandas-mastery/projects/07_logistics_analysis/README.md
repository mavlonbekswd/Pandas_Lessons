# Project 07 — Logistics Analysis (Aurora Outfitters)

*Part of the main investigation.* The operations team suspects late deliveries
are driving returns and complaints. Prove or disprove it.

## Business problem
Which **carrier** and **warehouse** are dragging down delivery performance, and
does lateness correlate with returns?

## Dataset
`../../datasets/raw/shipments.csv` (+ `orders.csv`, `returns.csv`). See
`../../datasets/docs/DATA_DICTIONARY.md`.

## Tasks
1. Parse `promised_date` and `shipped_date`; compute `days_late = shipped - promised`.
2. Flag `is_late` (shipped after promised). Late-delivery **rate** per carrier and per warehouse.
3. Join shipments to `returns` — is the return rate higher for late shipments?
4. A chart that argues: late-rate by carrier (sorted bar) + a takeaway title.
5. One-paragraph recommendation tied to a number.

## Hints
- `pd.to_datetime(..., errors="coerce")` then `.dt.days`.
- Late rate = `is_late.mean()` within a `groupby`.
- For task 3, build a per-order `is_late` and `is_returned`, then `crosstab(normalize="index")`.

## Self-check
```python
assert 0 <= late_rate_by_carrier.max() <= 1
```
Full worked solution: **`SOLUTION.md`** (look only after a real attempt).
