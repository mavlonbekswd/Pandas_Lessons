# Project 08 — Data Cleaning Project (Aurora Outfitters)

*Part of the main investigation.* Before any KPI is trustworthy, the raw tables
must be cleaned. This project is a focused cleaning sprint and a reusable
`clean_aurora()` pipeline.

## Business problem
Produce **analysis-ready** versions of `customers`, `orders`, `products`,
`order_items` with a documented cleaning log — so every later number is defensible.

## Dataset
All of `../../datasets/raw/`. See the data dictionary for the planted issues.

## Tasks
1. Fix dtypes (ids as str, dates parsed, numerics numeric).
2. Standardise categories: `channel`, `status`, `country`, `segment` (case/whitespace/synonyms).
3. De-duplicate customers on `customer_id`.
4. Handle impossible values: negative `list_price`, absurd `quantity`, missing `unit_price`.
5. Flag orphan orders (customer_id not in customers).
6. Write a **cleaning log** (what/why/how many rows affected) and a `clean_aurora()` function.

## Hints
- Build one function per table; compose them in `clean_aurora()`.
- Count affected rows *before* you change them (`mask.sum()`), for the log.
- Decide each missing-value strategy explicitly and justify it.

## Self-check
```python
assert customers["customer_id"].is_unique
assert orders["channel"].nunique() <= 4
assert (products["list_price"].dropna() >= 0).all()
```
Worked solution: **`SOLUTION.md`**.
