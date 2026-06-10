import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from v2common import convert_lesson, build_practice_solutions, cleanup_topic

IMP = "import numpy as np\nimport pandas as pd\npd.set_option('display.max_columns', 30)\nRAW = '../datasets/raw/'\n"
# common cleaned-load used by several topics
LOAD = (IMP +
 "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
 "orders['channel'] = orders['channel'].str.strip().str.title()\n"
 "orders['status'] = orders['status'].str.strip().str.lower()\n"
 "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
 "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
 "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
 "oi = items.merge(orders[['order_id','channel','customer_id']], on='order_id', how='left')\n")

# ===========================================================================
T5 = dict(
 num="05", dir="05_GroupBy_And_Aggregation", title="GroupBy & Aggregation",
 boot=LOAD,
 warmup_md=("From **Topics 01–04**:\n\n1. (T04) How does standardising casing change Aurora's channel totals?\n"
   "2. (T03) Why must boolean masks use `&` not `and`?\n3. NumPy: how do you sum only the elements where a mask is True?"),
 warmup_code=("# NumPy recall: segmented sum via masks (a manual 'groupby')\n"
   "keys = np.array(['a','b','a','b','a']); vals = np.array([1.,2.,3.,4.,5.])\n"
   "sum_a = ...   # TODO sum of vals where key=='a'\nassert sum_a == 9\nprint(sum_a)"),
 warmup_sol=("keys = np.array(['a','b','a','b','a']); vals = np.array([1.,2.,3.,4.,5.])\n"
   "sum_a = vals[keys=='a'].sum()\nprint(sum_a)"),
 core_intro="Split → apply → combine. Use named aggregation; `transform` to broadcast a group stat back to rows.",
 core=[
  dict(md="**Core 1 — channel revenue.** Total `line_revenue` per `channel` (use `oi`).",
       task="channel_rev = ...\nassert channel_rev.sum() > 0\nchannel_rev.sort_values(ascending=False)",
       sol="channel_rev = oi.groupby('channel')['line_revenue'].sum()\nprint(channel_rev.sort_values(ascending=False))"),
  dict(md="**Core 2 — named aggregation.** Per `product_id`: `revenue` (sum), `units` (sum qty), `lines` (count).",
       task="summary = ...\nassert {'revenue','units','lines'} <= set(summary.columns)\nsummary.sort_values('revenue', ascending=False).head()",
       sol="summary = items.groupby('product_id').agg(revenue=('line_revenue','sum'), units=('quantity','sum'), lines=('order_id','count'))\n"
           "print(summary.sort_values('revenue', ascending=False).head())"),
  dict(md="**Core 3 — transform.** Add `pct_of_product` = a line's revenue ÷ that product's total revenue.",
       task="items['pct_of_product'] = ...\n"
            "chk = items.groupby('product_id')['pct_of_product'].sum().dropna().mean()\nassert np.isclose(chk, 1.0)\nprint('ok')",
       sol="items['pct_of_product'] = items['line_revenue'] / items.groupby('product_id')['line_revenue'].transform('sum')\n"
           "print(items.groupby('product_id')['pct_of_product'].sum().dropna().mean())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 04) — clean then group.** Confirm `channel` has ≤4 distinct values before trusting the groupby.",
       task="assert orders['channel'].nunique() <= 4\nprint(orders['channel'].unique())",
       sol="print(orders['channel'].nunique(), orders['channel'].unique())"),
  dict(md="**Mixed review (Topic 03) — filter + aggregate.** Revenue from *delivered* orders only.",
       task="delivered_rev = ...\nassert delivered_rev > 0\nprint(f'£{delivered_rev:,.0f}')",
       sol="oi2 = oi.merge(orders[['order_id','status']], on='order_id', how='left')\n"
           "delivered_rev = oi2.loc[oi2['status']=='delivered','line_revenue'].sum()\nprint(f'£{delivered_rev:,.0f}')"),
 ],
 detective_md=("**Case file #5 — top customer & AOV.** Management asks: who is the top customer by revenue, and "
   "what is the average order value (revenue per order)?"),
 detective_task=("order_rev = oi.groupby('order_id')['line_revenue'].sum()\naov = order_rev.mean()\n"
   "cust_rev = oi.groupby('customer_id')['line_revenue'].sum()\ntop_customer = cust_rev.idxmax()\n"
   "assert aov > 0\nprint('AOV £%.2f | top customer %s' % (aov, top_customer))"),
 detective_sol=("order_rev = oi.groupby('order_id')['line_revenue'].sum()\n"
   "print('AOV', round(order_rev.mean(),2), '| top', oi.groupby('customer_id')['line_revenue'].sum().idxmax())"),
 interview_md=("- **Q14:** Explain split–apply–combine in your own words.\n"
   "- **Q15:** Why choose `groupby` over `pivot_table` — and vice versa?\n"
   "- **Q16:** Difference between `transform`, `agg`, and `apply` on a groupby."),
 reflection_md=("1. Answer Q14 and Q16 in writing.\n2. Did the channel revenue ranking match the *raw* (dirty) ranking? Why does cleaning matter here?\n"
   "3. **Investigation log:** which channel/products drive revenue?"),
 interview_notes=("- **Q14:** split rows by key → reduce each group → combine to a table.\n"
   "- **Q16:** agg=one value/group; transform=same-length broadcast; apply=arbitrary per-group function (slowest)."),
)

