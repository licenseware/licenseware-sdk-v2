# import unittest
# from licenseware

# from flask import request
# from typing import Callable
# from functools import wraps



# def xss(fn: Callable = None) -> Callable:
#     """
#     Added to flask-restx Api class decorators parameter
#     This will be applied to each resource and raise an error when suspicious payload is added.
#     """

#     def decorator(fn: Callable) -> Callable:
#         @wraps(fn)
#         def wrapper(*args, **kwargs) -> Callable:
            
#             return result

#         return wrapper

#     return decorator(fn) if fn else decorator







# # python3 -m unittest tests/test_xss_decorator.py


# class TestXSSDecorator(unittest.TestCase):

#     def test_xss_decorator(self):

