"""Generate topics 01-03: lesson.md, quiz.md, challenge.md, practice.ipynb, solutions.ipynb."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import build_notebook

ROOT = os.path.join(os.path.dirname(__file__), "..")

BOOT = (
    "import numpy as np\n"
    "import pandas as pd\n"
    "pd.set_option('display.max_columns', 30)\n"
    "RAW = '../datasets/raw/'   # the Aurora Outfitters messy data\n"
    "print('pandas', pd.__version__)"
)

def write(topic_dir, lesson, quiz, challenge, practice, solutions):
    d = os.path.join(ROOT, topic_dir)
    with open(os.path.join(d, "lesson.md"), "w") as f: f.write(lesson)
    with open(os.path.join(d, "quiz.md"), "w") as f: f.write(quiz)
    with open(os.path.join(d, "challenge.md"), "w") as f: f.write(challenge)
    build_notebook(practice, os.path.join(d, "practice.ipynb"))
    build_notebook(solutions, os.path.join(d, "solutions.ipynb"))
    print("wrote", topic_dir)

# ===========================================================================
# TOPIC 01 — Introduction & Data Loading
# ===========================================================================
t1_lesson = r"""# Topic 01 — Introduction & Data Loading

> **Investigation milestone:** Day one at Aurora Outfitters. Before you can find
> the revenue problem, you have to *get the data into Python*. Today you load
> every table and take a first, careful look.

**Time split: 20% reading this · 80% in `practice.ipynb`.**

---

## Why Pandas exists (and why you already half-know it)

You know NumPy arrays: fast, homogeneous, numeric. Real business data is
none of those things — it's a mix of strings, dates, money, missing values, and
it has **labels** (column names, customer ids). Pandas is NumPy with labels and
mixed types bolted on, plus a huge toolbox for the boring 80% of analytics:
loading, cleaning, joining, grouping.

- A **`Series`** is a 1-D labelled array (think: one column).
- A **`DataFrame`** is a 2-D table of `Series` sharing one **index** (the row labels).
- Under the hood, each column is essentially a NumPy array — so your NumPy
  instincts about vectorization still apply. We will lean on that all course.

## The single most-used function: `read_csv`

```python
import pandas as pd
orders = pd.read_csv("../datasets/raw/orders.csv")
```

That one line does a lot, and the parameters are where the skill is:

| Parameter | Why you reach for it |
|---|---|
| `dtype=` | Force a column's type (e.g. ids as `str` so `C00123` keeps its zeros). |
| `parse_dates=` | Turn date strings into real datetimes **at load time**. |
| `usecols=` | Read only the columns you need (faster, less memory). |
| `nrows=` | Peek at the first N rows of a huge file. |
| `na_values=` | Tell Pandas which strings mean "missing" (e.g. `"unknown"`, `"N/A"`). |
| `chunksize=` | Stream a file too big for memory (post-course territory, but know it exists). |

> **WHY at load time?** Fixing types while reading is cheaper and avoids a class
> of bugs where `customer_id` becomes a float and `C10000` turns into `10000.0`.

## First-look ritual (do this for EVERY new table)

```python
df.shape        # (rows, columns) — sanity check the size
df.head()       # eyeball the first rows
df.info()       # dtypes + non-null counts → spot wrong types & missing data
df.describe()   # numeric summary → spot outliers and impossible values
df.columns      # exact column names (watch for trailing spaces!)
df.dtypes       # what Pandas guessed
```

`info()` is your best friend on day one: if a column you *expect* to be numeric
shows up as `object`, something is dirty (text mixed in, a stray symbol, …).

## Other readers you'll meet

