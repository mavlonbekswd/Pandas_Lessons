# Project 07 — Solution (Logistics)

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
