"""Generate topics 04-06."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import build_notebook
ROOT = os.path.join(os.path.dirname(__file__), "..")
BOOT = ("import numpy as np\nimport pandas as pd\n"
        "pd.set_option('display.max_columns', 30)\nRAW = '../datasets/raw/'\n")

def write(topic_dir, lesson, quiz, challenge, practice, solutions):
    d = os.path.join(ROOT, topic_dir)
    open(os.path.join(d, "lesson.md"), "w").write(lesson)
    open(os.path.join(d, "quiz.md"), "w").write(quiz)
    open(os.path.join(d, "challenge.md"), "w").write(challenge)
    build_notebook(practice, os.path.join(d, "practice.ipynb"))
    build_notebook(solutions, os.path.join(d, "solutions.ipynb"))
    print("wrote", topic_dir)

# ===========================================================================
# TOPIC 04 — Data Cleaning & Missing Data
# ===========================================================================
t4_lesson = r"""# Topic 04 — Data Cleaning & Missing Data

> **Investigation milestone:** This is where the case cracks open. Aurora's
> `channel` and `status` have inconsistent casing (so totals are split),
> `customers` has duplicate rows (inflating customer counts), prices are
> missing, and dates are text. Until you clean, every number is a lie.

**Time split: 20% reading · 80% in `practice.ipynb`. Cleaning is ~80% of real analyst work.**

---

## A repeatable cleaning workflow

1. **Profile** — `info()`, `describe()`, `isna().sum()`, `nunique()`, `value_counts()`.
2. **Fix dtypes** — `astype`, `pd.to_datetime`, `pd.to_numeric(errors="coerce")`.
3. **Standardise categories** — strip whitespace, fix casing, map synonyms.
4. **Handle duplicates** — `duplicated`, `drop_duplicates(subset=, keep=)`.
5. **Handle missing** — decide per column: drop / fill / leave NaN.
6. **Validate** — re-profile; assert invariants.

## Missing data — `NaN`, `None`, `pd.NA`

- `NaN` is a float (`np.nan`); it propagates (`NaN + 1 = NaN`) and `NaN != NaN`.
- `None` becomes `NaN` in numeric columns, stays `None`/`NaN` in object columns.
- `pd.NA` is the newer, dtype-agnostic missing marker.

Detect & act:
```python
df.isna().sum()                 # missing per column
df["unit_price"].fillna(0)      # fill (decide if 0 is honest!)
df.dropna(subset=["email"])     # drop rows missing a key field
df["unit_price"].fillna(df["unit_price"].median())   # impute
```

> **Judgement, not reflex.** Filling missing *revenue* with 0 understates it;
> filling with the mean invents money. The right move depends on *why* it's
> missing. Investigate before you impute (Interview Q6, Q8).

## Strings & categories

```python
orders["channel"] = orders["channel"].str.strip().str.title()  # "online " -> "Online"
orders["status"]  = orders["status"].str.lower()
country_map = {"uk": "United Kingdom", "u.k.": "United Kingdom"}
customers["country"] = customers["country"].str.lower().replace(country_map)
```
Standardising casing **merges the split categories** — and Aurora's channel
revenue suddenly stops being double-counted.

## Duplicates

```python
customers.duplicated(subset=["customer_id"]).sum()        # how many dupes
customers = customers.drop_duplicates(subset=["customer_id"], keep="first")
```
Choose the `subset` deliberately: full-row dupes vs same-key dupes are different
problems. Dropping blindly can delete legitimate rows (Interview Q10).

## Wrong values / outliers

`pd.to_numeric(s, errors="coerce")` turns junk into NaN. Negative `list_price`
and 1,500-unit quantities are *impossible* — flag or clip them, don't silently keep.

## NumPy connection 🔢

`np.where(cond, a, b)` is the vectorized "if-else" for cleaning:
```python
items["unit_price"] = np.where(items["unit_price"] < 0, np.nan, items["unit_price"])
```
`np.nan` is literally a NumPy float. `isna()` mirrors `np.isnan` but also handles
object/`pd.NA`. Masking (Topic 3) is how you target the rows to fix.

## Visual learning 📊

