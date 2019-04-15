# encoding: utf-8
"""
@author: liuyun
@time: 2019/4/10/010 10:22
@desc:
"""
import re


class _Option:
    def __init__(self, field, value, formatter=None):
        self.field = field
        self.value = value
        self.formatter = formatter or (lambda e: e)


def _non_null_options_to_dict(*options):
    return {o.field: o.formatter(o.value) for o in options if o.value is not None}


def params(*options):
    return _non_null_options_to_dict(*options)


def param(key, value):
    return _Option(key, value)


def regex(str):
    # return {"type": Type.REGEX, "value": str}
    return re.compile(str)