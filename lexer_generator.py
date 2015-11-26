import nfa_generator as nfa_gen
import dfa_generator as dfa_gen
from automaton_utils import StateCounter
import copy
from string import ascii_lowercase, ascii_uppercase

class Lexer:
  def __init__(self, tokens):
    self.nfas = []
    self.dfas = []
    nfa_sc = StateCounter('nfa')
    dfa_sc = StateCounter('dfa')

    for regex in tokens:
      nfa = nfa_gen.generate_nfa(regex, nfa_sc, tokens[regex])
      dfa = dfa_gen.generate_dfa(nfa, dfa_sc)
      self.nfas.append(nfa)
      self.dfas.append(dfa)

    for dfa in self.dfas:
      dfa.pretty_print()
      print '------------'

  def tokenize(self, input, tokenized=None):
    if tokenized == None:
      tokenized = []

    current_states = copy.copy([dfa.start_state for dfa in self.dfas])
    stop = False

    match = []

    while len(current_states) and len(input) and not stop:
      next_char = input[0]
      updated_states = []

      for state in current_states:
        if state.transitions.has_key(next_char):
          updated_states.append(state.transitions[next_char][0])

      if len(updated_states) != 0:
        match.append(input.pop(0))
      else:
        if len(current_states[0].accepting) > 0:
          tokenized.append((''.join(match), current_states[0].accepting))
          if next_char == ' ':
            input = input[1:]
          if len(input):
            self.tokenize(input, tokenized)
          return tokenized
        else:
          raise RuntimeError('Input is not in language')

      current_states = updated_states

def run(input):
  alph_lower = '|'.join(list(ascii_lowercase))
  alph_upper = '|'.join(list(ascii_uppercase))
  alph = '%s|%s' % (alph_lower, alph_upper)

  # How to solve aabab? Should get a, abab; gets aa, [bab] <- invalid
  # (overlapping tokens)
  print alph_lower
  tokens = {
    'if|elif|else': 'keyword',
    #'(%s)+' % 'a|b|i|f': 'variable'
    '(a+|(ab)+)_': 'variable'
    #'(x(a*)y)+': '(x(a*)y)+'
  }
  print tokens
  lex = Lexer(tokens)
  input = list(input)
  input.append(' ')
  print lex.tokenize(input)