Before/after `value_counts().plot(kind="bar")` on `channel` is the perfect
"look what cleaning did" chart — categories collapse from 6 messy to 4 clean.

---

## 🔎 Interview Lens (answer in writing)
- **Q6:** How do you choose between dropping, filling with 0, mean-filling, and leaving NaN for missing revenue?
- **Q9:** A numeric column loads as `object` — likely causes and how to confirm each?

### Recap
1. Three ways to handle a missing value, and when each is honest.
2. How does standardising casing change Aurora's channel totals?
3. Why prefer `to_numeric(errors="coerce")` over `astype(float)` on dirty data?

➡️ Open **`practice.ipynb`**.
"""

t4_quiz = r"""# Topic 04 — Quiz (Data Cleaning & Missing Data)

15 questions. Answers in `../quizzes/04_answers.md`.

## Part A — Multiple Choice
1. `df.isna().sum()` returns:
   - (a) total cells  (b) missing count per column  (c) rows with any NaN  (d) a boolean
2. Best for converting a dirty numeric column with junk strings:
   - (a) `astype(float)`  (b) `pd.to_numeric(s, errors="coerce")`  (c) `int(s)`  (d) `round(s)`
3. `drop_duplicates(subset=["customer_id"], keep="first")`:
   - (a) drops all dupes incl. first  (b) keeps the first occurrence per id  (c) keeps last  (d) errors
4. Filling missing revenue with the column mean:
   - (a) is always correct  (b) can invent money that wasn't earned  (c) is required  (d) drops rows
5. `NaN == NaN` evaluates to:
   - (a) True  (b) False  (c) NaN  (d) error

## Part B — Predict the Output
6. `pd.Series([1,np.nan,3]).sum()` → ? (default skipna)
7. `pd.Series(["a","a","b"]).duplicated().sum()` → ?
8. `pd.to_numeric(pd.Series(["1","x","3"]), errors="coerce").isna().sum()` → ?

## Part C — Fill in the Blank
9. Standardise channel casing: `orders["channel"].str.________().str.________()`.
10. Drop rows missing email: `customers.________(subset=["email"])`.
11. Impute with median: `s.________(s.median())`.
12. Map synonyms: `s.________({"uk": "United Kingdom"})`.

## Part D — Debug the Code
13. ```python
    customers.drop_duplicates()      # didn't change anything
    ```
    The dupes share `customer_id` but differ in a whitespace name. How to catch them?
14. ```python
    products["unit_cost"].astype(int)   # ValueError: cannot convert NaN
    ```
    Fix so it works.
15. ```python
    orders["channel"].replace("online", "Online")   # 'Online ' (trailing space) untouched
    ```
    Why did some values escape? Fix the pipeline.
"""

t4_challenge = r"""# Topic 04 — Challenges (Cleaning & Missing Data)

## 🟢 Easy
Profile `customers`: print missing counts per column and the number of duplicate
`customer_id` rows. Note (no key) which columns most need cleaning.

## 🟡 Medium
Clean `orders["channel"]` and `orders["status"]` so casing/whitespace is
standardised. Self-check:
`assert orders["channel"].nunique() <= 4` and
`assert orders["status"].str.islower().all()`.

## 🔴 Hard
De-duplicate `customers` on `customer_id` (keep first) AND strip whitespace from
`first_name`. Self-check:
`assert customers["customer_id"].is_unique` and
`assert not customers["first_name"].str.endswith(" ").any()`.

## 🏢 Real Business Challenge — "The double-counted channel"
Compute total orders per channel **before** and **after** standardising casing.
Show that cleaning *merges* `online`+`Online` etc. and changes the ranking.
Self-check:
```python
assert clean_counts.shape[0] < raw_counts.shape[0], "Cleaning should reduce category count"
print(raw_counts, "\n---\n", clean_counts)
```
Investigation log: *was the finance team double-counting channels?*

