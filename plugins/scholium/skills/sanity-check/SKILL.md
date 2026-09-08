---
name: sanity-check
description: Test a mathematical claim computationally before trying to prove it — enumerate small and degenerate cases, hunt for a counterexample, and report honestly what was searched. Use this whenever someone asks whether a statement is true, says "I think this holds but I'm not sure", wants a conjecture checked, is about to spend real effort proving something, needs to confirm a problem or exercise is actually true before handing it to a student, or has a claimed counterexample that should be verified. Reach for it BEFORE proving or disproving anything where small cases are computable — thirty seconds of enumeration routinely settles what an hour of proof attempts would not, and a claim that dies on a two-element example should die before anyone writes a lemma about it.
---

# Sanity check

Before proving a statement, try to break it. Most false conjectures die on a
small case, and finding that case costs seconds where a proof attempt costs an
hour and produces nothing when the statement is false. This applies just as much
to the statements *you* are about to assert — a problem you are shipping to a
student, a counterexample you are about to cite, an aside claiming some standard
space has some property.

The output is evidence, never proof. Everything below is about keeping that
distinction honest, because a computational check that overstates itself is
worse than none: it converts "I don't know" into false confidence.

## Use the bundled harness

`scripts/probe.py` is pure standard library — no sympy, numpy or networkx, which
are frequently absent. It provides `search` (reports the extent of what was
checked, not just a verdict), `must_fail` (the poison test below), and
enumerators for small groups, graphs, topologies, subsets, functions, matrices
and exact rationals. Each case list says whether it is **exhaustive**, and
`search` repeats that in its report — "all 355 topologies on 4 points" and "a
hand-built library of 13 groups" are different evidence, and a partial family
that reports like a complete one is the most dangerous thing in the box. The
group library is called `some_groups` for that reason.

```python
from probe import search, must_fail, some_groups, graphs, topologies

print(search(lambda G: G.is_abelian(), some_groups(8), "all finite groups are abelian"))
# [all finite groups are abelian] FALSE - counterexample after 9 cases: D_3
```

Import it rather than rewriting it. If a library like sympy *is* available and
would help, use it — just check first rather than assuming, and fall back to the
harness when the import fails.

`references/recipes.md` has worked patterns per area — algebra, graphs, topology,
linear algebra, number theory, inequalities — including which claims in each area
are not decidable this way.

## Make the test able to fail

This is the discipline that matters most, and the one people skip. The dominant
way computational checking misleads is not a wrong answer; it is a predicate
that is accidentally vacuous — a quantifier encoded backwards, a filter that
empties the case list, a condition that is trivially satisfied — which then
passes every search in silence and reads as confirmation.

So before believing a green result, feed the predicate something you *know*
violates it and confirm it says so. `must_fail` does exactly this and raises if
nothing is caught:

```python
must_fail(my_property, family_containing_a_known_violation, "poison test")
```

An exception inside a predicate is reported as a broken harness rather than a
passing case, for the same reason.

## Search where counterexamples actually live

**Degenerate cases first.** The empty set, $n = 0$ and $n = 1$, the trivial
group, the zero matrix, the one-point space, the empty graph, the constant
function. This is where most false statements break, and random sampling never
visits any of it.

**Then exhaustive small.** All groups up to order 8, all graphs on 5 vertices,
all topologies on 4 points. Exhaustive beats random at small sizes because it
cannot miss the sparse case.

**Then structured large**, only if the small search survives, and chosen to
stress whatever the statement is about rather than sampled uniformly.

**Say where you stopped, and whether that was enough.** If the smallest possible
counterexample could sit at $n = 6$ and you searched to $n = 4$, your green
result means nothing and reporting it as reassurance is the failure mode this
skill exists to prevent. Estimate where a counterexample could first appear; if
you cannot reach it, say the search was inadequate rather than implying it
passed.

## Arithmetic

Use exact arithmetic for anything involving equality — `fractions.Fraction`,
integers, symbolic values. Two floats that agree to fifteen places are not
equal, and floating-point noise produces both false counterexamples and false
confirmations. The harness's `rationals()` yields exact values for this reason.

Floats are fine for strict inequalities with a real margin, and for orders of
magnitude. If a claimed inequality is tight, exact arithmetic or nothing.

## When computation cannot decide it

Say so plainly rather than testing a proxy that is not the claim. Computation
does not settle statements quantified over all reals or all groups, asymptotic
claims, non-constructive existence, or anything about objects you cannot
represent finitely. Checking $n \le 10$ says nothing about a claim for all $n$
unless you have a separate argument bounding where a counterexample must appear.

Testing a weaker computable statement is legitimate and often useful — but name
the substitution. "I checked the finite-dimensional case" is honest; letting it
stand as a check of the general claim is not.

## Everything you assert gets the same treatment

The result is not the only claim in your reply. The redirect — "the true theorem
nearby is…", "what you should prove instead is…", the suggested exercise, the
attribution — are claims too, and they are the ones you will state from memory
because the computation is already done and the interesting part feels finished.

An early version of this skill correctly refuted a student's conjecture, found
the minimal counterexample by exhaustive search, and then handed them a false
theorem to spend the evening on instead — a statement its own counterexample
refuted, four lines further up. Saving someone's evening and then misdirecting it
is not a win. Check the redirect before you send it, or say plainly that you are
recalling rather than checking.

## Reporting

**If a counterexample is found** the matter is settled: the statement is false.
Minimise it — the smallest counterexample is the one that shows *why* — and give
it explicitly enough to verify by hand. Then say which hypothesis, if added,
would exclude it, since that is usually the repair.

**If nothing is found**, report the extent and stop short of endorsement:

> No counterexample among all 1044 graphs on ≤ 5 vertices, all groups of order
> ≤ 8, and the degenerate cases. That is evidence the statement is true; it is
> not a proof, and the smallest counterexample to a statement of this shape
> could easily live past where I searched.

Never write "verified", "confirmed" or "proven" about a finite search.

## Related skills

- `problem-set` requires every problem to be solvable before it ships; this is
  the tool for the "is it even true?" half of that check.
- `proof-review` — when a proof cites a counterexample or claims some standard
  object has a property, this settles it rather than trusting recall.
