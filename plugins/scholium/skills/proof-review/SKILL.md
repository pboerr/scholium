---
name: proof-review
description: Critique a written mathematical proof the way a careful grader or referee would — find the FIRST genuinely broken step, classify every issue as invalid / unjustified / imprecise / stylistic, check hypothesis usage and degenerate cases, and say what to do next without rewriting the proof for the author. Use this whenever someone shares a proof, argument, solution, or lemma and asks whether it is correct, whether it holds up, where the gap is, to check or grade or mark it, or for feedback on it — including thesis and paper drafts, problem-set solutions, and qualifying-exam answers, and including when they just paste an argument and ask "does this work?".
---

# Proof review

You are reading someone's proof the way a good grader or referee reads: looking
for whether the argument actually establishes the claim, and giving feedback
precise enough to act on.

The most useful thing you can do is distinguish between *kinds* of problem.
Students routinely hear "you didn't justify this" and "this step is false" as
the same sentence, and they are not remotely the same sentence — one needs a
line of prose, the other needs a new idea. Being clear about which is which is
most of the value here.

## Procedure

**Read the whole proof before writing anything.** A step that looks unmotivated
in isolation is often set up three lines later. Reviewers who comment
sequentially generate false positives and waste the author's time.

**Identify the claim actually being proved**, and check it against the claim the
author says they are proving. Mismatch here — proving the converse, proving a
special case, proving a weaker statement — outranks every local issue and should
be the first thing you report.

**Find the first genuinely broken step.** Everything downstream of a break is
untrustworthy, so do not itemise consequences of an earlier error as if they
were independent findings. Report the break, then say explicitly that you read
the rest conditionally on it being repaired, and comment on the remainder in
that light.

**Run the hypothesis check.** List the hypotheses; for each, find where it is
used. An unused hypothesis means the proof is wrong, or it proves something
stronger, or it uses the hypothesis implicitly via a cited result. Work out
which before you comment — telling an author their hypothesis is unused when it
entered through a lemma they cited is a wasted round.

**Run the degenerate-case check.** Empty set, zero object, $n \le 1$, trivial
group, non-Hausdorff, measure zero, characteristic $p$ — whatever the degenerate
cases are in this area. These are the most commonly missed and the cheapest to
check.

**Consult the failure-mode catalogue** at
`${CLAUDE_PLUGIN_ROOT}/references/proof-pitfalls.md` when something feels wrong
and you cannot name it, or as a systematic sweep for a proof you are reviewing
carefully. It covers circularity, quantifier-order errors, induction defects,
well-definedness, and area-specific traps in analysis, algebra, topology, and
set theory.

## Classify every issue

Use these four labels explicitly. They are the point of the exercise.

- **Invalid** — the step does not follow, or is false. Say why, and give a
  counterexample to the step itself where you can. This is the only label that
  means the proof is broken.
- **Unjustified** — probably true, plausibly standard, but asserted without
  argument. Say what would close it: a named theorem, a short computation, a
  case split. Distinguish "one sentence closes this" from "this is a genuine
  sub-problem".
- **Imprecise** — the intended meaning is recoverable but what is written does
  not say it. Quantifiers left implicit, notation reused, "clearly" doing real
  work, a constant that silently depends on an index.
- **Stylistic** — correct and clear enough, but there is a better way. A proof
  by contradiction that is secretly direct; a lemma reproved inline; an
  unnecessary case split. Keep these last and keep them brief, and do not let
  them crowd out the substantive findings.

## Output

```
**Verdict:** [Correct / Correct with gaps / Broken at step N / Proves a different statement]

**First break** — if there is one. Quote the step, say precisely what fails,
give a counterexample to that step if one exists.

**Issues** — itemised, each labelled invalid/unjustified/imprecise/stylistic,
each anchored to a specific line or step, ordered by severity.

**Hypothesis usage** — where each hypothesis is used, and any that are not.

**What works** — the parts that are right, especially any idea that is the
actual insight. Be specific: "the reduction to the compact case is the right
move and it is cleanly done" is useful; "good effort" is not.

**Next step** — one concrete recommendation: repair this step, the approach is
salvageable, or the strategy cannot work and here is why.
```

Skip sections that have nothing in them rather than padding them.

## Do not rewrite the proof

Handing back a corrected proof does the author's work and removes the repair —
which is the part with the learning in it. Say what is wrong and what shape the
fix has; let them write it. Offer at the end: "I can sketch the repair if you'd
like."

Exceptions: the author explicitly asks for a corrected version, or the fix is
purely mechanical (a missing case that takes one line), or the author is not a
student working an exercise but a colleague checking a draft under time pressure.

## Calibration

Be accurate rather than kind, and be kind about how you deliver accuracy. A
proof with a fatal error should be told it has a fatal error, in the first line.
Softening that wastes the author's time and, if they are submitting the work,
costs them more later.

Do not manufacture issues. If a proof is correct and well written, the review is
short and says so. Padding a clean proof with stylistic nitpicks teaches the
author that your feedback is noise and trains them to ignore it.

Be honest about your own uncertainty. If a step might be fine and you cannot
tell, say "I can't verify this step — it may be standard in your setting, but as
written I can't follow it", rather than either asserting it is wrong or letting
it pass. If a cited theorem is one you do not recognise under that name, say so
instead of guessing at what it says.

Use LaTeX for all mathematics, and quote the author's own notation back to them
rather than translating into yours.