## 🔎 Interview Lens — write answers
- Q6 (missing-revenue strategy) and Q9 (object dtype causes).
"""

t4_practice = [
 ("md", "# Topic 04 — Practice: Data Cleaning & Missing Data\n\nThe case cracks open. Clean before you conclude."),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str})\n"
          "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})"),
 ("md", "## Concept\nProfile → fix dtypes → standardise categories → dedupe → handle missing → validate."),
 ("md", "## Example — profile customers\nWhere is the dirt?"),
 ("code", "print(customers.isna().sum())\nprint('dup customer_id rows:', customers.duplicated(subset=['customer_id']).sum())\ncustomers.head()"),
 ("md", "## Your Turn — standardise channel & status\nMake `channel` Title Case (stripped) and `status` lowercase."),
 ("code", "# TODO\norders['channel'] = ...\norders['status'] = ...\n"
          "assert orders['channel'].nunique() <= 4, 'channels not fully merged'\n"
          "assert orders['status'].str.islower().all()\n"
          "print(orders['channel'].value_counts())"),
 ("md", "## Mini Mission — dedupe customers\nDrop duplicate `customer_id` (keep first) and strip name whitespace."),
 ("code", "# TODO\ncustomers = ...\n"
          "assert customers['customer_id'].is_unique\n"
          "assert not customers['first_name'].astype(str).str.endswith(' ').any()\n"
          "print('clean customers:', customers.shape)"),
 ("md", "## Boss Fight — the double-counted channel\n"
        "Compare channel order counts BEFORE vs AFTER cleaning (reload raw for 'before')."),
 ("code", "raw = pd.read_csv(RAW+'orders.csv')\n"
          "raw_counts = raw['channel'].value_counts()\n"
          "clean_counts = orders['channel'].value_counts()\n"
          "assert clean_counts.shape[0] < raw_counts.shape[0]\n"
          "print('BEFORE\\n', raw_counts, '\\n\\nAFTER\\n', clean_counts)"),
 ("md", "## Mini Mission — honest missing prices\nLines with missing `unit_price`: decide a strategy and justify it in writing. "
        "Negative `list_price` in products is impossible — coerce those to NaN."),
 ("code", "print('missing unit_price lines:', items['unit_price'].isna().sum())\n"
          "products['list_price'] = np.where(products['list_price'] < 0, np.nan, products['list_price'])\n"
          "assert (products['list_price'].dropna() >= 0).all()\nprint('negative prices fixed')"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q6 and Q9 in writing.\n"
        "2. Did cleaning change which channel looks biggest? (log it)\n"
        "3. For missing `unit_price`: did you drop, fill, or flag? Defend it."),
]

t4_solutions = [
 ("md", "# Topic 04 — Solutions"),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str})\n"
          "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})"),
 ("code", "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['status'] = orders['status'].str.strip().str.lower()\n"
          "print(orders['channel'].value_counts())\nprint(orders['status'].value_counts())"),
 ("code", "customers['first_name'] = customers['first_name'].astype(str).str.strip()\n"
          "customers = customers.drop_duplicates(subset=['customer_id'], keep='first')\n"
          "print(customers.shape, customers['customer_id'].is_unique)"),
 ("code", "raw = pd.read_csv(RAW+'orders.csv')\n"
          "print('BEFORE\\n', raw['channel'].value_counts())\n"
          "print('AFTER\\n', orders['channel'].value_counts())\n"
          "# 'Retail Store' uses a space; .str.title() keeps it as 'Retail Store'. The split\n"
          "# online/Online and marketplace/Marketplace collapse — finance WAS double-counting."),
 ("code", "products['list_price'] = np.where(products['list_price'] < 0, np.nan, products['list_price'])\n"
          "print('missing unit_price lines:', items['unit_price'].isna().sum())"),
 ("md", "### Interview Lens\n- **Q6:** Trace *why* it's missing. If the price genuinely was 0 (free gift) → 0; "
        "if it's a logging gap → impute from product `list_price` via a join (Topic 6) or median; if it could "
        "bias the headline number → keep NaN and report coverage. Never silently fill revenue with the mean.\n"
        "- **Q9:** Object dtype usually = stray text/symbols (£, commas), mixed types, or a sentinel like "
        "'unknown'. Confirm with `s.str.isnumeric()` / `pd.to_numeric(errors='coerce').isna()` to find offenders."),
]

write("04_Data_Cleaning_And_Missing_Data", t4_lesson, t4_quiz, t4_challenge, t4_practice, t4_solutions)

# ===========================================================================
# TOPIC 05 — GroupBy & Aggregation
# ===========================================================================
t5_lesson = r"""# Topic 05 — GroupBy & Aggregation

