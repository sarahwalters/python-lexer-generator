import nfa_generator as nfa_gen
import dfa_generator as dfa_gen
from automaton_utils import StateCounter

def generate_dfa(regex, token, nfa_sc, dfa_sc):
  nfa = nfa_gen.generate_nfa(regex, nfa_sc)
  nfa.pretty_print()
  print
  dfa = dfa_gen.generate_dfa(nfa, token, dfa_sc)
  dfa.pretty_print()
  print '--------------------'
  return dfa

class LexerGenerator:
  def __init__(self, tokens):
    self.dfas = []
    nfa_sc = StateCounter('nfa')
    dfa_sc = StateCounter('dfa')
    for regex in tokens:
      self.dfas.append(generate_dfa(regex, tokens[regex], nfa_sc, dfa_sc))

    # for dfa in self.dfas:
    #   dfa.pretty_print()
    #   print '------------'


def run():
  tokens = {
    'a+': 'strings of As',
    '(ab)+': 'strings of ABs'
  }
  return LexerGenerator(tokens)
