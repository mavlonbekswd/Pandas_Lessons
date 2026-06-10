import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from v2common import convert_lesson, build_practice_solutions, cleanup_topic

IMP = "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\npd.set_option('display.max_columns', 30)\nRAW = '../datasets/raw/'\n"
MASTER = (IMP +
 "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
 "products['list_price'] = np.where(products['list_price']<0, np.nan, products['list_price'])\n"
 "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
 "orders['channel'] = orders['channel'].str.strip().str.title()\n"
 "orders['status'] = orders['status'].str.strip().str.lower()\n"
 "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
 "orders['month'] = orders['order_date'].dt.to_period('M').astype(str)\n"
 "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
 "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
 "master = (items.merge(products[['product_id','category','unit_cost']], on='product_id', how='left')\n"
 "              .merge(orders[['order_id','channel','status','month','order_date']], on='order_id', how='left'))\n"
 "master['line_cogs'] = master['quantity']*master['unit_cost']\n"
 "master['line_profit'] = master['line_revenue'] - master['line_cogs']\n")

# ===========================================================================
T9 = dict(
 num="09", dir="09_Apply_Map_Transform", title="Apply / Map / Transform",
 boot=MASTER + "import time\ncustomers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n",
 warmup_md=("From **Topics 01–08**:\n\n1. (T06) What do `validate=` and `indicator=` protect you from?\n"
   "2. (T08) Why pass `na=False` to `str.contains`?\n3. NumPy: what does `np.select` do that `np.where` can't?"),
 warmup_code=("# NumPy recall: multi-branch banding with np.select\n"
   "q = np.array([3, 12, 150, 8, 99])\nbands = ...   # bulk>=100, medium>=10, else small\n"
   "assert list(bands) == ['small','medium','bulk','small','medium']\nprint('ok')"),
 warmup_sol=("q = np.array([3,12,150,8,99])\nbands = np.select([q>=100, q>=10], ['bulk','medium'], default='small')\nprint(list(bands))"),
 core_intro="Toolbox fastest→slowest: vectorized/np.where/np.select → map → apply. Avoid apply(axis=1) for math.",
 core=[
  dict(md="**Core 1 — map lookup.** Map lowercased `segment` to `{consumer→B2C, business→B2B, pro athlete→B2C}` into `seg2`.",
       task="seg = {'consumer':'B2C','business':'B2B','pro athlete':'B2C'}\ncustomers['seg2'] = ...\n"
            "assert customers['seg2'].isin(['B2C','B2B']).any()\nprint(customers['seg2'].value_counts(dropna=False))",
       sol="seg = {'consumer':'B2C','business':'B2B','pro athlete':'B2C'}\ncustomers['seg2'] = customers['segment'].str.lower().map(seg)\nprint(customers['seg2'].value_counts(dropna=False))"),
  dict(md="**Core 2 — vectorized bands.** `margin_band` via `np.where` (profit/loss); `size_band` via `np.select` (bulk≥100, medium≥10, else small).",
       task="master['margin_band'] = ...\nmaster['size_band'] = ...\n"
            "assert set(master['size_band'].dropna().unique()) <= {'bulk','medium','small'}\nprint(master['size_band'].value_counts())",
       sol="master['margin_band'] = np.where(master['line_profit'] > 0, 'profit', 'loss')\n"
           "master['size_band'] = np.select([master['quantity']>=100, master['quantity']>=10], ['bulk','medium'], default='small')\nprint(master['size_band'].value_counts())"),
  dict(md="**Core 3 — prove vectorization wins.** Compute line revenue vectorized vs `apply(axis=1)`; compare time & equality.",
       task="t0=time.time(); v = master['quantity']*master['unit_price']*(1-master['discount']); tv=time.time()-t0\n"
            "t0=time.time(); a = master.apply(lambda r: r['quantity']*r['unit_price']*(1-r['discount']), axis=1); ta=time.time()-t0\n"
            "assert np.allclose(v, a, equal_nan=True)\nprint(f'vectorized {tv:.4f}s  apply {ta:.4f}s  -> {ta/max(tv,1e-9):.0f}x')",
       sol="v = master['quantity']*master['unit_price']*(1-master['discount'])\n"
           "a = master.apply(lambda r: r['quantity']*r['unit_price']*(1-r['discount']), axis=1)\nprint(np.allclose(v, a, equal_nan=True))"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 07) — late flag.** From `shipments`, flag `is_late` (shipped after promised), vectorized, dtype bool.",
       task="ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
            "ship['is_late'] = ...\nassert ship['is_late'].dtype == bool\nprint('late shipments:', ship['is_late'].sum())",
       sol="ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
           "ship['is_late'] = ship['shipped_date'] > ship['promised_date']\nprint(ship['is_late'].sum())"),
  dict(md="**Mixed review (Topic 05/06) — group the features.** Mean `line_profit` by `size_band`.",
       task="profit_by_band = ...\nassert len(profit_by_band) <= 3\nprofit_by_band",
       sol="print(master.groupby('size_band')['line_profit'].mean())"),
 ],
 detective_md=("**Case file #9 — the analyst feature set.** Engineer per-order features the capstone needs: "
   "`revenue`, `is_returned`, `days_to_ship`, `is_late`. Use vectorized ops only."),
 detective_task=("ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
   "ship['days_to_ship'] = (ship['shipped_date'] - ship['promised_date']).dt.days\nship['is_late'] = ship['shipped_date'] > ship['promised_date']\n"
   "order_rev = master.groupby('order_id')['line_revenue'].sum().rename('revenue')\n"
   "features = order_rev.to_frame().join(ship.set_index('order_id')[['days_to_ship','is_late']])\n"
   "features['is_returned'] = orders.set_index('order_id')['status'].eq('returned')\n"
   "assert features['is_late'].dropna().dtype == bool\nprint(features.head())"),
 detective_sol=("ship = pd.read_csv(RAW+'shipments.csv', dtype={'order_id':str}, parse_dates=['promised_date','shipped_date'])\n"
   "ship['is_late'] = ship['shipped_date'] > ship['promised_date']\nprint(ship['is_late'].mean())"),
 interview_md=("- **Q26:** Why is vectorization faster than `iterrows`/loops? What's happening underneath?\n"
   "- **Q27:** When is `apply` a code smell, and what replaces it?\n"
   "- **Q28:** How do `category` dtypes save memory and speed up groupby? When can they hurt?"),
 reflection_md=("1. Answer Q26 and Q27 in writing.\n2. What was your apply-vs-vectorized speed ratio?\n"
   "3. **Investigation log:** which engineered features matter most for the capstone?"),
 interview_notes=("- **Q26:** vectorized ops run one compiled C loop over contiguous arrays; iterrows/apply(axis=1) build a Python object per row.\n"
   "- **Q27:** apply is a smell when the body is plain arithmetic/conditionals expressible with column math, np.where, np.select, or map."),
)