# ===========================================================================
T6 = dict(
 num="06", dir="06_Merge_Join_Concat", title="Merge / Join / Concat",
 boot=LOAD + "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str}).drop_duplicates('customer_id')\n"
             "products['list_price'] = np.where(products['list_price']<0, np.nan, products['list_price'])\n",
 warmup_md=("From **Topics 01–05**:\n\n1. (T05) What does `transform` give you that `agg` doesn't?\n"
   "2. (T04) Why coerce negative prices to NaN before joining cost data?\n3. NumPy: how do you test membership of one array's values in another?"),
 warmup_code=("# NumPy recall: a 'join audit' on key arrays\n"
   "left = np.array([1,2,3,4,5]); right = np.array([3,4,5,6])\n"
   "matched = ...   # in both\norphans_n = ...   # in left, not in right\n"
   "assert sorted(matched) == [3,4,5] and orphans_n == 2\nprint('ok')"),
 warmup_sol=("left = np.array([1,2,3,4,5]); right = np.array([3,4,5,6])\n"
   "matched = np.intersect1d(left, right); orphans_n = int((~np.isin(left, right)).sum())\nprint(matched, orphans_n)"),
 core_intro="A `left` join must not change the left row count — unless the right key has duplicates. Validate every join.",
 core=[
  dict(md="**Core 1 — safe left join.** Bring `unit_cost` into `items` (validate many_to_one). Row count must not change.",
       task="before = len(items)\nm = ...\nassert len(m) == before\nprint('rows preserved:', len(m))",
       sol="m = items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')\nprint(len(m))"),
  dict(md="**Core 2 — line profit.** On `m`, compute `line_profit = line_revenue - quantity*unit_cost`. Count lines missing cost.",
       task="m['line_profit'] = ...\nmissing_cost = ...\nassert 'line_profit' in m.columns\nprint('missing cost:', missing_cost)",
       sol="m['line_profit'] = m['line_revenue'] - m['quantity']*m['unit_cost']\nprint(m['unit_cost'].isna().sum())"),
  dict(md="**Core 3 — find orphans.** Left-merge `orders`→`customers` with `indicator=True`; isolate `left_only`.",
       task="om = orders.merge(customers[['customer_id']], on='customer_id', how='left', indicator=True)\n"
            "orphans = ...\nassert orphans.shape[0] > 0\nprint('orphan orders:', orphans.shape[0])",
       sol="om = orders.merge(customers[['customer_id']], on='customer_id', how='left', indicator=True)\n"
           "orphans = om[om['_merge']=='left_only']\nprint(orphans.shape[0])"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 05) — group the joined table.** Profit per channel from the costed master table.",
       task="master = items.merge(products[['product_id','unit_cost']], on='product_id', how='left').merge(orders[['order_id','channel']], on='order_id', how='left')\n"
            "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\n"
            "profit_by_channel = ...\nassert len(master)==len(items)\nprofit_by_channel.sort_values(ascending=False)",
       sol="master = items.merge(products[['product_id','unit_cost']], on='product_id', how='left').merge(orders[['order_id','channel']], on='order_id', how='left')\n"
           "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\n"
           "print(master.groupby('channel')['line_profit'].sum().sort_values(ascending=False))"),
  dict(md="**Mixed review (Topic 03) — mask the result.** From the costed master, how many lines are loss-making (`line_profit < 0`)?",
       task="n_loss = ...\nassert n_loss >= 0\nprint(n_loss)",
       sol="n_loss = (master['line_profit'] < 0).sum()\nprint(int(n_loss))"),
 ],
 detective_md=("**Case file #6 — true profit, joined safely.** Revenue lied because cost lived in another table. "
   "Build the master table (items→products→orders), compute profit per channel, and prove no join changed the grain."),
 detective_task=("master = (items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one')\n"
   "              .merge(orders[['order_id','channel']], on='order_id', how='left', validate='many_to_one'))\n"
   "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\n"
   "assert len(master) == len(items), 'a join changed the grain!'\n"
   "print(master.groupby('channel')['line_profit'].sum().sort_values(ascending=False))"),
 detective_sol=("master = items.merge(products[['product_id','unit_cost']], on='product_id', how='left', validate='many_to_one').merge(orders[['order_id','channel']], on='order_id', how='left', validate='many_to_one')\n"
   "master['line_profit'] = master['line_revenue'] - master['quantity']*master['unit_cost']\nprint(master.groupby('channel')['line_profit'].sum())"),
 interview_md=("- **Q18:** Walk through inner/left/right/outer with two Aurora tables — who's lost or invented?\n"
   "- **Q19:** What risks exist when merging? How do you detect a many-to-many blow-up *before* it corrupts totals?\n"
   "- **Q20:** After a left merge your row count went *up*. What happened and how do you prove it?"),
 reflection_md=("1. Answer Q18 and Q19 in writing.\n2. Did any join change your row count? What would that do to revenue?\n"
   "3. **Investigation log:** what is *profit* (not revenue) telling you now?"),
 interview_notes=("- **Q18:** inner=intersection; left=all orders (orphans→NaN); right=all customers; outer=union.\n"
   "- **Q19:** duplicate join keys fan out rows and inflate sums. Detect with `validate=`, row-count asserts, `indicator=True`, `df[key].is_unique`."),
)

