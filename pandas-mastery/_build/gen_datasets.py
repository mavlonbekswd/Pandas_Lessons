"""
Generate the Aurora Outfitters dataset ecosystem.

ONE company, many connected, deliberately MESSY tables. Every lesson and the
final capstone investigate this same company. Messiness is intentional:
inconsistent casing, whitespace, mixed date formats, duplicates, missing
values, wrong dtypes, outliers and a few planted data-quality "crimes" that
the student must discover.

Run from the repo root:  python _build/gen_datasets.py
"""
import os
import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)
OUT = os.path.join(os.path.dirname(__file__), "..", "datasets", "raw")
os.makedirs(OUT, exist_ok=True)

START = pd.Timestamp("2023-01-01")
END = pd.Timestamp("2024-12-31")
N_DAYS = (END - START).days + 1
dates = pd.date_range(START, END, freq="D")

COUNTRIES = ["United Kingdom", "uk", "U.K.", "Germany", "germany", "France",
             "Spain", "spain", "Italy", "Netherlands", "Ireland", "Poland"]
CHANNELS = ["Online", "online", "Retail Store", "Marketplace", "marketplace", "Phone"]
CATEGORIES = ["Jackets", "Footwear", "Backpacks", "Tents", "Sleeping Bags",
              "Accessories", "Climbing", "Navigation"]

# ----------------------------------------------------------------------------
# PRODUCTS
# ----------------------------------------------------------------------------
n_products = 120
prod_ids = [f"P{1000+i}" for i in range(n_products)]
cat = rng.choice(CATEGORIES, n_products)
cost = np.round(rng.uniform(8, 220, n_products), 2)
margin = rng.uniform(1.4, 2.8, n_products)
price = np.round(cost * margin, 2)
products = pd.DataFrame({
    "product_id": prod_ids,
    "product_name": [f"{c[:-1] if c.endswith('s') else c} Model {i%30}" for i, c in enumerate(cat)],
    "category": cat,
    "unit_cost": cost,
    "list_price": price,
    "supplier": rng.choice(["Summit Co", "TrailMakers", "PeakGear", "NordicSupply", "unknown"], n_products),
})
# Plant messiness: some missing costs, a few negative prices (data entry error)
products.loc[rng.choice(n_products, 6, replace=False), "unit_cost"] = np.nan
products.loc[rng.choice(n_products, 2, replace=False), "list_price"] *= -1
products.to_csv(os.path.join(OUT, "products.csv"), index=False)

# ----------------------------------------------------------------------------
# CUSTOMERS
# ----------------------------------------------------------------------------
n_customers = 4000
cust_ids = [f"C{10000+i}" for i in range(n_customers)]
first = rng.choice(["James", "Olivia", "Liam", "Emma", "Noah", "Ava", "Sofia",
                    "Lucas", "Mia", "Leon", "Hannah", "Marco", "Elena", "Piotr"], n_customers)
signup = START + pd.to_timedelta(rng.integers(0, N_DAYS, n_customers), unit="D")
# Mixed date string formats on purpose
def messy_date(ts, i):
    fmts = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d %b %Y"]
    return ts.strftime(fmts[i % len(fmts)])
signup_str = [messy_date(s, i) for i, s in enumerate(signup)]
emails = []
for i, f in enumerate(first):
    if rng.random() < 0.06:
        emails.append(np.nan)                       # missing email
    else:
        sep = rng.choice([".", "_", ""])
        dom = rng.choice(["gmail.com", "outlook.com", "yahoo.co.uk", "aurora-test.com"])
        emails.append(f"{f.lower()}{sep}{cust_ids[i][1:]}@{dom}")
customers = pd.DataFrame({
    "customer_id": cust_ids,
    "first_name": first,
    "email": emails,
    "country": rng.choice(COUNTRIES, n_customers),
    "signup_date": signup_str,
    "segment": rng.choice(["Consumer", "consumer", "Business", "Pro Athlete", np.nan], n_customers,
                          p=[0.5, 0.1, 0.25, 0.1, 0.05]),
    "loyalty_points": rng.integers(0, 5000, n_customers).astype(float),
})
# Whitespace messiness in names
customers.loc[rng.choice(n_customers, 200, replace=False), "first_name"] = \
    customers.loc[rng.choice(n_customers, 200, replace=False), "first_name"].astype(str) + "  "