# ===========================================================================
T10 = dict(
 num="10", dir="10_Pivot_Tables_And_MultiIndex", title="Pivot Tables & MultiIndex",
 boot=MASTER,
 warmup_md=("From **Topics 01–09**:\n\n1. (T09) Order the toolbox fastest→slowest (vectorized…apply).\n"
   "2. (T05) What does `transform` return vs `agg`?\n3. NumPy: `np.reshape` changes shape — what's the pandas label-aware cousin?"),
 warmup_code=("# NumPy recall: reshape a flat array into a 2-D grid\n"
   "flat = np.arange(12)\ngrid = ...   # TODO 3x4\nassert grid.shape == (3,4) and grid[1,2] == 6\nprint(grid)"),
 warmup_sol=("flat = np.arange(12)\ngrid = flat.reshape(3,4)\nprint(grid)"),
 core_intro="`pivot_table` aggregates + reshapes (use it, not `pivot`, on real data). `unstack`/`stack` move levels.",
 core=[
  dict(md="**Core 1 — crosstab.** Row-normalised `crosstab` of `channel` × `status`. Which channel returns most?",
       task="ct = ...\nassert np.allclose(ct.sum(axis=1), 1)\nct.round(3)",
       sol="ct = pd.crosstab(master['channel'], master['status'], normalize='index')\nprint(ct.round(3))"),
  dict(md="**Core 2 — revenue pivot.** Revenue by `channel` (rows) × `month` (cols), `aggfunc='sum'`, with margins.",
       task="pivot = ...\nassert 'All' in pivot.index\npivot.iloc[:, :4]",
       sol="pivot = master.pivot_table(index='channel', columns='month', values='line_revenue', aggfunc='sum', margins=True, fill_value=0)\nprint(pivot.iloc[:, :4])"),
  dict(md="**Core 3 — MultiIndex.** GroupBy `['category','channel']` revenue → MultiIndex Series; `unstack` channel to columns.",
       task="grp = ...\nassert isinstance(grp.index, pd.MultiIndex)\ngrp.unstack().round(0).head()",
       sol="grp = master.groupby(['category','channel'])['line_revenue'].sum()\nprint(grp.unstack().round(0).head())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 07) — month ordering.** Confirm `month` columns sort chronologically (string YYYY-MM works).",
       task="months = sorted(master['month'].dropna().unique())\nassert months == list(pd.Series(months).sort_values())\nprint(months[:3], '...', months[-1])",
       sol="months = sorted(master['month'].dropna().unique())\nprint(months[0], months[-1])"),
  dict(md="**Mixed review (Topic 06) — grain check.** Prove the master table didn't fan out: `len(master) == len(items)`.",
       task="items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\nassert len(master) == len(items)\nprint('grain preserved:', len(master))",
       sol="items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\nprint(len(master) == len(items))"),
 ],
 detective_md=("**Case file #10 — the management cross-tab.** Produce the board-ready grid: revenue by "
   "`category × month`, then a heatmap. Which category drove the seasonal swing the totals hid?"),
 detective_task=("cat_month = master.pivot_table(index='category', columns='month', values='line_revenue', aggfunc='sum', fill_value=0)\n"
   "assert cat_month.shape[1] >= 12\n"
   "plt.figure(figsize=(12,4)); plt.imshow(cat_month, aspect='auto')\n"
   "plt.yticks(range(len(cat_month)), cat_month.index); plt.title('Revenue: category x month'); plt.colorbar(); plt.show()\n"
   "print(cat_month.sum(axis=1).sort_values(ascending=False).head())"),
 detective_sol=("cat_month = master.pivot_table(index='category', columns='month', values='line_revenue', aggfunc='sum', fill_value=0)\n"
   "print(cat_month.sum(axis=1).sort_values(ascending=False))"),
 interview_md=("- **Q15:** When `groupby` over `pivot_table`, and vice versa?\n"
   "- **Q17:** What do `observed=` and `dropna=` control on a groupby, and when do the defaults surprise you?"),
 reflection_md=("1. Answer Q15 in writing.\n2. Which category drove the seasonal swing?\n"
   "3. **Investigation log:** what does the cross-tab reveal that the totals hid?"),
 interview_notes=("- **Q15:** pivot_table for a ready-to-read 2-D grid/heatmap; groupby for multi-metric aggregation or further computation. pivot_table = groupby + unstack."),
)

