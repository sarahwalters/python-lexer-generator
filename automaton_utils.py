import copy

class StateCounter:
  def __init__(self, prefix):
    self.prefix = prefix
    self.val = 0

  def tag(self):
    self.val += 1
    return '%s%s' % (self.prefix, self.val)


class Automaton:
  # https://swtch.com/~rsc/regexp/regexp1.html
  def __init__(self, start_state, end_state):
    self.start_state = start_state
    self.end_state = end_state

  def pretty_print(self):
    global states_seen
    states_seen = []
    self.start_state.pretty_print()

  def is_dfa(self):
    queue = [self.start_state]
    considered_states = []

    while len(queue):
      state = queue.pop(0)
      considered_states.append(state)

      for key in state.transitions:
        if len(state.transitions[key]) == 1:
          queue.append(state.transitions[key][0])
        else:
          return False

    return True


class State:
  def __init__(self, state_counter):
    self.id = state_counter.tag()
    self.transitions = {}
    self.accepting = []

  def add_transition(self, key, value):
    ''' Adds a transition from self to value on key
    '''
    if self.transitions.has_key(key):
      self.transitions[key].append(value)
    else:
      self.transitions[key] = [value]

  def find_in(self, states):
    ''' Returns true if there is a state in states with an id of state.id
    '''
    matches = [s for s in states if s.id == self.id]
    return len(matches) >= 1

  def pretty_print(self):
    ''' Displays a state and its transitions in human-readable format
    '''
    global states_seen
    states_seen.append(self)

    pretty_transitions = ['%s on %s' % self._pretty_tuple(key) for key in self.transitions]
    print_base = '%s: ' % self.id + ', '.join(pretty_transitions)
    accepting_prefix = '(ACC ' + ', '.join(self.accepting) + ') '
    print_full = accepting_prefix + print_base if len(self.accepting) > 0 else print_base
    print print_full

    # recurse:
    for key in self.transitions:
      for state in self.transitions[key]:
        if not state.find_in(states_seen):
          state.pretty_print()

  def _pretty_tuple(self, key):
    ''' Helper function for pretty_print -- returns (list of state ids, key) tuples
    '''
    return ([state.id for state in self.transitions[key]], key)


class NFAState(State):
  def __init__(self, state_counter):
    State.__init__(self, state_counter)


class DFAState(State):
  def __init__(self, state_counter, nfa_states):
    State.__init__(self, state_counter)
    self.nfa_states = nfa_states
    self.nfa_state_ids = [state.id for state in self.nfa_states]
    self.nfa_state_str = ','.join(sorted(self.nfa_state_ids))

    self.accepting = []
    for nfa_state in self.nfa_states:
      for token_name in nfa_state.accepting:
        if token_name not in self.accepting:
          self.accepting.append(token_name)


def epsilon_closure(states):
  '''
    Returns the epsilon closure of a set of states in an automaton.
    input: states, a list of State objects (either NFAState or DFAState)
    output: eclosure, the states reachable on epsilon transitions from those states
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
        if not s.find_in(eclosure):
          eclosure.append(s)

        # queue state for consideration if it hasn't been considered
        # and isn't already queued
        if not s.find_in(considered_states) and not s.find_in(queue):
          queue.append(s)

  # (?) include states or not?
  # for state in states:
  #   if not state.find_in(eclosure):
  #     eclosure.append(state)

  return eclosure if len(eclosure) else states
