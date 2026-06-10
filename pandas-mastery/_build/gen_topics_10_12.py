"""Generate topics 10-12 (incl. capstone)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import build_notebook
ROOT = os.path.join(os.path.dirname(__file__), "..")
BOOT = ("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
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
# TOPIC 10 — Pivot Tables & MultiIndex
# ===========================================================================
t10_lesson = r"""# Topic 10 — Pivot Tables & MultiIndex

> **Investigation milestone:** Management wants a cross-tab: revenue by
> **channel × month**, by **category × segment**. Pivot tables are how analysts
> turn long data into the management-ready grids executives expect.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## Long vs wide — the mental model

- **Long (tidy):** one row per observation (your order lines). Best for *computing*.
- **Wide:** categories spread across columns (a cross-tab). Best for *reading*.

Reshaping moves between them. You compute in long, present in wide.

## `pivot_table` — aggregate + reshape in one call

```python
pivot = master.pivot_table(
    index="channel",       # rows
    columns="month",       # columns
    values="line_revenue", # what to aggregate
    aggfunc="sum",         # how
    margins=True,          # adds row/column totals ("All")
    fill_value=0,
)
```
`pivot_table` *aggregates* (handles duplicate index/column pairs). Plain
`pivot` does **not** aggregate and errors on duplicates — use `pivot_table` for
real data.

## `groupby` vs `pivot_table`

They answer the same questions; `pivot_table` is `groupby(['index','columns'])`
+ `unstack`. Choose `pivot_table` when you want the 2-D grid directly; choose
`groupby` for flexible multi-metric aggregation or further computation
(Interview Q15).

## MultiIndex — hierarchical labels

```python
g = master.groupby(["channel", "category"])["line_revenue"].sum()  # MultiIndex Series
g.loc["Online"]                 # all categories for Online
g.unstack()                     # category -> columns (back to wide)
g.xs("Jackets", level="category")
```
- `unstack(level)` moves an index level to columns; `stack()` does the reverse.
- `swaplevel`, `sort_index(level=)` keep MultiIndexes usable.
- Flatten with `reset_index()` before plotting/exporting.

## `melt` — wide back to long

```python
long = wide.melt(id_vars="channel", var_name="month", value_name="revenue")
```
Essential for getting messy spreadsheet exports into tidy form.

## `crosstab` — quick frequency pivots

```python
pd.crosstab(orders["channel"], orders["status"], normalize="index")
```

## NumPy connection 🔢

A pivot table is a 2-D reduction — conceptually grouping a flat array and
reshaping the reduced values into a matrix. `unstack`/`stack` are reshape ops
(like `np.reshape`) but label-aware. `fill_value=0` is the labelled cousin of
`np.nan_to_num`.

## Visual learning 📊

A pivot of revenue by `channel × month` drops straight into a **heatmap**
(`sns.heatmap(pivot)`) — instantly showing seasonality and which channel cooled
off. This is your headline capstone visual.

---

## 🔎 Interview Lens (answer in writing)
- **Q15:** When `groupby` over `pivot_table` and vice versa?
- Connect MultiIndex `stack`/`unstack` to reshaping you'd do for a report.

### Recap
1. `pivot` vs `pivot_table` — the crucial difference?
2. What does `unstack` do to a MultiIndex?
3. When do you `melt`?

➡️ Open **`practice.ipynb`**.
"""

t10_quiz = r"""# Topic 10 — Quiz (Pivot Tables & MultiIndex)

15 questions. Answers in `../quizzes/10_answers.md`.

## Part A — Multiple Choice
1. Plain `pivot` errors on duplicate index/column pairs; the fix is:
   - (a) `pivot_table` (aggregates)  (b) `merge`  (c) `concat`  (d) `melt`
2. `margins=True` adds:
   - (a) padding  (b) row/column totals  (c) a MultiIndex  (d) NaNs
3. `unstack()` moves:
   - (a) columns to rows  (b) an index level to columns  (c) rows to a list  (d) nothing
4. `melt` converts:
   - (a) long→wide  (b) wide→long  (c) numeric→text  (d) index→column
