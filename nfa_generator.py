class NFA():
  def __init__(self, regexp):
    self.regexp = regexp
    self.state_counter = -1
    self.states = []

  def add_state(self, state):
    self.state_counter += 1
    state.state_number = self.state_counter
    self.states.append(state)

class State():
  def __init__(self, nfa):
    self.nfa = nfa
    self.nfa.add_state(self)
