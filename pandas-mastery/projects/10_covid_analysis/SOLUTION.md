# Project 10 — Solution (COVID)

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