5. `pivot_table` is roughly:
   - (a) `merge + sort`  (b) `groupby(index,columns) + unstack`  (c) `concat`  (d) `apply`

## Part B — Predict the Output
6. `pd.crosstab([0,0,1],[1,1,1]).values.sum()` → ?
7. A pivot index=channel(4), columns=month(24): shape (excluding margins)?
8. `s.unstack()` on a 2-level MultiIndex Series returns a:

## Part C — Fill in the Blank
9. Revenue grid: `df.pivot_table(index="channel", columns="month", values="line_revenue", aggfunc="________")`.
10. Add totals: `pivot_table(..., ________=True)`.
11. Index level to columns: `g.________()`.
12. Wide→long: `wide.________(id_vars="channel")`.

## Part D — Debug the Code
13. ```python
    master.pivot(index="channel", columns="month", values="line_revenue")  # ValueError duplicates
    ```
    Switch to the function that aggregates.
14. ```python
    g = df.groupby(["a","b"]).sum()
    g["x"]   # works, but g.loc["a1","b1"] confuses you
    ```
    How do you select one outer level cleanly?
15. ```python
    pivot.plot()   # MultiIndex columns look messy
    ```
    What single call flattens it for plotting/export?
"""

t10_challenge = r"""# Topic 10 — Challenges (Pivot Tables & MultiIndex)

## 🟢 Easy
`crosstab` of `channel` × `status` (cleaned). Which channel has the highest share
of returns? (log it; normalize by index.)

## 🟡 Medium
Pivot revenue by `channel` (rows) × `month` (cols), `aggfunc="sum"`, with margins.
Self-check: `assert "All" in pivot.index`.

## 🔴 Hard — MultiIndex
GroupBy `["category","channel"]` revenue → MultiIndex Series. `unstack` channel to
columns and find, per category, the strongest channel. Self-check:
`assert isinstance(grp.index, pd.MultiIndex)`.

## 🏢 Real Business Challenge — "The management cross-tab"
Produce the board-ready grid: revenue by `category × month`, plus a heatmap.
Identify which category drove the seasonal swing. Self-check:
```python
assert pivot.shape[1] >= 12, "Need at least 12 months of columns"
print(pivot.round(0))
```

## 🔎 Interview Lens — write answers
- Q15 (groupby vs pivot_table).
"""

t10_practice = [
 ("md", "# Topic 10 — Practice: Pivot Tables & MultiIndex\n\nLong→wide for management-ready grids."),
 ("code", BOOT + "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['status'] = orders['status'].str.strip().str.lower()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "orders['month'] = orders['order_date'].dt.to_period('M').astype(str)\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "master = (items.merge(products[['product_id','category']], on='product_id', how='left')\n"
          "               .merge(orders[['order_id','channel','status','month']], on='order_id', how='left'))"),
 ("md", "## Example — crosstab channel × status (row-normalised)"),
 ("code", "ct = pd.crosstab(master['channel'], master['status'], normalize='index')\nct.round(3)"),
 ("md", "## Your Turn — revenue pivot channel × month\nWith margins (totals)."),
 ("code", "pivot = ...\nassert 'All' in pivot.index\npivot.round(0).head()"),
 ("md", "## Mini Mission — MultiIndex\nGroupBy `['category','channel']` revenue; unstack channel to columns."),
 ("code", "grp = ...\nassert isinstance(grp.index, pd.MultiIndex)\nwide = grp.unstack()\nwide.round(0).head()"),
 ("md", "## Boss Fight — management heatmap\nPivot revenue by category × month and draw a heatmap."),
 ("code", "cat_month = master.pivot_table(index='category', columns='month', values='line_revenue', aggfunc='sum', fill_value=0)\n"
          "assert cat_month.shape[1] >= 12\n"
          "plt.figure(figsize=(12,4)); plt.imshow(cat_month, aspect='auto')\n"
          "plt.yticks(range(len(cat_month)), cat_month.index); plt.title('Revenue: category x month'); plt.colorbar(); plt.show()"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q15.\n2. Which category drove the seasonal swing?\n"
        "3. Investigation log: what does the cross-tab reveal that the totals hid?"),
]

t10_solutions = [
 ("md", "# Topic 10 — Solutions"),
 ("code", BOOT + "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "orders['month'] = orders['order_date'].dt.to_period('M').astype(str)\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "master = (items.merge(products[['product_id','category']], on='product_id', how='left')\n"
          "               .merge(orders[['order_id','channel','month']], on='order_id', how='left'))"),
 ("code", "pivot = master.pivot_table(index='channel', columns='month', values='line_revenue', aggfunc='sum', margins=True, fill_value=0)\n"
          "print(pivot.iloc[:, :4])"),
 ("code", "grp = master.groupby(['category','channel'])['line_revenue'].sum()\nprint(grp.unstack().round(0).head())"),
 ("md", "### Interview Lens\n- **Q15:** `pivot_table` when you want the 2-D grid (index×columns) ready to read or "
        "heatmap. `groupby` when you need several metrics at once, custom aggregations, or to keep computing on "
        "the result. `pivot_table` is `groupby + unstack` under the hood."),
]

write("10_Pivot_Tables_And_MultiIndex", t10_lesson, t10_quiz, t10_challenge, t10_practice, t10_solutions)

# ===========================================================================
# TOPIC 11 — Exploratory Analysis & Visualization
# ===========================================================================
t11_lesson = r"""# Topic 11 — Exploratory Analysis & Visualization

