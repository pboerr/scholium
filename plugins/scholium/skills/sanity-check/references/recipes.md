# Probing recipes by area

Every snippet assumes `from probe import *` with `scripts/` on the path, and
every one has been run. Each section ends with what computation **cannot**
settle in that area — check that before reaching for code.

## Contents

- [Finite groups](#finite-groups)
- [Graphs](#graphs)
- [Topology](#topology)
- [Linear algebra](#linear-algebra)
- [Number theory](#number-theory)
- [Inequalities and analysis](#inequalities-and-analysis)
- [Combinatorial identities](#combinatorial-identities)

## Finite groups

`some_groups(order_max)` returns a hand-built library — cyclic, dihedral, symmetric,
alternating, $Q_8$, and small products. It is deliberately **not** named `groups`: it does not contain every group of
every order, `search` will say so in its report, and a survival over it is much
weaker evidence than a survival over an exhaustive family. If the claim is about
a specific order, build those groups yourself and check each with `is_valid()`.

```python
# "a group where every non-identity element has order 2 is abelian"  (true)
def prop(G):
    e = G.identity()
    if any(x != e and G.element_order(x) != 2 for x in G.elements):
        return True                      # hypothesis fails, nothing to test
    return G.is_abelian()
print(search(prop, some_groups(8), "exponent 2 implies abelian"))
```

Note the shape: a conditional claim returns `True` when the hypothesis fails.
That is also exactly how a predicate goes vacuous — if no case in your family
satisfies the hypothesis, everything passes and you have learned nothing. Run
`must_fail` against a family that does satisfy it, or count the cases that
reached the conclusion.

**Cannot settle:** anything about infinite groups, or a claim for all finite
groups when your library covers a dozen. Small-order searches miss phenomena
that first appear at order 16 or 32.

## Graphs

`graphs(n)` yields every labelled simple graph on `{0..n-1}` as a frozenset of
edges — 64 for $n = 4$, 1024 for $n = 5$, 32768 for $n = 6$ (still seconds).

```python
def connected(edges, n):
    adj = {v: set() for v in range(n)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in adj[v] - seen:
            seen.add(w); stack.append(w)
    return len(seen) == n

# "every connected graph on n vertices has at least n-1 edges"  (true)
print(search(lambda g: not connected(g, 5) or len(g) >= 4, graphs(5),
             "connected implies >= n-1 edges"))
```

Labelled enumeration counts isomorphic copies many times over. That is wasteful
but never wrong — and for finding a counterexample, wasteful is fine.

**Cannot settle:** claims about all graphs, or about large sparse structure.
Many graph statements have smallest counterexamples past $n = 7$, beyond
exhaustive reach.

## Topology

`topologies(n)` yields every topology on `{0..n-1}`: 29 for $n = 3$, 355 for
$n = 4$, 6942 for $n = 5$. Finite spaces settle far more separation-axiom and
connectedness questions than people expect.

```python
def is_T1(tau, n):
    return all(frozenset(range(n)) - {x} in tau for x in range(n))

def is_discrete(tau, n):
    return len(tau) == 2 ** n

# "T1 implies discrete" - true for FINITE spaces only, and worth knowing
print(search(lambda t: not is_T1(t, 4) or is_discrete(t, 4), topologies(4),
             "T1 implies discrete (finite)"))
```

**Cannot settle:** anything where the interesting behaviour is infinite —
compactness beyond the trivial, metrisability, the Sorgenfrey line, the long
line. Every finite topological space is compact, so a finite search will
"confirm" compactness claims that are false in general. This is the single most
misleading area to probe naively.

## Linear algebra

`matrices(n, entries)` enumerates $n \times n$ matrices over a small entry set.
Work over $\mathbb{Z}$ or $\mathbb{Z}/p$ with exact integers, never floats.

```python
def matmul(A, B, p=None):
    n = len(A)
    C = [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)]
         for i in range(n)]
    if p: C = [[x % p for x in row] for row in C]
    return tuple(tuple(r) for r in C)

# "A^2 = I implies A = I" over F_2  (false - find the counterexample).
# Note there is no "+/- I" to state here: over F_2, -I = I. Writing the
# condition as `A in (I, -I)` would list the same matrix twice and quietly
# weaken nothing - the kind of redundant encoding worth catching early.
I2 = ((1, 0), (0, 1))
print(search(lambda A: matmul(A, A, 2) != I2 or A == I2,
             matrices(2, [0, 1]), "A^2 = I implies A = I over F_2"))
```

**Cannot settle:** anything in infinite dimensions — that is where most
functional-analysis counterexamples live, and no finite matrix will produce one.
Also nothing about characteristic 0 from evidence over $\mathbb{F}_p$, or the
reverse.

## Number theory

Direct ranges, exact integer arithmetic.

```python
# "n^2 + n + 41 is prime for all n >= 0"  (false at n = 40)
def is_prime(m):
    if m < 2: return False
    return all(m % d for d in range(2, int(m ** 0.5) + 1))
print(search(lambda n: is_prime(n*n + n + 41), range(100), "Euler's polynomial"))
```

**Cannot settle:** almost every genuine open question. A pattern holding to
$10^6$ is weak evidence in number theory specifically — counterexamples to
plausible statements are routinely astronomically large.

## Inequalities and analysis

Exact rationals for equality and for tight inequalities; floats only with a real
margin.

```python
from fractions import Fraction
# AM-GM for two terms, exactly
print(search(lambda ab: (ab[0] + ab[1]) ** 2 >= 4 * ab[0] * ab[1],
             [(a, b) for a in rationals(4, 0, 3) for b in rationals(4, 0, 3)],
             "AM-GM, two terms"))
```

For a claimed inequality, probe the boundary rather than the interior: equality
cases, zero, and the extremes of the domain are where a false inequality fails,
and uniform random sampling almost never lands there.

**Cannot settle:** anything asymptotic, anything involving limits, and any
inequality over an unbounded domain. Finitely many points cannot distinguish
"true" from "true until $x$ gets large".

## Combinatorial identities

Both sides as exact integers over a range. A mismatch is decisive; agreement over
a decent range is strong evidence, since these identities are rigid.

```python
from math import comb
# sum of C(n,k)^2 = C(2n,n)
print(search(lambda n: sum(comb(n, k) ** 2 for k in range(n + 1)) == comb(2*n, n),
             range(15), "Vandermonde special case"))
```

**Cannot settle:** identities with a free parameter beyond the range checked,
though for polynomial identities agreement at more points than the degree is a
proof — if you can bound the degree, say so and the check becomes decisive.
