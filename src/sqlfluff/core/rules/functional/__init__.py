"""Modules in this directory provide a "functional" API for rule writing.

Wikipedia defines functional programming (https://en.wikipedia.org/wiki/Functional_programming)
as a declarative programming paradigm where code is built by applying and composing functions.

The modules in this API provide classes and predicates for working with segments
and slices. The API is loosely inspired by packages such as Pandas and Numpy.

These classes provide a simpler, higher-level API for writing rules, resulting
in shorter, simpler, easier-to-read code. Rules can use these classes, the
lower-level classes, or a mix, but it is suggested that each rule primarily
use one or the other for readability.
"""

__all__ = ("Segments", "sp")

from sqlfluff.core.rules.functional.segments import Segments
import sqlfluff.core.rules.functional.segment_predicates as sp