> **Investigation milestone:** You have the findings; now you must *show* them.
> Every chart answers a business question. You'll build the visuals that go into
> the capstone report — and learn to make charts that argue, not decorate.

**Time split: 20% reading · 80% in `practice.ipynb`.**

---

## EDA as a question loop

EDA is not "make many charts". It's: *ask a question → reduce data → draw the one
chart that answers it → write the takeaway*. If a chart doesn't answer a
question, delete it.

## Pandas → Matplotlib → Seaborn

- `df.plot(...)` — quickest path; wraps Matplotlib. Good for exploration.
- **Matplotlib** — full control (titles, labels, annotations) for the final figure.
- **Seaborn** — statistical charts in one line (`histplot`, `barplot`, `heatmap`,
  `boxplot`) with sensible defaults.

## The analyst's core chart vocabulary

| Question | Chart | Code |
|---|---|---|
| Trend over time? | line | `monthly.plot()` |
| Compare categories? | bar | `rev_by_channel.plot(kind="bar")` |
| Distribution / outliers? | hist / box | `s.plot(kind="hist")`, `sns.boxplot` |
| Relationship? | scatter | `df.plot.scatter("spend","revenue")` |
| Two-way pattern? | heatmap | `sns.heatmap(pivot)` |
| Part-to-whole? | stacked bar | `pivot.plot(kind="bar", stacked=True)` |

## Make the chart argue
- **Title = the takeaway**, not the variable ("Online revenue cooled in Q1", not "revenue").
- Label axes and units (£, %, dates).
- Sort bars by value. Annotate the one number that matters.
- Prefer a few honest charts over a dashboard of noise.

## A quick "business dashboard"

`plt.subplots(2,2)` to place: monthly revenue trend, revenue by channel, returns
by month, and the channel×month heatmap — one figure the manager actually reads.

## NumPy connection 🔢

Histograms are `np.histogram` under the hood; a heatmap renders a 2-D NumPy
array of your pivot. `corr()` computes Pearson correlation (a normalized dot
product). The chart is a *view* of the array math you already did.

## Visual learning 📊

This whole topic *is* the visual-learning topic. Reproduce, then improve: take
one default `df.plot()` and turn it into a titled, labelled, sorted, annotated
figure worthy of a board pack.

---

## 🔎 Interview Lens (answer in writing)
- **Q30:** A stakeholder doubts your number — how do you trace it to raw data and defend/correct it?
- **Q31:** How do you make the analysis reproducible next quarter?

### Recap
1. What makes a chart "answer a question"?
2. When Seaborn over bare Matplotlib?
3. What belongs in a good title?