# Plant duplicate customer rows (same customer entered twice)
dupes = customers.sample(40, random_state=SEED).copy()
customers = pd.concat([customers, dupes], ignore_index=True)
customers.to_csv(os.path.join(OUT, "customers.csv"), index=False)

# ----------------------------------------------------------------------------
# ORDERS + ORDER ITEMS
# ----------------------------------------------------------------------------
n_orders = 26000
order_ids = [f"O{200000+i}" for i in range(n_orders)]
# Seasonality: more orders in Nov/Dec
day_weights = np.ones(N_DAYS)
for i, d in enumerate(dates):
    if d.month in (11, 12):
        day_weights[i] *= 2.2
    if d.weekday() >= 5:
        day_weights[i] *= 1.3
day_weights /= day_weights.sum()
order_day_idx = rng.choice(N_DAYS, n_orders, p=day_weights)
order_dates = dates[order_day_idx]
order_date_str = [messy_date(d, i) for i, d in enumerate(order_dates)]

orders = pd.DataFrame({
    "order_id": order_ids,
    "customer_id": rng.choice(cust_ids, n_orders),
    "order_date": order_date_str,
    "channel": rng.choice(CHANNELS, n_orders),
    "status": rng.choice(["delivered", "Delivered", "shipped", "cancelled", "returned", "processing"],
                         n_orders, p=[0.55, 0.1, 0.15, 0.07, 0.08, 0.05]),
})
# A handful of orders reference a customer id that does NOT exist (orphan rows)
orphans = rng.choice(n_orders, 50, replace=False)
orders.loc[orphans, "customer_id"] = [f"C{99000+i}" for i in range(50)]
orders.to_csv(os.path.join(OUT, "orders.csv"), index=False)

# Order items: 1-4 lines per order
rows = []
price_lookup = dict(zip(products["product_id"], np.abs(products["list_price"].values)))
for oid in order_ids:
    for _ in range(rng.integers(1, 5)):
        pid = rng.choice(prod_ids)
        qty = int(rng.integers(1, 6))
        unit = price_lookup[pid]
        disc = float(rng.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.2]))
        rows.append((oid, pid, qty, round(unit, 2), disc))
items = pd.DataFrame(rows, columns=["order_id", "product_id", "quantity", "unit_price", "discount"])
# Messiness: some missing unit_price, a few impossible quantities (outliers)
items.loc[rng.choice(len(items), 300, replace=False), "unit_price"] = np.nan
items.loc[rng.choice(len(items), 15, replace=False), "quantity"] = rng.integers(500, 2000, 15)
items.to_csv(os.path.join(OUT, "order_items.csv"), index=False)

# ----------------------------------------------------------------------------
# RETURNS
# ----------------------------------------------------------------------------
returned_orders = orders.loc[orders["status"].str.lower() == "returned", "order_id"]
ret = returned_orders.sample(frac=0.9, random_state=SEED)
returns = pd.DataFrame({
    "order_id": ret.values,
    "return_reason": rng.choice(["wrong size", "Wrong Size", "damaged", "not as described",
                                 "changed mind", "late delivery", np.nan], len(ret)),
    "refund_amount": np.round(rng.uniform(10, 400, len(ret)), 2),
})
returns.to_csv(os.path.join(OUT, "returns.csv"), index=False)

# ----------------------------------------------------------------------------
# MARKETING SPEND (daily, per channel)  -- time series
# ----------------------------------------------------------------------------
mk_channels = ["Paid Search", "Social", "Email", "Affiliate", "Display"]
mrows = []
for d in dates:
    for ch in mk_channels:
        base = {"Paid Search": 800, "Social": 500, "Email": 120,
                "Affiliate": 300, "Display": 250}[ch]
        seasonal = 1.8 if d.month in (11, 12) else 1.0
        spend = max(0, rng.normal(base * seasonal, base * 0.25))
        mrows.append((d.strftime("%Y-%m-%d"), ch, round(spend, 2)))
