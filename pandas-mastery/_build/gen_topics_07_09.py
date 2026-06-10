"""Generate topics 07-09."""
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
# TOPIC 07 — DateTime & Time Series
# ===========================================================================
t7_lesson = r"""# Topic 07 — DateTime & Time Series

> **Investigation milestone:** The big break. Aurora's `order_date` is stored in
> *mixed formats*; once parsed correctly you can finally plot revenue over time —
> and the suspicious **dip** the finance team worried about becomes visible. Was
> it real, or a parsing artifact?

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## Parsing messy dates

```python
orders["order_date"] = pd.to_datetime(orders["order_date"],
                                       format="mixed", dayfirst=True,
                                       errors="coerce")
```
- `format="mixed"` handles rows with different formats (Aurora has 4).
- `dayfirst=True` reads `03/04/2023` as 3 April (European), not 4 March.
- `errors="coerce"` turns unparseable junk into `NaT` (missing datetime) instead
  of crashing — then you *count* the NaT to measure data quality.

> **WHY parse, not eyeball:** as text, `"12/2023"` sorts before `"2/2024"`
> alphabetically. A wrong dip in the chart is often just a wrong sort.

## The `.dt` accessor — pull parts out

```python
orders["year"]  = orders["order_date"].dt.year
orders["month"] = orders["order_date"].dt.to_period("M")   # 2023-11
orders["dow"]   = orders["order_date"].dt.day_name()
orders["is_weekend"] = orders["order_date"].dt.weekday >= 5
```

## `resample` — groupby for time

Set a datetime index, then resample to any frequency:
```python
ts = order_rev.set_index("order_date")
monthly = ts["line_revenue"].resample("M").sum()   # ME in newer pandas
weekly  = ts["line_revenue"].resample("W").sum()
```
`resample` = "group by time bucket". `D`, `W`, `M`, `Q`, `Y` (and `ME`/`MS`).

## Rolling & shift — trends and growth

```python
monthly.rolling(3).mean()         # 3-month moving average (smooths noise)
monthly.pct_change()              # month-over-month growth
monthly.shift(1)                  # previous month's value (for comparisons)
monthly - monthly.shift(12)       # year-over-year change
```

## Gaps in time series

Aurora's `marketing_spend` is **missing a few days**. Reindex to a full date
range and decide: `fillna(0)`? interpolate? leave NaT? (Interview Q24).
```python
full = pd.date_range(start, end, freq="D")
daily = daily.reindex(full)
```

## NumPy connection 🔢

Datetimes are stored as `datetime64[ns]` — a NumPy dtype (int nanoseconds under
the hood). Differences give `timedelta64`. `rolling().mean()` is a vectorized
windowed reduction; `shift` is an array roll. Your NumPy intuition transfers.

## Visual learning 📊

The signature chart: `monthly.plot()` with a `rolling(3).mean()` overlay. This
is *the* chart that reveals (or debunks) the revenue dip. Add it to the capstone.

---

## 🔎 Interview Lens (answer in writing)
- **Q22:** Why is `parse_dates`/parsing at load better than converting after? When is the reverse true?
- **Q24:** How do you handle gaps in a daily series — `fillna` vs interpolation risks?

### Recap
1. What does `errors="coerce"` give you, and why is that *useful*?
2. `resample("M").sum()` vs `groupby(month).sum()` — same or different?
3. How do you compute month-over-month growth in one call?

➡️ Open **`practice.ipynb`**.
"""

