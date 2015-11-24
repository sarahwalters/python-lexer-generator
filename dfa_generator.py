import nfa_generator as nfa_gen
from automaton_utils import StateCounter, State, Automaton
import copy

def run(regex):
  print 'NFA generation'
  nfa = nfa_gen.generate_nfa(regex)
  nfa.pretty_print()
  print
  print 'DFA generation'
  generate_dfa(nfa)

def generate_dfa(nfa):
  sc = StateCounter('dfa')

  dfa_state_queue = [[nfa.start_state]]

  dfa_state = State(sc, {})
  eclosure = epsilon_closure(dfa_state_queue.pop())
  print [state.id for state in eclosure]

  for state in eclosure:
    for key in state.transitions:
      dfa_state.add_transitions(key, state.transitions[key])

  for key in dfa_state.transitions:
    dfa_state_queue.append(dfa_state.transitions[key])

  print dfa_state_queue
  dfa_state.pretty_print()


def epsilon_closure(states):
  # TODO clean up
  res_eclosure = []

  i = 0
  while i < len(states):
    state = states[i]

    if not state.transitions.has_key('epsilon'):
      return []
    else:
      first_deg_eclosure = state.transitions['epsilon']
      higher_deg_eclosures = [epsilon_closure([_state]) for _state in first_deg_eclosure]
      res_eclosure += copy.copy(first_deg_eclosure + [state])
      for eclosure_set in higher_deg_eclosures:
        res_eclosure += eclosure_set

    i += 1

  return list(set(res_eclosure))

# def epsilon_closure_single_state(state):
#   if not state.transitions.has_key('epsilon')
