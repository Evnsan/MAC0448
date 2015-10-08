#! /usr/bin/env python

import pyparsing as pp
import sys

class Pars(object):
    def __init__(self):
#        self.SPACE = pp.Literal(' ').suppress()
        self.COLON = pp.Literal(':').suppress()
        self.args =pp.Group(pp.ZeroOrMore(pp.Regex(r"[^  :]+")))
        self.trail = pp.Word(pp.alphanums)
        self.cmd = pp.Word(pp.srange("[A-Z]"), min = 3, max = 6) 
        self.login = pp.Word(pp.alphanums, min = 3, max = 10)
        self.user = pp.Or(self.login | "*").setName('user')
        self.line = (self.user.setResultsName('user').setName('USER') +
#           self.SPACE +
            self.cmd.setResultsName('cmd').setName('CMD') +
            self.args.setResultsName('args').setName('ARGS') +
             pp.Optional(self.COLON +
                 self.trail.setResultsName('trail').setName('trail')
             )
        ).setName('line')


    def tok(self, s):
        result = self.line.parseString(s)
        return result

p = Pars()
try:
    r = p.tok("CCjMM MMM %ajsh sd,lkfj lslakdj :traiiil")
    print len(r['args'])
    print r
except pp.ParseException as x:
    print x.line
    print " No match: {0}".format(str(x))

