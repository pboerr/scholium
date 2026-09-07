# Catalogue of proof failure modes

A checklist for reading a proof adversarially. Not every item applies to every
proof — run down it looking for the ones that bite.

## Contents

- [Logical structure](#logical-structure)
- [Quantifiers](#quantifiers)
- [Hypothesis usage](#hypothesis-usage)
- [Induction](#induction)
- [Degenerate and edge cases](#degenerate-and-edge-cases)
- [Analysis-flavoured errors](#analysis-flavoured-errors)
- [Algebra-flavoured errors](#algebra-flavoured-errors)
- [Topology-flavoured errors](#topology-flavoured-errors)
- [Set theory and foundations](#set-theory-and-foundations)
- [Writing problems that are not errors](#writing-problems-that-are-not-errors)

## Logical structure

**Circularity.** The proof uses the statement it is proving, or a result whose
own proof depends on it. The disguised form is the dangerous one: invoking a
named theorem that is itself a corollary of the target. Always ask what the
cited result's proof depends on.

**Proving the converse.** The student assumes the conclusion and derives the
hypothesis. This is very common when the write-up starts from the goal and works
backwards without saying so. Backwards work is fine as *discovery*; the write-up
must be reversible and stated in the forward direction, or every step must be
explicitly an equivalence.

**Affirming a one-directional implication.** Given $P \Rightarrow Q$ and $Q$,
concluding $P$. Often hides inside a chain where one link is only an implication
but the surrounding argument treats the chain as equivalences.

**Contrapositive vs. converse confusion** in proofs by contraposition — negating
only part of a compound statement, most often mishandling the negation of an
implication or of a conjunction.

**Contradiction that never contradicts.** A proof by contradiction that derives
something merely surprising, or that derives a contradiction with an assumption
introduced later in the argument rather than with the negated conclusion. Also:
proofs by contradiction that are secretly direct proofs — not an error, but worth
flagging, since the direct version is clearer.

**Assuming a specific case.** "Let $x$ be a limit point of $A$" when the argument
must cover $A$ with no limit points; "consider the largest element" when the set
may be infinite or empty; picking a basis when the space may be infinite-dimensional.

**"WLOG" that loses generality.** A genuine WLOG needs a symmetry or a reduction
argument that maps the general case to the assumed one. If the reduction is not
stated and is not obvious, the WLOG is a gap. Frequent offender: "WLOG $a \le b$"
in a situation where the roles of $a$ and $b$ are not actually symmetric.

## Quantifiers

**Order swap ($\forall\exists$ vs $\exists\forall$).** The single most common
serious error in analysis. Pointwise convergence vs. uniform convergence,
pointwise continuity vs. uniform continuity, "for each $\varepsilon$ there is an
$N$" vs. "there is an $N$ for each $\varepsilon$". Diagnostic: check whether the
witness ($N$, $\delta$, the index) is allowed to depend on the universally
quantified variable, and whether the proof silently makes it independent.

**Dependence smuggled in later.** $\delta$ is chosen before $x$ but the formula
for $\delta$ mentions $x$. Read the order of introduction literally.

**Negation errors.** The negation of $\forall x \exists y\, P(x,y)$ is
$\exists x \forall y\, \neg P(x,y)$. Students often keep the quantifier order
or forget to negate all the way in.

**Vacuous or unbounded quantification.** A statement quantified over an empty set
is true and proves nothing; a variable used outside the scope where it was bound.

## Hypothesis usage

**An unused hypothesis is a red flag, not a bonus.** If the proof never uses
compactness, or never uses that the ring is commutative, exactly one of these
holds:

1. The proof is wrong and the hypothesis was needed at a step that was skipped.
2. The proof is right and proves something strictly stronger.
3. The hypothesis was used implicitly through a cited theorem.

Case 3 is fine but should be made explicit. Case 2 is worth celebrating and
worth stating. Case 1 is the usual reality. Determine which before commenting.

**A hypothesis used at the wrong strength.** Using continuity where uniform
continuity is needed; using "measurable" where "integrable" is needed; using
finite generation where Noetherian is needed.

**Silent extra hypotheses.** The proof assumes without saying so that a set is
nonempty, a function is nonzero, a group is finite, a space is Hausdorff, a
measure is $\sigma$-finite, a module is free, an index set is countable.

## Induction

- **Missing or wrong base case**, or a base case that does not match where the
  inductive step starts working. The step often silently requires $n \ge 2$.
- **The inductive hypothesis is never used.** If it is not used, either the
  statement is provable directly or the step is wrong.
- **Weak induction where strong induction is needed** — the step reaches back to
  $k < n$ rather than $n-1$ only.
- **Induction over the wrong set** — over the reals, or over a set with no
  well-ordering, or a "downward" induction with no least element.
- **Quantifier inside the induction.** Inducting on a statement whose constants
  ($\varepsilon$, $C$, $\delta$) are allowed to change with $n$, producing a
  bound that degrades and is worthless in the limit.

## Degenerate and edge cases

Standard omissions: the empty set; $n = 0$ or $n = 1$; the trivial group, ring,
or vector space; the zero vector, zero polynomial, zero ideal; the zero map;
a single point; the empty product or empty sum; the whole space as a subspace;
$p = 1$ or $p = \infty$ in $L^p$; characteristic $2$ or characteristic $p$;
the non-orientable case; measure-zero sets; the improper ideal; graphs with no
edges.

## Analysis-flavoured errors

- **Interchanging limits, sums, integrals, or derivatives** with no justification.
  Name the theorem: dominated convergence, monotone convergence, Fubini–Tonelli,
  uniform convergence, Weierstrass M-test. "Clearly we may exchange" is a gap.
- **Assuming a limit exists** before proving it does — including implicitly, by
  writing $\lim a_n$ and manipulating it.
- **Dividing by a quantity not shown to be nonzero**; taking $\log$ or a square
  root of something not shown positive; inverting a matrix or operator not shown
  invertible.
- **Losing uniformity in a limit** — a constant $C_n$ or $\delta_n$ that depends
  on the index and is then used as if uniform.
- **Convergence of a subsequence** presented as convergence of the sequence.
- **Sup/inf treated as max/min** — assuming the supremum is attained.
- **Term-by-term differentiation** of a series with only pointwise convergence.
- **Confusing pointwise, uniform, $L^p$, almost-everywhere, and in-measure
  convergence**, or asserting an implication between them that requires extra
  hypotheses (finite measure, domination, a subsequence).
- **Boundedness vs. compactness** in infinite dimensions — closed and bounded
  does not give compact outside finite dimensions.

## Algebra-flavoured errors

- **Well-definedness of a map on a quotient.** Any map defined by a choice of
  representative needs a well-definedness check. This is the most-skipped
  obligation in a first algebra course and it does not stop being skipped later.
- **Assuming commutativity** of a ring, group, or of composition; assuming
  a ring has a unit; assuming an integral domain.
- **Confusing normal subgroups with subgroups** when forming quotients; confusing
  ideals with subrings.
- **Assuming a basis exists constructively** in infinite dimensions (this needs
  choice/Zorn) or that every module is free.
- **Order of composition** in a group action or in matrix–map correspondence;
  row vs. column convention silently swapped.
- **Cardinality arguments that assume finiteness** — counting arguments, "an
  injective endomorphism is surjective" (true for finite-dimensional spaces and
  finite sets, false generally).
- **Characteristic assumptions** — dividing by $2$ or by $n!$, using that a
  polynomial's derivative detects repeated roots, assuming separability.

## Topology-flavoured errors

- **Sequences where nets are needed** — sequential compactness, sequential
  continuity, and sequential closure are not the general notions outside
  first-countable spaces.
- **Assuming Hausdorff** — uniqueness of limits, compact implies closed, and the
  closedness of the diagonal all need it.
- **Confusing "closure of the interior" with "interior of the closure"**, or
  assuming the boundary behaves like a set difference of the naive kind.
- **Assuming a continuous bijection is a homeomorphism** without compactness plus
  Hausdorff, or without an explicit inverse.
- **Confusing connectedness with path-connectedness** in either direction.
- **Local vs. global** — a locally constant function is constant only on connected
  components; a local homeomorphism is not a homeomorphism.
- **Product topology vs. box topology** on infinite products.

## Set theory and foundations

- **Silent use of the axiom of choice** — choosing an element from each of
  infinitely many sets, well-ordering, Zorn's lemma, "pick a basis", "pick a
  representative from each equivalence class". Not an error, but should be named.
- **Cardinal arithmetic assumed to behave like finite arithmetic** — cancellation,
  or $|A| < |B|$ from a proper inclusion.
- **Unrestricted comprehension** — forming "the set of all sets such that ..."
  without a bounding set.
- **Confusing a class with a set.**
- **Recursion without a well-founded relation.**

## Writing problems that are not errors

Distinguish these from actual defects, and say which you are flagging:

- A step that is true and standard but has no justification written down. This is
  a **gap**, not an error — the fix is a sentence, not a new idea.
- Notation introduced without definition, or reused for two different objects.
- Undischarged "it suffices to show" — a reduction claimed and then never used,
  or used in the wrong direction.
- A proof that is correct but three times longer than necessary because it
  reproves a standard lemma inline.
- Missing statement of what is being proved at the point of proving it, so the
  reader cannot check the logic against a target.