t7_quiz = r"""# Topic 07 — Quiz (DateTime & Time Series)

15 questions. Answers in `../quizzes/07_answers.md`.

## Part A — Multiple Choice
1. `errors="coerce"` in `to_datetime`:
   - (a) drops rows  (b) turns bad values into NaT  (c) raises  (d) guesses
2. `dayfirst=True` reads `03/04/2023` as:
   - (a) 4 March  (b) 3 April  (c) error  (d) 2023-03-04
3. `resample("M").sum()` requires:
   - (a) a sorted column  (b) a datetime index  (c) a category dtype  (d) no NaN
4. `monthly.pct_change()` gives:
   - (a) cumulative sum  (b) period-over-period growth  (c) rolling mean  (d) rank
5. `s.dt.day_name()` returns:
   - (a) numbers  (b) weekday names  (c) month names  (d) NaT

## Part B — Predict the Output
6. `pd.to_datetime("13/01/2023", dayfirst=True).month` → ?
7. `pd.Series(pd.to_datetime(["2023-01-01","2023-02-01"])).diff().iloc[1].days` → ?
8. `pd.to_datetime("not a date", errors="coerce")` → ?

## Part C — Fill in the Blank
9. Parse mixed formats: `pd.to_datetime(s, format="________", dayfirst=True)`.
10. Month period: `s.dt.________("M")`.
11. 3-period moving average: `m.________(3).mean()`.
12. Monthly buckets from datetime index: `ts.________("M").sum()`.

## Part D — Debug the Code
13. ```python
    orders["order_date"].dt.year   # AttributeError: .dt accessor
    ```
    Why? Fix it before using `.dt`.
14. ```python
    monthly = rev.resample("M").sum()   # TypeError: not DatetimeIndex
    ```
    Fix the index.
15. ```python
    pd.to_datetime(orders["order_date"])   # some dates flipped month/day
    ```
    Why are European dates misread? Add the right argument.
"""

t7_challenge = r"""# Topic 07 — Challenges (DateTime & Time Series)

## 🟢 Easy
Parse `orders["order_date"]` robustly. Count how many became `NaT`. Self-check:
`assert orders["order_date"].notna().mean() > 0.95`.

## 🟡 Medium
Build monthly revenue (join line revenue to order dates, resample to month).
Add a 3-month moving average. Self-check:
`assert monthly.index.is_monotonic_increasing`.

## 🔴 Hard — the dip
Compute month-over-month growth (`pct_change`). Find the worst month and the
best month. Is the "dip" a real revenue fall or an artifact of dirty
dates/returns? Write your verdict (no key). Self-check:
`assert mom.notna().sum() > 10`.

## 🏢 Real Business Challenge — "Marketing vs revenue, aligned in time"
`marketing_spend` has missing days. Build a daily revenue series and a daily
spend series on a *complete* date index, then compute their correlation.
Self-check:
```python
assert daily_rev.index.equals(daily_spend.index), "Series must share a full date index"
print("corr(spend, revenue):", round(corr, 3))
```

## 🔎 Interview Lens — write answers
- Q22 (parse at load) and Q24 (time-series gaps).
"""

t7_practice = [
 ("md", "# Topic 07 — Practice: DateTime & Time Series\n\nParse the messy dates; reveal (or debunk) the dip."),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])"),
 ("md", "## Example — parse mixed-format dates\nNote how many fail to parse (NaT)."),
 ("code", "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "print('parsed ok:', orders['order_date'].notna().mean())\norders[['order_id','order_date']].head()"),
 ("md", "## Your Turn — monthly revenue\nJoin line revenue to order dates, set datetime index, resample to monthly sum."),
 ("code", "oi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
          "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\n"
          "monthly = ...\n"
          "assert monthly.index.is_monotonic_increasing\nmonthly.plot(title='Aurora monthly revenue')"),
 ("md", "## Mini Mission — moving average + growth\nAdd a 3-month moving average and month-over-month growth."),
 ("code", "ma3 = monthly.rolling(3).mean()\nmom = monthly.pct_change()\n"
          "assert mom.notna().sum() > 10\n"
          "print('worst month:', mom.idxmin(), '| best month:', mom.idxmax())\n"
          "monthly.plot(label='revenue'); ma3.plot(label='3mo MA'); import matplotlib.pyplot as plt; plt.legend()"),
 ("md", "## Boss Fight — align spend & revenue on a full daily index\nReindex to a gap-free date range, then correlate."),
 ("code", "mk = pd.read_csv(RAW+'marketing_spend.csv', parse_dates=['date'])\n"
          "daily_spend = mk.groupby('date')['spend_gbp'].sum()\n"
          "daily_rev = oi.dropna(subset=['order_date']).groupby('order_date')['line_revenue'].sum()\n"
          "full = pd.date_range(daily_rev.index.min(), daily_rev.index.max(), freq='D')\n"
          "daily_rev = daily_rev.reindex(full).fillna(0)\ndaily_spend = daily_spend.reindex(full).fillna(0)\n"
          "corr = ...\nassert daily_rev.index.equals(daily_spend.index)\nprint('corr:', round(corr,3))"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q22 and Q24.\n2. Is the dip real? What's your evidence?\n"
        "3. Investigation log: what does the time pattern say about Aurora's revenue?"),
]

