"""Generate projects/: datasets + brief (README) + separate SOLUTION files."""
import os
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(__file__), "..")
P = os.path.join(ROOT, "projects")
rng = np.random.default_rng(7)

# ------------------------------------------------------------------ datasets
# Netflix-style content catalogue (realistic business domain, messy)
n = 2500
titles = pd.DataFrame({
    "show_id": [f"s{i}" for i in range(1, n + 1)],
    "type": rng.choice(["Movie", "TV Show", "movie", "tv show"], n, p=[0.6, 0.3, 0.06, 0.04]),
    "title": [f"Title {i}" for i in range(1, n + 1)],
    "country": rng.choice(["United States", "India", "United Kingdom", "us", "Japan", "", "South Korea"], n),
    "release_year": rng.integers(1955, 2025, n),
    "rating": rng.choice(["TV-MA", "TV-14", "PG-13", "R", "PG", "TV-PG", np.nan], n),
    "duration": [f"{rng.integers(60,180)} min" if t.lower() == "movie"
                 else f"{rng.integers(1,9)} Seasons" for t in
                 rng.choice(["Movie", "TV Show"], n)],
    "date_added": pd.to_datetime("2008-01-01") + pd.to_timedelta(rng.integers(0, 6000, n), unit="D"),
    "listed_in": rng.choice(["Dramas, International", "Comedies", "Documentaries",
                             "Action & Adventure", "Kids' TV, Children"], n),
})
titles.loc[rng.choice(n, 120, replace=False), "country"] = np.nan
titles["date_added"] = titles["date_added"].dt.strftime("%B %d, %Y")  # messy text date
os.makedirs(os.path.join(P, "09_netflix_analysis", "data"), exist_ok=True)
titles.to_csv(os.path.join(P, "09_netflix_analysis", "data", "netflix_titles.csv"), index=False)

# COVID-style daily cases by country (real-world domain, messy)
countries = ["United Kingdom", "Germany", "France", "Italy", "Spain"]
dates = pd.date_range("2020-03-01", "2021-12-31", freq="D")
rows = []
for c in countries:
    base = rng.uniform(500, 3000)
    wave = base * (1 + np.sin(np.arange(len(dates)) * 2 * np.pi / 180) + rng.normal(0, 0.2, len(dates)))
    wave = np.clip(wave, 0, None)
    for d, v in zip(dates, wave):
        rows.append((c, d.strftime("%Y-%m-%d"), int(v), int(v * rng.uniform(0.005, 0.03))))
covid = pd.DataFrame(rows, columns=["country", "date", "new_cases", "new_deaths"])
# plant some missing days and a negative correction
covid.loc[rng.choice(len(covid), 200, replace=False), "new_cases"] = np.nan
covid.loc[rng.choice(len(covid), 5, replace=False), "new_cases"] = -50
os.makedirs(os.path.join(P, "10_covid_analysis", "data"), exist_ok=True)
covid.to_csv(os.path.join(P, "10_covid_analysis", "data", "covid_daily.csv"), index=False)

# ------------------------------------------------------------------ writers
def proj(folder, readme, solution):
    d = os.path.join(P, folder)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "README.md"), "w").write(readme)
    open(os.path.join(d, "SOLUTION.md"), "w").write(solution)
    print("wrote project", folder)

# ---- 07 Logistics (uses Aurora shipments) --------------------------------
proj("07_logistics_analysis", r"""# Project 07 — Logistics Analysis (Aurora Outfitters)

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
""", r"""# Project 07 — Solution (Logistics)

```python
import numpy as np, pandas as pd
RAW = "../../datasets/raw/"
ship = pd.read_csv(RAW+"shipments.csv", dtype={"order_id":str}, parse_dates=["promised_date","shipped_date"])
ship["days_late"] = (ship["shipped_date"] - ship["promised_date"]).dt.days
ship["is_late"] = ship["days_late"] > 0

late_rate_by_carrier = ship.groupby("carrier")["is_late"].mean().sort_values(ascending=False)
late_rate_by_wh = ship.groupby("warehouse")["is_late"].mean().sort_values(ascending=False)
print(late_rate_by_carrier, late_rate_by_wh, sep="\n\n")

orders = pd.read_csv(RAW+"orders.csv", dtype={"order_id":str})
orders["is_returned"] = orders["status"].str.strip().str.lower().eq("returned")
j = ship.merge(orders[["order_id","is_returned"]], on="order_id", how="left")
print(pd.crosstab(j["is_late"], j["is_returned"], normalize="index"))
```
**Interpretation (defend your own):** compare the return rate for late vs on-time
shipments. If late shipments return more, recommend re-routing volume away from
the worst carrier/warehouse and quantify the avoidable returns.
""")

