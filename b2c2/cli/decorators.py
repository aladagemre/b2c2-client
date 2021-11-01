# -*- coding: utf-8 -*-
from functools import wraps


def check_connection_before(f):
    """
    A decorator for CommandLineInterface
    Checks whether API connection is available
    before calling the actual function.
    :param f: function to call
    :return: result of the function
    """

    @wraps(f)
    def wrapper(self, *args, **kw):
        if not self.check_api_connection():
            return
        result = f(self, *args, **kw)
        return result

    return wrapper