t7_solutions = [
 ("md", "# Topic 07 — Solutions"),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "oi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')"),
 ("code", "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\n"
          "monthly = ts['line_revenue'].resample('ME').sum()\nprint(monthly.head())"),
 ("code", "mom = monthly.pct_change()\nprint('worst:', mom.idxmin(), 'best:', mom.idxmax())"),
 ("code", "mk = pd.read_csv(RAW+'marketing_spend.csv', parse_dates=['date'])\n"
          "daily_spend = mk.groupby('date')['spend_gbp'].sum()\n"
          "daily_rev = ts['line_revenue'].resample('D').sum()\n"
          "full = pd.date_range(daily_rev.index.min(), daily_rev.index.max(), freq='D')\n"
          "daily_rev = daily_rev.reindex(full).fillna(0); daily_spend = daily_spend.reindex(full).fillna(0)\n"
          "print('corr:', round(daily_rev.corr(daily_spend),3))"),
 ("md", "### Interview Lens\n- **Q22:** Parsing at load sets the right dtype once, avoids repeated conversions "
        "and float-id style corruption; convert-after is fine for ad-hoc/one-off columns or when you must "
        "inspect the raw text first.\n- **Q24:** `fillna(0)` says 'nothing happened' (honest for spend on a "
        "non-spend day, dishonest for a sensor that was merely offline); interpolation invents plausible "
        "values (good for continuous signals, dangerous for counts/money). Always reindex to a full range first."),
]

write("07_DateTime_And_Time_Series", t7_lesson, t7_quiz, t7_challenge, t7_practice, t7_solutions)

# ===========================================================================
# TOPIC 08 — String Operations & Text Data
# ===========================================================================
t8_lesson = r"""# Topic 08 — String Operations & Text Data

> **Investigation milestone:** Customers are *telling* you what's wrong — in
> 3,000 support tickets. You'll mine free text for order numbers, complaint
> themes (damaged, late, wrong size), and rough sentiment to corroborate the
> returns spike.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## The `.str` accessor — vectorized string ops

Every Python string method has a vectorized `.str` twin that runs across the
whole column and skips `NaN` safely:

```python
s.str.lower()             # casing
s.str.strip()             # trim whitespace
s.str.contains("late")    # boolean mask (regex by default!)
s.str.replace("damaged", "broken", regex=False)
s.str.len()               # length
s.str.split(" ")          # list per row
s.str.startswith("RETURN")
```

> `contains` uses **regex by default**. Pass `regex=False` for literal text, or
> `na=False` so missing values don't poison your boolean mask.

## Extracting structure with regex

```python
tickets["order_ref"] = tickets["message"].str.extract(r"(O\d{6})")
```
`extract` pulls the first capture group into a new column — perfect for fishing
order ids out of free text. `str.extractall` gets *every* match.

## Cleaning text categories

The messy `return_reason` (`"wrong size"`, `"Wrong Size"`) is a string-cleaning
job: `str.strip().str.lower()` then map synonyms — exactly Topic 4, applied to text.

## Building features from text (theme flags)

```python
msg = tickets["message"].str.lower()
tickets["is_late"]    = msg.str.contains("late|where is", regex=True, na=False)
tickets["is_damaged"] = msg.str.contains("damaged|broken|leak", regex=True, na=False)
```
These boolean flags become countable evidence — *how many* tickets mention
lateness, and do they spike with the revenue dip?

## NumPy connection 🔢

`.str.contains(...)` returns a boolean Series = a NumPy boolean mask. `.sum()`
counts matches; combine flags with `&`/`|` exactly like Topic 3. Text → booleans
→ vectorized counting.

## Visual learning 📊

A bar chart of theme-flag counts (`late`, `damaged`, `wrong size`) turns 3,000
unstructured messages into one readable "voice of the customer" chart.

---

## 🔎 Interview Lens (answer in writing)
- **Q9 (revisit):** A text column hides numbers — how do you reliably extract and validate them?
- Pick any open question and connect it to mining unstructured data.

### Recap
1. Why pass `na=False` to `str.contains`?
2. What does `str.extract(r"(O\d{6})")` return, and from where?
3. How do theme flags turn text into countable evidence?

➡️ Open **`practice.ipynb`**.
"""