➡️ Open **`practice.ipynb`**.
"""

t11_quiz = r"""# Topic 11 — Quiz (Exploratory Analysis & Visualization)

15 questions. Answers in `../quizzes/11_answers.md`.

## Part A — Multiple Choice
1. Best chart for a trend over time:
   - (a) bar  (b) line  (c) pie  (d) scatter
2. Best chart to spot outliers in one numeric column:
   - (a) line  (b) box/hist  (c) heatmap  (d) bar
3. A good chart title states:
   - (a) the column name  (b) the takeaway  (c) the dtype  (d) the row count
4. `sns.heatmap` expects:
   - (a) a long DataFrame  (b) a 2-D array/pivot  (c) a Series  (d) a dict
5. Stacked bar shows:
   - (a) trend  (b) part-to-whole across categories  (c) correlation  (d) distribution

## Part B — Predict the Output
6. `pd.Series([1,1,2,3]).plot(kind="hist")` draws bars counting what?
7. `df.corr()` on 3 numeric cols returns a matrix of shape?
8. `pivot.plot(kind="bar", stacked=True)` — bars represent index or columns?

## Part C — Fill in the Blank
9. Trend line: `monthly.________()`.
10. Category bars: `rev.plot(kind="________")`.
11. Heatmap of a pivot: `sns.________(pivot)`.
12. Scatter: `df.plot.________("spend","revenue")`.

## Part D — Debug the Code
13. ```python
    rev_by_channel.plot()   # meaningless line across categories
    ```
    Pick the right `kind`.
14. ```python
    plt.plot(monthly); # no title/labels — unreadable
    ```
    Add the three things every chart needs.
15. ```python
    df.plot.scatter("spend")   # error: needs y
    ```
    Fix the scatter call.
"""

t11_challenge = r"""# Topic 11 — Challenges (EDA & Visualization)

Each chart MUST have a takeaway title and labelled axes.

## 🟢 Easy
Line chart of monthly revenue with a 3-month moving average overlay.

## 🟡 Medium
Bar chart of revenue by channel (sorted) and a histogram of order values.
Write one-sentence takeaways for each (no key).

## 🔴 Hard
Heatmap of revenue by `category × month`. Annotate the seasonal peak. What story
does it tell about the "dip"?

## 🏢 Real Business Challenge — "One-page dashboard"
Build a 2×2 figure: (1) monthly revenue trend, (2) revenue by channel,
(3) returns by month, (4) spend-vs-revenue scatter. This figure goes into the
capstone. Self-check:
```python
assert len(fig.axes) == 4, "Dashboard must have 4 panels"
fig.savefig("aurora_dashboard.png", dpi=120, bbox_inches="tight")
```

