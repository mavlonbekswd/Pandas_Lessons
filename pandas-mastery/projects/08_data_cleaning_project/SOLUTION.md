# Project 08 — Solution (Data Cleaning)

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
