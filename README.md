# Scholium

A Claude Code plugin that behaves like a university mathematics instructor for
proof-based work — upper-division and graduate analysis, algebra, topology,
geometry, logic, probability, combinatorics.

A *scholium* is a note written in the margin beside a proposition — the form the
commentary takes in the manuscripts of Euclid and in Newton's *Principia*. It
explicates, qualifies, and points out where an argument is doing more work than
it appears to. It does not replace the proposition.

That is the design constraint. This plugin annotates your mathematics; it tries
hard not to do your mathematics for you.

## Why this exists

Claude will happily solve your problem set. That is the problem. The moment of
finding the idea is the moment the learning happens, and there is exactly one of
those per exercise — an answer handed over early doesn't just spoil the problem,
it consumes the only repetition you were going to get at that move.

This plugin encodes what a good lecturer does instead: motivate before defining,
give the proof idea before the proof, hint at the smallest possible rung, and —
when marking work — distinguish *this step is false* from *this step is true but
you didn't justify it*, which are wildly different sentences that students
routinely hear as the same one.

One thing these skills do **not** do is make Claude better at mathematics. That
was measured rather than assumed (see [Evidence](#evidence)), and the model
finds subtle errors, motivates theorems, and builds counterexamples perfectly
well unaided. What it will not do on its own is withhold. Left alone it solves
the problem you were working, writes out the proof you were about to repair, and
puts the solutions in the same file as the exercises. Every skill here is an
override of a default that is helpful in general and wrong for a student.

## Install

```
/plugin marketplace add pboerr/scholium
/plugin install scholium@scholium
```

Or from the command line:

```bash
claude plugin marketplace add pboerr/scholium
claude plugin install scholium@scholium
```

The skills trigger on their own from context — you don't need to invoke them by
name. Ask a question about a theorem and you get the lecture treatment; paste a
proof and ask if it holds up and you get the review treatment.

## The four skills

### `lecture` — explain the material

Motivation first (the question this answers, or what breaks without it), then
the definition with examples *and non-examples*, then the statement with its
quantifiers read out loud, then **the proof idea in plain words before the
proof**, then the proof with each hypothesis marked where it enters — and
finally what breaks when you delete each hypothesis.

That last part is the one nothing else does, and it's what turns a memorised
theorem into an understood one.

> *"why is the closed graph theorem true, I can follow the proof but I don't see
> where completeness is doing the work"*

### `office-hours` — get unstuck without being told

Diagnoses *what kind of stuck you are* before hinting, because the right
intervention is completely different for each:

| Stuck type | What it looks like | What it gets |
|---|---|---|
| Doesn't understand the statement | restating it wrong, proving the converse | no hint at all — asked to restate the goal |
| No entry point | blank page | redirect to the *shape* of the conclusion |
| Plan is fine, one step is stuck | structure with a hole | confirmation the plan works + a local nudge |
| Plan won't work | plausible but doomed | asked to test it on the case where it fails |
| Already solved it, doesn't believe it | correct but hedged | told plainly that it works |

Then a six-rung hint ladder, one rung at a time — from *restate the target* and
*you haven't used compactness anywhere* up to naming the technique, and only at
the very top, after real effort, the key idea. It also knows when to just answer:
if you've been at it two hours and ask directly, being withholding is its own
failure.

> *"stuck on showing this operator is compact, here's what I have so far…"*

### `proof-review` — critique what you wrote

This one is deliberately thin, because testing showed the model already finds
the error. It contains no detection procedure at all. What it enforces:

**It does not rewrite your proof.** Without the skill, Claude diagnoses the
break and then writes out the corrected argument — on one test it did so twice
in a single reply, leaving nothing for the author. The skill points at the route
and stops. If you want the repair, you ask.

**Every issue gets one of four labels** — **invalid** (doesn't follow, or is
false), **unjustified** (probably true, but a gap), **imprecise** (right idea,
wrong words), **stylistic**. Only the first means your proof is broken. Without
labels a review reads as an undifferentiated list of complaints.

**A guarded hypothesis audit.** An unused hypothesis means your proof is wrong or
proves something stronger. But the skill forbids saying "unused" until implicit
use has been searched for — inside a cited theorem, inside an existential you
wrote down, inside an unstated convergence assumption. An earlier version
declared a hypothesis unused when the proof spent it implicitly, which is a
false finding that sends you hunting for an error that isn't there.

**No padding on a correct proof.** At most one item below "unjustified".

> *"does this argument hold up? [pasted lemma from a thesis draft]"*

### `problem-set` — practice that isn't fake

Generates exercises on a ladder (warm-up → core → stretch → open-ended), with
one hard rule: **every problem is solved before it ships**. Generated problems
that turn out false, vacuous, or accidentally open are actively harmful, because
a student can't tell whether the fault is theirs. If it can't be solved, it's
cut, not labelled hard.

Includes formats that build proof skill and are otherwise easy to forget:
*prove or disprove* (some of them false — real mathematics doesn't come
pre-labelled), *find the error* in a plausible proof, and *construct an example*
that is X but not Y.

Solutions go in a separate file. If you can see them while reading the problem,
you'll read them.

> *"give me some practice on quotient topologies, I have quals in three weeks"*

## The pitfalls catalogue

`plugins/scholium/references/proof-pitfalls.md` is a shared reference the
review, hints, and problem-generation skills all draw on: circularity and its
disguised forms, ∀∃ vs ∃∀ order swaps, induction defects, WLOG that loses
generality, well-definedness on quotients, silent uses of choice, and
area-specific traps across analysis, algebra, topology, and set theory.

It's useful on its own as a checklist for reading your own work adversarially.

## Repository layout

```
scholium/
├── .claude-plugin/marketplace.json
└── plugins/scholium/
    ├── .claude-plugin/plugin.json
    ├── references/proof-pitfalls.md
    └── skills/
        ├── lecture/SKILL.md
        ├── office-hours/SKILL.md
        ├── proof-review/SKILL.md
        └── problem-set/SKILL.md
```

To use a single skill without the plugin, copy its directory into
`.claude/skills/` in your project (the ones referencing
`${CLAUDE_PLUGIN_ROOT}/references/proof-pitfalls.md` will need that file's path
adjusted).

## Evidence

Each skill was run against realistic prompts alongside a baseline — the same
prompt with no skill loaded — and both were graded blind against assertions
fixed in advance, with a separate pass re-proving the mathematics independently.

| Test | With skill | Baseline |
|---|---|---|
| office-hours — stuck on a qual problem | **5/5** | **1/5** |
| office-hours — asked outright after three hours | **5/5** | **3/5** |
| lecture — closed graph theorem, no leading question | **6/6** | **5/6** |
| proof-review — false claim, memorised error | 6/6 | 5/6 |
| proof-review — true claim, invalid proof | 6/6 | 5/6 |
| proof-review — valid proof (false-positive control) | 5/5 | 5/5 |
| problem-set — five compactness problems | 5/5 | 5/5 |

Read the small numbers, not the average. `office-hours` is the one with a large,
repeatable gap, and it is the skill asking for the behaviour the model least
wants to produce. `problem-set` shows **no measured gap at all** — its real
difference (solutions in a separate file, truth values withheld from the
student) is something the rubric never learned to see, and the baseline
satisfies "every problem is true" effortlessly by choosing five canonical
theorems.

Across three separate proof-review tests, the **baseline never once missed the
error or misjudged whether the claim was true**, including on a non-famous flaw
and on a correct proof. That result is why the skill contains no detection
instructions.

Two real defects were found in the skills' own output and fixed:

- `problem-set` shipped a solutions file asserting that a flawed proof would
  imply "every Hausdorff space in which closed sets are compact is normal" and
  called that far too strong. Such a space *is* compact Hausdorff. The skill now
  requires commentary to be verified like problem statements.
- `proof-review` declared a hypothesis unused when the proof spent it implicitly.
  The skill now forbids "unused" until implicit use has been ruled out.

Honest limits: one run per cell, one model, a handful of prompts, and rubrics
written by the same person who wrote the skills. These numbers show direction,
not effect size. The raw runs and grading are not in this repo.

## Possible additions

A `qual-prep` skill — oral-exam drilling on definitions and theorem statements
under time pressure — is the obvious next one for graduate students. Not built
yet. Issues and PRs welcome.

## License

MIT
