# Aurora Outfitters — Data Dictionary

> **Aurora Outfitters** is a (fictional) European outdoor-gear retailer selling
> jackets, tents, footwear and climbing equipment online, through marketplaces,
> and in physical stores. You have just joined as a **Junior Data Analyst**.
> Something is wrong with the numbers the finance team is reporting, and over
> the next 12 topics you will investigate it using this exact data.

All raw files live in `datasets/raw/`. **They are deliberately messy** —
inconsistent casing, whitespace, mixed date formats, duplicates, missing
values, orphan keys and a few planted data-quality "crimes". Cleaning them is
part of the job.

---

## `customers.csv`
One row per customer account (with some duplicate rows planted).

| Column | Type | Notes |
|---|---|---|
| `customer_id` | string | Primary key, e.g. `C10042`. **Has duplicate rows.** |
| `first_name` | string | Some values have trailing whitespace. |
| `email` | string | ~6% missing. |
| `country` | string | Inconsistent casing/spelling (`uk`, `U.K.`, `United Kingdom`). |
| `signup_date` | string | **Mixed formats** (`YYYY-MM-DD`, `DD/MM/YYYY`, ...). |
| `segment` | string | `Consumer`/`Business`/`Pro Athlete`, inconsistent case, some missing. |
| `loyalty_points` | float | Stored as float; really an integer count. |

## `products.csv`
Product catalogue, one row per SKU.

| Column | Type | Notes |
|---|---|---|
| `product_id` | string | Primary key, e.g. `P1007`. |
| `product_name` | string | |
| `category` | string | One of 8 categories. |
| `unit_cost` | float | What Aurora pays. **Some missing.** |
| `list_price` | float | Sticker price. **A few are negative (data-entry error).** |
| `supplier` | string | Some `unknown`. |

## `orders.csv`
One row per order (order header). ~26k rows.

| Column | Type | Notes |
|---|---|---|
| `order_id` | string | Primary key, e.g. `O200512`. |
| `customer_id` | string | FK → customers. **~50 orphan ids that do not exist in customers.** |
| `order_date` | string | **Mixed date formats.** |
| `channel` | string | Online / Retail Store / Marketplace / Phone (inconsistent case). |
| `status` | string | delivered / shipped / cancelled / returned / processing (inconsistent case). |

## `order_items.csv`
Order line items (one row per product line). FK `order_id` → orders.

| Column | Type | Notes |
|---|---|---|
| `order_id` | string | FK → orders. |
| `product_id` | string | FK → products. |
| `quantity` | int | **A few absurd outliers (500–2000).** |
| `unit_price` | float | Price charged. **~300 missing.** |
| `discount` | float | Fraction 0–0.20. |

## `returns.csv`
One row per returned order. FK `order_id` → orders.

| Column | Type | Notes |
|---|---|---|
| `order_id` | string | FK → orders. |
| `return_reason` | string | Free-ish text, inconsistent case, some missing. |
| `refund_amount` | float | GBP refunded. |

## `marketing_spend.csv`
Daily marketing spend per channel. **Time series** (a few days are missing).

| Column | Type | Notes |
|---|---|---|
| `date` | string | `YYYY-MM-DD`. |
| `channel` | string | Paid Search / Social / Email / Affiliate / Display. |
| `spend_gbp` | float | GBP spent that day on that channel. |

## `web_traffic.csv`
Daily website metrics. **Time series.**

| Column | Type | Notes |
|---|---|---|
| `date` | string | `YYYY-MM-DD`. |
| `sessions` | int | Visits that day (trend + seasonality + noise). |
| `conversion_rate` | float | Fraction of sessions that ordered. |
| `bounce_rate` | float | Fraction that bounced. |

## `support_tickets.csv`
Customer support messages. **Text data.**

| Column | Type | Notes |
|---|---|---|
| `ticket_id` | string | Primary key. |
| `order_id` | string | FK → orders, ~10% missing. |
| `ticket_status` | string | open / closed / pending (inconsistent case). |
| `message` | string | Free text — sentiment, order numbers, whitespace. |
| `channel` | string | email / phone / chat. |

## `shipments.csv`
Logistics, one row per shipped order (~85% of orders). FK `order_id` → orders.

| Column | Type | Notes |
|---|---|---|
| `order_id` | string | FK → orders. |
| `carrier` | string | RoyalShip / DPDx / FastFreight / EuroPost. |
| `warehouse` | string | Manchester / Berlin / Lyon / Madrid. |
| `promised_date` | string | Promised delivery date. |
| `shipped_date` | string | Actual ship date. |
| `shipping_cost_gbp` | float | GBP. |

---

## How the tables connect

```
customers (customer_id) ──< orders (order_id) ──< order_items >── products (product_id)
                                   │
                                   ├──< returns
                                   ├──< shipments
                                   └──< support_tickets
marketing_spend (date) ── web_traffic (date)   [join to orders on the order date]
```

Keep this map open. Almost every Merge/Join exercise (Topic 06) relies on it.