> **Investigation milestone:** Now you turn 64,000 order lines into *answers*:
> revenue by month, by channel, by category; average order value; the best and
> worst performers. GroupBy is how analysts summarise.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## Split–Apply–Combine

Every groupby does three things:
1. **Split** rows into groups by a key.
2. **Apply** a function to each group.
3. **Combine** the results into a new Series/DataFrame.

```python
items.groupby("product_id")["line_revenue"].sum()
orders.groupby("channel").size()           # rows per group
```

## `agg` — one or many functions

```python
items.groupby("product_id").agg(
    revenue=("line_revenue", "sum"),
    avg_qty=("quantity", "mean"),
    lines=("order_id", "count"),
)
```
**Named aggregation** (`new=("col","func")`) gives clean output columns — use it.

## `transform` vs `agg` vs `apply`

| Method | Returns | Use |
|---|---|---|
| `agg` | one value per group | summary tables |
| `transform` | **same shape as input** | broadcast a group stat back to rows |
| `apply` | anything | flexible, slower; last resort |

```python
# % of each product's revenue that a line represents:
items["pct_of_product"] = items["line_revenue"] / \
    items.groupby("product_id")["line_revenue"].transform("sum")
```
`transform` is the secret weapon for "group stat, but keep every row".

## Multiple keys & flags

```python
orders.groupby(["channel", "status"]).size().unstack()   # cross-tab feel
```

## Gotchas
- `as_index=False` keeps the group key as a column (handy before plotting/merging).
- `observed=True` matters for `category` dtype (avoids empty combinations).
- `dropna=` controls whether NaN keys form their own group.
- `count` ignores NaN; `size` counts rows including NaN.

## NumPy connection 🔢

A groupby aggregation is a *segmented reduction* — conceptually `np.add.reduceat`
on sorted groups, but Pandas handles the bookkeeping. The per-group `mean`/`sum`
are the same NumPy reductions you know, applied to slices. Vectorized and fast;
a Python loop over groups is the slow anti-pattern.

## Visual learning 📊

`monthly_revenue.plot(kind="line")` and
`channel_revenue.plot(kind="bar")` are the bread-and-butter analyst charts.
A groupby feeds almost every business chart you'll ever draw.

---

## 🔎 Interview Lens (answer in writing)
- **Q14:** Explain split–apply–combine in your own words.
- **Q16:** Difference between `transform`, `agg`, and `apply` on a groupby — a use case each.

### Recap
1. What does `transform` give you that `agg` doesn't?
2. Write revenue-per-channel with named aggregation.
3. When do you need `as_index=False`?

➡️ Open **`practice.ipynb`**.
"""

t5_quiz = r"""# Topic 05 — Quiz (GroupBy & Aggregation)

15 questions. Answers in `../quizzes/05_answers.md`.

## Part A — Multiple Choice
1. Split–apply–combine's middle step:
   - (a) sort  (b) apply a function per group  (c) merge  (d) pivot
2. `transform` returns an object that is:
   - (a) one row per group  (b) the same shape as the input  (c) always scalar  (d) a dict
3. Named aggregation syntax:
   - (a) `agg("sum")`  (b) `agg(rev=("line_revenue","sum"))`  (c) `agg({sum})`  (d) `sum(agg)`
4. `size()` vs `count()`:
   - (a) identical  (b) `size` includes NaN rows, `count` excludes NaN  (c) reverse  (d) `count` is faster only
5. To keep the group key as a column:
   - (a) `reset_columns`  (b) `as_index=False`  (c) `keep_key=True`  (d) `inplace`

## Part B — Predict the Output
6. `pd.DataFrame({"g":["a","a","b"],"v":[1,2,3]}).groupby("g")["v"].sum()` → values for a,b?
7. `df.groupby("g").size().sum()` vs `len(df)` → relationship?
8. `groupby("g")["v"].transform("sum")` length vs `len(df)` → ?

