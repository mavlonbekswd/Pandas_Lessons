import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from v2common import convert_lesson, build_practice_solutions, cleanup_topic

IMP = "import numpy as np\nimport pandas as pd\npd.set_option('display.max_columns', 30)\nRAW = '../datasets/raw/'\n"

# ===========================================================================
T1 = dict(
 num="01", dir="01_Introduction_And_Data_Loading", title="Introduction & Data Loading",
 boot=IMP,
 warmup_md=(
  "You arrive at Aurora Outfitters knowing Python + NumPy. Prove the NumPy is still sharp "
  "(this is your prerequisite recall). **Predict each answer in your head first, then run.**\n\n"
  "1. How do you count how many elements of a NumPy array are `> 100`?\n"
  "2. How do you take a mean while ignoring `NaN`?\n"
  "3. Why is `arr * 2` faster than a Python `for` loop?"),
 warmup_code=(
  "arr = np.array([10., np.nan, 250., 5., 999.])\n"
  "# self-check (no answer shown): count > 100, and nan-safe mean\n"
  "n_big = ...   # TODO\nm = ...        # TODO nan-safe mean\n"
  "assert n_big == 2 and round(m, 2) == round(np.nanmean(arr), 2)\nprint('NumPy recall ok')"),
 warmup_sol=("arr = np.array([10., np.nan, 250., 5., 999.])\n"
             "n_big = int((arr > 100).sum())\nm = np.nanmean(arr)\nprint(n_big, round(m,2))"),
 core_intro="Load Aurora's data and run the first-look ritual: `shape`, `info()`, `head()`.",
 core=[
  dict(md="**Core 1 — load with intent.** Load `customers.csv` (force `customer_id` to `str`) and `products.csv`.",
       task="customers = ...\nproducts = ...\n"
            "assert customers['customer_id'].dtype == object\nassert products.shape[0] > 100\nprint(customers.shape, products.shape)",
       sol="customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str})\n"
           "products = pd.read_csv(RAW+'products.csv')\nprint(customers.shape, products.shape)"),
  dict(md="**Core 2 — spot the dirty dtype.** Count how many columns of `customers` are `object` "
          "(text). Which date-like column is text when it should be a date?",
       task="obj_cols = ...   # number of object-dtype columns\nassert obj_cols >= 4\ncustomers.dtypes",
       sol="obj_cols = int((customers.dtypes == object).sum())\nprint(obj_cols)\n"
           "# signup_date is text (mixed formats) — fixed in Topic 04/07"),
  dict(md="**Core 3 — reusable loader.** Write `load_aurora(raw)` returning a dict of all 9 tables "
          "with id columns as `str`. You will reuse this all course.",
       task="def load_aurora(raw):\n    ...\n\ndata = load_aurora(RAW)\n"
            "need = {'customers','products','orders','order_items','returns','marketing_spend','web_traffic','support_tickets','shipments'}\n"
            "assert set(data) >= need\nprint({k: v.shape for k, v in data.items()})",
       sol="def load_aurora(raw):\n    ids = ['customer_id','order_id','product_id','ticket_id']\n"
           "    files = ['customers','products','orders','order_items','returns','marketing_spend','web_traffic','support_tickets','shipments']\n"
           "    out = {}\n    for n in files:\n        df = pd.read_csv(raw+n+'.csv')\n"
           "        for c in ids:\n            if c in df.columns: df[c] = df[c].astype(str)\n        out[n] = df\n    return out\n\n"
           "data = load_aurora(RAW)\nprint({k: v.shape for k, v in data.items()})"),
 ],
 mixed=[],  # first topic
 detective_md=("**Case file #1 — sizing the evidence.** Before hunting the revenue problem, an analyst "
   "inventories the data. Load every table and answer: which table has the most rows, and how many "
   "customers are missing an email? Write your read in the reflection."),
 detective_task=("data = load_aurora(RAW)\nbiggest = max(data, key=lambda k: len(data[k]))\n"
   "missing_email = data['customers']['email'].isna().sum()\n"
   "assert biggest in data\nprint('biggest table:', biggest, '| customers missing email:', missing_email)"),
 detective_sol=("data = load_aurora(RAW)\nbiggest = max(data, key=lambda k: len(data[k]))\n"
   "print(biggest, data['customers']['email'].isna().sum())"),
 interview_md=("- **Q1:** What is the difference between a `Series` and a single-column `DataFrame`? When does it matter?\n"
   "- **Q2:** What exactly is the *index*, and name two real problems a bad index causes."),
 reflection_md=("1. Which Aurora columns are the wrong dtype, and what damage could that cause downstream?\n"
   "2. Why fix dtypes at *load* time instead of after?\n"
   "3. **Investigation log:** what is your first impression of where revenue might be leaking?"),
)