# ===========================================================================
T11 = dict(
 num="11", dir="11_Exploratory_Analysis_And_Visualization", title="Exploratory Analysis & Visualization",
 boot=MASTER + "oi = master  # alias\n"
   "ts = master.dropna(subset=['order_date']).set_index('order_date').sort_index()\n"
   "monthly = ts['line_revenue'].resample('ME').sum()\n",
 warmup_md=("From **Topics 01–10**:\n\n1. (T10) `pivot` vs `pivot_table` — the crucial difference?\n"
   "2. (T07) How do you compute month-over-month growth in one call?\n3. NumPy: a histogram is built on which NumPy function?"),
 warmup_code=("# NumPy recall: bin counts with np.histogram\n"
   "data = np.array([1,1,2,3,3,3,4])\ncounts, edges = ...   # TODO np.histogram(data, bins=4)\n"
   "assert counts.sum() == len(data)\nprint(counts)"),
 warmup_sol=("data = np.array([1,1,2,3,3,3,4])\ncounts, edges = np.histogram(data, bins=4)\nprint(counts)"),
 core_intro="Every chart answers a question. Title = the takeaway. Label axes & units. Sort bars.",
 core=[
  dict(md="**Core 1 — trend with takeaway title.** Plot `monthly` with a 3-month moving average overlay; set a takeaway title + ylabel.",
       task="ax = monthly.plot(figsize=(10,4))\n# TODO add rolling(3).mean(), a takeaway title, ylabel\nassert len(monthly) >= 12\nplt.show()",
       sol="ax = monthly.plot(figsize=(10,4)); monthly.rolling(3).mean().plot(ax=ax)\n"
           "ax.set_title('Aurora revenue is seasonal, not declining'); ax.set_ylabel('Revenue (£)'); plt.show()"),
  dict(md="**Core 2 — sorted bar.** Revenue by channel, sorted, labelled, titled.",
       task="channel_rev = master.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
            "# TODO bar chart with title + ylabel\nassert channel_rev.is_monotonic_decreasing\nchannel_rev",
       sol="channel_rev = master.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
           "ax = channel_rev.plot(kind='bar', title='Online dominates revenue; Phone is marginal'); ax.set_ylabel('Revenue (£)'); plt.tight_layout(); plt.show()"),
  dict(md="**Core 3 — distribution.** Histogram of per-order revenue; note skew/outliers in the reflection.",
       task="order_rev = master.groupby('order_id')['line_revenue'].sum()\n# TODO hist with title + xlabel\norder_rev.describe()",
       sol="order_rev = master.groupby('order_id')['line_revenue'].sum()\n"
           "order_rev.plot(kind='hist', bins=50, title='Per-order revenue is right-skewed'); plt.xlabel('Order revenue (£)'); plt.show()"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 06) — join for the chart.** Build refunds-by-month (join `returns`→order dates, resample).",
       task="returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n"
            "rmonth = returns.merge(orders[['order_id','order_date']], on='order_id', how='left').dropna(subset=['order_date'])\n"
            "refunds_by_month = ...\nassert refunds_by_month.sum() > 0\nrefunds_by_month.tail()",
       sol="returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n"
           "rmonth = returns.merge(orders[['order_id','order_date']], on='order_id', how='left').dropna(subset=['order_date'])\n"
           "print(rmonth.set_index('order_date')['refund_amount'].resample('ME').sum().tail())"),
  dict(md="**Mixed review (Topic 09) — feature then plot.** Profit by `category` (sorted barh).",
       task="cat_profit = ...\nassert cat_profit.is_monotonic_increasing or cat_profit.is_monotonic_decreasing\ncat_profit",
       sol="cat_profit = master.groupby('category')['line_profit'].sum().sort_values()\ncat_profit.plot(kind='barh', title='Profit by category'); plt.show()"),
 ],
 detective_md=("**Case file #11 — the one-page dashboard.** Assemble a 2×2 figure for the manager: monthly revenue, "
   "revenue by channel, profit by category, profit by channel. This becomes the capstone centerpiece."),
 detective_task=("channel_rev = master.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
   "fig, axes = plt.subplots(2,2, figsize=(13,8))\nmonthly.plot(ax=axes[0,0], title='Monthly revenue')\n"
   "channel_rev.plot(kind='bar', ax=axes[0,1], title='Revenue by channel')\n"
   "master.groupby('category')['line_profit'].sum().sort_values().plot(kind='barh', ax=axes[1,0], title='Profit by category')\n"
   "master.groupby('channel')['line_profit'].sum().plot(kind='bar', ax=axes[1,1], title='Profit by channel')\n"
   "fig.tight_layout()\nassert len(fig.axes) >= 4\nplt.show()"),
 detective_sol=("print('Dashboard = 4 panels: revenue trend, revenue by channel, profit by category, profit by channel.')"),
 interview_md=("- **Q30:** A stakeholder doubts your number — how do you trace it to raw data and defend/correct it?\n"
   "- **Q31:** How do you make the analysis reproducible next quarter?"),
 reflection_md=("1. Answer Q30 and Q31 in writing.\n2. Which single chart best explains the case to a manager?\n"
   "3. **Investigation log:** finalize the story for the capstone."),
 interview_notes=("- **Q30:** reproduce from raw with a documented filter/join chain, check grain (row counts), show coverage of excluded rows, reconcile order-level vs line-level.\n"
   "- **Q31:** one parameterised notebook, pinned versions, deterministic load, asserts on invariants, no manual spreadsheet steps."),
)