t8_quiz = r"""# Topic 08 — Quiz (String Operations & Text Data)

15 questions. Answers in `../quizzes/08_answers.md`.

## Part A — Multiple Choice
1. `s.str.contains("late")` by default treats the pattern as:
   - (a) literal  (b) regex  (c) glob  (d) case-sensitive only
2. To avoid NaN breaking a boolean mask:
   - (a) `regex=True`  (b) `na=False`  (c) `case=False`  (d) `strip()`
3. `s.str.extract(r"(O\d{6})")` returns:
   - (a) a boolean  (b) a DataFrame/Series of the captured group  (c) a count  (d) a list
4. Vectorized lowercase:
   - (a) `s.lower()`  (b) `s.str.lower()`  (c) `lower(s)`  (d) `s.map(str.lower)` only
5. `str.strip()` removes:
   - (a) all spaces  (b) leading/trailing whitespace  (c) vowels  (d) digits

## Part B — Predict the Output
6. `pd.Series(["abc","de"]).str.len().tolist()` → ?
7. `pd.Series(["late","ok"]).str.contains("late").sum()` → ?
8. `pd.Series(["O200001 hi"]).str.extract(r"(O\d{6})").iloc[0,0]` → ?

## Part C — Fill in the Blank
9. Literal (non-regex) replace: `s.str.replace("a","b", ________=False)`.
10. Trim + lowercase reasons: `s.str.________().str.________()`.
11. Pull order ids: `s.str.________(r"(O\d{6})")`.
12. Safe contains with NaN: `s.str.contains("x", ________=False)`.

## Part D — Debug the Code
13. ```python
    tickets["message"].contains("late")   # AttributeError
    ```
    Add the missing accessor.
14. ```python
    s.str.contains("late")   # ValueError: cannot mask with NA
    ```
    Add the argument that fixes it.
15. ```python
    s.str.replace(".", "")   # removed everything!
    ```
    Why? `.` is regex 'any char'. Fix it two ways.
"""

t8_challenge = r"""# Topic 08 — Challenges (String Operations & Text Data)

## 🟢 Easy
Standardise `support_tickets["ticket_status"]` casing and `returns["return_reason"]`
(strip + lower). Self-check: `assert tickets["ticket_status"].str.islower().all()`.

## 🟡 Medium
Extract the order id (`O######`) from each ticket message into `order_ref`.
How many messages contain a recoverable order id? Self-check:
`assert tickets["order_ref"].notna().sum() > 0`.

## 🔴 Hard — theme flags
Create boolean columns `is_late`, `is_damaged`, `is_refund` from message text.
Count each. Self-check: `assert tickets[["is_late","is_damaged","is_refund"]].dtypes.eq(bool).all()`.

## 🏢 Real Business Challenge — "Voice of the customer"
Join tickets to orders (via extracted `order_ref`) and check: do tickets
mentioning *late/damaged* concentrate in the same months as the revenue dip and
the returns spike? Produce a count-by-month of complaint themes. Self-check:
```python
assert theme_by_month.sum().sum() > 0
print(theme_by_month)
```
Investigation log: does the customer's voice corroborate the numbers?

## 🔎 Interview Lens — write answers
- Q9 revisited (extracting/validating numbers hidden in text).
"""

t8_practice = [
 ("md", "# Topic 08 — Practice: String Operations & Text Data\n\nLet customers tell you what went wrong."),
 ("code", BOOT + "tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str,'order_id':str})\n"
          "returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})"),
 ("md", "## Example — find tickets about lateness"),
 ("code", "msg = tickets['message'].str.lower()\nlate = msg.str.contains('late|where is', regex=True, na=False)\n"
          "print('late-themed tickets:', late.sum())\ntickets.loc[late, 'message'].head()"),
 ("md", "## Your Turn — extract order ids\nPull `O######` from each message into `order_ref`."),
 ("code", "tickets['order_ref'] = ...\nassert tickets['order_ref'].notna().sum() > 0\nprint('recovered order refs:', tickets['order_ref'].notna().sum())"),
 ("md", "## Mini Mission — theme flags\nCreate `is_late`, `is_damaged`, `is_refund` boolean columns and count them."),
 ("code", "m = tickets['message'].str.lower()\ntickets['is_late'] = ...\ntickets['is_damaged'] = ...\ntickets['is_refund'] = ...\n"
          "assert tickets[['is_late','is_damaged','is_refund']].dtypes.eq(bool).all()\n"
          "print(tickets[['is_late','is_damaged','is_refund']].sum())"),
 ("md", "## Boss Fight — complaint themes by month\nUse `order_ref` to bring in `order_date`, then count themes per month."),
 ("code", "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "tk = tickets.merge(orders[['order_id','order_date']], left_on='order_ref', right_on='order_id', how='left')\n"
          "tk['month'] = tk['order_date'].dt.to_period('M')\n"
          "theme_by_month = ...\nassert theme_by_month.sum().sum() > 0\nprint(theme_by_month.tail())"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q9 (revisited) in writing.\n"
        "2. Do complaint themes line up with the revenue/returns timing?\n3. Investigation log: voice-of-customer findings."),
]