# ===========================================================================
T7 = dict(
 num="07", dir="07_DateTime_And_Time_Series", title="DateTime & Time Series",
 boot=IMP + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
            "orders['channel'] = orders['channel'].str.strip().str.title()\n"
            "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
            "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n",
 warmup_md=("From **Topics 01–06**:\n\n1. (T06) Why does a left join sometimes increase the row count?\n"
   "2. (T05) Write revenue-per-channel with named aggregation.\n3. NumPy: what dtype underlies pandas datetimes?"),
 warmup_code=("# NumPy recall: timedelta arithmetic\n"
   "d = np.array(['2023-01-01','2023-02-01'], dtype='datetime64[D]')\n"
   "gap = ...   # TODO days between the two (int)\nassert gap == 31\nprint(gap)"),
 warmup_sol=("d = np.array(['2023-01-01','2023-02-01'], dtype='datetime64[D]')\n"
   "gap = int((d[1]-d[0]) / np.timedelta64(1,'D'))\nprint(gap)"),
 core_intro="Parse messy dates with format='mixed', dayfirst=True, errors='coerce'. Then `.dt`, `resample`, `rolling`.",
 core=[
  dict(md="**Core 1 — parse mixed dates.** Parse `orders['order_date']` robustly; report the parsed fraction.",
       task="orders['order_date'] = ...\nassert orders['order_date'].notna().mean() > 0.95\nprint(orders['order_date'].notna().mean())",
       sol="orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\nprint(orders['order_date'].notna().mean())"),
  dict(md="**Core 2 — monthly revenue.** Join line revenue to dates, set a datetime index, resample to monthly sum.",
       task="oi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
            "monthly = ...\nassert monthly.index.is_monotonic_increasing\nmonthly.tail()",
       sol="oi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
           "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\nmonthly = ts['line_revenue'].resample('ME').sum()\nprint(monthly.tail())"),
  dict(md="**Core 3 — growth.** Month-over-month growth via `pct_change`; print the worst and best month.",
       task="mom = ...\nassert mom.notna().sum() > 10\nprint('worst', mom.idxmin(), '| best', mom.idxmax())",
       sol="mom = monthly.pct_change()\nprint(mom.idxmin(), mom.idxmax())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 05) — group by time part.** Total revenue by day-of-week name (use `.dt.day_name()`).",
       task="oi['dow'] = oi['order_date'].dt.day_name()\ndow_rev = ...\nassert len(dow_rev) <= 7\ndow_rev",
       sol="oi['dow'] = oi['order_date'].dt.day_name()\nprint(oi.groupby('dow')['line_revenue'].sum())"),
  dict(md="**Mixed review (Topic 04) — gaps.** `marketing_spend` is missing a few days. Reindex daily spend to a gap-free range; count filled days.",
       task="mk = pd.read_csv(RAW+'marketing_spend.csv', parse_dates=['date'])\n"
            "daily = mk.groupby('date')['spend_gbp'].sum()\nfull = pd.date_range(daily.index.min(), daily.index.max(), freq='D')\n"
            "n_missing = ...\nassert n_missing >= 0\nprint('missing days:', n_missing)",
       sol="mk = pd.read_csv(RAW+'marketing_spend.csv', parse_dates=['date'])\ndaily = mk.groupby('date')['spend_gbp'].sum()\n"
           "full = pd.date_range(daily.index.min(), daily.index.max(), freq='D')\nprint(len(full) - len(daily))"),
 ],
 detective_md=("**Case file #7 — is the dip real?** The finance team panicked over a revenue 'dip'. Plot monthly "
   "revenue with a 3-month moving average. Once the dates are parsed correctly, decide: real fall, or an artifact "
   "of dirty dates / seasonality? Write your verdict in the reflection."),
 detective_task=("import matplotlib.pyplot as plt\noi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
   "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\nmonthly = ts['line_revenue'].resample('ME').sum()\n"
   "ax = monthly.plot(figsize=(10,4)); monthly.rolling(3).mean().plot(ax=ax)\n"
   "ax.set_title('Verdict: real dip or seasonal artifact?'); ax.set_ylabel('Revenue £'); plt.show()\n"
   "assert len(monthly) >= 12\nprint('months:', len(monthly))"),
 detective_sol=("oi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
   "ts = oi.dropna(subset=['order_date']).set_index('order_date').sort_index()\nprint(ts['line_revenue'].resample('ME').sum().describe())\n"
   "# The 'dip' is seasonal (Nov/Dec peaks); once parsed, revenue is not structurally falling."),
 interview_md=("- **Q22:** Why is parsing at load better than converting after? When is the reverse true?\n"
   "- **Q23:** `resample` vs `groupby` on a datetime — when interchangeable?\n"
   "- **Q24:** Handling gaps in a daily series — `fillna` vs interpolation risks?"),
 reflection_md=("1. Answer Q22 and Q24 in writing.\n2. Is the dip real? State your evidence.\n"
   "3. **Investigation log:** what does the time pattern say about Aurora's revenue?"),
 interview_notes=("- **Q22:** parse at load sets dtype once, avoids repeated conversions & id corruption; convert-after suits ad-hoc/inspection-first.\n"
   "- **Q24:** fillna(0) claims 'nothing happened'; interpolation invents values. Reindex to a full range first; choose by what the series means."),
)