## 🔎 Interview Lens — write answers
- Q30 (defend a number) and Q31 (reproducibility).
"""

t11_practice = [
 ("md", "# Topic 11 — Practice: EDA & Visualization\n\nEvery chart answers a business question. Build the capstone visuals."),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "oi = items.merge(orders[['order_id','channel','order_date']], on='order_id', how='left')\n"
          "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\n"
          "monthly = ts['line_revenue'].resample('ME').sum()"),
 ("md", "## Example — trend with takeaway title"),
 ("code", "ax = monthly.plot(figsize=(10,4))\nmonthly.rolling(3).mean().plot(ax=ax)\n"
          "ax.set_title('Aurora revenue is seasonal, not declining (3mo MA overlay)')\n"
          "ax.set_ylabel('Revenue (£)'); ax.set_xlabel('Month'); plt.show()"),
 ("md", "## Your Turn — revenue by channel (sorted bar, labelled)\nGive it a takeaway title."),
 ("code", "channel_rev = oi.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
          "# TODO plot a labelled, titled bar chart\nassert channel_rev.is_monotonic_decreasing\nchannel_rev"),
 ("md", "## Mini Mission — distribution\nHistogram of per-order revenue; note the skew/outliers (no key)."),
 ("code", "order_rev = oi.groupby('order_id')['line_revenue'].sum()\n# TODO hist with title + xlabel\norder_rev.describe()"),
 ("md", "## Boss Fight — one-page 2x2 dashboard\nMonthly trend, channel bar, returns by month, spend-vs-revenue scatter."),
 ("code", "returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n"
          "rmonth = returns.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
          "rmonth = rmonth.dropna(subset=['order_date']).set_index('order_date')['refund_amount'].resample('ME').sum()\n"
          "mk = pd.read_csv(RAW+'marketing_spend.csv', parse_dates=['date'])\n"
          "daily_spend = mk.groupby('date')['spend_gbp'].sum().resample('ME').sum()\n"
          "fig, axes = plt.subplots(2,2, figsize=(13,8))\n"
          "monthly.plot(ax=axes[0,0], title='Monthly revenue')\n"
          "channel_rev.plot(kind='bar', ax=axes[0,1], title='Revenue by channel')\n"
          "rmonth.plot(ax=axes[1,0], title='Refunds by month')\n"
          "axes[1,1].scatter(daily_spend.reindex(monthly.index), monthly); axes[1,1].set_title('Spend vs revenue (monthly)')\n"
          "fig.tight_layout()\nassert len(fig.axes) == 4\nfig.savefig('aurora_dashboard.png', dpi=120, bbox_inches='tight'); print('saved aurora_dashboard.png')"),
 ("md", "## Reflection / Interview Lens\n1. Answer Q30 and Q31.\n2. Which single chart best explains the case to a manager?\n"
        "3. Investigation log: finalize the story for the capstone."),
]

t11_solutions = [
 ("md", "# Topic 11 — Solutions"),
 ("code", BOOT + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "oi = items.merge(orders[['order_id','channel']], on='order_id', how='left')"),
 ("code", "channel_rev = oi.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
          "ax = channel_rev.plot(kind='bar', title='Online dominates revenue; Phone is marginal')\n"
          "ax.set_ylabel('Revenue (£)'); plt.tight_layout(); plt.show()"),
 ("md", "### Interview Lens\n- **Q30:** Reproduce the number from raw with a documented chain of filters/joins; "
        "check grain (row counts), show coverage of missing/excluded rows, and reconcile against an independent "
        "cut (e.g. order-level vs line-level). If it still differs, the stakeholder's mental model or the source "
        "is wrong — show them the lineage.\n- **Q31:** One parameterised notebook/script, pinned versions, a "
        "deterministic data load, asserts on invariants, and no manual spreadsheet steps."),
]

write("11_Exploratory_Analysis_And_Visualization", t11_lesson, t11_quiz, t11_challenge, t11_practice, t11_solutions)

# ===========================================================================
# TOPIC 12 — Capstone Investigation
# ===========================================================================
t12_lesson = r"""# Topic 12 — Capstone Investigation

> **The case closes.** You now own every skill the investigation needs. This
> topic is not a new technique — it's the **real Data Analyst job**: take Aurora
> Outfitters' messy ecosystem and deliver a defensible report answering *what
> happened to revenue, and what should we do about it.*

**Time split: 10% reading · 90% doing. This is the portfolio piece.**

---

## The brief (from the Head of Finance)

> "Our headline revenue looked like it dropped, returns feel high, and marketing
> spend keeps rising. I need one analyst to tell me, with evidence: **is revenue
> actually falling? where is margin leaking? and what are the top 3 actions?**"

## What you must deliver

A single notebook + a short written report containing:

1. **Data quality appendix** — what was dirty, what you fixed, what you excluded
   and why (casing, dupes, mixed dates, orphan orders, impossible prices/quantities).
2. **KPI dashboard** — revenue trend, AOV, returns rate, gross margin, CAC proxy
   (spend ÷ new customers), by month and channel.
3. **Findings** — answer the three brief questions with charts that argue.
4. **Recommendations** — top 3 actions, each tied to a number.
5. **Reproducibility** — runs top-to-bottom from raw with no manual steps.

## The KPIs (define them precisely)

