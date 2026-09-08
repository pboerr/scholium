"""Exhaustive-search harness for probing mathematical conjectures.

Pure standard library — no sympy, numpy or networkx required, because the
environment often does not have them and a probe that cannot run is worse than
no probe at all.

The point of this module is not the enumerators; it is `search`, which reports
what was actually checked. "No counterexample among all 1044 graphs on <= 5
vertices" is evidence. "Verified" is not a thing a finite search can say.

Usage:
    from probe import search, must_fail, groups, graphs, topologies

    r = search(lambda G: G.is_abelian(), groups(order_max=8), "all groups abelian")
    print(r)        # -> counterexample: S_3
"""

from fractions import Fraction
from itertools import combinations, permutations, product

__all__ = [
    "search", "must_fail", "Result", "Family",
    "Group", "cyclic", "dihedral", "symmetric", "alternating", "quaternion8",
    "direct_product", "some_groups",
    "graphs", "topologies", "subsets", "functions", "matrices", "rationals",
]


# --------------------------------------------------------------------------
# The harness
# --------------------------------------------------------------------------

class Family:
    """A case list that knows whether it is exhaustive.

    Completeness is the difference between "no counterexample among all 355
    topologies on 4 points" and "no counterexample among the dozen groups I
    happened to build". A search cannot tell these apart by itself, and a
    partial family that reports like an exhaustive one is the most dangerous
    thing in this module.
    """

    def __init__(self, items, complete, description):
        self.items = items
        self.complete = complete
        self.description = description

    def __iter__(self):
        return iter(self.items)

    def note(self):
        if self.complete:
            return f"exhaustive over {self.description}"
        return (f"{self.description} - NOT exhaustive, so a counterexample "
                f"outside this family would not have been seen")


class Result:
    """Outcome of a finite search. Carries the extent, not just the verdict."""

    def __init__(self, name, checked, counterexample=None, found=False,
                 error=None, family=None):
        self.name = name
        self.checked = checked
        self.counterexample = counterexample
        self.found = found
        self.error = error
        self.family = family

    @property
    def refuted(self):
        return self.found

    def __bool__(self):
        # True means "survived a non-empty search" - NOT "true".
        return not self.found and self.error is None and self.checked > 0

    def __str__(self):
        if self.error is not None:
            return (f"[{self.name}] SEARCH FAILED after {self.checked} cases: "
                    f"{self.error!r} - the harness is broken, not the conjecture")
        if self.found:
            return (f"[{self.name}] FALSE - counterexample after {self.checked} "
                    f"cases: {self.counterexample!r}")
        if self.checked == 0:
            return (f"[{self.name}] NO CASES CHECKED - the family was empty. "
                    f"This is not evidence of anything; a filter has probably "
                    f"excluded everything you meant to test.")
        note = f" ({self.family.note()})" if self.family is not None else \
               " (completeness of this family unknown)"
        return (f"[{self.name}] no counterexample in {self.checked} cases"
                f"{note}. This is evidence, not a proof.")


def search(predicate, cases, name="conjecture", limit=None):
    """Apply `predicate` to each case; stop at the first falsifying one.

    An exception inside the predicate is reported as a broken harness rather
    than a counterexample, because the usual cause is that the property was
    encoded wrongly and a silent pass would be a false reassurance.
    """
    family = cases if isinstance(cases, Family) else None
    checked = 0
    for case in cases:
        if limit is not None and checked >= limit:
            break
        try:
            ok = predicate(case)
        except Exception as exc:              # noqa: BLE001 - deliberate
            return Result(name, checked, case, found=False, error=exc,
                          family=family)
        checked += 1
        if not ok:
            return Result(name, checked, case, found=True, family=family)
    return Result(name, checked, family=family)


def must_fail(predicate, cases, name="poison test"):
    """Confirm the encoding CAN reject something.

    A predicate that is accidentally always true - the commonest way a
    computational check misleads - passes every search silently. Feed this a
    family you know contains a violation; if nothing is found, the encoding is
    wrong and every other result from it is worthless.
    """
    r = search(predicate, cases, name)
    if r.error is not None:
        raise AssertionError(
            f"POISON TEST CRASHED: {name!r} raised {r.error!r}. The predicate is "
            f"broken, not vacuous - fix the exception before reading anything "
            f"into a pass or a fail."
        )
    if not r.found:
        raise AssertionError(
            f"POISON TEST FAILED: {name!r} found no violation in {r.checked} "
            f"cases that should contain one. The predicate is probably "
            f"vacuously true - fix the encoding before trusting any result."
        )
    return r


