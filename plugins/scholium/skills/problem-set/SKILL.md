---
name: problem-set
description: Generate practice problems and problem sets for proof-based mathematics, at a chosen difficulty ladder, with every problem verified solvable before it ships and solutions kept separate so the student can work first. Use this whenever someone asks for practice problems, exercises, a problem set, review questions, qualifying-exam practice, or "give me something to work on" for a mathematical topic; also when they want harder or easier variants of a problem they already have, or want to drill a specific technique. Prefer this over inventing exercises ad hoc, since it enforces verification and includes formats — find-the-error, prove-or-disprove — that build proof skill and are otherwise easy to forget.
---

# Problem sets

Generating exercises for proof-based mathematics has one dominant failure mode:
producing problems that are false, vacuous, wildly harder than intended, or
accidentally open. A student who spends four hours on a generated problem that
has no elementary proof has been actively harmed — and cannot tell whether the
fault is theirs.

So the central discipline here is: **solve every problem before you ship it.**

## Verify before shipping

For each candidate problem, work the solution through internally to the point
where you are convinced a correct proof exists at roughly the level intended.
Then:

- **If you cannot solve it, cut it.** Not "mark it hard" — cut it. A problem you
  cannot prove may be false or may be a research question.
- **If the solution turned out much harder than intended**, either relabel its
  difficulty honestly or add the hypothesis that tames it.
- **If it turned out trivial or vacuous** — the hypotheses are contradictory, or
  the conclusion follows immediately from a definition — cut or strengthen it.
- **If it depends on a result the student has not met**, say which result it
  needs, or replace it.

Check the degenerate cases of your own problems too. A statement that fails for
the empty set or $n = 0$ needs its hypotheses fixed before it goes out.

**The same discipline applies to everything you write around the problems.**
Solutions, hints, and the remarks explaining why a hypothesis matters or what a
flawed proof would imply are all mathematical assertions, and they reach the
student as authoritative. They are also read less carefully than the problem
statements — by you when writing them and by the student when reading them —
which is exactly why an error there is more likely to be absorbed uncorrected.
A throwaway line like "this argument would prove something far too strong to be
true" is a claim, and it needs checking like any other.

This covers examples you name in passing. "A second standard example is the
Sorgenfrey line" is a claim about the Sorgenfrey line, and a decorative aside
propping up no argument is exactly where an unverified name slips through —
nothing downstream depends on it, so nothing forces you to check it. Confirm the
object really has the property you are attributing to it, or cut the aside; a
named example the student then looks up and finds wrong costs you more than the
aside was ever worth.

The asides you are most confident about are the ones to check, since those are
the ones you will not have worked through.

Prefer adapting well-known exercises whose difficulty you can actually judge over
inventing novel ones. Novelty is not a virtue in a problem set; calibration is.

## Structure of a set

Unless asked otherwise, build a ladder — students need to succeed at something
early or they stop:

1. **Warm-ups** (2–3). Directly exercise a definition. Can the student
   *use* the definition, not just recite it? These should take minutes.
2. **Core** (3–4). The standard techniques of the topic, one technique each,
   in the form they will meet on an exam.
3. **Stretch** (1–2). Combine two ideas, or require a construction, or need a
   non-obvious first move.
4. **Exploration** (0–1, optional). Open-ended: generalise, find the sharp
   constant, ask what happens without a hypothesis. No single expected answer.

## Include these formats

Ordinary "prove that X" problems are necessary but they train only one move.
Include at least one of each of these in any set of six or more, because they
build the skills that separate a student who can follow proofs from one who can
write them:

**Prove or disprove.** State something that may be true or false and require a
proof or a counterexample. Real mathematics does not come pre-labelled as true,
and a student who has only ever been handed true statements has never practised
the most important judgement there is. Make sure some are false.

**Find the error.** Present a plausible-looking proof of something — either false,
or true but proved invalidly — and ask the student to locate the first broken
step and say what kind of break it is. Draw the error from
`${CLAUDE_PLUGIN_ROOT}/references/proof-pitfalls.md`; a quantifier-order swap or
an unjustified limit interchange is far more instructive than an arithmetic slip.
Make the flawed proof genuinely plausible — an obvious error teaches nothing.

**Construct an example.** "Give a space that is X but not Y." These force
engagement with what the definitions actually exclude, and they are how students
build the mental library of counterexamples they will use for years.

## Presentation

Number problems, and for each one give:

- The statement, in LaTeX, precise about all quantifiers and hypotheses.
- A difficulty marker and a rough time estimate. Be honest — an underestimate is
  demoralising in a specific and avoidable way.
- Which named results the problem expects them to use, if it is not obvious.
  This is not a hint; it is telling them which chapter they are in.
- Optionally a hint, written to reveal the *class* of approach rather than the
  move — and placed so it is not read by accident.

**Keep solutions separate.** Put them in a clearly marked section after the
problems, or in a separate file, or offer them on request. A student who can see
the solution while reading the problem will read the solution. If you are writing
files, `problems.md` and `solutions.md` is the right split.

Write full solutions, not sketches — they are the answer key, and a gap in the
key is worse than useless when a student is checking their own work against it.
Where a problem has an instructive alternative proof, mention it.

## Calibration

Ask what course or book they are working from, or what they have covered, if it
is not clear — the same topic sits at wildly different levels in a first course
and a graduate one, and "prove the open mapping theorem" is a reasonable exercise
in one context and absurd in another. One question, then build.

Match the conventions of their source: notation, whether measure theory is
available, whether they are allowed to cite a given theorem or expected to prove
it. If they are preparing for a specific exam, mirror its format and its
characteristic problem types.
