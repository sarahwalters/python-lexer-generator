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
  eclosure = copy.copy(epsilon_closure(start_nfa_states))
  start_state = DFAState(sc, {}, eclosure)

  unmarked_queue = [start_state]
  nfa_to_dfa = {start_state.nfa_state_str: start_state}

  while len(unmarked_queue):
    # mark the state
    unmarked = unmarked_queue.pop(0)
    unmarked.marked = True

    # compute transitions
    transitions = {}
    for nfa_state in unmarked.nfa_states:
      for key in nfa_state.transitions:
        if transitions.has_key(key):
          transitions[key] += nfa_state.transitions[key]
        else:
          transitions[key] = nfa_state.transitions[key]

    for key in transitions:
      eclosure = epsilon_closure(transitions[key])
      nfa_state_str = ','.join(sorted([state.id for state in eclosure]))
      if nfa_to_dfa.has_key(nfa_state_str):
        existing_state = nfa_to_dfa[nfa_state_str]
        unmarked.add_transitions(key, existing_state)
      else:
        new_state = DFAState(sc, {}, eclosure)
        nfa_to_dfa[new_state.nfa_state_str] = new_state
        unmarked.add_transitions(key, new_state)
        unmarked_queue.append(new_state)

  start_state.pretty_print()

seen_state_ids = []

def epsilon_closure(states):
  print '------------------'
  print [state.id for state in states]
  queue = copy.copy(states)
  considered_states = []
  eclosure = []

  while len(queue):

    state = queue.pop(0)
    considered_states.append(state)
    if state.transitions.has_key('epsilon'):
      for s in state.transitions['epsilon']:
        if not find_by_id(eclosure, s):
          eclosure.append(s)
        if not find_by_id(considered_states, s) and not find_by_id(queue, s):
          queue.append(s)

  print [state.id for state in eclosure]

  return eclosure

def find_by_id(states, state):
  match = [s for s in states if s.id == state.id]
  return len(match) >= 1