# ===========================================================================
T2 = dict(
 num="02", dir="02_Series_And_DataFrames", title="Series & DataFrames",
 boot=IMP + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
            "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n",
 warmup_md=("From **Topic 01** (loading) and NumPy:\n\n"
   "1. Which `read_csv` argument keeps `customer_id` like `C00042` intact?\n"
   "2. What does `df.info()` show that `df.head()` does not?\n"
   "3. NumPy: how do you element-wise multiply two arrays?"),
 warmup_code=("# NumPy recall: line revenue with raw arrays (no pandas)\n"
   "q = np.array([2, 1, 3]); pr = np.array([10., 20., 5.]); disc = np.array([0., 0.1, 0.])\n"
   "rev = ...   # TODO vectorized q*pr*(1-disc)\n"
   "assert np.allclose(rev, [20., 18., 15.])\nprint('ok')"),
 warmup_sol=("q = np.array([2,1,3]); pr = np.array([10.,20.,5.]); disc = np.array([0.,0.1,0.])\n"
   "rev = q*pr*(1-disc)\nprint(rev)"),
 core_intro="A Series = values + index. A DataFrame = aligned Series. New columns are vectorized NumPy.",
 core=[
  dict(md="**Core 1 — line revenue.** Add `line_revenue = quantity*unit_price*(1-discount)` to `items`.",
       task="items['line_revenue'] = ...\nassert items['line_revenue'].notna().sum() > 0\nprint(items['line_revenue'].notna().sum())",
       sol="items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\nprint(items['line_revenue'].describe())"),
  dict(md="**Core 2 — channel mix.** Make a Series of `channel` value counts on `orders`.",
       task="counts = ...\nassert counts.sum() == len(orders)\ncounts",
       sol="counts = orders['channel'].value_counts()\nprint(counts)  # note online/Online split — a Topic 04 cleaning job"),
  dict(md="**Core 3 — index lookup.** Set `order_id` as the index of `orders` into `orders_idx`, then `.loc` three ids.",
       task="orders_idx = ...\nassert orders_idx.index.name == 'order_id'\norders_idx.loc[orders['order_id'].head(3).tolist()]",
       sol="orders_idx = orders.set_index('order_id')\nprint(orders_idx.head())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 01) — reload correctly.** Re-load `products.csv` treating the string "
          "`'unknown'` supplier as missing. How many products then have a missing supplier?",
       task="products = ...\nn_missing_supplier = ...\nassert n_missing_supplier > 0\nprint(n_missing_supplier)",
       sol="products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str}, na_values=['unknown'])\n"
           "print(products['supplier'].isna().sum())"),
 ],
 detective_md=("**Case file #2 — the first revenue number.** Finance wants a single figure: gross line-item "
   "revenue, ignoring lines with a missing price. Compute it with one vectorized expression — this is the "
   "number you'll spend the rest of the course reconciling."),
 detective_task=("revenue = ...\nassert revenue > 0, 'The report still contains an issue.'\nprint(f'Gross line revenue: £{revenue:,.0f}')"),
 detective_sol=("revenue = (items['quantity']*items['unit_price']*(1-items['discount'])).sum()\nprint(f'£{revenue:,.0f}')"),
 interview_md=("- **Q1:** `Series` vs single-column `DataFrame` — when does it matter?\n"
   "- **Q2:** What is the index and what breaks with a bad one?\n"
   "- **Q5:** View vs copy — how do you know which you have, and why care?"),
 reflection_md=("1. Where could index *misalignment* silently inject `NaN`s into your work?\n"
   "2. Why is the vectorized revenue formula better than a Python row loop?\n"
   "3. **Investigation log:** record your first gross-revenue figure."),
)

