# 🏔️ Pandas Mastery — The Aurora Outfitters Investigation

A **practice-first** Pandas curriculum that takes you from "I know Python and a
little NumPy" to **job-ready data analyst**. The notebook *is* the lesson — you
learn by doing, with spaced repetition baked into every topic. No toy data, no
fruit, no student-score spreadsheets.

> **The story.** You are the new Junior Data Analyst at **Aurora Outfitters**, a
> European outdoor-gear retailer. The finance team's revenue numbers don't add
> up. Across 12 topics you clean, reshape, join and analyse the company's messy
> data ecosystem — and in the capstone you deliver the report that explains what
> really happened. Every notebook moves the investigation forward.

---

## Who this is for

You already know: Python basics, variables, loops, functions, lists,
dictionaries, and **NumPy basics**. You do **not** need prior Pandas.

By the end you can clean messy data, run exploratory analysis, build business
reports, prepare data for ML, reason about performance, and pass Pandas
technical interviews.

---

## Three files per topic — that's it

Each topic folder contains exactly:

| File | What it's for |
|---|---|
| `lesson.ipynb` | The *why / when / how* — read it, run the examples (~20% of your time) |
| `practice.ipynb` | **Where you actually learn** (~80%) — see the fixed structure below |
| `solutions.ipynb` | Reference solutions for the *objective* tasks only |

There are **no separate quizzes, challenges, or trackers** — everything lives in
the practice notebook.

### Every `practice.ipynb` follows the same rhythm
1. **🔁 Warm-Up Recall** — questions from earlier topics + a NumPy recall task. *No answers given.*
2. **🎯 Core Lesson Tasks** — the current topic, learned by doing.
3. **🔀 Mixed Review** — tasks that re-use earlier topics (spaced repetition).
4. **🕵️ Data Detective** — a business problem in the ongoing Aurora story.
5. **🔎 Interview Lens** — 2–3 interview questions. *No model answers.*
6. **✍️ Reflection** — short written explanations (why it worked, alternatives, assumptions).

**Spaced repetition rule:** ~60% current topic, ~40% earlier topics — you never
fully leave old material behind. **NumPy** is reinforced in every notebook.

### ⚠️ How grading works (anti-passive learning)
- Objective tasks self-check with `assert`. A cell that runs **silently = pass**;
  an `AssertionError` means fix your code. The answer value is never shown.
- Warm-Up, Interview Lens and Reflection have **no key** — you write the answers.
- Open `solutions.ipynb` only after a real attempt.

---

## How to use this repo
1. Read the story: [`datasets/docs/DATA_DICTIONARY.md`](datasets/docs/DATA_DICTIONARY.md).
2. Work topics **in order**, `01` → `12`. For each: skim `lesson.ipynb`, then live in `practice.ipynb`.
3. After topics **3, 6, 9, 12**, do the matching `revision_checkpoint_*.ipynb` in [`notebooks/`](notebooks).
4. Fill a blank cheatsheet from memory after each topic ([`cheatsheets/`](cheatsheets)).
5. Keep your interview answers and investigation log in your own file.

## Repository layout

```
pandas-mastery/
├── README.md
├── interview_lens.md          ← ~30 unanswered interview questions
├── datasets/
│   ├── raw/                    ← the messy Aurora Outfitters CSVs
│   └── docs/DATA_DICTIONARY.md
├── cheatsheets/               ← BLANK templates you fill from memory
├── resources/                 ← curated links & further reading
├── notebooks/                 ← revision checkpoints (every 3 topics)
├── projects/                  ← applied projects (each with a separate SOLUTION)
├── 01_Introduction_And_Data_Loading/
│   ├── lesson.ipynb  practice.ipynb  solutions.ipynb
├── 02_Series_And_DataFrames/
├── ...
└── 12_Capstone_Investigation/
```

## Curriculum map

| # | Topic | Investigation milestone |
|---|---|---|
| 01 | Introduction & Data Loading | Load every Aurora table; first look |
| 02 | Series & DataFrames | Building blocks; first revenue number |
| 03 | Selection, Filtering & Boolean Logic | Isolate suspicious orders |
| 04 | Data Cleaning & Missing Data | Fix dates, dupes, the double-counted channel |
| 05 | GroupBy & Aggregation | Revenue by month, channel, category |
| 06 | Merge / Join / Concat | Stitch the ecosystem together for true profit |
| 07 | DateTime & Time Series | Trends, seasonality, "is the dip real?" |
| 08 | String Operations & Text Data | Mine support tickets |
| 09 | Apply / Map / Transform | Engineer analyst features (fast) |
| 10 | Pivot Tables & MultiIndex | Build the management cross-tabs |
| 11 | Exploratory Analysis & Visualization | Turn findings into charts |
| 12 | Capstone Investigation | Deliver the final report |

## Requirements

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

Regenerate the datasets at any time:

```bash
python _build/gen_datasets.py
```

---

*NumPy note:* there is no separate NumPy course. NumPy is reinforced **inside**
every practice notebook — masking, vectorization, `np.where`/`np.select`,
`np.nan`, statistics and performance — with an extra recall checkpoint every 3
topics. Advanced performance / advanced Pandas are left for a post-course
extension.