## Part C — Fill in the Blank
9. Rows per channel: `orders.groupby("channel").________()`.
10. Revenue per product: `items.groupby("product_id")["line_revenue"].________()`.
11. Broadcast group sum to rows: `g["v"].________("sum")`.
12. Keep key as column: `df.groupby("g", ________=False)`.

## Part D — Debug the Code
13. ```python
    items.groupby("product_id").sum()   # sums order_id strings too / slow
    ```
    Aggregate only `line_revenue`. Fix it.
14. ```python
    items["share"] = items.groupby("product_id")["line_revenue"].sum()  # NaN / misaligned
    ```
    You want a per-row share. Which method should replace `sum()`?
15. ```python
    orders.groupby("channel").size().plot()   # ugly line for categories
    ```
    Pick a better `kind=` for category counts.
"""

t5_challenge = r"""# Topic 05 — Challenges (GroupBy & Aggregation)

Assume cleaned `orders` (Topic 4) and `items` with `line_revenue`.

## 🟢 Easy
Revenue per `channel`. Which channel earns most after cleaning? (log it)

## 🟡 Medium
Build a product summary with named aggregation: `revenue` (sum), `units`
(sum of quantity), `lines` (count). Self-check:
`assert {"revenue","units","lines"} <= set(summary.columns)`.

## 🔴 Hard
Add a per-line column `pct_of_product` = this line's revenue / that product's
total revenue, using `transform`. Self-check:
`assert np.isclose(items.groupby("product_id")["pct_of_product"].sum().dropna().mean(), 1.0)`.

## 🏢 Real Business Challenge — "Top customer, worst month, AOV, growth"
Using groupby, compute and print (no values given):
- the **top customer** by total revenue,
- **average order value** (revenue per order),
- (you'll need order dates from Topic 7 for *worst month* & *growth* — set up the
  per-order revenue table now and leave a TODO).
Self-check:
```python
assert aov > 0, "AOV must be positive."
print("Top customer:", top_customer, "| AOV: £%.2f" % aov)
```

