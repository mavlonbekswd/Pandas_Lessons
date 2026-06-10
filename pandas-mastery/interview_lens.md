# 🔍 Interview Lens

**~30 carefully chosen Pandas / data-analyst interview questions.**

These are **deliberately unanswered.** There is no answer key in this repo and
there never will be. Interviews test *reasoning*, not recall — so you must
write your own answers, in your own words, and defend them.

## How to use
- Starting at **Topic 03**, each lesson surfaces 2–3 of these. Answer them *in
  writing* before moving on.
- Keep your answers in a personal file (e.g. `my_interview_answers.md`).
- Revisit old answers after later topics — your reasoning should deepen.
- A good answer states a **trade-off** and a **when-I'd-do-otherwise**.

---

## Foundations & data model
1. What is the difference between a `Series` and a single-column `DataFrame`? When does it matter?
2. What exactly is the *index*, and name two real problems a bad index causes.
3. `.loc` vs `.iloc` — explain the difference and a bug each can cause.
4. Why can chained indexing (`df[df.a > 0]['b'] = 1`) silently fail? What is `SettingWithCopyWarning` really telling you?
5. View vs copy — how do you know which one you have, and why care?

## Cleaning & missing data
6. You find missing values in a revenue column. Walk through how you decide between dropping, filling with 0, filling with the mean, and leaving them `NaN`.
7. What is the difference between `NaN`, `None`, and `pd.NA`? When does the distinction bite you?
8. How would you investigate *unexpected* missing values rather than just imputing them?
9. A column of "numbers" loads as `object` dtype. List the likely causes and how you'd confirm each.
10. Why is silently dropping duplicate rows dangerous? How do you decide the subset and `keep` strategy?

## Selection & boolean logic
11. Why do you need `&`/`|` (not `and`/`or`) for boolean masks, and why the parentheses?
12. When is `query()` preferable to boolean masking, and when is it worse?
13. How does `isin()` differ from chained `==` conditions in both readability and performance?

## GroupBy & aggregation
14. Explain the split–apply–combine model in your own words.
15. Why might you choose `groupby` over `pivot_table` for the same question — and vice versa?
16. What's the difference between `transform`, `agg`, and `apply` on a groupby? Give a use case for each.
17. What does `groupby(..., observed=)` and `dropna=` control, and when would the defaults surprise you?

## Merging & joining
18. Walk through `inner`, `left`, `right`, `outer` joins using two business tables. When does each lose or invent rows?
19. What risks exist when merging datasets? How do you detect a many-to-many blow-up before it corrupts your totals?
20. After a `left` merge your row count went *up*. What happened and how do you prove it?
21. `merge` vs `join` vs `concat` — when do you reach for each?

## DateTime & time series
22. Why is `parse_dates` at load time better than converting afterwards? When is the reverse true?
23. Explain `resample` vs `groupby` on a datetime. When are they interchangeable?
24. How would you handle gaps (missing days) in a daily time series, and what's the risk of `fillna` vs interpolation here?
25. What is the difference between a rolling and an expanding window, with a business example of each?

## Performance & NumPy
26. Why is vectorization typically faster than `iterrows`/Python loops? What's actually happening under the hood?
27. When is `apply` a code smell, and what would you replace it with?
28. How do `category` dtypes save memory and speed up groupby? When can they hurt?
29. Give two NumPy ideas (masking, broadcasting, `np.where`, `np.select`) that you use *inside* Pandas, and why.

## Judgement / communication
30. You produce a number a stakeholder doesn't believe. How do you trace it back to the raw data and defend (or correct) it?
31. How do you make an analysis *reproducible* so a teammate gets the same answer next quarter?
32. What does "data quality" mean to you, concretely, on a dataset like Aurora's?
