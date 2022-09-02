import unittest


def load_ordered_tests(loader, standard_tests, pattern):
    """
    Test loader that keeps the tests in the order they were declared in the class.
    This works only for unittests, this will have no effect when running tests with pytest
    """
    ordered_cases = []
    for test_suite in standard_tests:
        ordered = []
        for test_case in test_suite:
            test_case_type = type(test_case)
            method_name = test_case._testMethodName
            testMethod = getattr(test_case, method_name)
            line = testMethod.__code__.co_firstlineno
            ordered.append((line, test_case_type, method_name))
        ordered.sort()
        for line, case_type, name in ordered:
            ordered_cases.append(case_type(name))
    return unittest.TestSuite(ordered_cases)


# from order_tests import load_ordered_tests

# # This orders the tests to be run in the order they were declared.
# # It uses the unittest load_tests protocol.
# load_tests = load_ordered_tests