## 🔎 Interview Lens — write answers
- Q14 (split-apply-combine) and Q16 (transform vs agg vs apply).
"""

t5_practice = [
 ("md", "# Topic 05 — Practice: GroupBy & Aggregation\n\nTurn rows into answers."),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['status'] = orders['status'].str.strip().str.lower()\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])"),
 ("md", "## Example — revenue per product (top 5)"),
 ("code", "rev = items.groupby('product_id')['line_revenue'].sum().sort_values(ascending=False)\nrev.head()"),
 ("md", "## Your Turn — channel revenue\nJoin line revenue to its order's channel and total revenue per channel. "
        "(Hint: merge `items` to `orders[['order_id','channel']]` — a taste of Topic 6.)"),
 ("code", "oi = items.merge(orders[['order_id','channel']], on='order_id', how='left')\n"
          "channel_rev = ...\n"
          "assert channel_rev.sum() > 0\nchannel_rev.sort_values(ascending=False)"),
 ("md", "## Mini Mission — product summary (named agg)\n`revenue`=sum line_revenue, `units`=sum quantity, `lines`=count."),
 ("code", "summary = ...\nassert {'revenue','units','lines'} <= set(summary.columns)\nsummary.sort_values('revenue', ascending=False).head()"),
 ("md", "## Boss Fight — transform: share of product revenue\n`pct_of_product` per line; each product's shares sum to 1."),
 ("code", "items['pct_of_product'] = ...\n"
          "chk = items.groupby('product_id')['pct_of_product'].sum().dropna().mean()\n"
          "assert np.isclose(chk, 1.0), 'shares should sum to 1 within each product'\nprint('transform OK')"),
 ("md", "## Mini Mission — AOV & top customer\nPer-order revenue, then AOV and top customer by revenue."),
 ("code", "order_rev = oi.groupby('order_id')['line_revenue'].sum()\n"
          "aov = order_rev.mean()\n"
          "cust_rev = oi.merge(orders[['order_id','customer_id']], on='order_id').groupby('customer_id')['line_revenue'].sum()\n"
          "top_customer = cust_rev.idxmax()\n"
          "assert aov > 0\nprint('AOV £%.2f, top customer %s' % (aov, top_customer))"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q14 and Q16 in writing.\n"
        "2. Did channel revenue ranking match the raw (dirty) ranking? Why does cleaning matter here?\n"
        "3. Investigation log: which channel/products drive revenue?"),
]

t5_solutions = [
 ("md", "# Topic 05 — Solutions"),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "oi = items.merge(orders[['order_id','channel','customer_id']], on='order_id', how='left')"),
 ("code", "channel_rev = oi.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\nprint(channel_rev)"),
 ("code", "summary = items.groupby('product_id').agg(revenue=('line_revenue','sum'),\n"
          "                                          units=('quantity','sum'),\n"
          "                                          lines=('order_id','count'))\nprint(summary.sort_values('revenue', ascending=False).head())"),
 ("code", "items['pct_of_product'] = items['line_revenue'] / items.groupby('product_id')['line_revenue'].transform('sum')\n"
          "print(items.groupby('product_id')['pct_of_product'].sum().dropna().mean())"),
 ("code", "order_rev = oi.groupby('order_id')['line_revenue'].sum()\n"
          "aov = order_rev.mean()\n"
          "cust_rev = oi.groupby('customer_id')['line_revenue'].sum()\n"
          "print('AOV £%.2f' % aov, '| top customer', cust_rev.idxmax())"),
 ("md", "### Interview Lens\n- **Q14:** Split rows by key → apply a reduction per group → combine into one table.\n"
        "- **Q16:** `agg` collapses each group to a summary; `transform` returns a same-length result to "
        "broadcast a group stat onto rows; `apply` runs an arbitrary function per group (flexible, slowest)."),
]

write("05_GroupBy_And_Aggregation", t5_lesson, t5_quiz, t5_challenge, t5_practice, t5_solutions)

# ===========================================================================
# TOPIC 06 — Merge / Join / Concat
# ===========================================================================
t6_lesson = r"""# Topic 06 — Merge / Join / Concat

> **Investigation milestone:** The truth lives *across* tables. To compute real
> profit you need order_items × products (cost), orders (channel, date),
> customers (segment), returns (refunds). One bad join can silently double your
> revenue — so this topic is about joining *safely*.

**Time split: 20% reading · 80% in `practice.ipynb`. NumPy recall checkpoint at the end.**

---

## `merge` — the SQL join of Pandas

```python
oi = items.merge(products, on="product_id", how="left")
```

### `how=` decides who survives
| how | keeps |
|---|---|
| `inner` | only keys in **both** (default) |
| `left` | all left rows; unmatched right → NaN |
| `right` | all right rows |
| `outer` | union of keys |

> A `left` join should **not** change your left row count — *unless* the right
> side has duplicate keys, which causes a **many-to-many blow-up** that inflates
> totals. This is the #1 way analysts corrupt revenue numbers.

### Guardrails (use them every time)
```python
items.merge(products, on="product_id", how="left",
            validate="many_to_one",   # raises if right keys aren't unique
            indicator=True)            # adds _merge: left_only/right_only/both
```
- `validate=` catches unexpected duplication *before* it ruins your sums.
- `indicator=True` lets you count `left_only` (orphans) and `right_only`.

### Different key names
```python
a.merge(b, left_on="cust", right_on="customer_id", how="left")
```

## `concat` — stacking, not matching

```python
pd.concat([jan, feb, mar], ignore_index=True)   # stack rows (axis=0)
pd.concat([df1, df2], axis=1)                    # glue columns (aligns on index!)
```
Use `concat` for "more of the same rows"; use `merge` for "bring in related columns".

## `join` — merge on the index

`a.join(b)` is `merge` that defaults to the index. Convenient when your tables
are already indexed by the key.

## Detecting damage
```python
before = len(items)
m = items.merge(products, on="product_id", how="left")
assert len(m) == before, "row count changed → many-to-many!"
```

## NumPy connection 🔢