# ===========================================================================
T3 = dict(
 num="03", dir="03_Selection_Filtering_And_Boolean_Logic", title="Selection, Filtering & Boolean Logic",
 boot=IMP + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
            "orders['status'] = orders['status'].str.strip().str.lower()\n"
            "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
            "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n",
 warmup_md=("From **Topics 01–02**:\n\n1. (T01) What does `errors`/dtype handling buy you at load time?\n"
   "2. (T02) Why does selecting `df[['a','b']]` use double brackets?\n3. NumPy: how do you build a boolean mask for `arr > 100`?"),
 warmup_code=("# NumPy recall: boolean masking + counting\n"
   "arr = np.array([5, 150, 30, 1200, 12])\nmask = ...   # TODO arr > 100\n"
   "assert mask.sum() == 2\nprint('masked count:', int(mask.sum()))"),
 warmup_sol=("arr = np.array([5,150,30,1200,12])\nmask = arr > 100\nprint(int(mask.sum()))"),
 core_intro="Reach for `.loc` + a boolean mask. Use `&`/`|`/`~` with parentheses, never `and`/`or`.",
 core=[
  dict(md="**Core 1 — combine conditions.** Mask `items` where `quantity > 100` AND `unit_price > 50`.",
       task="big = ...\nassert big.dtype == bool\nprint('big lines:', big.sum())",
       sol="big = (items['quantity'] > 100) & (items['unit_price'] > 50)\nprint(big.sum())"),
  dict(md="**Core 2 — isin.** Select marketplace orders regardless of casing (`Marketplace`/`marketplace`).",
       task="mkt = ...\nassert mkt.sum() > 0\nprint(mkt.sum())",
       sol="mkt = orders['channel'].isin(['Marketplace','marketplace'])\nprint(mkt.sum())"),
  dict(md="**Core 3 — no chained indexing.** Add `is_suspect` to `items` (`quantity>100` OR missing `unit_price`) in ONE statement.",
       task="items['is_suspect'] = ...\nassert items['is_suspect'].dtype == bool\nprint(items['is_suspect'].sum())",
       sol="items['is_suspect'] = (items['quantity'] > 100) | (items['unit_price'].isna())\nprint(items['is_suspect'].sum())"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 02) — Series ops.** Using `value_counts`, find the most common order `status`.",
       task="top_status = ...\nassert isinstance(top_status, str)\nprint(top_status)",
       sol="top_status = orders['status'].value_counts().idxmax()\nprint(top_status)"),
  dict(md="**Mixed review (Topic 01) — loading recall.** How many order rows are there, and how many distinct channels (raw, dirty)?",
       task="n_rows = ...\nn_channels = ...\nassert n_rows > 1000\nprint(n_rows, n_channels)",
       sol="n_rows = len(orders); n_channels = orders['channel'].nunique()\nprint(n_rows, n_channels)"),
 ],
 detective_md=("**Case file #3 — where is revenue leaking?** An auditor wants suspect orders: status in "
   "`{cancelled, returned}` AND channel online or marketplace (any casing). What share of all orders is that?"),
 detective_task=("bad_status = orders['status'].isin(['cancelled','returned'])\n"
   "bad_channel = orders['channel'].isin(['Online','online','Marketplace','marketplace'])\n"
   "leak_share = (bad_status & bad_channel).mean()\n"
   "assert 0 < leak_share < 1, 'Share must be a fraction.'\nprint(f'Suspect orders: {leak_share:.1%}')"),
 detective_sol=("bad = orders['status'].isin(['cancelled','returned']) & orders['channel'].isin(['Online','online','Marketplace','marketplace'])\n"
   "print(f'{bad.mean():.1%}')"),
 interview_md=("- **Q3:** `.loc` vs `.iloc` — difference and a bug each can cause.\n"
   "- **Q4:** Why can chained indexing silently fail? What is `SettingWithCopyWarning` telling you?\n"
   "- **Q11:** Why `&`/`|` instead of `and`/`or`, and why the parentheses?"),
 reflection_md=("1. Answer Q4 and Q11 in writing.\n2. When is `query()` clearer than a mask? When worse?\n"
   "3. **Investigation log:** what did filtering reveal about suspect orders?"),
 interview_notes=("- **Q11:** `&/|` are element-wise on arrays; `and/or` need a single truth value of the whole "
   "Series → ambiguous error. Parens because `&` binds tighter than `>`.\n"
   "- **Q4:** Chained indexing assigns into a possible temporary copy. Use one `.loc[mask, col] = ...` or `.copy()`."),
)

