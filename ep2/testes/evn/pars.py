#! /usr/bin/env python

import pyparsing as pp
import sys

first = pp.Word(pp.alphas+"_", exact=1)
rest = pp.Word(pp.alphanums+"_")
identifier = first+pp.Optional(rest)

try:
    result = identifier.parseString("_teste")
    type(result[1])
    print " Matches: {0}".format(result)
except pp.ParseException as x:
    print " No match: {0}".format(str(x))

