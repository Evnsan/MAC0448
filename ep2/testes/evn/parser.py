#! /usr/bin/env python

import pyparsing as pp
import sys

class LineParse(object):
    def __init__(self):
        
        #Tokens finais
        self.COLON = pp.Literal(':').suppress()
        self.WORD = pp.Word(
                        "abcdefghijklmnopqrstuvxywzABCDEFGHIJKLMNOPQRSTUVXYWZ1234567890:.,*"
                    )
        #Tokens n-finais
#        self.user = pp.Word(pp.alphanums, min = 3, max = 10) + self.COLON
#        self.prefix = pp.Or(self.user | "*:")
        self.args = pp.OneOrMore(self.WORD) + pp.White('\n')
#        self.cmd = pp.Word(pp.srange("[A-Z]"), min = 3, max = 6) 
        #Token mensagem 
#        self.mensagem = self.arg
#     self.mensagem = (self.prefix.setResultsName('prefix') +
#            self.cmd.setResultsName('cmd') +
#            self.args.setResultsName('args') +
#            pp.White('\n').suppress()
#        ).setName('mensagem')

        #Token Line
#        self.line = pp.OneOrMore(self.mensagem)
        self.line = pp.OneOrMore(self.args)


    def tok(self, s):
        result = self.line.parseString(s)
        return result

p = LineParse()
try:
    r = p.tok("aad\n skdaj\n")
#    r = p.tok("CCjMM: MMM ajsh sd,lkfj lslakdj :traiiil\n sd: KMG slkdjf sdlkfj skld")
#    print len(r['args'])
    print r
except pp.ParseException as x:
    print x.line
    print " No match: {0}".format(str(x))

