# Project 09 — Netflix Content Analysis (supplementary)

> Optional portfolio extension in a *different* domain (streaming catalogue) to
> prove your skills transfer beyond Aurora. Realistic, messy content data.

## Business problem
A streaming team wants to understand its catalogue: the **movie vs TV** mix over
time, top countries, and how content additions trend by year.

## Dataset
`data/netflix_titles.csv` — columns: `show_id, type, title, country,
release_year, rating, duration, date_added, listed_in`. **Messy on purpose:**
inconsistent `type`/`country` casing, missing values, `date_added` as text,
`duration` mixing "min" and "Seasons".

## Tasks
1. Clean `type` (Movie/TV Show) and `country` casing; treat `""` as missing.
2. Parse `date_added`; extract `year_added`. Trend of titles added per year (line).
3. Movie vs TV split per year (stacked bar) — has the mix shifted?
4. Split `duration` into a numeric movie length vs season count (two columns).
5. Top 10 countries by title count (bar, sorted).

## Hints
- `pd.to_datetime(date_added, format="%B %d, %Y", errors="coerce")`.
- `str.extract(r"(\d+)")` to pull numbers from `duration`.
- `pivot_table(index="year_added", columns="type", aggfunc="size")` for the mix.

## Self-check
```python
assert titles["type"].nunique() == 2
assert titles["year_added"].notna().mean() > 0.9
```
Worked solution: **`SOLUTION.md`**.
