"""Shared builder for the practice-first restructure.

Per topic we now produce ONLY: lesson.ipynb, practice.ipynb, solutions.ipynb.
Practice notebooks follow a fixed spaced-repetition structure:
  Warm-Up Recall -> Core Lesson Tasks -> Mixed Review -> Data Detective
  -> Interview Lens -> Reflection
60% current topic / 40% earlier topics; >=1 NumPy task each; no answers in
warm-up / interview / reflection.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbutil import build_notebook

ROOT = os.path.join(os.path.dirname(__file__), "..")


def convert_lesson(topic_dir):
    """lesson.md -> lesson.ipynb (markdown cells split on '## ' headings)."""
    d = os.path.join(ROOT, topic_dir)
    src = os.path.join(d, "lesson.md")
    if not os.path.exists(src):
        return
    text = open(src, encoding="utf-8").read()
    # split keeping the heading with its section
    parts = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    cells = [("md", p.strip()) for p in parts if p.strip()]
    build_notebook(cells, os.path.join(d, "lesson.ipynb"))
    os.remove(src)


def _section(title, body=""):
    return ("md", f"## {title}\n\n{body}".rstrip())


def build_practice_solutions(spec):
    """spec is a dict — see topic files. Writes practice.ipynb & solutions.ipynb."""
    d = os.path.join(ROOT, spec["dir"])
    n = spec["num"]
    title = spec["title"]

    # ---------- practice ----------
    p = []
    p.append(("md", f"# Topic {n} — Practice: {title}\n\n"
              "**The notebook is the lesson.** Work top to bottom. Cells with `assert` grade "
              "themselves — a silent run = pass, an `AssertionError` = fix your code. "
              "Warm-Up, Interview Lens and Reflection have **no answer key** — answer in writing.\n\n"
              "_Spaced repetition: ~60% of this notebook is the current topic, ~40% revisits earlier topics._"))
    p.append(("code", spec["boot"]))

    p.append(_section("🔁 Warm-Up Recall (earlier topics — no answers given)", spec["warmup_md"]))
    if spec.get("warmup_code"):
        p.append(("code", spec["warmup_code"]))

    p.append(_section("🎯 Core Lesson Tasks (current topic)", spec.get("core_intro", "")))
    for c in spec["core"]:
        p.append(("md", c["md"]))
        p.append(("code", c["task"]))

    p.append(_section("🔀 Mixed Review Tasks (earlier topics — spaced repetition)",
                      spec.get("mixed_intro", "")))
    if spec["mixed"]:
        for m in spec["mixed"]:
            p.append(("md", m["md"]))
            p.append(("code", m["task"]))
    else:
        p.append(("md", "_This is Topic 01 — no earlier material yet. Your warm-up above is the "
                  "NumPy prerequisite recall._"))

    p.append(_section("🕵️ Data Detective Investigation", spec["detective_md"]))
    p.append(("code", spec["detective_task"]))

    p.append(_section("🔎 Interview Lens (write answers — no model answers)", spec["interview_md"]))
    p.append(_section("✍️ Reflection (write short explanations)", spec["reflection_md"]))

    build_notebook(p, os.path.join(d, "practice.ipynb"))

    # ---------- solutions ----------
    s = []
    s.append(("md", f"# Topic {n} — Solutions: {title}\n\n"
              "*Reference solutions for the objective tasks. Try the practice first.* "
              "The Warm-Up concept questions, Interview Lens and Reflection have **no key** — by design."))
    s.append(("code", spec.get("boot_sol", spec["boot"])))
    if spec.get("warmup_sol"):
        s.append(("md", "### Warm-Up — NumPy recall (self-check)"))
        s.append(("code", spec["warmup_sol"]))
    s.append(("md", "### Core lesson tasks"))
    for c in spec["core"]:
        s.append(("code", c["sol"]))
    if spec["mixed"]:
        s.append(("md", "### Mixed review (earlier topics)"))
        for m in spec["mixed"]:
            s.append(("code", m["sol"]))
    s.append(("md", "### Data detective"))
    s.append(("code", spec["detective_sol"]))
    if spec.get("interview_notes"):
        s.append(("md", "### Interview Lens — discussion points (not full answers)\n" + spec["interview_notes"]))
    build_notebook(s, os.path.join(d, "solutions.ipynb"))
    print("rebuilt", spec["dir"])


def cleanup_topic(topic_dir):
    """Remove quiz.md and challenge.md from a topic folder."""
    d = os.path.join(ROOT, topic_dir)
    for f in ("quiz.md", "challenge.md"):
        fp = os.path.join(d, f)
        if os.path.exists(fp):
            os.remove(fp)
