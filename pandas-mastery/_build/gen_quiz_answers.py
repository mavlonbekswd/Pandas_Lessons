"""Generate quiz answer keys in quizzes/ (kept separate from the quizzes on purpose)."""
import os
ROOT = os.path.join(os.path.dirname(__file__), "..")
Q = os.path.join(ROOT, "quizzes")
os.makedirs(Q, exist_ok=True)

ANS = {
"01": ("Introduction & Data Loading", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-a
**B.** 6 `(3,)` · 7 a `Series` · 8 `26049` (rows minus header)
**C.** 9 `parse_dates` · 10 `na_values` · 11 `shape` · 12 `to_csv`
**D.**
13. Use the relative path: `pd.read_csv(RAW + "orders.csv")` (or the correct path to `datasets/raw/`).
14. `df.info` references the method object; call it: `df.info()`.
15. `int` can't hold `NaN`. Load as float (the default) or use the nullable `Int64`: `dtype={"unit_cost":"Int64"}` only after deciding how to treat missing.
"""),
"02": ("Series & DataFrames", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 index0=NaN, index1=`1+1`? — careful: first series has index 0,1; second 1,2 → idx0 NaN, idx1 `2+1=3`, idx2 NaN · 7 `4.0` · 8 `1`
**C.** 9 `set_index` · 10 `value_counts` · 11 `assign` · 12 `values`
**D.**
13. Precedence: multiply binds before subtract, so `*1 - discount` subtracts discount once. Wrap: `quantity*unit_price*(1-discount)`.
14. Use double brackets: `orders[["channel","status"]]`.
15. Indexes differ (`a,b,c` vs `0,1,2`); alignment yields all NaN. Reset/align indexes first.
"""),
"03": ("Selection, Filtering & Boolean Logic", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 `2` (values 2 and 3) · 7 `2` · 8 `2`
**C.** 9 `"cancelled"` · 10 `isin` · 11 `~` · 12 `copy`
**D.**
13. `items[(items.quantity>100) & (items.unit_price>50)]`.
14. `online = orders.loc[orders.channel=="Online"].copy(); online["promo"]=True`.
15. `and` evaluates a whole Series' truth value (ambiguous). Use `&` with parentheses: `orders.loc[(orders.status=="cancelled") & (orders.channel=="Phone")]`.
"""),
"04": ("Data Cleaning & Missing Data", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 `4.0` (skipna) · 7 `1` · 8 `1`
**C.** 9 `strip` then `title` (or `lower`) · 10 `dropna` · 11 `fillna` · 12 `replace`
**D.**
13. Default `drop_duplicates()` needs *all* columns equal; the whitespace name differs. Strip names first, or `drop_duplicates(subset=["customer_id"])`.
14. Missing values block `int`. Keep float, or `pd.to_numeric(..., errors="coerce")`, or nullable `Int64`.
15. Trailing space means the value is `"Online "` not `"online"`; `replace` is exact-match. Strip + lower first, then map.
"""),
"05": ("GroupBy & Aggregation", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 a=3, b=3 · 7 equal (`size().sum()==len(df)`) · 8 equal to `len(df)`
**C.** 9 `size` · 10 `sum` · 11 `transform` · 12 `as_index`
**D.**
13. `items.groupby("product_id")["line_revenue"].sum()`.
14. Replace `sum()` with `transform("sum")` to get a per-row aligned result.
15. Use `kind="bar"` for category counts.
"""),
"06": ("Merge / Join / Concat", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 `2` (keys 2,3) · 7 `(2,1)` · 8 `100`
**C.** 9 `on` · 10 `validate` · 11 `right_on` · 12 `indicator`
**D.**
13. order_items has many lines per order → many-to-one from items side, but joining orders→items fans out; use `how`/`validate="one_to_many"` and check row counts.
14. Cast keys to the same dtype: `b["id"]=b["id"].astype(str)`.
15. `axis=1` aligns on the **index**, not row order; reset/align indexes or use `merge`.
"""),
"07": ("DateTime & Time Series", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 `1` (13 Jan → month 1) · 7 `31` · 8 `NaT`
**C.** 9 `"mixed"` · 10 `to_period` · 11 `rolling` · 12 `resample`
**D.**
13. The column is still a string; `pd.to_datetime(...)` first, then `.dt`.
14. Set a DatetimeIndex: `rev.set_index("order_date").resample("ME").sum()`.
15. Ambiguous `dd/mm` vs `mm/dd`; add `dayfirst=True` (and `format="mixed"`).
"""),
"08": ("String Operations & Text Data", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 `[3,2]` · 7 `1` · 8 `"O200001"`
**C.** 9 `regex` · 10 `strip` then `lower` · 11 `extract` · 12 `na`
**D.**
13. `tickets["message"].str.contains("late")` (missing `.str`).
14. `s.str.contains("late", na=False)`.
15. `.` is regex "any char". Use `regex=False` or escape: `s.str.replace(r"\\.", "", regex=True)`.
"""),
"09": ("Apply / Map / Transform", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-c
**B.** 6 `["a","b",NaN]` (missing key→NaN) · 7 `["p","n","p"]` · 8 `["small","big"]`
**C.** 9 `map` · 10 `where` · 11 `select` · 12 `transform`
**D.**
13. `df["rev"] = df["q"] * df["p"]`.
14. `np.select([df["q"]>=100, df["q"]>=10], ["big","med"], default="small")`.
15. `str.upper` fails on the float `NaN`. Use `s.str.upper()` (NaN-safe) or `.map(lambda x: x.upper() if isinstance(x,str) else x)`.
"""),
"10": ("Pivot Tables & MultiIndex", """
**A.** 1-a · 2-b · 3-b · 4-b · 5-b
**B.** 6 `3` · 7 `(4, 24)` · 8 a `DataFrame` ·
**C.** 9 `sum` · 10 `margins` · 11 `unstack` · 12 `melt`
**D.**
13. Use `pivot_table` (it aggregates duplicates).
14. `g.loc["a1"]` selects the outer level, or `g.xs("a1", level=0)`.
15. `pivot.reset_index()` (or flatten columns) before plotting/exporting.
"""),
"11": ("Exploratory Analysis & Visualization", """
**A.** 1-b · 2-b · 3-b · 4-b · 5-b
**B.** 6 counts of values per bin (frequency) · 7 `(3,3)` · 8 columns are stacked within each index bar
**C.** 9 `plot` · 10 `bar` · 11 `heatmap` · 12 `scatter`
**D.**
13. `rev_by_channel.plot(kind="bar")`.
14. Add `plt.title(...)`, `plt.xlabel(...)`, `plt.ylabel(...)`.
15. Provide both axes: `df.plot.scatter("spend","revenue")`.
"""),
"12": ("Capstone Self-Assessment", """
This is a completeness/rigor checklist, not a trivia quiz — there are no
lettered answers. **Standard:** every box should be a confident "yes" with
evidence in your notebook. If you cannot trace your headline revenue number back
to raw rows (item 7), or you silently dropped data without reporting coverage
(item 11), the capstone is not finished. Re-read `challenge.md` acceptance
checks and the `interview_lens.md` questions, and make sure the narrative takes
a clear, numbers-backed position.
"""),
}

for k, (title, body) in ANS.items():
    path = os.path.join(Q, f"{k}_answers.md")
    with open(path, "w") as f:
        f.write(f"# Topic {k} — Quiz Answer Key ({title})\n\n"
                "> Check yourself *after* attempting. Letters refer to the quiz parts.\n"
                + body.strip() + "\n")
# index
with open(os.path.join(Q, "README.md"), "w") as f:
    f.write("# Quiz Answer Keys\n\nKept **separate** from the quizzes on purpose — attempt first.\n\n")
    for k, (title, _) in ANS.items():
        f.write(f"- [Topic {k} — {title}]({k}_answers.md)\n")
print("quiz answer keys written:", len(ANS) + 1)