| KPI | Definition |
|---|---|
| Gross revenue | Σ `quantity × unit_price × (1 − discount)` over valid lines |
| Net revenue | Gross − refunds |
| AOV | revenue ÷ number of orders |
| Returns rate | returned orders ÷ all orders |
| Gross margin | (revenue − COGS) ÷ revenue, COGS = Σ `quantity × unit_cost` |
| Late-delivery rate | shipments shipped after promised ÷ shipments |

## How the course feeds the capstone

Topic 01–02 load & build revenue · 03 isolate suspects · 04 clean (the
double-counted channel!) · 05 aggregate KPIs · 06 join safely for margin · 07
the time story · 08 voice-of-customer · 09 features · 10 management cross-tabs ·
11 the dashboard. **You already did the pieces — now assemble them.**

## The twist to resolve

Early in the course the "dip" looked alarming. By now you should be able to show
whether it was **real** or an **artifact** of dirty dates / split channel
categories / returns timing. Your report must take a clear, evidenced position.

## NumPy connection 🔢 (final recall)
The capstone leans on everything: vectorized KPI math, `np.where`/`np.select`
features, boolean masks for filters, `np.nan` handling. The Topic-12 revision
checkpoint closes the loop.

## Visual learning 📊
The one-page dashboard from Topic 11 is your centerpiece. Add the channel×month
heatmap and a returns-rate trend.

---

## 🔎 Interview Lens (final)
Re-answer **Q30 (defend the number)** and **Q32 (what data quality means here)**
as if presenting to the Head of Finance. This is the interview.

➡️ Open **`practice.ipynb`** for the scaffolded capstone, and use
`projects/` + the report template in `challenge.md`.
"""

t12_quiz = r"""# Topic 12 — Capstone Self-Assessment (not a trivia quiz)

This "quiz" checks whether your capstone is *complete and defensible*. Tick each.
Answers/standards in `../quizzes/12_answers.md`.

## Completeness checklist
1. Does your notebook run top-to-bottom from raw with no manual edits?
2. Did you document every cleaning decision (casing, dupes, dates, orphans, impossible values)?
3. Are all six KPIs computed with stated definitions?
4. Did you join for margin **without** changing the grain (row-count asserts)?
5. Does every chart have a takeaway title and labelled axes?

## Reasoning checklist
6. Did you take a clear position on whether revenue truly fell?
7. Can you trace your headline revenue number back to raw rows?
8. Did you quantify the impact of the double-counted channel?
9. Are the top-3 recommendations each backed by a specific number?
10. Did you state what you would do with more time/data?

## Rigor checklist
11. Did you report coverage of excluded/missing rows (not silently drop)?
12. Did you validate joins (`validate=`, `indicator=`)?
13. Did you handle returns when computing **net** revenue?
14. Did you sanity-check outliers (1,500-unit lines, negative prices)?
15. Is the analysis reproducible (seeded, versioned, asserts)?
"""

t12_challenge = r"""# Topic 12 — Capstone Brief & Final Report Template

## 🏢 The capstone (this is the whole job)

Deliver `capstone_report.ipynb` (start from `practice.ipynb`) that answers, with
evidence and charts:

1. **Is revenue actually falling, or was the "dip" an artifact?**
2. **Where is margin leaking** (channel, category, returns, late delivery)?
3. **Top 3 actions**, each tied to a number.

### Required sections (use as headings)

```
# Aurora Outfitters — Revenue & Margin Investigation
## 1. Executive summary            (≤ 150 words, the answer first)
## 2. Data & quality appendix      (what was dirty, fixed, excluded — with counts)
## 3. KPIs                         (revenue, net revenue, AOV, returns rate, margin, late rate)
## 4. Findings                     (charts that argue; the dip resolved)
## 5. Recommendations              (top 3, each with a number and expected impact)
## 6. Appendix / reproducibility   (assumptions, definitions, how to re-run)
```

### Acceptance self-checks (objective parts only)
```python
assert net_revenue == gross_revenue - total_refunds
assert 0 <= returns_rate <= 1
assert 0 <= gross_margin <= 1
assert len(fig.axes) >= 4            # dashboard present
assert master_rowcount == items_rowcount   # joins preserved grain
print("Capstone objective checks passed.")
```