# --------------------------------------------------------------------------
# Finite groups
# --------------------------------------------------------------------------

class Group:
    def __init__(self, elements, op, name="G"):
        self.elements = list(elements)
        self.op = op
        self.name = name

    def __repr__(self):
        return self.name

    @property
    def order(self):
        return len(self.elements)

    def identity(self):
        for e in self.elements:
            if all(self.op(e, x) == x and self.op(x, e) == x for x in self.elements):
                return e
        raise ValueError(f"{self.name} has no identity - not a group")

    def inverse(self, x):
        e = self.identity()
        for y in self.elements:
            if self.op(x, y) == e:
                return y
        raise ValueError(f"no inverse for {x!r} in {self.name}")

    def is_abelian(self):
        return all(self.op(a, b) == self.op(b, a)
                   for a in self.elements for b in self.elements)

    def is_valid(self):
        """Closure, associativity, identity, inverses. Use it on anything you build."""
        els = set(self.elements)
        if any(self.op(a, b) not in els for a in self.elements for b in self.elements):
            return False
        if any(self.op(self.op(a, b), c) != self.op(a, self.op(b, c))
               for a in self.elements for b in self.elements for c in self.elements):
            return False
        try:
            self.identity()
            for x in self.elements:
                self.inverse(x)
        except ValueError:
            return False
        return True

    def element_order(self, x):
        e, cur, n = self.identity(), x, 1
        while cur != e:
            cur, n = self.op(cur, x), n + 1
        return n


def _compose(p, q):
    """Permutations as tuples: (p*q)[i] = p[q[i]]."""
    return tuple(p[q[i]] for i in range(len(p)))


def _closure(gens, n):
    ident = tuple(range(n))
    seen, frontier = {ident}, [ident]
    while frontier:
        nxt = []
        for a in frontier:
            for g in gens:
                b = _compose(a, g)
                if b not in seen:
                    seen.add(b)
                    nxt.append(b)
        frontier = nxt
    return sorted(seen)


def _perm_group(gens, n, name):
    return Group(_closure(gens, n), _compose, name)


def cyclic(n):
    return _perm_group([tuple((i + 1) % n for i in range(n))], n, f"C_{n}")


def dihedral(n):
    if n < 3:
        raise ValueError(
            "dihedral(n) is only correct for n >= 3; this rotation-reflection "
            "construction silently returns the wrong group for n = 1, 2. "
            "Use cyclic(2) for D_1 and direct_product(cyclic(2), cyclic(2)) "
            "for D_2 (the Klein four-group)."
        )
    r = tuple((i + 1) % n for i in range(n))
    s = tuple((-i) % n for i in range(n))
    return _perm_group([r, s], n, f"D_{n}")


def symmetric(n):
    return Group(sorted(permutations(range(n))), _compose, f"S_{n}")


def alternating(n):
    def even(p):
        inv = sum(1 for i, j in combinations(range(len(p)), 2) if p[i] > p[j])
        return inv % 2 == 0
    return Group(sorted(p for p in permutations(range(n)) if even(p)),
                 _compose, f"A_{n}")


def quaternion8():
    els = ["1", "-1", "i", "-i", "j", "-j", "k", "-k"]
    sign = {"1": 1, "-1": -1, "i": 1, "-i": -1, "j": 1, "-j": -1, "k": 1, "-k": -1}
    base = {"1": "1", "-1": "1", "i": "i", "-i": "i", "j": "j", "-j": "j",
            "k": "k", "-k": "k"}
    table = {("1", "1"): ("1", 1), ("1", "i"): ("i", 1), ("1", "j"): ("j", 1),
             ("1", "k"): ("k", 1), ("i", "1"): ("i", 1), ("j", "1"): ("j", 1),
             ("k", "1"): ("k", 1), ("i", "i"): ("1", -1), ("j", "j"): ("1", -1),
             ("k", "k"): ("1", -1), ("i", "j"): ("k", 1), ("j", "i"): ("k", -1),
             ("j", "k"): ("i", 1), ("k", "j"): ("i", -1), ("k", "i"): ("j", 1),
             ("i", "k"): ("j", -1)}

    def op(a, b):
        bs, s = table[(base[a], base[b])]
        s *= sign[a] * sign[b]
        return bs if s == 1 else ("1" if bs == "1" and s == 1 else
                                  ("-1" if bs == "1" else "-" + bs))
    return Group(els, op, "Q_8")


