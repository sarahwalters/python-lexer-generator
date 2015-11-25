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
    if self.transitions.has_key(key):
      if type(value) == list:
        self.transitions[key] += value
      else:
        self.transitions[key].append(value)
      self.transitions[key] = list(set(self.transitions[key]))
    else:
      self.transitions[key] = value if type(value) == list else [value]

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
  def __init__(self, state_counter, transitions, nfa_states, accepting_id):
    State.__init__(self, state_counter, transitions)
    nfa_state_ids = [state.id for state in nfa_states]
    self.nfa_state_str = ','.join(sorted(nfa_state_ids))
    self.nfa_states = nfa_states
    self.marked = False
    self.accepting = accepting_id in nfa_state_ids


class Automaton:
  # https://swtch.com/~rsc/regexp/regexp1.html
  def __init__(self, start_state, end_state):
    self.start_state = start_state
    self.end_state = end_state

  def pretty_print(self):
    global states_seen
    states_seen = []
    self.start_state.pretty_print()
