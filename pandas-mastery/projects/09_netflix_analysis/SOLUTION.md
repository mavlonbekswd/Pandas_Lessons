# Project 09 — Solution (Netflix)

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