t8_solutions = [
 ("md", "# Topic 08 — Solutions"),
 ("code", BOOT + "tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str,'order_id':str})"),
 ("code", "tickets['order_ref'] = tickets['message'].str.extract(r'(O\\d{6})')\n"
          "print(tickets['order_ref'].notna().sum())"),
 ("code", "m = tickets['message'].str.lower()\n"
          "tickets['is_late'] = m.str.contains('late|where is', regex=True, na=False)\n"
          "tickets['is_damaged'] = m.str.contains('damaged|broken|leak', regex=True, na=False)\n"
          "tickets['is_refund'] = m.str.contains('refund|return', regex=True, na=False)\n"
          "print(tickets[['is_late','is_damaged','is_refund']].sum())"),
 ("code", "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "tk = tickets.merge(orders[['order_id','order_date']], left_on='order_ref', right_on='order_id', how='left')\n"
          "tk['month'] = tk['order_date'].dt.to_period('M')\n"
          "theme_by_month = tk.groupby('month')[['is_late','is_damaged','is_refund']].sum()\n"
          "print(theme_by_month.tail())"),
 ("md", "### Interview Lens\n- **Q9 revisited:** Extract with a *validated* regex (`O\\d{6}`), then confirm the "
        "extracted ids actually exist in `orders` via a merge with `indicator=True`. Report extraction rate and "
        "unmatched refs rather than trusting the regex blindly."),
]

write("08_String_Operations_And_Text_Data", t8_lesson, t8_quiz, t8_challenge, t8_practice, t8_solutions)

# ===========================================================================
# TOPIC 09 — Apply / Map / Transform
# ===========================================================================
t9_lesson = r"""# Topic 09 — Apply / Map / Transform

> **Investigation milestone:** Time to engineer the analyst features the capstone
> needs: customer segments, margin bands, delivery-late flags, RFM-style fields.
> And to learn *when not to use `apply`* — because on Aurora's 64k lines, the
> wrong choice is 100× slower.

**Time split: 20% reading · 80% in `practice.ipynb`. NumPy recall checkpoint at the end.**

---

## The toolbox, fastest → slowest

1. **Vectorized ops / `np.where` / `np.select`** — always try first.
2. **`map`** (Series) — element-wise via a dict or function. Great for lookups.
3. **`apply`** (Series/DataFrame) — arbitrary Python per element/row. Flexible, slow.
4. **`transform`** (groupby) — group stat broadcast back to rows (Topic 5).

```python
# map: dictionary lookup (fast, clear)
seg = {"consumer": "B2C", "business": "B2B", "pro athlete": "B2C"}
customers["seg2"] = customers["segment"].str.lower().map(seg)

# np.where: vectorized if/else
items["margin_band"] = np.where(items["line_profit"] > 0, "profit", "loss")

# np.select: multi-branch
cond = [items["quantity"] >= 100, items["quantity"] >= 10]
items["size_band"] = np.select(cond, ["bulk", "medium"], default="small")
```

## When `apply` is a code smell

```python
# ❌ slow: row-wise Python
df["rev"] = df.apply(lambda r: r["q"] * r["p"], axis=1)
# ✅ fast: vectorized
df["rev"] = df["q"] * df["p"]
```
`apply(axis=1)` runs a Python function per row — it defeats vectorization. Reach
for it only when the logic genuinely can't be expressed with column math,
`np.where`, `np.select`, or `map`. **Never** use `iterrows` for math.

## `map` vs `apply` vs `applymap`
- `Series.map` — element-wise, takes a dict **or** function. Best for lookups.
- `Series.apply` — element-wise function (no dict).
- `DataFrame.apply` — per column (`axis=0`) or per row (`axis=1`).
- `DataFrame.map` (was `applymap`) — element-wise over every cell.

## NumPy connection 🔢

This whole topic *is* the NumPy lesson: vectorization vs Python loops,
`np.where`, `np.select`, broadcasting. The performance gap (often 50–200×) comes
from staying in compiled NumPy land instead of bouncing into the Python
interpreter once per row. Time it yourself in practice.

## Visual learning 📊

After feature engineering, a stacked bar of orders by `size_band` × `channel`,
or a histogram of `margin_band`, validates that your new features behave sanely.

---

## 🔎 Interview Lens (answer in writing)
- **Q26:** Why is vectorization faster than `iterrows`/loops? What's happening underneath?
- **Q27:** When is `apply` a code smell, and what replaces it?

### Recap
1. Order the toolbox fastest → slowest.
2. Rewrite a row-wise `apply` multiply as vectorized.
3. `map` vs `apply` on a Series — the key difference?

➡️ Open **`practice.ipynb`** (NumPy recall checkpoint 3).
"""