mk = pd.DataFrame(mrows, columns=["date", "channel", "spend_gbp"])
# Plant a few missing days (gaps in the time series)
mk = mk[~mk["date"].isin(["2023-07-04", "2023-07-05", "2024-03-15"])]
mk.to_csv(os.path.join(OUT, "marketing_spend.csv"), index=False)

# ----------------------------------------------------------------------------
# WEB TRAFFIC (daily)  -- time series with trend + noise
# ----------------------------------------------------------------------------
trend = np.linspace(4000, 9000, N_DAYS)
season = 1500 * np.sin(np.arange(N_DAYS) * 2 * np.pi / 365)
noise = rng.normal(0, 600, N_DAYS)
sessions = np.clip(trend + season + noise, 500, None).astype(int)
conv = np.clip(rng.normal(0.022, 0.004, N_DAYS), 0.005, 0.08)
web = pd.DataFrame({
    "date": dates.strftime("%Y-%m-%d"),
    "sessions": sessions,
    "conversion_rate": np.round(conv, 4),
    "bounce_rate": np.round(np.clip(rng.normal(0.46, 0.07, N_DAYS), 0.1, 0.9), 4),
})
web.to_csv(os.path.join(OUT, "web_traffic.csv"), index=False)

# ----------------------------------------------------------------------------
# SUPPORT TICKETS  -- text data
# ----------------------------------------------------------------------------
templates = [
    "Order {oid} arrived damaged, the zip is broken",
    "Where is my order {oid}?? It is 2 weeks late!!!",
    "I want a refund for {oid}, wrong size delivered",
    "Great service, jacket fits perfectly. thanks",
    "Cancel order {oid} please, ordered by mistake",
    "the tent {oid} leaked on first use, very disappointed",
    "Can I change the delivery address for {oid}?",
    "  RETURN REQUEST: item not as described  ",
]
n_tickets = 3000
tk_rows = []
for i in range(n_tickets):
    oid = rng.choice(order_ids)
    msg = rng.choice(templates).format(oid=oid)
    tk_rows.append((
        f"T{500000+i}",
        oid if rng.random() > 0.1 else np.nan,
        rng.choice(["open", "Open", "closed", "pending"]),
        msg,
        rng.choice(["email", "phone", "chat"]),
    ))
tickets = pd.DataFrame(tk_rows, columns=["ticket_id", "order_id", "ticket_status", "message", "channel"])
tickets.to_csv(os.path.join(OUT, "support_tickets.csv"), index=False)

# ----------------------------------------------------------------------------
# SHIPMENTS  -- logistics
# ----------------------------------------------------------------------------
ship_orders = orders.sample(frac=0.85, random_state=SEED)
parsed = pd.to_datetime(ship_orders["order_date"], format="mixed", dayfirst=True, errors="coerce")
ship_days = rng.integers(1, 12, len(ship_orders))
shipped = parsed + pd.to_timedelta(ship_days, unit="D")
promised = parsed + pd.to_timedelta(5, unit="D")
shipments = pd.DataFrame({
    "order_id": ship_orders["order_id"].values,
    "carrier": rng.choice(["RoyalShip", "DPDx", "FastFreight", "EuroPost"], len(ship_orders)),
    "warehouse": rng.choice(["Manchester", "Berlin", "Lyon", "Madrid"], len(ship_orders)),
    "promised_date": promised.dt.strftime("%Y-%m-%d").values,
    "shipped_date": shipped.dt.strftime("%Y-%m-%d").values,
    "shipping_cost_gbp": np.round(rng.uniform(2, 30, len(ship_orders)), 2),
})
shipments.to_csv(os.path.join(OUT, "shipments.csv"), index=False)

print("Datasets written to", os.path.abspath(OUT))
for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    print(f"  {f:28s} {os.path.getsize(p)//1024:6d} KB")