- `pd.read_excel(...)` — spreadsheets (needs `openpyxl`).
- `pd.read_json`, `pd.read_parquet`, `pd.read_sql` — JSON, columnar files, databases.
- Writing back out: `df.to_csv("out.csv", index=False)` (drop the index unless it's meaningful).

## NumPy connection 🔢

`df.values` (or `df.to_numpy()`) hands you the underlying NumPy array. Every
numeric column is a NumPy array, which is *why* `orders["quantity"] * 2` is
vectorized and fast — no Python loop. Keep this in mind: when something is slow,
you're probably fighting the vectorized path.

## Visual learning 📊

You won't plot much today, but note: the very first chart an analyst draws is
usually a `df["col"].value_counts().plot(kind="bar")` to see category balance.
You'll use it to see how lopsided Aurora's `channel` column is.

---

### Recap (active recall — answer before the quiz)
1. Why force `customer_id` to `str` at load time?
2. What does `info()` tell you that `head()` doesn't?
3. When would you pass `na_values=["unknown"]`?

➡️ Now open **`practice.ipynb`**. Reading is over; loading begins.
"""

t1_quiz = r"""# Topic 01 — Quiz (Introduction & Data Loading)

15 questions. **Answers are in `../quizzes/01_answers.md` — do not peek until you've committed.**

## Part A — Multiple Choice
1. Which is the best way to keep `customer_id` values like `C00042` intact?
   - (a) `read_csv(...)` then `.astype(int)`  (b) `read_csv(..., dtype={"customer_id": str})`  (c) nothing, Pandas handles it  (d) `parse_dates=["customer_id"]`
2. `df.info()` is most useful for:
   - (a) plotting  (b) seeing dtypes and non-null counts  (c) sorting  (d) renaming columns
3. A numeric-looking column loads as `object` dtype. The most likely cause:
   - (a) the file is too big  (b) non-numeric characters are mixed in  (c) Pandas is broken  (d) you used `usecols`
4. `df.describe()` by default summarises:
   - (a) all columns  (b) only numeric columns  (c) only object columns  (d) the index
5. To read only the first 1,000 rows of a large CSV:
   - (a) `nrows=1000`  (b) `head=1000`  (c) `limit=1000`  (d) `chunksize=1000`

## Part B — Predict the Output
6. `pd.Series([1,2,3]).shape` → ?
7. After `df = pd.read_csv(...)`, what type is `df["quantity"]`?
8. If `orders.csv` has 26,050 rows incl. header, what does `len(orders)` return?

## Part C — Fill in the Blank
9. `orders = pd.read_csv(RAW + "orders.csv", ________=["order_date"])`  → parse dates at load.
10. To treat the literal string `"unknown"` as missing: `read_csv(..., ________=["unknown"])`.
11. `df.________` returns the (rows, columns) tuple.
12. Write the index-free CSV export: `df.________("clean.csv", index=False)`.

## Part D — Debug the Code
13. ```python
    orders = pd.read_csv("orders.csv")   # FileNotFoundError
    ```
    The file is in `datasets/raw/`. Fix the path.
14. ```python
    df.info     # nothing prints
    ```
    Why no output? Fix it.
15. ```python
    df = pd.read_csv(RAW + "products.csv", dtype={"unit_cost": int})  # ValueError
    ```
    `unit_cost` has missing values. Why does `int` fail, and what dtype works?
"""

t1_challenge = r"""# Topic 01 — Challenges (Loading & First Look)

No expected outputs are given. Verify your own work with `assert` where stated.

## 🟢 Easy
Load `customers.csv` and `products.csv`. Print the shape and dtypes of each.
Identify (in a markdown note) one column in each that has the *wrong* dtype.

## 🟡 Medium
Load `orders.csv` but: (a) force `customer_id` and `order_id` to `str`, and
(b) read only the columns `order_id, customer_id, channel, status`. Confirm with
`assert set(orders.columns) == {"order_id","customer_id","channel","status"}`.

## 🔴 Hard
The `products.csv` file uses the string `"unknown"` for missing suppliers and
has missing `unit_cost`. Load it so that:
- `"unknown"` suppliers become real `NaN`, and
- `unit_cost` is a float column.
Then report how many products have a missing supplier and how many have a
missing cost — **without** revealing the values here; print them yourself.

## 🏢 Real Business Challenge — "Inventory of evidence"
You can't investigate what you can't load. Write a single function
`load_aurora(raw_dir)` that returns a **dict** of all 9 tables, each loaded with
sensible dtypes (ids as `str`). This loader will be reused in later topics, so
make it clean. Self-check:

```python
data = load_aurora(RAW)
assert set(data) >= {"customers","products","orders","order_items",
                     "returns","marketing_spend","web_traffic",
                     "support_tickets","shipments"}
assert data["orders"]["order_id"].dtype == object   # str stored as object
print("All Aurora tables loaded:", {k: v.shape for k, v in data.items()})
```
"""

t1_practice = [
 ("md", "# Topic 01 — Practice: Introduction & Data Loading\n\n"
        "**Aurora Outfitters, Day 1.** You'll load the company's data and take a first look.\n\n"
        "> Rules of this repo: no expected outputs are shown. Cells with `assert` grade themselves — "
        "if a cell runs silently you passed; an `AssertionError` means fix your code."),
 ("code", BOOT),
 ("md", "## Concept\nA `DataFrame` is a labelled table; `read_csv` loads one. The skill is in the parameters and the *first-look ritual*."),
 ("md", "## Example (worked)\nLoad `orders.csv` and run the first-look ritual. Read the output carefully — which dtypes look wrong?"),
 ("code", "orders = pd.read_csv(RAW + 'orders.csv')\n"
          "print(orders.shape)\n"
          "orders.info()\n"
          "orders.head()"),
 ("md", "## Your Turn\nLoad `customers.csv` into `customers`. Then load `products.csv` into `products`.\n"
        "Force `customer_id` to `str` when loading customers."),
 ("code", "# TODO: load customers (customer_id as str) and products\ncustomers = ...\nproducts = ...\n\n"
          "assert customers.shape[1] == 7, 'customers should have 7 columns'\n"
          "assert customers['customer_id'].dtype == object, 'customer_id should be str/object'\n"
          "assert products.shape[0] > 100, 'products should have >100 rows'\n"
          "print('ok — loaded', customers.shape, products.shape)"),
 ("md", "## Mini Mission — spot the dirty column\n"
        "Use `.info()` and `.head()` on `customers`. In the markdown cell below, write which column "
        "is the wrong dtype and why (hint: a date that's stored as text)."),
 ("code", "customers.info()\ncustomers.head()"),
 ("md", "_Your notes:_ \n\n- The wrong-dtype column is … because …"),
 ("md", "## Boss Fight — the reusable loader\n"
        "Write `load_aurora(raw)` returning a dict of all 9 tables with ids as `str`. "
        "You will import this idea in later topics."),
 ("code", "def load_aurora(raw):\n"
          "    # TODO: load all 9 csvs into a dict; keep *_id columns as str where present\n"
          "    ...\n\n"
          "data = load_aurora(RAW)\n"
          "expected = {'customers','products','orders','order_items','returns',\n"
          "            'marketing_spend','web_traffic','support_tickets','shipments'}\n"
          "assert set(data) >= expected, 'missing tables: ' + str(expected - set(data))\n"
          "print('Loaded:', {k: v.shape for k, v in data.items()})"),
 ("md", "## Reflection (write answers — no key provided)\n"
        "1. Which Aurora columns are stored as the wrong type, and what damage could that cause downstream?\n"
        "2. Why is fixing dtypes at *load* time better than after?\n"
        "3. NumPy recall: `df['quantity'] * 2` is vectorized — what is actually being multiplied under the hood?"),
]

t1_solutions = [
 ("md", "# Topic 01 — Solutions\n\n*Reference solutions. Try the practice first — these spoil the learning if read early.*"),
 ("code", BOOT),
 ("md", "### Your Turn"),
 ("code", "customers = pd.read_csv(RAW + 'customers.csv', dtype={'customer_id': str})\n"
          "products = pd.read_csv(RAW + 'products.csv')\n"
          "print(customers.shape, products.shape)"),
 ("md", "### Mini Mission\n`signup_date` loads as `object` (string) because it contains mixed formats "
        "like `12/03/2023` and `2023-03-12`. Stored as text you cannot do date arithmetic, sort "
        "chronologically, or resample. We fix this properly in Topic 04/07."),
 ("md", "### Boss Fight — loader"),
 ("code", "def load_aurora(raw):\n"
          "    id_cols = ['customer_id','order_id','product_id','ticket_id']\n"
          "    files = ['customers','products','orders','order_items','returns',\n"
          "             'marketing_spend','web_traffic','support_tickets','shipments']\n"
          "    out = {}\n"
          "    for name in files:\n"
          "        df = pd.read_csv(raw + name + '.csv')\n"
          "        for c in id_cols:\n"
          "            if c in df.columns:\n"
          "                df[c] = df[c].astype(str)\n"
          "        out[name] = df\n"
          "    return out\n\n"
          "data = load_aurora(RAW)\n"
          "print({k: v.shape for k, v in data.items()})"),
 ("md", "### Reflection (discussion)\n"
        "1. `signup_date`, `order_date`, `promised/shipped_date` are text; numeric ids could become "
        "floats and lose leading info. Damage: broken joins, wrong sorts, impossible aggregations.\n"
        "2. Cheaper, and avoids float-id corruption + repeated conversions.\n"
        "3. Two NumPy int/float arrays element-wise — no Python-level loop, executed in C."),
]

write("01_Introduction_And_Data_Loading", t1_lesson, t1_quiz, t1_challenge, t1_practice, t1_solutions)

# ===========================================================================
# TOPIC 02 — Series & DataFrames
# ===========================================================================
t2_lesson = r"""# Topic 02 — Series & DataFrames

> **Investigation milestone:** To compute revenue you must understand the two
> objects everything is made of. Today you build `Series`, inspect the index,
> and compute **line revenue** on Aurora's order items — your first real metric.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## The Series: a labelled 1-D array

```python
s = pd.Series([10, 20, 30], index=["a", "b", "c"], name="spend")
```

A `Series` has **values** (a NumPy array) and an **index** (the labels). The
index is not decoration — it drives **alignment**: when you add two Series,
Pandas lines them up *by label*, not by position.

```python
pd.Series({"uk": 1}) + pd.Series({"uk": 10, "de": 5})
# uk -> 11, de -> NaN   (de had no match → missing)
```

> This auto-alignment is a superpower and a footgun. Most "why is everything
> NaN?!" bugs are misaligned indexes.

## The DataFrame: aligned Series sharing one index

A `DataFrame` is a dict of `Series` that all share the **same row index**.
Selecting one column returns a `Series`:

```python
orders["channel"]          # Series
orders[["channel","status"]]  # DataFrame (note the double brackets)
```

## The index — respect it

- Default index is a `RangeIndex` (0,1,2,…). You can set a meaningful one:
  `orders.set_index("order_id")`.
- `reset_index()` pushes the index back into a column.
- A good index makes lookups (`.loc["O200001"]`) and joins effortless.

## Creating columns = vectorized NumPy

Your first metric. Each order line's revenue is
`quantity × unit_price × (1 − discount)`:

```python
items["line_revenue"] = items["quantity"] * items["unit_price"] * (1 - items["discount"])
```

No loop. This is element-wise NumPy across three columns at once. **This is the
single most important habit in the course: think in whole columns, not rows.**

## Useful Series/DataFrame methods

| Method | Use |
|---|---|
| `value_counts()` | frequency of each category (great first chart) |
| `unique()`, `nunique()` | distinct values / count of them |
| `sort_values()`, `sort_index()` | ordering |
| `rename(columns={...})` | tidy names |
| `assign(new=...)` | add columns without mutating in place |
| `astype()` | change dtype |

## NumPy connection 🔢

A `Series` *is* a NumPy array plus an index. `s.values` → the array.
Operations like `np.log(s)`, `s > s.mean()`, and boolean masks behave exactly
like NumPy — because they essentially *are* NumPy. When you write
`items["line_revenue"] = ...`, you're doing array math and Pandas keeps the labels aligned.

## Visual learning 📊

`orders["channel"].value_counts().plot(kind="bar")` answers a business
question: *which sales channel dominates?* You'll draw it in practice.

---

### Recap
1. What does the index control when you add two Series?
2. Why double brackets for multiple columns?
3. Write line revenue as a single vectorized expression.

➡️ Open **`practice.ipynb`**.
"""

t2_quiz = r"""# Topic 02 — Quiz (Series & DataFrames)

15 questions. Answers in `../quizzes/02_answers.md`.

## Part A — Multiple Choice
1. Selecting a single column `df["x"]` returns a:
   - (a) DataFrame  (b) Series  (c) NumPy array  (d) list
2. `df[["a","b"]]` returns a:
   - (a) Series  (b) DataFrame  (c) tuple  (d) error
3. Adding two Series aligns them by:
   - (a) position  (b) the index labels  (c) dtype  (d) column order
4. Which gives the number of *distinct* channels?
   - (a) `df.channel.count()`  (b) `df.channel.nunique()`  (c) `len(df)`  (d) `df.channel.shape`
5. `assign` differs from `df["new"]=...` because it:
   - (a) is slower always  (b) returns a new DataFrame without mutating in place  (c) can't add columns  (d) drops the index

## Part B — Predict the Output
6. `pd.Series([1,2]) + pd.Series([1,2], index=[1,2])` → values at index 0,1,2?
7. `(pd.Series([2,4,6])).mean()` → ?
8. `df[["channel"]].shape[1]` → ?

## Part C — Fill in the Blank
9. Make order_id the row label: `orders.________("order_id")`.
10. Frequency of each status: `orders["status"].________()`.
11. Add a column without mutating: `orders.________(year=2024)`.
12. Underlying NumPy array of a Series: `s.________`.

## Part D — Debug the Code
13. ```python
    items["rev"] = items.quantity * items.unit_price * 1 - items.discount  # wrong totals
    ```
    Operator precedence bug — fix it.
14. ```python
    top = orders["channel","status"]   # KeyError
    ```
    Fix the selection of two columns.
15. ```python
    s = pd.Series([1,2,3], index=["a","b","c"])
    s2 = pd.Series([10,20,30])
    s + s2   # all NaN — why?
    ```
"""

t2_challenge = r"""# Topic 02 — Challenges (Series & DataFrames)

## 🟢 Easy
From `orders`, produce a Series of `channel` frequencies sorted high→low.
Which channel dominates? (Write your read of it — no key.)

## 🟡 Medium
On `order_items`, create `line_revenue = quantity * unit_price * (1 - discount)`.
Then `assert items["line_revenue"].notna().sum() > 0` and report total revenue
across all lines that have a price.

## 🔴 Hard
Set `order_id` as the index of `orders`, then look up three specific order ids
with `.loc[[...]]`. Explain why a meaningful index makes this cleaner than
boolean filtering. Self-check: `assert orders_idx.index.name == "order_id"`.

## 🏢 Real Business Challenge — "First revenue number"
Management asks: *"What was our gross line-item revenue, ignoring returns and
missing prices?"* Compute it from `order_items` with one vectorized expression,
guarding against the missing `unit_price` rows. Self-check:

```python
assert revenue > 0, "The report still contains an issue."
print(f"Gross line revenue: £{revenue:,.0f}")
```
Note in your investigation log: this is the number we'll later try to reconcile.
"""

t2_practice = [
 ("md", "# Topic 02 — Practice: Series & DataFrames\n\nBuild the objects, respect the index, compute your first metric."),
 ("code", BOOT),
 ("md", "## Concept\nSeries = values + index. DataFrame = aligned Series. New columns are vectorized NumPy."),
 ("md", "## Example — alignment in action\nRun this and notice how `de` becomes NaN (no match)."),
 ("code", "a = pd.Series({'uk': 1, 'fr': 2})\n"
          "b = pd.Series({'uk': 10, 'de': 5})\n"
          "print(a + b)"),
 ("md", "## Your Turn — line revenue\nLoad `order_items.csv` and add a `line_revenue` column "
        "(`quantity * unit_price * (1 - discount)`)."),
 ("code", "items = pd.read_csv(RAW + 'order_items.csv', dtype={'order_id': str, 'product_id': str})\n"
          "# TODO: add line_revenue\nitems['line_revenue'] = ...\n\n"
          "assert 'line_revenue' in items.columns\n"
          "assert items['line_revenue'].notna().sum() > 0, 'all revenue is NaN — check the formula/columns'\n"
          "print('rows with a revenue value:', items['line_revenue'].notna().sum())"),
 ("md", "## Mini Mission — channel mix\nMake a Series of `channel` value counts on `orders` and plot a bar chart. "
        "What does it say about where Aurora sells?"),
 ("code", "orders = pd.read_csv(RAW + 'orders.csv', dtype={'order_id': str})\n"
          "# TODO: counts = ...  then counts.plot(kind='bar')\ncounts = ...\n"
          "assert counts.sum() == len(orders)\ncounts"),
 ("md", "_Your read:_ "),
 ("md", "## Boss Fight — first revenue number\nCompute total gross line revenue (ignore NaN prices). One expression."),
 ("code", "revenue = ...\nassert revenue > 0, 'The report still contains an issue.'\n"
          "print(f'Gross line revenue: £{revenue:,.0f}')"),
 ("md", "## Reflection\n1. Where could index misalignment silently inject NaNs in your work?\n"
        "2. Why is the vectorized revenue formula better than a Python loop over rows?\n"
        "3. NumPy recall: how would you write the same revenue calc with raw NumPy arrays?"),
]

t2_solutions = [
 ("md", "# Topic 02 — Solutions"),
 ("code", BOOT),
 ("code", "items = pd.read_csv(RAW + 'order_items.csv', dtype={'order_id': str, 'product_id': str})\n"
          "items['line_revenue'] = items['quantity'] * items['unit_price'] * (1 - items['discount'])\n"
          "print(items['line_revenue'].describe())"),
 ("code", "orders = pd.read_csv(RAW + 'orders.csv', dtype={'order_id': str})\n"
          "counts = orders['channel'].value_counts()\n"
          "counts.plot(kind='bar', title='Orders by channel (raw, before cleaning case)')\n"
          "print(counts)\n"
          "# Note: 'Online' and 'online' are split — a cleaning problem for Topic 04."),
 ("code", "revenue = (items['quantity'] * items['unit_price'] * (1 - items['discount'])).sum()\n"
          "print(f'Gross line revenue: £{revenue:,.0f}')"),
 ("md", "### Reflection\n1. Any time you build a Series from a groupby/lookup and combine with another — "
        "align indexes first.\n2. Vectorized = one C-level pass, readable, less error-prone.\n"
        "3. `q = items['quantity'].to_numpy(); p = items['unit_price'].to_numpy(); (q*p*(1-d)).sum()` with nan-safe handling."),
]

write("02_Series_And_DataFrames", t2_lesson, t2_quiz, t2_challenge, t2_practice, t2_solutions)

# ===========================================================================
# TOPIC 03 — Selection, Filtering & Boolean Logic
# ===========================================================================
t3_lesson = r"""# Topic 03 — Selection, Filtering & Boolean Logic

> **Investigation milestone:** Now you can *interrogate* the data. You'll isolate
> cancelled orders, marketplace sales, and the absurd 1,500-unit order lines that
> are skewing totals. Filtering is how an analyst asks questions.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## Three ways to select, and when to use each

| Tool | Selects by | Use when |
|---|---|---|
| `df["col"]` / `df[["a","b"]]` | column name | grabbing columns |
| `df.loc[rows, cols]` | **labels** (and boolean masks) | the default for analysts |
| `df.iloc[rows, cols]` | **integer positions** | you genuinely mean "the 3rd row" |

```python
orders.loc[orders["status"] == "cancelled", ["order_id", "channel"]]
orders.iloc[0:5, :]      # first 5 rows, all columns — by position
```

> **Rule of thumb:** reach for `.loc` with a boolean mask. Use `.iloc` rarely.

## Boolean masks — the heart of filtering

A comparison on a Series gives a boolean Series (a mask). Pass it to `.loc`:

```python
mask = orders["status"] == "cancelled"
orders.loc[mask]
```

### Combining conditions — `&  |  ~` and **parentheses**
```python
big = (items["quantity"] > 100) & (items["unit_price"] > 50)
items.loc[big]
```
- Use `&` (and), `|` (or), `~` (not) — **not** Python's `and/or/not`.
- **Wrap each condition in parentheses** — `&` binds tighter than `>`, so
  missing parens raises a confusing error.

### Handy mask builders
- `s.isin(["online", "Online"])` — membership (cleaner than chained `==`).
- `s.between(10, 100)` — inclusive range.
- `s.isna()` / `s.notna()` — missingness.
- `~mask` — invert.

## `query()` — readable filtering

```python
items.query("quantity > 100 and unit_price > 50")
```
Nice for long conditions; uses column names directly. Slightly slower and less
flexible than masks — your call.

## View vs copy & the `SettingWithCopyWarning`

```python
subset = orders[orders["channel"] == "Online"]
subset["flag"] = 1     # ⚠️ SettingWithCopyWarning — maybe a view, maybe a copy
```
If you intend a separate object, **be explicit**: `subset = orders.loc[mask].copy()`.
To assign back into the original, do it in one `.loc` statement:
`orders.loc[mask, "flag"] = 1`. Avoid chained indexing like `df[mask]["col"] = ...`.

## NumPy connection 🔢

A boolean mask is exactly NumPy boolean indexing. `np.where(mask, a, b)` and
`s.where(cond, other)` both pick element-wise. `mask.sum()` counts `True`s
because `True==1` — a NumPy idiom you'll use constantly to *count matching rows*.

## Visual learning 📊

Filter, then plot: `items.loc[big, "quantity"].plot(kind="hist")` shows just how
extreme the outlier order lines are. Filtering + a quick chart = fast evidence.

---

## 🔎 Interview Lens (answer in writing)
- **Q11:** Why must you use `&`/`|` instead of `and`/`or`, and why the parentheses?
- **Q4:** Why can chained indexing silently fail? What is `SettingWithCopyWarning` telling you?

### Recap
1. `.loc` vs `.iloc` in one sentence each.
2. Rewrite `(s=="a")|(s=="b")|(s=="c")` with `isin`.
3. How do you count how many rows match a mask?

➡️ Open **`practice.ipynb`**. NumPy recall checkpoint is at the end (every 3 topics).
"""

t3_quiz = r"""# Topic 03 — Quiz (Selection, Filtering & Boolean Logic)

15 questions. Answers in `../quizzes/03_answers.md`.

## Part A — Multiple Choice
1. To select by integer position use:
   - (a) `.loc`  (b) `.iloc`  (c) `.at`  (d) `.query`
2. The correct boolean AND for masks is:
   - (a) `and`  (b) `&`  (c) `+`  (d) `&&`
3. `orders["status"].isin(["cancelled","returned"])` is cleaner than:
   - (a) two merges  (b) `(status=="cancelled") | (status=="returned")`  (c) a groupby  (d) `.iloc`
4. `SettingWithCopyWarning` usually means:
   - (a) out of memory  (b) you assigned into a possible view via chained indexing  (c) wrong dtype  (d) missing index
5. `mask.sum()` returns:
   - (a) the matching rows  (b) the count of True values  (c) always 0  (d) the column sum

## Part B — Predict the Output
6. `pd.Series([1,2,3,4]).between(2,3).sum()` → ?
7. `(pd.Series([5,15,25]) > 10).sum()` → ?
8. `pd.Series([1,np.nan,3]).notna().sum()` → ?

## Part C — Fill in the Blank
9. Cancelled orders only: `orders.loc[orders["status"] == ________]`.
10. Members of a set: `s.________(["a","b"])`.
11. Invert a mask: `________mask`.
12. Safe subset copy: `sub = orders.loc[mask].________()`.

## Part D — Debug the Code
13. ```python
    items[items.quantity > 100 & items.unit_price > 50]   # error
    ```
    Add the missing parentheses.
14. ```python
    online = orders[orders.channel == "Online"]
    online["promo"] = True     # warning
    ```
    Rewrite to avoid `SettingWithCopyWarning`.
15. ```python
    orders.loc[orders.status == "cancelled" and orders.channel == "Phone"]  # ValueError
    ```
    Why does `and` fail here? Fix it.
"""

t3_challenge = r"""# Topic 03 — Challenges (Selection & Filtering)

## 🟢 Easy
Select all orders whose `channel` is any marketplace spelling
(`"Marketplace"` or `"marketplace"`) using `isin`. Count them with `.sum()` on the mask.

## 🟡 Medium
On `order_items` with `line_revenue` computed, isolate the **outlier** lines where
`quantity > 100`. How many are there, and what is their combined `line_revenue`?
Self-check: `assert outliers.shape[0] >= 1`.

## 🔴 Hard
Without chained indexing, add a boolean column `is_suspect` to `order_items` that
is `True` when `quantity > 100` **or** `unit_price` is missing. Do it in a single
`.loc` (or `np.where`) statement. Self-check:
`assert items["is_suspect"].dtype == bool`.

## 🏢 Real Business Challenge — "Where is revenue leaking?"
Build a filtered view of `orders` that an auditor would want: status in
`{cancelled, returned}` **and** channel is online or marketplace (any casing).
Report the share of all orders this represents. Self-check:

```python
assert 0 < leak_share < 1, "Share must be a fraction between 0 and 1."
print(f"Suspect orders: {leak_share:.1%} of all orders")
```

## 🔎 Interview Lens — answer in writing
- Q11 (parentheses & `&`/`|`) and Q4 (`SettingWithCopyWarning`) from `interview_lens.md`.
"""

t3_practice = [
 ("md", "# Topic 03 — Practice: Selection, Filtering & Boolean Logic\n\nAsk the data questions. Then a NumPy recall checkpoint."),
 ("code", BOOT + "\n"
          "orders = pd.read_csv(RAW + 'orders.csv', dtype={'order_id': str, 'customer_id': str})\n"
          "items = pd.read_csv(RAW + 'order_items.csv', dtype={'order_id': str, 'product_id': str})\n"
          "items['line_revenue'] = items['quantity'] * items['unit_price'] * (1 - items['discount'])"),
 ("md", "## Example\nIsolate cancelled orders with a boolean mask and `.loc`."),
 ("code", "mask = orders['status'] == 'cancelled'\nprint('cancelled orders:', mask.sum())\norders.loc[mask].head()"),
 ("md", "## Your Turn — combine conditions\nSelect order *lines* where `quantity > 100` AND `unit_price > 50`. "
        "Remember `&` and parentheses."),
 ("code", "big = ...\nassert big.dtype == bool, 'big should be a boolean mask'\nprint('big lines:', big.sum())\nitems.loc[big]"),
 ("md", "## Mini Mission — isin\nSelect all marketplace orders regardless of casing using `isin`, and count them."),
 ("code", "mkt = orders['channel'].isin(['Marketplace','marketplace'])\n# TODO confirm\nassert mkt.sum() > 0\nprint('marketplace orders:', mkt.sum())"),
 ("md", "## Boss Fight — revenue leak view (no chained indexing!)\n"
        "Add `is_suspect` to items (`quantity>100` OR missing `unit_price`) in ONE statement."),
 ("code", "# TODO: items['is_suspect'] = ...\n"
          "assert items['is_suspect'].dtype == bool\n"
          "print('suspect lines:', items['is_suspect'].sum())"),
 ("md", "## 🔢 NumPy Recall Checkpoint (Topics 1–3)\nNo Pandas allowed in this cell — pure NumPy. "
        "Prove you still own the fundamentals."),
 ("code", "arr = np.array([5, 150, 30, np.nan, 1200, 12])\n"
          "# TODO with NumPy only:\n"
          "# 1) count values > 100  -> n_big\n"
          "# 2) replace NaN with 0  -> filled\n"
          "# 3) mean ignoring NaN   -> m\n"
          "n_big = ...\nfilled = ...\nm = ...\n"
          "assert n_big == 2\nassert not np.isnan(filled).any()\nassert round(m,2) == round(np.nanmean(arr),2)\n"
          "print('NumPy recall passed')"),
 ("md", "## Reflection / Interview Lens\n"
        "1. Answer interview Q11 and Q4 in writing.\n"
        "2. When is `query()` clearer than a mask? When worse?\n"
        "3. Investigation log: what did filtering reveal about suspect orders?"),
]

t3_solutions = [
 ("md", "# Topic 03 — Solutions"),
 ("code", BOOT + "\n"
          "orders = pd.read_csv(RAW + 'orders.csv', dtype={'order_id': str, 'customer_id': str})\n"
          "items = pd.read_csv(RAW + 'order_items.csv', dtype={'order_id': str, 'product_id': str})\n"
          "items['line_revenue'] = items['quantity'] * items['unit_price'] * (1 - items['discount'])"),
 ("code", "big = (items['quantity'] > 100) & (items['unit_price'] > 50)\nprint(big.sum())"),
 ("code", "mkt = orders['channel'].isin(['Marketplace','marketplace'])\nprint(mkt.sum())"),
 ("code", "items['is_suspect'] = (items['quantity'] > 100) | (items['unit_price'].isna())\n"
          "# equivalently: np.where((items['quantity']>100)|(items['unit_price'].isna()), True, False)\n"
          "print(items['is_suspect'].sum())"),
 ("code", "arr = np.array([5, 150, 30, np.nan, 1200, 12])\n"
          "n_big = int((arr > 100).sum())          # NaN compares False, fine here\n"
          "filled = np.nan_to_num(arr, nan=0.0)\n"
          "m = np.nanmean(arr)\n"
          "print(n_big, filled, round(m,2))"),
 ("md", "### Interview Lens (talking points)\n"
        "- **Q11:** `&/|` are element-wise on arrays; `and/or` try to take the truth value of a whole "
        "Series → ambiguous → error. Parentheses because `&` has higher precedence than `>`.\n"
        "- **Q4:** Chained indexing creates an intermediate object that may be a view or copy; assigning "
        "to it may touch the temporary, not the original. Use a single `.loc[mask, col] = ...` or `.copy()`."),
]

write("03_Selection_Filtering_And_Boolean_Logic", t3_lesson, t3_quiz, t3_challenge, t3_practice, t3_solutions)
print("Topics 01-03 done.")