# ===========================================================================
T8 = dict(
 num="08", dir="08_String_Operations_And_Text_Data", title="String Operations & Text Data",
 boot=IMP + "tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str,'order_id':str})\n"
            "returns = pd.read_csv(RAW+'returns.csv', dtype={'order_id':str})\n",
 warmup_md=("From **Topics 01–07**:\n\n1. (T07) What does `errors='coerce'` give you, and why is it useful?\n"
   "2. (T04) How would you standardise the messy `return_reason` text?\n3. NumPy: a boolean mask `.sum()` counts what?"),
 warmup_code=("# NumPy recall: count matches in a boolean mask built from text\n"
   "flags = np.array([True, False, True, True])\nn = ...   # TODO count True\nassert n == 3\nprint(n)"),
 warmup_sol=("flags = np.array([True, False, True, True])\nn = int(flags.sum())\nprint(n)"),
 core_intro="The `.str` accessor vectorizes string ops and skips NaN. `contains` is regex by default — use `na=False`.",
 core=[
  dict(md="**Core 1 — extract order ids.** Pull `O######` from each ticket message into `order_ref`.",
       task="tickets['order_ref'] = ...\nassert tickets['order_ref'].notna().sum() > 0\nprint(tickets['order_ref'].notna().sum())",
       sol="tickets['order_ref'] = tickets['message'].str.extract(r'(O\\d{6})')\nprint(tickets['order_ref'].notna().sum())"),
  dict(md="**Core 2 — theme flags.** From lowercased messages create booleans `is_late`, `is_damaged`, `is_refund`.",
       task="m = tickets['message'].str.lower()\ntickets['is_late'] = ...\ntickets['is_damaged'] = ...\ntickets['is_refund'] = ...\n"
            "assert tickets[['is_late','is_damaged','is_refund']].dtypes.eq(bool).all()\nprint(tickets[['is_late','is_damaged','is_refund']].sum())",
       sol="m = tickets['message'].str.lower()\n"
           "tickets['is_late'] = m.str.contains('late|where is', regex=True, na=False)\n"
           "tickets['is_damaged'] = m.str.contains('damaged|broken|leak', regex=True, na=False)\n"
           "tickets['is_refund'] = m.str.contains('refund|return', regex=True, na=False)\nprint(tickets[['is_late','is_damaged','is_refund']].sum())"),
  dict(md="**Core 3 — clean text categories.** Standardise `return_reason` (strip + lower). How many distinct reasons remain?",
       task="returns['return_reason'] = ...\nn_reasons = ...\nassert n_reasons > 0\nprint(n_reasons)",
       sol="returns['return_reason'] = returns['return_reason'].str.strip().str.lower()\nprint(returns['return_reason'].nunique())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 07) — text → time.** Bring `order_date` in via `order_ref` and count complaint themes per month.",
       task="orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
            "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
            "tk = tickets.merge(orders[['order_id','order_date']], left_on='order_ref', right_on='order_id', how='left')\n"
            "tk['month'] = tk['order_date'].dt.to_period('M')\ntheme_by_month = ...\nassert theme_by_month.sum().sum() > 0\ntheme_by_month.tail()",
       sol="orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
           "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
           "tk = tickets.merge(orders[['order_id','order_date']], left_on='order_ref', right_on='order_id', how='left')\n"
           "tk['month'] = tk['order_date'].dt.to_period('M')\nprint(tk.groupby('month')[['is_late','is_damaged','is_refund']].sum().tail())"),
  dict(md="**Mixed review (Topic 05) — group the flags.** Which ticket `channel` has the most late complaints?",
       task="tickets['ch'] = tickets['channel'].str.lower()\nworst_ch = ...\nassert isinstance(worst_ch, str)\nprint(worst_ch)",
       sol="tickets['ch'] = tickets['channel'].str.lower()\nprint(tickets.groupby('ch')['is_late'].sum().idxmax())"),
 ],
 detective_md=("**Case file #8 — voice of the customer.** Do tickets mentioning *late/damaged* concentrate in the "
   "same months as the returns spike? Count complaint themes by month and compare to your time story from Topic 7."),
 detective_task=("m = tickets['message'].str.lower()\n"
   "total_late = m.str.contains('late|where is', regex=True, na=False).sum()\n"
   "total_damaged = m.str.contains('damaged|broken|leak', regex=True, na=False).sum()\n"
   "assert total_late > 0 and total_damaged > 0\nprint('late mentions:', total_late, '| damaged mentions:', total_damaged)"),
 detective_sol=("m = tickets['message'].str.lower()\nprint(m.str.contains('late|where is', regex=True, na=False).sum(), m.str.contains('damaged|broken|leak', regex=True, na=False).sum())"),
 interview_md=("- **Q9 (revisit):** A text column hides numbers — how do you reliably extract *and validate* them?\n"
   "- **Q29:** Name two NumPy ideas (masking, `np.where`, broadcasting) you use *inside* pandas, and why."),
 reflection_md=("1. Answer Q9 (revisited) in writing.\n2. Do complaint themes line up with the revenue/returns timing?\n"
   "3. **Investigation log:** voice-of-customer findings."),
 interview_notes=("- **Q9 revisited:** extract with a validated regex (`O\\d{6}`), then confirm the ids exist in `orders` via a merge "
   "with `indicator=True`; report extraction rate and unmatched refs rather than trusting the regex."),
)

for spec in (T5, T6, T7, T8):
    convert_lesson(spec["dir"])
    cleanup_topic(spec["dir"])
    build_practice_solutions(spec)
print("v2 topics 05-08 done")