t9_quiz = r"""# Topic 09 — Quiz (Apply / Map / Transform)

15 questions. Answers in `../quizzes/09_answers.md`.

## Part A — Multiple Choice
1. Fastest way to add two columns:
   - (a) `apply(axis=1)`  (b) `df["a"] + df["b"]`  (c) `iterrows`  (d) `map`
2. `Series.map` can take:
   - (a) only functions  (b) a dict or a function  (c) only dicts  (d) a DataFrame
3. Multi-branch vectorized choice:
   - (a) `np.where` only  (b) `np.select`  (c) `apply`  (d) `groupby`
4. `apply(axis=1)` is slow because:
   - (a) it sorts  (b) it runs Python per row  (c) it copies the index  (d) it uses regex
5. `DataFrame.map` (formerly applymap) operates:
   - (a) per row  (b) per column  (c) on every cell  (d) on the index

## Part B — Predict the Output
6. `pd.Series([1,2,3]).map({1:"a",2:"b"}).tolist()` → ? (note the missing key)
7. `np.where(pd.Series([1,-1,2])>0,"p","n").tolist()` → ?
8. `np.select([pd.Series([5,50])>=10],["big"],default="small").tolist()` → ?

## Part C — Fill in the Blank
9. Dict lookup on a Series: `s.________({"a":1})`.
10. Vectorized if/else: `np.________(cond, x, y)`.
11. Multi-branch: `np.________([c1,c2],[v1,v2], default=...)`.
12. Group stat to rows: `g["v"].________("mean")`.

## Part D — Debug the Code
13. ```python
    df["rev"] = df.apply(lambda r: r.q * r.p, axis=1)   # slow on 64k rows
    ```
    Rewrite vectorized.
14. ```python
    df["band"] = df["q"].apply(lambda x: "big" if x>=100 else ("med" if x>=10 else "small"))
    ```
    Replace with a vectorized `np.select`.
15. ```python
    customers["seg2"] = customers["segment"].map(str.upper)  # NaN -> error/odd
    ```
    Why can NaN break `map(str.upper)`? Make it NaN-safe.
"""

t9_challenge = r"""# Topic 09 — Challenges (Apply / Map / Transform)

## 🟢 Easy
Map `segment` (lowercased) to `{consumer→B2C, business→B2B, pro athlete→B2C}`
into `seg2`. Self-check: `assert customers["seg2"].isin(["B2C","B2B"]).any()`.

## 🟡 Medium
On the costed master table, create `margin_band` with `np.where` (profit/loss)
and `size_band` with `np.select` (bulk≥100, medium≥10, else small). Self-check:
`assert set(master["size_band"].unique()) <= {"bulk","medium","small"}`.

## 🔴 Hard — prove vectorization wins
Compute line revenue two ways: vectorized vs `apply(axis=1)`. Time both with
`%timeit` (or `time`). Self-check: results match —
`assert np.allclose(v, a, equal_nan=True)` — and note the speed ratio.

## 🏢 Real Business Challenge — "Analyst feature set"
Engineer a feature table per order: `revenue`, `is_returned`, `days_to_ship`
(from shipments), `is_late` (shipped after promised). Use vectorized ops only.
Self-check:
```python
assert features["is_late"].dtype == bool
print(features.head())
```

## 🔎 Interview Lens — write answers
- Q26 (vectorization vs loops) and Q27 (apply code smell).
"""