# ===========================================================================
T4 = dict(
 num="04", dir="04_Data_Cleaning_And_Missing_Data", title="Data Cleaning & Missing Data",
 boot=IMP + "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
            "customers = pd.read_csv(RAW+'customers.csv', dtype={'customer_id':str})\n"
            "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
            "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
            "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n",
 warmup_md=("From **Topics 01–03**:\n\n1. (T03) Rewrite `(s=='a')|(s=='b')|(s=='c')` with `isin`.\n"
   "2. (T02) What does the index control when you add two Series?\n3. NumPy: how does `np.where(cond, a, b)` behave?"),
 warmup_code=("# NumPy recall: vectorized cleaning with np.where (negatives -> NaN)\n"
   "vals = np.array([10., -5., 30., -1.])\nclean = ...   # TODO negatives -> np.nan\n"
   "assert np.isnan(clean).sum() == 2 and np.nanmin(clean) == 10\nprint('ok')"),
 warmup_sol=("vals = np.array([10.,-5.,30.,-1.])\nclean = np.where(vals < 0, np.nan, vals)\nprint(clean)"),
 core_intro="Profile → fix dtypes → standardise categories → dedupe → handle missing → validate.",
 core=[
  dict(md="**Core 1 — standardise categories.** Make `channel` Title Case (stripped) and `status` lowercase.",
       task="orders['channel'] = ...\norders['status'] = ...\n"
            "assert orders['channel'].nunique() <= 4 and orders['status'].str.islower().all()\nprint(orders['channel'].value_counts())",
       sol="orders['channel'] = orders['channel'].str.strip().str.title()\n"
           "orders['status'] = orders['status'].str.strip().str.lower()\nprint(orders['channel'].value_counts())"),
  dict(md="**Core 2 — dedupe.** Strip whitespace from `first_name`, then drop duplicate `customer_id` (keep first).",
       task="customers['first_name'] = ...\ncustomers = ...\n"
            "assert customers['customer_id'].is_unique\nassert not customers['first_name'].str.endswith(' ').any()\nprint(customers.shape)",
       sol="customers['first_name'] = customers['first_name'].astype(str).str.strip()\n"
           "customers = customers.drop_duplicates('customer_id', keep='first')\nprint(customers.shape)"),
  dict(md="**Core 3 — impossible values.** Set negative `list_price` in `products` to `NaN`.",
       task="products['list_price'] = ...\nassert (products['list_price'].dropna() >= 0).all()\nprint('fixed')",
       sol="products['list_price'] = np.where(products['list_price'] < 0, np.nan, products['list_price'])\nprint('fixed')"),
 ],
 mixed=[
  dict(md="**Mixed review (Topic 03) — filter on cleaned data.** After cleaning `status`, count cancelled orders with a mask.",
       task="n_cancelled = ...\nassert n_cancelled > 0\nprint(n_cancelled)",
       sol="n_cancelled = (orders['status'] == 'cancelled').sum()\nprint(n_cancelled)"),
  dict(md="**Mixed review (Topic 02) — first metric still holds.** Total gross line revenue on `items` (ignore NaN price).",
       task="rev = ...\nassert rev > 0\nprint(f'£{rev:,.0f}')",
       sol="rev = items['line_revenue'].sum()\nprint(f'£{rev:,.0f}')"),
 ],
 detective_md=("**Case file #4 — the double-counted channel.** The big break. Compare channel order counts "
   "**before** vs **after** standardising casing. Did finance double-count `online` and `Online`?"),
 detective_task=("raw = pd.read_csv(RAW+'orders.csv')\nbefore = raw['channel'].value_counts()\n"
   "after = orders['channel'].value_counts()\n"
   "assert after.shape[0] < before.shape[0], 'cleaning should merge categories'\n"
   "print('BEFORE\\n', before, '\\n\\nAFTER\\n', after)"),
 detective_sol=("raw = pd.read_csv(RAW+'orders.csv')\nprint(raw['channel'].nunique(), '->', orders['channel'].nunique())"),
 interview_md=("- **Q6:** Choosing between dropping, filling with 0, mean-filling, or leaving missing revenue as NaN.\n"
   "- **Q8:** How would you *investigate* unexpected missing values rather than just imputing?\n"
   "- **Q9:** A numeric column loads as `object` — likely causes and how to confirm each."),
 reflection_md=("1. Answer Q6 and Q9 in writing.\n2. Did cleaning change which channel looks biggest? (log it)\n"
   "3. For missing `unit_price`: would you drop, fill, or flag? Defend it."),
 interview_notes=("- **Q6:** Trace *why* it's missing. Free gift → 0; logging gap → impute from product list_price/median; "
   "could bias headline → keep NaN and report coverage. Never silently mean-fill revenue.\n"
   "- **Q9:** object dtype = stray text/symbols (£, commas), mixed types, or sentinels like 'unknown'. Confirm with "
   "`pd.to_numeric(errors='coerce').isna()`."),
)

for spec in (T1, T2, T3, T4):
    convert_lesson(spec["dir"])
    cleanup_topic(spec["dir"])
    build_practice_solutions(spec)
print("v2 topics 01-04 done")
