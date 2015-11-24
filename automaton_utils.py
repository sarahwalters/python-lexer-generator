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
  def pretty_print(self, states_seen=[]):
    pretty_transitions = ['%s on %s' % self.pretty_tuple(key) for key in self.transitions]
    print '%s: ' % self.id + ', '.join(pretty_transitions)

    # recurse:
    for key in self.transitions:
      states_seen_update = [state.id for state in self.transitions[key]]
      new_states_seen = list(set(states_seen + states_seen_update))

      for state in self.transitions[key]:
        if state.id not in states_seen:
          state.pretty_print(states_seen=new_states_seen)


class Automaton:
  # https://swtch.com/~rsc/regexp/regexp1.html
  def __init__(self, start_state, end_state):
    self.start_state = start_state
    self.end_state = end_state

  def pretty_print(self):
    self.start_state.pretty_print()