t9_practice = [
 ("md", "# Topic 09 — Practice: Apply / Map / Transform\n\nEngineer features the fast way. NumPy recall at the end."),
 ("code", BOOT + "import time\n"
          "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "master = items.merge(products[['product_id','unit_cost']], on='product_id', how='left')\n"
          "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']"),
 ("md", "## Example — segment lookup with map"),
 ("code", "seg = {'consumer':'B2C','business':'B2B','pro athlete':'B2C'}\n"
          "customers['seg2'] = customers['segment'].str.lower().map(seg)\nprint(customers['seg2'].value_counts(dropna=False))"),
 ("md", "## Your Turn — vectorized bands\n`margin_band` via `np.where`; `size_band` via `np.select` (bulk≥100, medium≥10, else small)."),
 ("code", "master['margin_band'] = ...\nmaster['size_band'] = ...\n"
          "assert set(master['size_band'].dropna().unique()) <= {'bulk','medium','small'}\n"
          "print(master['size_band'].value_counts())"),
 ("md", "## Mini Mission — prove vectorization wins\nCompute line revenue vectorized vs apply(axis=1); compare time & equality."),
 ("code", "t0=time.time(); v = master['quantity']*master['unit_price']*(1-master['discount']); tv=time.time()-t0\n"
          "t0=time.time(); a = master.apply(lambda r: r['quantity']*r['unit_price']*(1-r['discount']), axis=1); ta=time.time()-t0\n"
          "assert np.allclose(v, a, equal_nan=True)\nprint(f'vectorized {tv:.4f}s  apply {ta:.4f}s  -> {ta/max(tv,1e-9):.0f}x slower')"),
 ("md", "## Boss Fight — late-delivery feature\n`is_late` = shipped after promised, vectorized, dtype bool."),
 ("code", "ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
          "ship['days_to_ship'] = (ship['shipped_date'] - ship['promised_date']).dt.days\n"
          "ship['is_late'] = ...\nassert ship['is_late'].dtype == bool\nprint('late shipments:', ship['is_late'].sum())"),
 ("md", "## 🔢 NumPy Recall Checkpoint (Topics 7–9)\nPure NumPy: vectorized banding with `np.select`."),
 ("code", "q = np.array([3, 12, 150, 8, 99])\n"
          "# TODO numpy-only: band 'bulk'(>=100),'medium'(>=10),'small' else\n"
          "bands = ...\nassert list(bands) == ['small','medium','bulk','small','medium']\nprint('NumPy banding passed')"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q26 and Q27.\n2. What was your apply-vs-vectorized speed ratio?\n"
        "3. Investigation log: which engineered features matter for the capstone?"),
]

t9_solutions = [
 ("md", "# Topic 09 — Solutions"),
 ("code", BOOT + "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "master = items.merge(products[['product_id','unit_cost']], on='product_id', how='left')\n"
          "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']"),
 ("code", "master['margin_band'] = np.where(master['line_profit'] > 0, 'profit', 'loss')\n"
          "cond = [master['quantity']>=100, master['quantity']>=10]\n"
          "master['size_band'] = np.select(cond, ['bulk','medium'], default='small')\n"
          "print(master['size_band'].value_counts())"),
 ("code", "ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
          "ship['is_late'] = ship['shipped_date'] > ship['promised_date']\nprint(ship['is_late'].sum())"),
 ("code", "q = np.array([3,12,150,8,99])\n"
          "bands = np.select([q>=100, q>=10], ['bulk','medium'], default='small')\nprint(list(bands))"),
 ("md", "### Interview Lens\n- **Q26:** Vectorized ops execute one compiled C loop over a contiguous array; "
        "`iterrows`/`apply(axis=1)` create a Python object per row and call back into the interpreter each "
        "iteration — orders of magnitude more overhead.\n- **Q27:** `apply` is a smell when the body is plain "
        "arithmetic/conditionals expressible with column math, `np.where`, `np.select`, or `map`. Keep it only "
        "for genuinely irregular per-group/row logic."),
]

write("09_Apply_Map_Transform", t9_lesson, t9_quiz, t9_challenge, t9_practice, t9_solutions)
print("Topics 07-09 done.")
