import nfa_generator as nfa_gen
from automaton_utils import StateCounter, DFAState, Automaton
import copy

def run(regex):
  print 'NFA generation'
  nfa = nfa_gen.generate_nfa(regex)
  nfa.pretty_print()
  print
  print 'DFA generation'
  sc = StateCounter('dfa')
  generate_dfa(sc, [nfa.start_state])

def generate_dfa(sc, start_nfa_states):
  start_state = DFAState(sc, {}, start_nfa_states)

  dfa_states = [start_state]
  unmarked_state = dfa_states[0]

  while unmarked_state:
    eclosure = epsilon_closure(unmarked_state.nfa_states)
    unmarked_state.marked = True

    transitions = {}
    for nfa_state in eclosure:
      for key in nfa_state.transitions:
        if transitions.has_key(key):
          transitions[key] += nfa_state.transitions[key]
        else:
          transitions[key] = nfa_state.transitions[key]

    for key in transitions:
        nfa_states_group = transitions[key]
        find_dfa_state = [dfa_state for dfa_state in dfa_states if dfa_state.nfa_states == nfa_states_group]

        if len(find_dfa_state) == 1:
          existing_dfa_state = find_dfa_state[0]
          unmarked_state.add_transitions(key, existing_dfa_state)
        elif len(find_dfa_state) == 0:
          new_dfa_state = DFAState(sc, {}, nfa_states_group)
          dfa_states.append(new_dfa_state)
          unmarked_state.add_transitions(key, new_dfa_state)
        else:
          raise RuntimeError("Duplicate DFA states")

    unmarked_state = None
    for state in dfa_states:
      if not state.marked:
        unmarked_state = state
        break

  start_state.pretty_print()

def epsilon_closure(states):
  eclosure_sets = [epsilon_closure_single_state(state) for state in states]
  res_eclosure = []
  for eclosure_set in eclosure_sets:
    res_eclosure += eclosure_set
  return list(set(res_eclosure))

def epsilon_closure_single_state(state):
  if not state.transitions.has_key('epsilon'):
    return []
  else:
    first_deg_eclosure = state.transitions['epsilon']
    higher_deg_eclosures = [epsilon_closure_single_state(_state) for _state in first_deg_eclosure]
    res_eclosure = copy.copy(first_deg_eclosure + [state])
    for eclosure_set in higher_deg_eclosures:
      res_eclosure += eclosure_set

  return list(set(res_eclosure))