There is **no answer key** for the narrative — that is the point. Defend your
numbers the way you would to the Head of Finance.

## 🔎 Interview Lens — final written answers
Re-answer Q30 and Q32 as a presentation.

## Difficulty curve reached
Beginner → Intermediate → Advanced → **Real business problem → Analyst-level
thinking.** If you can defend this report, you can pass the interview.
"""

t12_practice = [
 ("md", "# Topic 12 — Capstone: The Aurora Outfitters Investigation\n\n"
        "This is the job. Assemble everything into a defensible report. Objective KPIs are "
        "self-checked with asserts; the narrative has **no key** — you defend it."),
 ("code", BOOT),
 ("md", "## Step 0 — Reproducible load + clean\nLoad all tables, fix dtypes, clean casing/dupes/dates, "
        "drop impossible values. Document each decision in the markdown below."),
 ("code", "def load_clean():\n"
          "    products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "    products['list_price'] = np.where(products['list_price']<0, np.nan, products['list_price'])\n"
          "    customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n"
          "    customers['first_name'] = customers['first_name'].astype(str).str.strip()\n"
          "    orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "    orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "    orders['status'] = orders['status'].str.strip().str.lower()\n"
          "    orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "    items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "    items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "    returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n"
          "    return products, customers, orders, items, returns\n\n"
          "products, customers, orders, items, returns = load_clean()\n"
          "print('loaded & cleaned')"),
 ("md", "_Data-quality decisions (fill in):_\n- Casing merged on channel/status because …\n- Dropped N duplicate "
        "customers because …\n- Excluded/flagged impossible quantities and negative prices because …"),
 ("md", "## Step 1 — Build the safe master table (grain preserved)"),
 ("code", "master = (items\n"
          "  .merge(products[['product_id','category','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
          "  .merge(orders[['order_id','channel','status','order_date','customer_id']], on='order_id', how='left', validate='many_to_one'))\n"
          "master['line_cogs'] = master['quantity']*master['unit_cost']\n"
          "master['line_profit'] = master['line_revenue'] - master['line_cogs']\n"
          "master_rowcount = len(master); items_rowcount = len(items)\n"
          "assert master_rowcount == items_rowcount, 'a join changed the grain!'\nprint('master rows:', master_rowcount)"),
 ("md", "## Step 2 — KPIs (objective, self-checked)"),
 ("code", "gross_revenue = master['line_revenue'].sum()\n"
          "total_refunds = returns['refund_amount'].sum()\n"
          "net_revenue = gross_revenue - total_refunds\n"
          "n_orders = orders['order_id'].nunique()\n"
          "aov = gross_revenue / n_orders\n"
          "returns_rate = (orders['status']=='returned').mean()\n"
          "cogs = master['line_cogs'].sum()\n"
          "gross_margin = (gross_revenue - cogs) / gross_revenue\n"
          "assert net_revenue == gross_revenue - total_refunds\n"
          "assert 0 <= returns_rate <= 1\nassert 0 <= gross_margin <= 1\n"
          "print(f'gross £{gross_revenue:,.0f} | net £{net_revenue:,.0f} | AOV £{aov:,.2f} | returns {returns_rate:.1%} | margin {gross_margin:.1%}')"),
 ("md", "## Step 3 — The time story (resolve the dip)\nMonthly net revenue with moving average. Was the dip real?"),
 ("code", "ts = master.dropna(subset=['order_date']).set_index('order_date').sort_index()\n"
          "monthly = ts['line_revenue'].resample('ME').sum()\n"
          "ax = monthly.plot(figsize=(11,4)); monthly.rolling(3).mean().plot(ax=ax)\n"
          "ax.set_title('Verdict: is the dip real? (write your answer)'); ax.set_ylabel('Revenue £'); plt.show()"),
 ("md", "_Your verdict (no key):_ The dip was real / an artifact because …"),
 ("md", "## Step 4 — One-page dashboard (your Topic-11 figure, finalized)"),
 ("code", "channel_rev = master.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
          "fig, axes = plt.subplots(2,2, figsize=(13,8))\n"
          "monthly.plot(ax=axes[0,0], title='Monthly revenue')\n"
          "channel_rev.plot(kind='bar', ax=axes[0,1], title='Revenue by channel')\n"
          "master.groupby('category')['line_profit'].sum().sort_values().plot(kind='barh', ax=axes[1,0], title='Profit by category')\n"
          "master.groupby('channel')['line_profit'].sum().plot(kind='bar', ax=axes[1,1], title='Profit by channel')\n"
          "fig.tight_layout(); assert len(fig.axes) >= 4\nfig.savefig('capstone_dashboard.png', dpi=120, bbox_inches='tight'); print('saved')"),
 ("md", "## Step 5 — Findings & recommendations (write — no key)\n"
        "1. Is revenue falling? (evidence)\n2. Where is margin leaking? (channel/category/returns/late)\n"
        "3. **Top 3 actions, each tied to a number.**"),
 ("code", "# Final objective gate\nassert net_revenue == gross_revenue - total_refunds\n"
          "assert master_rowcount == items_rowcount\nprint('Capstone objective checks passed. Now write the narrative.')"),
 ("md", "## 🔢 Final NumPy Recall (Topics 10–12)\nPure NumPy: compute a weighted margin and a banded KPI."),
 ("code", "rev = np.array([100., 200., 50., 0.]); cogs = np.array([60., 150., 20., 0.])\n"
          "# TODO numpy-only: overall margin ignoring zero-revenue rows\n"
          "mask = rev > 0\nmargin = ...\n"
          "assert round(float(margin),3) == round(float((rev[mask]-cogs[mask]).sum()/rev[mask].sum()),3)\nprint('final NumPy recall passed')"),
 ("md", "## Reflection / Interview Lens (final)\n"
        "Re-answer Q30 and Q32 as a presentation to the Head of Finance. Then update "
        "`../progress_tracker.md` and write your capstone executive summary."),
]

t12_solutions = [
 ("md", "# Topic 12 — Capstone Reference Solution (objective parts only)\n\n"
        "*The narrative is yours to defend — only the mechanical KPI/reproducibility parts are shown.*"),
 ("code", BOOT),
 ("code", "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "products['list_price'] = np.where(products['list_price']<0, np.nan, products['list_price'])\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['status'] = orders['status'].str.strip().str.lower()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n"
          "master = (items.merge(products[['product_id','category','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
          "              .merge(orders[['order_id','channel','status','order_date']], on='order_id', how='left', validate='many_to_one'))\n"
          "master['line_cogs'] = master['quantity']*master['unit_cost']\n"
          "assert len(master)==len(items)"),
 ("code", "gross = master['line_revenue'].sum(); refunds = returns['refund_amount'].sum()\n"
          "net = gross - refunds; n_orders = orders['order_id'].nunique(); aov = gross/n_orders\n"
          "returns_rate = (orders['status']=='returned').mean()\n"
          "margin = (gross - master['line_cogs'].sum())/gross\n"
          "print(f'gross £{gross:,.0f} net £{net:,.0f} AOV £{aov:.2f} returns {returns_rate:.1%} margin {margin:.1%}')"),
 ("code", "rev = np.array([100.,200.,50.,0.]); cogs = np.array([60.,150.,20.,0.])\n"
          "mask = rev>0; margin = (rev[mask]-cogs[mask]).sum()/rev[mask].sum(); print(round(float(margin),3))"),
 ("md", "### Interview Lens (model talking points)\n- **Q30:** Show the lineage: raw rows → cleaning → joins → "
        "aggregation, with row-count asserts and coverage of excluded data; reconcile order-level vs line-level.\n"
        "- **Q32:** Data quality = accuracy, completeness, consistency, validity, uniqueness, timeliness — made "
        "concrete on Aurora: consistent channel casing, unique customers, valid prices/quantities, parsed dates, "
        "matched keys, and documented exclusions."),
]

write("12_Capstone_Investigation", t12_lesson, t12_quiz, t12_challenge, t12_practice, t12_solutions)
print("Topics 10-12 done.")
