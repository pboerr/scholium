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

This plugin encodes what a good lecturer actually does instead: motivate before
defining, give the proof idea before the proof, hint at the smallest possible
rung, and — when marking work — distinguish *this step is false* from *this step
is true but you didn't justify it*, which are wildly different sentences that
students routinely hear as the same one.

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

Reads the whole proof first, then finds the **first** genuinely broken step
(everything downstream of a break is untrustworthy, so it doesn't itemise
consequences as separate findings). Every issue gets one of four labels:

- **invalid** — doesn't follow, or is false
- **unjustified** — probably true, but a gap; here's what closes it
- **imprecise** — right idea, the words don't say it
- **stylistic** — fine, but there's a better way

Plus a hypothesis-usage audit — an unused hypothesis means your proof is wrong,
or you've proved something stronger, and it's worth knowing which — and a
degenerate-case sweep.

It deliberately **does not rewrite your proof**, because the repair is the part
with the learning in it. It offers.

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

## Possible additions

A `qual-prep` skill — oral-exam drilling on definitions and theorem statements
under time pressure — is the obvious next one for graduate students. Not built
yet. Issues and PRs welcome.

## License

MIT