Joins are *relational*, not array math — this is where Pandas goes beyond NumPy.
But the **validation** is pure NumPy thinking: `m["_merge"].value_counts()`,
`mask.sum()` to count orphans, set logic on key arrays. After a join you often
fill the NaNs from unmatched rows with `np.where`/`fillna`.

## Visual learning 📊

Post-join, a stacked bar of `_merge` categories (`both` vs `left_only`) instantly
shows your match rate — a data-quality chart worth keeping.

---

## 🔎 Interview Lens (answer in writing)
- **Q18:** Walk through inner/left/right/outer with two Aurora tables — who's lost or invented?
- **Q19:** What risks exist when merging? How do you detect a many-to-many blow-up *before* it corrupts totals?

### Recap
1. Why can a `left` join increase your row count?
2. What do `validate=` and `indicator=` protect you from?
3. `merge` vs `concat` in one line each.

➡️ Open **`practice.ipynb`** (includes NumPy recall checkpoint 2).
"""

t6_quiz = r"""# Topic 06 — Quiz (Merge / Join / Concat)

15 questions. Answers in `../quizzes/06_answers.md`.

## Part A — Multiple Choice
1. Default `how` for `merge`:
   - (a) left  (b) inner  (c) outer  (d) right
2. A left join unexpectedly increases row count because:
   - (a) left had dupes  (b) right key has duplicates (many-to-many)  (c) wrong dtype  (d) NaNs
3. `validate="many_to_one"` raises when:
   - (a) left keys duplicate  (b) right keys are not unique  (c) any NaN  (d) never
4. `indicator=True` adds a column showing:
   - (a) row number  (b) left_only/right_only/both  (c) dtype  (d) the join key
5. To stack three monthly frames row-wise:
   - (a) `merge`  (b) `pd.concat([...], ignore_index=True)`  (c) `join`  (d) `append` only

## Part B — Predict the Output
6. Inner join where left has keys {1,2,3} and right {2,3,4}: how many key matches?
7. `pd.concat([pd.DataFrame({"a":[1]}), pd.DataFrame({"a":[2]})]).shape` → ?
8. left join, 100 left rows, right key unique: row count after?

## Part C — Fill in the Blank
9. Bring product cost into items: `items.merge(products, ________="product_id", how="left")`.
10. Catch duplicate right keys: `merge(..., ________="many_to_one")`.
11. Different key names: `a.merge(b, left_on="cust", ________="customer_id")`.
12. Tag match source: `merge(..., ________=True)`.

## Part D — Debug the Code
13. ```python
    m = orders.merge(items, on="order_id")   # row count exploded
    ```
    Why? Which `how`/`validate` would have warned you?
14. ```python
    a.merge(b, on="id")   # MergeError: dtype mismatch
    ```
    `a.id` is str, `b.id` is int. Fix it.
15. ```python
    pd.concat([df1, df2], axis=1)   # rows misaligned / NaNs
    ```
    Why did axis=1 concat misalign? What controls it?
"""

t6_challenge = r"""# Topic 06 — Challenges (Merge / Join / Concat)

## 🟢 Easy
Left-merge `order_items` with `products` on `product_id`. Confirm the row count
did NOT change: `assert len(merged) == len(items)`.

## 🟡 Medium
Bring `unit_cost` in and compute `line_profit = line_revenue - quantity*unit_cost`.
Count how many lines you *couldn't* cost (missing `unit_cost`). Self-check:
`assert "_merge" in audit.columns`.

## 🔴 Hard — find the orphans
~50 orders reference a `customer_id` that doesn't exist in `customers`. Use a
left merge with `indicator=True` to find them. Self-check:
`assert orphans.shape[0] > 0` and they are all `left_only`.

## 🏢 Real Business Challenge — "True profit, joined safely"
Build the analyst master table: items → products (cost) → orders (channel,
date, customer) → customers (segment), then per-channel **profit**. Validate at
every join (`validate=`, row-count asserts). Self-check:
```python
assert len(master) == len(items), "A join changed the grain — investigate!"
print(profit_by_channel.sort_values(ascending=False))
```

