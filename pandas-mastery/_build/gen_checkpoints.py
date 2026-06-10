"""Generate revision checkpoints (every 3 topics) into notebooks/."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import build_notebook
ROOT = os.path.join(os.path.dirname(__file__), "..")
NB = os.path.join(ROOT, "notebooks")
os.makedirs(NB, exist_ok=True)
BOOT = ("import numpy as np\nimport pandas as pd\nRAW = '../datasets/raw/'\n"
        "# Mixed-skill spaced-repetition checkpoint. Asserts grade objective parts;\n"
        "# interview questions have NO key — answer in writing.")

# ---------------------------------------------------------------- Checkpoint 1
cp1 = [
 ("md", "# 🔁 Revision Checkpoint 1 — Topics 1–3\n\n"
        "**Loading · Series/DataFrame · Selection & Boolean logic.** Spaced repetition: "
        "do this without re-reading the lessons. Silent cell = pass."),
 ("code", BOOT),
 ("md", "## Mixed question 1 — load with intent\nLoad `orders.csv` keeping ids as `str`; load `order_items.csv`."),
 ("code", "orders = ...\nitems = ...\n"
          "assert orders['order_id'].dtype == object\nassert items.shape[0] > orders.shape[0]\nprint('ok')"),
 ("md", "## Mixed question 2 — first metric\nAdd `line_revenue` to items and report the count of priced lines."),
 ("code", "items['line_revenue'] = ...\nassert items['line_revenue'].notna().sum() > 0\nprint(items['line_revenue'].notna().sum())"),
 ("md", "## Mixed challenge — suspicious selection\nWith a single `.loc` + boolean mask, select cancelled OR returned "
        "orders. Count them."),
 ("code", "orders['status'] = orders['status'].str.strip().str.lower()\nbad = ...\n"
          "assert bad.dtype == bool\nprint('cancelled/returned:', bad.sum())"),
 ("md", "## 🔢 NumPy recall (1–3)\nPure NumPy: mask, count, nan-mean."),
 ("code", "a = np.array([10., np.nan, 250., 5., 999.])\n"
          "n_big = ...  # count > 100\nm = ...        # mean ignoring nan\n"
          "assert n_big == 2\nassert round(m,2) == round(np.nanmean(a),2)\nprint('numpy ok')"),
 ("md", "## 🔎 Interview questions (write answers — no key)\n"
        "- Q3: `.loc` vs `.iloc` — difference and a bug each can cause.\n"
        "- Q11: why `&`/`|` and parentheses for masks?\n"
        "- Q5: view vs copy — how do you tell, why care?"),
 ("md", "## Self-rating\nRate 1–5 your confidence on loading, the index, and boolean filtering. "
        "Anything ≤3 → redo that topic's practice."),
]

# ---------------------------------------------------------------- Checkpoint 2
cp2 = [
 ("md", "# 🔁 Revision Checkpoint 2 — Topics 4–6\n\n**Cleaning · GroupBy · Merge.** No peeking."),
 ("code", BOOT + "\nproducts = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str,'customer_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])"),
 ("md", "## Mixed question 1 — clean then count\nStandardise `channel` casing; assert ≤4 distinct channels."),
 ("code", "orders['channel'] = ...\nassert orders['channel'].nunique() <= 4\nprint(orders['channel'].value_counts())"),
 ("md", "## Mixed question 2 — grouped KPI\nRevenue per product (top 5)."),
 ("code", "top5 = ...\nassert len(top5) == 5\nprint(top5)"),
 ("md", "## Mixed challenge — safe join + profit\nLeft-join product cost (validate many_to_one), compute line profit, "
        "assert grain preserved."),
 ("code", "m = ...\nm['line_profit'] = ...\nassert len(m) == len(items)\nprint('profit sum:', round(m['line_profit'].sum(),2))"),
 ("md", "## 🔢 NumPy recall (4–6)\nPure NumPy: segmented sum via boolean masks (group by a key array)."),
 ("code", "keys = np.array(['a','b','a','b','a'])\nvals = np.array([1.,2.,3.,4.,5.])\n"
          "sum_a = ...  # sum of vals where key=='a'\nsum_b = ...\n"
          "assert sum_a == 9 and sum_b == 6\nprint('numpy ok')"),
 ("md", "## 🔎 Interview questions (write answers)\n"
        "- Q6: choosing drop vs 0 vs mean vs NaN for missing revenue.\n"
        "- Q15: groupby vs pivot_table.\n"
        "- Q19: merge risks & detecting many-to-many."),
 ("md", "## Self-rating\nCleaning, split-apply-combine, safe joins — rate 1–5. Redo any ≤3."),
]

# ---------------------------------------------------------------- Checkpoint 3
cp3 = [
 ("md", "# 🔁 Revision Checkpoint 3 — Topics 7–9\n\n**DateTime · Strings · Apply/Map.** No peeking."),
 ("code", BOOT + "\norders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "tickets = pd.read_csv(RAW+'support_tickets.csv', dtype={'ticket_id':str})"),
 ("md", "## Mixed question 1 — parse + resample\nParse `order_date` (mixed, dayfirst), build monthly revenue."),
 ("code", "orders['order_date'] = ...\noi = items.merge(orders[['order_id','order_date']], on='order_id', how='left')\n"
          "monthly = ...\nassert monthly.index.is_monotonic_increasing\nprint(len(monthly), 'months')"),
 ("md", "## Mixed question 2 — text extract\nExtract `O######` order refs from ticket messages; count hits."),
 ("code", "tickets['order_ref'] = ...\nassert tickets['order_ref'].notna().sum() > 0\nprint(tickets['order_ref'].notna().sum())"),
 ("md", "## Mixed challenge — vectorized banding\n`np.select`: bulk≥100, medium≥10, else small on quantity."),
 ("code", "items['size_band'] = ...\nassert set(items['size_band'].unique()) <= {'bulk','medium','small'}\nprint(items['size_band'].value_counts())"),
 ("md", "## 🔢 NumPy recall (7–9)\nPure NumPy: vectorized if/else with `np.where`, and a multi-branch `np.select`."),
 ("code", "x = np.array([-2., 0., 5., -1.])\nsign = ...  # 'pos' if >0 else 'nonpos'\n"
          "assert list(sign) == ['nonpos','nonpos','pos','nonpos']\nprint('numpy ok')"),
 ("md", "## 🔎 Interview questions (write answers)\n"
        "- Q22: parse at load vs after.\n- Q24: time-series gaps (fillna vs interpolate).\n"
        "- Q26/Q27: vectorization vs loops; when apply is a smell."),
 ("md", "## Self-rating\nDatetime, text mining, vectorized features — rate 1–5."),
]

# ---------------------------------------------------------------- Checkpoint 4
cp4 = [
 ("md", "# 🏁 Revision Checkpoint 4 — Topics 10–12 (Course Capstone Review)\n\n"
        "**Reshape · Viz · Capstone.** This is your final pre-interview rehearsal."),
 ("code", BOOT + "\nimport matplotlib.pyplot as plt\n"
          "products = pd.read_csv(RAW+'products.csv', dtype={'product_id':str})\n"
          "orders = pd.read_csv(RAW+'orders.csv', dtype={'order_id':str})\n"
          "orders['channel'] = orders['channel'].str.strip().str.title()\n"
          "orders['order_date'] = pd.to_datetime(orders['order_date'], format='mixed', dayfirst=True, errors='coerce')\n"
          "orders['month'] = orders['order_date'].dt.to_period('M').astype(str)\n"
          "items = pd.read_csv(RAW+'order_items.csv', dtype={'order_id':str,'product_id':str})\n"
          "items['line_revenue'] = items['quantity']*items['unit_price']*(1-items['discount'])\n"
          "master = (items.merge(products[['product_id','category']], on='product_id', how='left')\n"
          "               .merge(orders[['order_id','channel','month']], on='order_id', how='left'))"),
 ("md", "## Mixed question 1 — the management pivot\nRevenue by channel × month with margins."),
 ("code", "pivot = ...\nassert 'All' in pivot.index\nprint(pivot.iloc[:, :3])"),
 ("md", "## Mixed challenge — one chart that argues\nDraw revenue by category (sorted bar) with a takeaway title and ylabel."),
 ("code", "cat_rev = master.groupby('category')['line_revenue'].sum().sort_values(ascending=False)\n"
          "# TODO plot\nassert cat_rev.is_monotonic_decreasing\nprint(cat_rev)"),
 ("md", "## 🔢 Final NumPy recall (10–12)\nWeighted margin ignoring zero-revenue rows."),
 ("code", "rev = np.array([100.,200.,0.,50.]); cogs = np.array([60.,120.,0.,25.])\n"
          "mask = rev>0\nmargin = ...\n"
          "assert round(float(margin),4) == round(float((rev[mask]-cogs[mask]).sum()/rev[mask].sum()),4)\nprint('numpy ok')"),
 ("md", "## 🔎 Interview questions (final, write answers)\n"
        "- Q15 groupby vs pivot_table · Q30 defend a number · Q31 reproducibility · Q32 data quality.\n\n"
        "## Capstone readiness\nIf you can complete every cell above unaided AND defend the capstone narrative, "
        "you are interview-ready. Log your verdict in your investigation notes."),
]

build_notebook(cp1, os.path.join(NB, "revision_checkpoint_1.ipynb"))
build_notebook(cp2, os.path.join(NB, "revision_checkpoint_2.ipynb"))
build_notebook(cp3, os.path.join(NB, "revision_checkpoint_3.ipynb"))
build_notebook(cp4, os.path.join(NB, "revision_checkpoint_4.ipynb"))
with open(os.path.join(NB, "README.md"), "w") as f:
    f.write("# Revision Checkpoints\n\nSpaced-repetition reviews after every 3 topics. Mixed questions, "
            "mixed challenges, interview prompts (unanswered), and a NumPy recall block.\n\n"
            "- `revision_checkpoint_1.ipynb` — after Topics 1–3\n"
            "- `revision_checkpoint_2.ipynb` — after Topics 4–6\n"
            "- `revision_checkpoint_3.ipynb` — after Topics 7–9\n"
            "- `revision_checkpoint_4.ipynb` — after Topics 10–12 (capstone review)\n")
print("checkpoints written")
