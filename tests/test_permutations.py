import numpy as np

import unittest
from hypothesis import given
from yarrow.finite_function import FiniteFunction
from tests.strategies import adapted_function, finite_functions, permutations, parallel_permutations

# Invert a permutation
def invert(p):
    return FiniteFunction(p.source, np.argsort(p.table, kind='stable'))

# return true if s sorts by f.
def sorts(s, f, strict=False):
    y = s >> f
    if len(y.table) <= 1:
        return True # arrays of length <= 1 are trivially sorted

    if strict:
        return np.all(y.table[:-1] < y.table[1:])
    return np.all(y.table[:-1] <= y.table[1:])

# Ensure the invert function works(!)
@given(p=permutations())
def test_invert(p):
    assert invert(p) >> p == FiniteFunction.identity(p.source)
    assert p >> invert(p) == FiniteFunction.identity(p.source)

# Definition A.2 "Sorting"
@given(f=finite_functions())
def test_argsort_matches_definition(f):
    p = f.argsort()
    y = p >> f

    if len(y.table) <= 1:
        return None

    assert sorts(p, f)

# Proposition A.3
# we test something slightly weaker; instead of a general monomorphism we just
# use a permutation.
# TODO: generate a monomorphism by just `spreading out' values of the identity
# function, then permuting?
@given(p=permutations())
def test_argsort_monomorphism_strictly_increasing(p):
    q = p.argsort()
    y = q >> p

    if len(y.table) <= 1:
        return None

    assert sorts(q, p, strict=True)

# TODO: test uniqueness A.4 (?)

# Proposition A.5
@given(fpq=adapted_function(source=None, target=None))
def test_sort_by_permuted_key(fpq):
    f, p, q = fpq
    s = f.argsort()
    assert sorts(s >> invert(p), p >> f)

# Proposition A.6
# Again using permutations instead of monomorphisms;
# see test_argsort_monomorphism_strictly_increasing
@given(fp=parallel_permutations())
def test_sort_pf_equals_sortf_p(fp):
    f, p = fp
    assert (p >> f).argsort() == (f.argsort() >> invert(p))