## 🔎 Interview Lens — write answers
- Q18 (join types) and Q19 (merge risks / many-to-many detection).
"""

t6_practice = [
 ("md", "# Topic 06 — Practice: Merge / Join / Concat\n\nThe truth is across tables. Join safely. NumPy recall at the end."),
 ("code", BOOT + "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n"
          "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "products['list_price'] = np.where(products['list_price']<0, np.nan, products['list_price'])\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])"),
 ("md", "## Example — safe left join (row count must not change)"),
 ("code", "before = len(items)\n"
          "m = items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
          "print('rows before/after:', before, len(m))\nassert len(m) == before"),
 ("md", "## Your Turn — line profit\nUsing `m`, compute `line_profit = line_revenue - quantity*unit_cost`. "
        "How many lines are missing cost?"),
 ("code", "m['line_profit'] = ...\nmissing_cost = ...\n"
          "assert 'line_profit' in m.columns\nprint('lines missing cost:', missing_cost)"),
 ("md", "## Mini Mission — find the orphans\nLeft-merge `orders` to `customers` with `indicator=True`; isolate `left_only`."),
 ("code", "om = orders.merge(customers[['customer_id']], on='customer_id', how='left', indicator=True)\n"
          "orphans = ...\nassert orphans.shape[0] > 0\nprint('orphan orders (no customer):', orphans.shape[0])"),
 ("md", "## Boss Fight — master table + profit by channel\nChain joins, validate the grain, then profit per channel."),
 ("code", "master = (items\n"
          "  .merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
          "  .merge(orders[['order_id','channel','customer_id']], on='order_id', how='left', validate='many_to_one'))\n"
          "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\n"
          "assert len(master) == len(items), 'grain changed!'\n"
          "profit_by_channel = ...\nprint(profit_by_channel.sort_values(ascending=False))"),
 ("md", "## 🔢 NumPy Recall Checkpoint (Topics 4–6)\nPure NumPy: simulate a 'join audit' on key arrays."),
 ("code", "left_keys = np.array([1,2,3,4,5])\nright_keys = np.array([3,4,5,6])\n"
          "# TODO numpy-only: matched (in both), orphans (left not in right)\n"
          "matched = ...\norphans_n = ...\n"
          "assert sorted(matched) == [3,4,5]\nassert orphans_n == 2\nprint('NumPy join-audit passed')"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q18 and Q19 in writing.\n"
        "2. Did any join change your row count? What would that have done to revenue?\n"
        "3. Investigation log: what's profit (not just revenue) telling you now?"),
]

t6_solutions = [
 ("md", "# Topic 06 — Solutions"),
 ("code", BOOT + "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "m = items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')"),
 ("code", "m['line_profit'] = m['line_revenue'] - m['quantity']*m['unit_cost']\n"
          "print('missing cost lines:', m['unit_cost'].isna().sum())"),
 ("code", "om = orders.merge(customers[['customer_id']], on='customer_id', how='left', indicator=True)\n"
          "orphans = om[om['_merge']=='left_only']\nprint('orphans:', orphans.shape[0])"),
 ("code", "master = (items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
          "              .merge(orders[['order_id','channel']], on='order_id', how='left', validate='many_to_one'))\n"
          "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\n"
          "print(master.groupby('channel')['line_profit'].sum().sort_values(ascending=False))"),
 ("code", "left_keys = np.array([1,2,3,4,5]); right_keys = np.array([3,4,5,6])\n"
          "matched = np.intersect1d(left_keys, right_keys)\n"
          "orphans_n = int((~np.isin(left_keys, right_keys)).sum())\nprint(matched, orphans_n)"),
 ("md", "### Interview Lens\n- **Q18:** inner=intersection of keys; left=all orders even without a matching "
        "customer (orphans→NaN); right=all customers even with no orders; outer=everything, NaN on both sides.\n"
        "- **Q19:** Risk = duplicate keys on the join side causing a many-to-many fan-out that multiplies rows "
        "and inflates sums. Detect with `validate=`, row-count asserts, `indicator=True`, and checking key "
        "uniqueness (`df[key].is_unique`) before merging."),
]

write("06_Merge_Join_Concat", t6_lesson, t6_quiz, t6_challenge, t6_practice, t6_solutions)
print("Topics 04-06 done.")
