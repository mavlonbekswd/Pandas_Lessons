# Project 10 — COVID Cases Time-Series (supplementary)

> Optional portfolio extension: a real-world **time-series** domain to stretch
> your DateTime/resample/rolling skills on something other than Aurora.

## Business problem
A public-health analyst needs clean weekly trends and 7-day moving averages of
new cases by country, robust to missing days and bad corrections.

## Dataset
`data/covid_daily.csv` — `country, date, new_cases, new_deaths`. **Messy:** some
missing `new_cases`, a few negative "corrections", daily granularity with gaps.

## Tasks
1. Parse `date`; set a clean per-country daily index (reindex to fill gaps).
2. Fix impossible values (negative `new_cases` → NaN), then choose an honest fill/interp.
3. 7-day rolling average of `new_cases` per country.
4. Weekly totals via `resample("W")`; find each country's peak week.
5. Small-multiples or overlay line chart of the 7-day average by country.

## Hints
- Group by country, then per group `set_index("date").asfreq("D")`.
- `new_cases.clip(lower=0)` or set negatives to NaN then interpolate — decide and justify.
- `rolling(7).mean()` after the index is complete.

## Self-check
```python
assert (clean["new_cases"].dropna() >= 0).all()
assert isinstance(weekly.index, pd.MultiIndex) and weekly.gt(0).any()
```
Worked solution: **`SOLUTION.md`**.
