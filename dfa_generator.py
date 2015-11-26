import nfa_generator as nfa_gen
from automaton_utils import StateCounter, DFAState, Automaton, epsilon_closure


def generate_dfa(nfa, sc):
  if nfa.is_dfa():
    # Just convert every NFA state to a DFA state & mark accepting
    start_state = DFAState(sc, [nfa.start_state])
    unmarked_queue = [start_state]
    nfa_to_dfa = {start_state.nfa_state_str: start_state}

    while len(unmarked_queue) > 0:
      unmarked = unmarked_queue.pop(0)

      nfa_state = unmarked.nfa_states[0]
      for key in nfa_state.transitions:
        target_state = nfa_state.transitions[key][0]
        if nfa_to_dfa.has_key(target_state.id):
          unmarked.add_transition(key, nfa_to_dfa[target_state.id])
        else:
          new_state = DFAState(sc, [target_state])
          nfa_to_dfa[target_state.id] = new_state
          unmarked.add_transition(key, new_state)
          unmarked_queue.append(new_state)

  else:
    eclosure = epsilon_closure([nfa.start_state])
    start_state = DFAState(sc, eclosure)
    unmarked_queue = [start_state]
    nfa_to_dfa = {start_state.nfa_state_str: start_state}

    while len(unmarked_queue):
      # mark the current DFA state
      unmarked = unmarked_queue.pop(0)

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
          unmarked.add_transition(key, existing_state)
        else:
          # the target DFA state does not exist -- create it and add transition
          new_state = DFAState(sc, eclosure)
          nfa_to_dfa[new_state.nfa_state_str] = new_state
          unmarked.add_transition(key, new_state)
          unmarked_queue.append(new_state)

  return Automaton(start_state, None)
