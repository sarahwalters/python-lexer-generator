import nfa_generator as nfa_gen
from automaton_utils import StateCounter, DFAState, Automaton
import copy


def generate_dfa(nfa):
  sc = StateCounter('dfa')
  accepting_id = nfa.end_state.id

  eclosure = epsilon_closure([nfa.start_state])
  start_state = DFAState(sc, {}, eclosure, accepting_id)

  unmarked_queue = [start_state]
  nfa_to_dfa = {start_state.nfa_state_str: start_state}

  while len(unmarked_queue):
    # mark the current DFA state
    unmarked = unmarked_queue.pop(0)
    unmarked.marked = True

    # collect transitions from the current DFA state's associated NFA states
    transitions = {}
    for nfa_state in unmarked.nfa_states:
      for key in nfa_state.transitions:
        if transitions.has_key(key):
          transitions[key] += nfa_state.transitions[key]
        else:
          transitions[key] = nfa_state.transitions[key]

    # add a transition from the current DFA state to a target DFA state for each key
    for key in transitions:
      # extend the set of NFA states associated with the target DFA state
      # by finding its epsilon closure
      eclosure = epsilon_closure(transitions[key])

      nfa_state_str = ','.join(sorted([state.id for state in eclosure]))
      if nfa_to_dfa.has_key(nfa_state_str):
        # the target DFA state exists -- add transition
        existing_state = nfa_to_dfa[nfa_state_str]
        unmarked.add_transitions(key, existing_state)
      else:
        # the target DFA state does not exist -- create it and add transition
        new_state = DFAState(sc, {}, eclosure, accepting_id)
        nfa_to_dfa[new_state.nfa_state_str] = new_state
        unmarked.add_transitions(key, new_state)
        unmarked_queue.append(new_state)

  return Automaton(start_state, None)


def epsilon_closure(states):
  '''
    Returns the epsilon closure of a set of states in an automaton.
    input: states, a list of State objects (either NFAState or DFAState)
    output: eclosure, the states reachable on epsilon transitions from those states
              -> DOES NOT include starting states unless they are reachable from
                 themselves on epsilon transitions
  '''
  queue = copy.copy(states)
  considered_states = []
  eclosure = []

  while len(queue):
    state = queue.pop(0)
    considered_states.append(state)

    if state.transitions.has_key('epsilon'):
      for s in state.transitions['epsilon']:
        # add state to epsilon closure, ensuring no duplicate items
        if not find_by_id(eclosure, s):
          eclosure.append(s)

        # queue state for consideration if it hasn't been considered
        # and isn't already queued
        if not find_by_id(considered_states, s) and not find_by_id(queue, s):
          queue.append(s)

  return eclosure if len(eclosure) else states


def find_by_id(states, state):
  '''
    Returns true if there is a state in states with an id of state.id
    inputs: states, a list of State objects (either NFAState or DFAState)
            state, a State object (either NFAState or DFAState)
    outputs: boolean
  '''
  matches = [s for s in states if s.id == state.id]
  return len(matches) >= 1
