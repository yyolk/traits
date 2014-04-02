#------------------------------------------------------------------------------
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
"""
Tests for List items_changed events.

"""
from __future__ import absolute_import

from traits.testing.unittest_tools import unittest

from ..api import HasTraits, Int, List


class MyClass(HasTraits):
    l = List(Int, [1, 2, 3])

    l_events = List

    def _l_items_changed(self, event):
        self.l_events.append(event)


class ListEventTestCase(unittest.TestCase):
    def test_initialization(self):
        # Just creating an instance of MyClass shouldn't cause
        # the items_changed handler to fire.
        foo = MyClass()
        self.assertEqual(foo.l, [1, 2, 3])
        self.assertEqual(len(foo.l_events), 0)

    def test_append(self):
        foo = MyClass()
        foo.l.append(4)
        self.assertEqual(foo.l, [1, 2, 3, 4])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [4])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 3)

    def test_extend(self):
        foo = MyClass()
        foo.l.extend([4, 5, 6])
        self.assertEqual(foo.l, [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [4, 5, 6])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 3)

    def test_extend_via_inplace_addition(self):
        foo = MyClass()
        foo.l += [4, 5, 6]
        self.assertEqual(foo.l, [1, 2, 3, 4, 5, 6])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [4, 5, 6])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 3)

    def test_insert(self):
        foo = MyClass()
        foo.l.insert(1, 99)
        self.assertEqual(foo.l, [1, 99, 2, 3])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [99])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 1)

    def test_insert_with_negative_argument(self):
        foo = MyClass()
        foo.l.insert(-1, 99)
        self.assertEqual(foo.l, [1, 2, 99, 3])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [99])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 2)

    def test_insert_at_extreme_negative_index(self):
        foo = MyClass()
        foo.l.insert(-100, 99)
        self.assertEqual(foo.l, [99, 1, 2, 3])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [99])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 0)

    def test_insert_at_extreme_positive_index(self):
        foo = MyClass()
        foo.l.insert(100, 99)
        self.assertEqual(foo.l, [1, 2, 3, 99])
        self.assertEqual(len(foo.l_events), 1)
        event = foo.l_events[0]
        self.assertEqual(event.added, [99])
        self.assertEqual(event.removed, [])
        self.assertEqual(event.index, 3)

    def test_insert_index_invariants(self):
        for index in range(-10, 10):
            foo = MyClass()
            foo.l.insert(index, 1729)
            self.assertEqual(len(foo.l_events), 1)
            event = foo.l_events[0]
            self.assertEqual(event.added, [1729])
            self.assertEqual(event.removed, [])
            self.assertGreaterEqual(event.index, 0)
            self.assertEqual(foo.l[event.index], 1729)