def direct_product(G, H):
    return Group([(g, h) for g in G.elements for h in H.elements],
                 lambda a, b: (G.op(a[0], b[0]), H.op(a[1], b[1])),
                 f"{G.name}x{H.name}")


def some_groups(order_max=8):
    """A hand-built library of small groups, returned as an INCOMPLETE Family.

    Deliberately not called `groups`. It does not contain every group of every
    order - at order 8 it has 3 of the 5 isomorphism classes, at order 16 it has
    2 of 14 - so a search over it can survive a false claim. `C_2^3` is absent,
    which is enough to let "every group of order 8 has an element of order 4"
    pass. The Family wrapper makes `search` say so in its report; heed that
    rather than reading a survival here as a small-order check.

    For a claim about one specific order, build the groups of that order
    yourself and check each with `is_valid()`.
    """
    out = []
    for n in range(1, order_max + 1):
        out.append(cyclic(n))
    for n in range(3, order_max // 2 + 1):
        out.append(dihedral(n))          # D_3 == S_3, so S_n starts at 4 below
    for n in (4,):
        if _fact(n) <= order_max:
            out.append(symmetric(n))
        if _fact(n) // 2 <= order_max:
            out.append(alternating(n))
    if order_max >= 8:
        out.append(quaternion8())
        out.append(direct_product(cyclic(2), cyclic(2)))
        out.append(direct_product(cyclic(2), direct_product(cyclic(2), cyclic(2))))
    kept = [g for g in out if g.order <= order_max]
    return Family(kept, complete=False,
                  description=f"hand-built library of {len(kept)} groups of "
                              f"order <= {order_max}")


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


# --------------------------------------------------------------------------
# Finite structures
# --------------------------------------------------------------------------

def subsets(items):
    items = list(items)
    for k in range(len(items) + 1):
        for c in combinations(items, k):
            yield frozenset(c)


def functions(domain, codomain):
    domain, codomain = list(domain), list(codomain)
    for vals in product(codomain, repeat=len(domain)):
        yield dict(zip(domain, vals))


def _graphs_iter(n):
    possible = list(combinations(range(n), 2))
    for k in range(len(possible) + 1):
        for es in combinations(possible, k):
            yield frozenset(es)


def graphs(n):
    """All labelled simple graphs on {0..n-1}, as frozensets of edges.

    Labelled, so isomorphic copies repeat - wasteful, never wrong.
    """
    return Family(_graphs_iter(n), complete=True,
                  description=f"all 2^C({n},2) labelled graphs on {n} vertices")


def _topologies_iter(n):
    points = frozenset(range(n))
    allsets = list(subsets(range(n)))
    for fam in subsets(allsets):
        fam = set(fam)
        if frozenset() not in fam or points not in fam:
            continue
        if any(a & b not in fam for a in fam for b in fam):
            continue
        if any(a | b not in fam for a in fam for b in fam):
            continue
        yield fam


def topologies(n):
    """All topologies on {0..n-1}: 1, 1, 4, 29, 355 for n = 0..4.

    Do not call this with n >= 5. It filters all 2^(2^n) families of subsets,
    which is 4.3 billion at n = 5 - hours, not seconds, despite there being only
    6942 topologies to find.
    """
    if n >= 5:
        raise ValueError(
            f"topologies({n}) would filter 2^(2^{n}) families of subsets and "
            f"take hours. Exhaustive finite-topology search is practical to "
            f"n = 4 only; for larger n, construct the specific spaces you care "
            f"about instead."
        )
    return Family(_topologies_iter(n), complete=True,
                  description=f"all topologies on {n} points")


def matrices(n, entries):
    """All n x n matrices with entries drawn from `entries`, as tuples of rows."""
    entries = list(entries)
    for flat in product(entries, repeat=n * n):
        yield tuple(tuple(flat[i * n:(i + 1) * n]) for i in range(n))


def rationals(max_denom=6, lo=-3, hi=3):
    """Exact rationals — never probe an equality with floats."""
    seen = set()
    for q in range(1, max_denom + 1):
        for p in range(lo * q, hi * q + 1):
            f = Fraction(p, q)
            if f not in seen:
                seen.add(f)
                yield f
