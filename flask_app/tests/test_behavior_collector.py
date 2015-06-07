# -*- coding: utf-8 -*-

__author__ = 'jiaying.lu'

from unittest import TestCase
import numpy as np

from flask_app.behavior_collector import _collect_probs, _get_arithmetic_average, _check_blank_condition


class MyTestCase(TestCase):
    """Provide base class for test complex structures have almost equal contents"""

    def assertDeepAlmostEqual(self, expected, actual, *args, **kwargs):
        """
        Assert that two complex structures have almost equal contents.

        Compares lists, dicts and tuples recursively. Checks numeric values
        using test_case's :py:meth:`unittest.TestCase.assertAlmostEqual` and
        checks all other values with :py:meth:`unittest.TestCase.assertEqual`.
        Accepts additional positional and keyword arguments and pass those
        intact to assertAlmostEqual() (that's how you specify comparison
        precision).

        Copy from http://stackoverflow.com/questions/23549419
          /assert-that-two-dictionaries-are-almost-equal

        :param self: TestCase object on which we can call all of the basic
        'assert' methods.
        :type self: :py:class:`unittest.TestCase` object
        """
        is_root = not '__trace' in kwargs
        trace = kwargs.pop('__trace', 'ROOT')
        try:
            if isinstance(expected, (int, float, long, complex)):
                self.assertAlmostEqual(expected, actual, *args, **kwargs)
            elif isinstance(expected, (list, tuple, np.ndarray)):
                self.assertEqual(len(expected), len(actual))
                for index in xrange(len(expected)):
                    v1, v2 = expected[index], actual[index]
                    self.assertDeepAlmostEqual(v1, v2,
                                               __trace=repr(index), *args, **kwargs)
            elif isinstance(expected, dict):
                self.assertEqual(set(expected), set(actual))
                for key in expected:
                    self.assertDeepAlmostEqual(expected[key], actual[key],
                                               __trace=repr(key), *args, **kwargs)
            else:
                self.assertEqual(expected, actual)
        except AssertionError as exc:
            exc.__dict__.setdefault('traces', []).append(trace)
            if is_root:
                trace = ' -> '.join(reversed(exc.traces))
                exc = AssertionError("%s\nTRACE: %s" % (exc.message, trace))
            raise exc


class TestInnerMethod(MyTestCase):

    def test_get_arithmetic_average(self):
        # case 1
        prob_list = [{'A': 0.9, 'B': 0.1}, {'A': 0.1, 'B': 0.9}]
        result = {'A': 0.5, 'B': 0.5}
        self.assertDeepAlmostEqual(result, _get_arithmetic_average(prob_list))

        # case 2
        prob_list = [{'A': 0.9, 'B': 0.1}, {'A': 0.1, 'B': 0.9}, {'A': 0.3, 'B': 0.3, 'C': 0.4}]
        result = {'A': 1.3/3, 'B': 1.3/3, 'C':0.4/3}
        self.assertDeepAlmostEqual(result, _get_arithmetic_average(prob_list))

    def test_collect_probs(self):
        # case 1
        cur_prob_list = [{'A': 0.9, 'B': 0.1}, {'A': 0.1, 'B': 0.9}]
        other_prob_list = [{'A': 0.4, 'C': 0.6}, {'A': 0.2, 'B': 0.4, 'C': 0.4}]
        k_weight = 0.5
        result = {'A': 0.4, 'B': 0.35, 'C': 0.25}
        self.assertDeepAlmostEqual(result, _collect_probs(cur_prob_list, other_prob_list, k_weight))

        # case 2
        cur_prob_list = [{'A': 0.9, 'B': 0.1}, {'A': 0.1, 'B': 0.9}]
        other_prob_list = [{'A': 0.4, 'C': 0.6}, {'A': 0.2, 'B': 0.4, 'C': 0.4}]
        k_weight = 0.8
        result = {'A': 0.46, 'B': 0.44, 'C': 0.1}
        self.assertDeepAlmostEqual(result, _collect_probs(cur_prob_list, other_prob_list, k_weight))

    def test_check_blank_condition(self):
        # case 1
        my_list = [1, 3, 5, 7]
        self.assertEqual(True, _check_blank_condition(1, 7, my_list))

        # case 2
        my_list = [1, 4, 5, 7]
        self.assertEqual(False, _check_blank_condition(1, 7, my_list))

        # case 3
        my_list = [4, 5, 6, 7]
        self.assertEqual(False, _check_blank_condition(2, 7, my_list))

        # case 4
        my_list = [4, 5, 6, 7]
        self.assertEqual(True, _check_blank_condition(3, 7, my_list))

        # case 5
        my_list = [4, 5, 6, 7]
        self.assertEqual(False, _check_blank_condition(4, 9, my_list))

        # case 6
        my_list = [4, 5, 6, 7]
        self.assertEqual(True, _check_blank_condition(4, 8, my_list))

        # case 7
        my_list = [1, 2, 4, 5, 6, 7]
        self.assertEqual(True, _check_blank_condition(3, 8, my_list))