# ---- 08 Data cleaning (uses Aurora raw) ----------------------------------
proj("08_data_cleaning_project", r"""# Project 08 — Data Cleaning Project (Aurora Outfitters)

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
""", r"""# Project 08 — Solution (Data Cleaning)

```python
import numpy as np, pandas as pd
RAW = "../../datasets/raw/"

def clean_aurora(raw=RAW):
    log = {}
    customers = pd.read_csv(raw+"customers.csv", dtype={"customer_id":str})
    log["dup_customers"] = int(customers.duplicated("customer_id").sum())
    customers["first_name"] = customers["first_name"].astype(str).str.strip()
    customers = customers.drop_duplicates("customer_id", keep="first")
    customers["country"] = (customers["country"].str.strip().str.lower()
        .replace({"uk":"united kingdom","u.k.":"united kingdom"}).str.title())
    customers["segment"] = customers["segment"].str.strip().str.lower()

    products = pd.read_csv(raw+"products.csv", dtype={"product_id":str})
    log["neg_price"] = int((products["list_price"] < 0).sum())
    products["list_price"] = np.where(products["list_price"] < 0, np.nan, products["list_price"])
    products["supplier"] = products["supplier"].replace("unknown", np.nan)

    orders = pd.read_csv(raw+"orders.csv", dtype={"order_id":str,"customer_id":str})
    orders["channel"] = orders["channel"].str.strip().str.title()
    orders["status"]  = orders["status"].str.strip().str.lower()
    orders["order_date"] = pd.to_datetime(orders["order_date"], format="mixed",
                                          dayfirst=True, errors="coerce")
    orphan = ~orders["customer_id"].isin(customers["customer_id"])
    log["orphan_orders"] = int(orphan.sum())
    orders["is_orphan"] = orphan

    items = pd.read_csv(raw+"order_items.csv", dtype={"order_id":str,"product_id":str})
    log["absurd_qty"] = int((items["quantity"] > 100).sum())
    log["missing_price"] = int(items["unit_price"].isna().sum())
    items["line_revenue"] = items["quantity"]*items["unit_price"]*(1-items["discount"])
    return dict(customers=customers, products=products, orders=orders, items=items, log=log)

out = clean_aurora()
print(out["log"])
assert out["customers"]["customer_id"].is_unique
assert out["orders"]["channel"].nunique() <= 4
```
The `log` dict **is** your cleaning appendix for the capstone.
""")

# ---- 09 Netflix --------------------------------------------------------
proj("09_netflix_analysis", r"""# Project 09 — Netflix Content Analysis (supplementary)

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
""", r"""# Project 09 — Solution (Netflix)

```python
import numpy as np, pandas as pd
t = pd.read_csv("data/netflix_titles.csv")
t["type"] = t["type"].str.strip().str.title().replace({"Tv Show":"TV Show"})
t["country"] = t["country"].replace("", np.nan).str.strip().str.title().replace({"Us":"United States"})
t["date_added"] = pd.to_datetime(t["date_added"], format="%B %d, %Y", errors="coerce")
t["year_added"] = t["date_added"].dt.year

t["minutes"] = t["duration"].str.extract(r"(\d+)\s*min").astype(float)
t["seasons"] = t["duration"].str.extract(r"(\d+)\s*Season").astype(float)

per_year = t.groupby("year_added").size()
mix = t.pivot_table(index="year_added", columns="type", aggfunc="size", fill_value=0)
top_countries = t["country"].value_counts().head(10)

print(mix.tail()); print(top_countries)
assert t["type"].nunique() == 2
```
Charts: `per_year.plot()` (trend), `mix.plot(kind="bar", stacked=True)` (mix),
`top_countries.plot(kind="barh")`. Write the takeaways yourself.
""")

# ---- 10 COVID ----------------------------------------------------------
proj("10_covid_analysis", r"""# Project 10 — COVID Cases Time-Series (supplementary)

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
""", r"""# Project 10 — Solution (COVID)

```python
import numpy as np, pandas as pd
df = pd.read_csv("data/covid_daily.csv", parse_dates=["date"])
df.loc[df["new_cases"] < 0, "new_cases"] = np.nan   # bad corrections -> missing

def clean_country(g):
    g = g.set_index("date").sort_index().asfreq("D")
    g["new_cases"] = g["new_cases"].interpolate(limit_direction="both")
    g["ma7"] = g["new_cases"].rolling(7).mean()
    return g

clean = df.groupby("country", group_keys=True).apply(clean_country, include_groups=False)
weekly = (df.dropna(subset=["new_cases"]).set_index("date")
            .groupby("country")["new_cases"].resample("W").sum())
print(clean.head()); print(weekly.groupby(level=0).idxmax())
assert (clean["new_cases"].dropna() >= 0).all()
```
Decision to defend: interpolation invents plausible counts for gaps — acceptable
for a smooth trend, risky for exact totals. State which you optimised for.
""")

# ---- projects index ----------------------------------------------------
open(os.path.join(P, "README.md"), "w").write(r"""# Projects

The **main curriculum is one investigation** (Aurora Outfitters), built
progressively across the 12 topics and finished in the Topic 12 capstone. These
projects are focused applications:

| Project | Domain | Ties to |
|---|---|---|
| `07_logistics_analysis` | Aurora shipments | Topics 6, 7, 9 |
| `08_data_cleaning_project` | Aurora raw tables | Topic 4 (reusable `clean_aurora()`) |
| `09_netflix_analysis` | Streaming catalogue (supplementary) | Topics 4, 7, 8, 10 |
| `10_covid_analysis` | Public-health time series (supplementary) | Topic 7 |

Each folder has a **README.md** (business problem, dataset, tasks, hints) and a
**SOLUTION.md** kept separate. Attempt before opening the solution.
""")
print("projects done")
