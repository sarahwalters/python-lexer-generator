import copy

class StateCounter:
  def __init__(self, prefix):
    self.prefix = prefix
    self.val = 0

  def tag(self):
    return '%s%s' % (self.prefix, self.val)


class State:
  def __init__(self, state_counter, transitions):
    self.id = state_counter.tag()
    state_counter.val += 1
    self.transitions = transitions

  def add_transitions(self, key, value):
    if type(value) != list:
      value = [value]

    if self.transitions.has_key(key):
      for v in value:
        if not self.find_in(self.transitions[key]):
          self.transitions[key].append(v)
    else:
      self.transitions[key] = value

  def find_in(self, states):
    '''
      Returns true if there is a state in states with an id of state.id
      inputs: states, a list of State objects (either NFAState or DFAState)
              state, a State object (either NFAState or DFAState)
      outputs: boolean
    '''
    matches = [s for s in states if s.id == self.id]
    return len(matches) >= 1

  def pretty_tuple(self, key):
      return ([state.id for state in self.transitions[key]], key)

  # still prints some states multiple times
  def pretty_print(self):
    global states_seen
    states_seen.append(self.id)

    pretty_transitions = ['%s on %s' % self.pretty_tuple(key) for key in self.transitions]
    to_print = '%s: ' % self.id + ', '.join(pretty_transitions)

    if hasattr(self, 'accepting') and self.accepting:
      to_print = '(ACC) ' + to_print

    print to_print

    # recurse:
    for key in self.transitions:
      for state in self.transitions[key]:
        if state.id not in states_seen:
          state.pretty_print()


class NFAState(State):
  def __init__(self, state_counter, transitions):
    State.__init__(self, state_counter, transitions)


class DFAState(State):
  def __init__(self, state_counter, transitions, nfa_states, accepting_id, token):
    State.__init__(self, state_counter, transitions)
    nfa_state_ids = [state.id for state in nfa_states]
    self.nfa_state_str = ','.join(sorted(nfa_state_ids))
    self.nfa_states = nfa_states
    self.marked = False
    self.accepting = accepting_id in nfa_state_ids
    self.token = token


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
        if not s.find_in(eclosure):
          eclosure.append(s)

        # queue state for consideration if it hasn't been considered
        # and isn't already queued
        if not s.find_in(considered_states) and not s.find_in(queue):
          queue.append(s)

  # for state in states:
  #   if not state.find_in(eclosure):
  #     eclosure.append(state)

  return eclosure if len(eclosure) else states
