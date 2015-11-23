import re
import pyparsing as pp

'''
Productions: (pseudo... written with regex syntax)

start -> regexp $
char -> [a-zA-Z0-9]
modifier -> '*' | '+'
interval -> [(char|'-')*]
base -> char | char base | interval | (base) | regexp
factor -> base modifier
term -> epsilon | factor term

regexp ->  term | regex '|' term

'''

REGEXP = pp.Forward()
BASE = pp.Forward()

MODIFIER = pp.Regex("[*+?]")
INTERVAL = '[' + pp.Word(pp.alphanums, bodyChars=pp.alphanums+'-') + ']'
BASE << pp.Or("("+BASE+")" | pp.Word(pp.alphanums) | INTERVAL)
BASE.setName("Base")
BASE.setDebug()
FACTOR = BASE + MODIFIER
FACTOR.setName("Factor")
FACTOR.setDebug()
TERM = pp.ZeroOrMore(FACTOR)
TERM.setName("Term")
TERM.setDebug()
REGEXP << pp.Or(TERM | TERM + "|" + REGEXP)
REGEXP.setName("Regexp")
REGEXP.setDebug()

def tokenize(regexp="(a*)(a|b)"):
  pattern = REGEXP
  print pattern
  print pattern.parseString("b*")
