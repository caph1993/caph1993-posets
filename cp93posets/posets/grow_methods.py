from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING, Type
if TYPE_CHECKING:
    from .posets import Poset

import numpy as np
from typing import List, Sequence
from itertools import chain
from ..poset_exceptions import PosetExceptions
from ..iterators import cartesian


def _add_edge(self: Poset, i, j, assume_poset=False):
    "Grow self by adding one edge 'i leq j'"
    leq = self.leq
    new_leq = leq + np.matmul(leq[:, i:i + 1], leq[j:j + 1, :])
    new_leq.flags.writeable = False
    obj = self.__class__(new_leq, _validate=False)
    if not assume_poset:
        _ = obj.toposort
    return obj


def _add_node(self: Poset, i, j, assume_poset=False):
    "Grow self by adding one node just between i and j"
    n = self.n
    leq = self.leq
    out = np.zeros((n + 1, n + 1), bool)
    out[:-1, :-1] = leq
    out[n, n] = True
    out[:-1, :-1] += np.matmul(leq[:, i:i + 1], leq[j:j + 1, :])
    out[n, :-1] = leq[j, :]
    out[:-1, n] = leq[:, i]
    out.flags.writeable = False
    obj = self.__class__(out)
    if not assume_poset:
        _ = obj.toposort
    return obj


def forbidden_pairs(self: Poset):
    "Pairs (i,j) that break lub uniqueness or partial order structure"
    n = self.n
    leq = self.leq
    joi = self.lub
    nocmp = ~(leq + leq.T)

    def f(a, b):
        if leq[b, a]:
            return True
        if leq[a, b]:
            return False
        X = [x for x in range(n) if leq[x, a]]
        Y = [y for y in range(n) if ~leq[b, y] and nocmp[y, a]]
        return any(nocmp[joi[x, y], joi[b, y]] for y in Y for x in X)

    fb = np.array([[f(i, j) for j in range(n)] for i in range(n)], dtype=bool)
    return fb


def iter_add_edge(self: Poset):
    "Grow self by adding one edge"
    n = self.n
    leq = self.leq
    fb = self.forbidden_pairs
    vis = set()
    h = self.hash_elems
    for i, j in cartesian(n, n):
        if not fb[i, j] and not leq[i, j] and (h[i], h[j]) not in vis:
            yield self._add_edge(i, j, assume_poset=True)
    return


def iter_add_node(self: Poset):
    "Grow self by adding one node"
    n = self.n
    fb = self.forbidden_pairs
    vis = set()  # Don't repeat isomorphical connections
    h = self.hash_elems
    for i, j in cartesian(n, n):
        if not fb[i, j] and not (h[i], h[j]) in vis:
            yield self._add_node(i, j, assume_poset=True)
    return


def iter_all_latices(cls: Type[Poset], max_size):
    q = deque([cls.from_children(x) for x in [[], [[]], [[], [0]]]])
    vis = set()
    while q:
        U = q.popleft()
        yield U.canonical
        it = U.iter_add_node() if U.n < max_size else iter([])
        for V in chain(U.iter_add_edge(), it):
            if V not in vis:
                vis.add(V)
                q.append(V)
