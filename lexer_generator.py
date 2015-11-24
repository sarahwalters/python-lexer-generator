import nfa_generator as nfa_gen
import dfa_generator as dfa_gen

def generate_dfa(regex):
  print 'NFA generation'
  nfa = nfa_gen.generate_nfa(regex)
  nfa.pretty_print()
  print
  print 'DFA generation'
  dfa_gen.generate_dfa(nfa)