# ===========================================================================
T12 = dict(
 num="12", dir="12_Capstone_Investigation", title="Capstone Investigation",
 boot=MASTER + "returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n",
 warmup_md=("Final recall across the whole course:\n\n1. (T04) Name three cleaning fixes Aurora's data needed.\n"
   "2. (T06) What invariant proves a join didn't fan out?\n3. NumPy: how do you compute a weighted ratio ignoring zero-denominator rows?"),
 warmup_code=("# Final NumPy recall: overall margin ignoring zero-revenue rows\n"
   "rev = np.array([100., 200., 0., 50.]); cogs = np.array([60., 120., 0., 25.])\n"
   "mask = rev > 0\nmargin = ...   # TODO (rev-cogs).sum()/rev.sum() over mask\n"
   "assert round(float(margin),4) == round(float((rev[mask]-cogs[mask]).sum()/rev[mask].sum()),4)\nprint('ok')"),
 warmup_sol=("rev = np.array([100.,200.,0.,50.]); cogs = np.array([60.,120.,0.,25.])\nmask = rev>0\n"
   "margin = (rev[mask]-cogs[mask]).sum()/rev[mask].sum()\nprint(round(float(margin),4))"),
 core_intro="This is the job: assemble everything into a defensible report. Objective KPIs self-check; the narrative has no key.",
 core=[
  dict(md="**Core 1 — grain-safe master.** Confirm the master table preserved the line grain.",
       task="items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
            "assert len(master) == len(items), 'a join changed the grain!'\nprint('master rows:', len(master))",
       sol="items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\nprint(len(master) == len(items))"),
  dict(md="**Core 2 — the KPIs.** Compute gross & net revenue, AOV, returns rate, gross margin. All self-checked.",
       task="gross = master['line_revenue'].sum()\ntotal_refunds = returns['refund_amount'].sum()\nnet = ...\n"
            "n_orders = orders['order_id'].nunique()\naov = ...\nreturns_rate = (orders['status']=='returned').mean()\n"
            "gross_margin = ...\n"
            "assert net == gross - total_refunds\nassert 0 <= returns_rate <= 1 and 0 <= gross_margin <= 1\n"
            "print(f'gross £{gross:,.0f} | net £{net:,.0f} | AOV £{aov:,.2f} | returns {returns_rate:.1%} | margin {gross_margin:.1%}')",
       sol="gross = master['line_revenue'].sum(); total_refunds = returns['refund_amount'].sum(); net = gross-total_refunds\n"
           "n_orders = orders['order_id'].nunique(); aov = gross/n_orders\nreturns_rate = (orders['status']=='returned').mean()\n"
           "gross_margin = (gross - master['line_cogs'].sum())/gross\n"
           "print(f'gross £{gross:,.0f} net £{net:,.0f} AOV £{aov:.2f} returns {returns_rate:.1%} margin {gross_margin:.1%}')"),
  dict(md="**Core 3 — resolve the dip.** Plot monthly revenue + 3mo MA and state your verdict (real vs artifact).",
       task="monthly = master.dropna(subset=['order_date']).set_index('order_date').sort_index()['line_revenue'].resample('ME').sum()\n"
            "ax = monthly.plot(figsize=(11,4)); monthly.rolling(3).mean().plot(ax=ax)\n"
            "ax.set_title('Verdict: real dip or seasonal artifact? (write it)'); ax.set_ylabel('Revenue £'); plt.show()\n"
            "assert len(monthly) >= 12\nprint('done')",
       sol="monthly = master.dropna(subset=['order_date']).set_index('order_date').sort_index()['line_revenue'].resample('ME').sum()\n"
           "print(monthly.pct_change().describe())  # seasonal swings, not a structural decline"),
 ],
 mixed=[
  dict(md="**Mixed review (Topics 08/09) — corroborate with text + features.** Count late & damaged support mentions.",
       task="tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str})\nm = tickets['message'].str.lower()\n"
            "late = ...\ndamaged = ...\nassert late > 0 and damaged > 0\nprint('late', late, 'damaged', damaged)",
       sol="tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str})\nm = tickets['message'].str.lower()\n"
           "print(m.str.contains('late|where is', regex=True, na=False).sum(), m.str.contains('damaged|broken|leak', regex=True, na=False).sum())"),
  dict(md="**Mixed review (Topic 10) — management cross-tab.** Revenue by channel × month with margins.",
       task="pivot = ...\nassert 'All' in pivot.index\npivot.iloc[:, :3]",
       sol="pivot = master.pivot_table(index='channel', columns='month', values='line_revenue', aggfunc='sum', margins=True, fill_value=0)\nprint(pivot.iloc[:, :3])"),
 ],
 detective_md=("**The case closes — final report.** Answer the brief with evidence: (1) is revenue actually falling? "
   "(2) where is margin leaking? (3) top 3 actions, each tied to a number. Build the one-page dashboard and write the "
   "narrative below (no key — you defend it like a real analyst)."),
 detective_task=("channel_rev = master.groupby('channel')['line_revenue'].sum().sort_values(ascending=False)\n"
   "monthly = master.dropna(subset=['order_date']).set_index('order_date').sort_index()['line_revenue'].resample('ME').sum()\n"
   "fig, axes = plt.subplots(2,2, figsize=(13,8))\nmonthly.plot(ax=axes[0,0], title='Monthly revenue')\n"
   "channel_rev.plot(kind='bar', ax=axes[0,1], title='Revenue by channel')\n"
   "master.groupby('category')['line_profit'].sum().sort_values().plot(kind='barh', ax=axes[1,0], title='Profit by category')\n"
   "master.groupby('channel')['line_profit'].sum().plot(kind='bar', ax=axes[1,1], title='Profit by channel')\n"
   "fig.tight_layout()\nassert len(fig.axes) >= 4\nplt.show()\nprint('Now write the executive summary + 3 recommendations.')"),
 detective_sol=("print('Objective gate passed; the narrative (exec summary, findings, 3 numbered recommendations) is yours to defend.')"),
 interview_md=("- **Q30:** Defend your headline revenue number to the Head of Finance — trace it to raw rows.\n"
   "- **Q32:** What does *data quality* mean, concretely, on a dataset like Aurora's?"),
 reflection_md=("1. Re-answer Q30 and Q32 as a presentation.\n2. Write your ≤150-word executive summary.\n"
   "3. List your top-3 recommendations, each tied to a specific number."),
 interview_notes=("- **Q30:** show lineage raw→clean→join→aggregate with row-count asserts and coverage of exclusions; reconcile order vs line level.\n"
   "- **Q32:** accuracy, completeness, consistency, validity, uniqueness, timeliness — made concrete on Aurora (channel casing, unique customers, valid prices, parsed dates, matched keys, documented exclusions)."),
)

for spec in (T9, T10, T11, T12):
    convert_lesson(spec["dir"])
    cleanup_topic(spec["dir"])
    build_practice_solutions(spec)
print("v2 topics 09-12 done")
