class Counter:
  def __init__(self):
    self.val = 0

class State:
  def __init__(self, transitions):
    self.id = state_counter.val
    state_counter.val += 1
    self.transitions = transitions

  def add_transition(self, key, value):
    print '-'
    if self.transitions.has_key(key):
      self.transitions[key].append(value)
      self.transitions[key] = list(set(self.transitions[key]))
    else:
      self.transitions[key] = [value]

  def pretty_tuple(self, key):
      return ([state.id for state in self.transitions[key]], key)

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


class NFA:
  def __init__(self, start_state, end_state):
    self.start_state = start_state
    self.end_state = end_state

  def pretty_print(self):
    self.start_state.pretty_print()


def create_nfa(regex):
  global state_counter
  state_counter = Counter()
  postfix = regex_to_postfix(regex)
  print postfix
  stack = []

  # doesn't support intervals yet
  for c in postfix:

    if c == '*':
      nfa = stack.pop()
      # push new nfa which accepts zero or more of nfa
      accepting = State({})
      print "Creating %s in *" % accepting.id
      nfa.start_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa.start_state.id, accepting.id)
      nfa.end_state.add_transition('epsilon', nfa.start_state)
      print "Adding eps trans from %s to %s" %(nfa.end_state.id, nfa.start_state.id)
      new_nfa = NFA(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '+': # one or more
      nfa = stack.pop()
      # push new nfa which accepts one or more of nfa
      accepting = State({})
      print "Creating %s in +" % accepting.id
      nfa.end_state.add_transition('epsilon', nfa.start_state)
      print "Adding eps trans from %s to %s" %(nfa1.end_state.id, nfa.start_state.id)
      nfa.end_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa1.end_state.id, accepting.id)
      new_nfa = NFA(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '?': # zero or one
      nfa = stack.pop()
      # push new nfa which accepts zero or one of nfa
      accepting = State({})
      print "Creating %s in ?" % accepting.id
      nfa.start_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa1.start_state.id, accepting.id)
      nfa.end_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa.end_state.id, accepting.id)
      new_nfa = NFA(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '|':
      nfa2 = stack.pop()
      nfa1 = stack.pop()
      # push new nfa which accepts alternation of nfa1 or nfa2
      accepting = State({})
      print "Creating %s in | (acc)" % accepting.id
      state = State({'epsilon':[nfa1.start_state, nfa2.start_state]})
      print "Creating %s in | (state)" % state.id
      nfa1.end_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa1.end_state.id, accepting.id)
      nfa2.end_state.add_transition('epsilon', accepting)
      print "Adding eps trans from %s to %s" %(nfa2.end_state.id, accepting.id)

      new_nfa = NFA(state, accepting)
      stack.append(new_nfa)

    elif c == chr(8):
      nfa2 = stack.pop()
      nfa1 = stack.pop()
      # push new nfa which accepts concatenation of nfa1 and nfa2
      nfa1.end_state.add_transition('epsilon', nfa2.start_state)
      print "Adding eps trans from %s to %s" %(nfa2.start_state.id, nfa1.end_state.id)
      new_nfa = NFA(nfa1.start_state, nfa2.end_state)
      stack.append(new_nfa)

    else:
      # push nfa which accepts character c
      accepting = State({})
      print "Creating %s in else (acc)" % accepting.id
      state = State({c:[accepting]})
      print "Creating %s in else (state)" % state.id
      print "Adding trans on %s from %s to %s" %(c, state.id, accepting.id)
      new_nfa = NFA(state, accepting)
      stack.append(new_nfa)

  return stack

def regex_to_postfix(regex):
  infix = concat_expand(regex)
  postfix = infix_to_postfix(infix)
  return postfix

def concat_expand(regex):
  # https://github.com/burner/dex/blob/master/concatexpand.cpp
  # Mark concatenation locations with chr(8) (backspace char)
  res = ''
  for i in range(len(regex)-1):

    char_left = regex[i]
    char_right = regex[i+1]
    res += char_left

    if char_left not in '-|([' and char_right not in '-|)]+*?':
      res += chr(8)

  res += regex[-1]
  return res

def infix_to_postfix(regex):
  # https://gist.github.com/DmitrySoshnikov/1239804
  # Converts infix notation to postfix -> e.g. a|b becomes ab|
  output = []
  stack = []

  for i, c in enumerate(regex):
      if c == '(':
        stack.append(c)

      elif c == ')':
        while stack[-1] != '(':
          output.append(stack.pop())
        stack.pop() # pop '('

      else:
        while len(stack):
          peeked_precedence = precedence_of(stack[-1])
          current_precedence = precedence_of(c)

          if peeked_precedence >= current_precedence:
            output.append(stack.pop())
          else:
            break
        stack.append(c)

  while len(stack):
    output.append(stack.pop())

  return ''.join(output)


precedence_map = {
  '(':1,
  '|':2,
  chr(8):3,
  '?':4,
  '*':4,
  '+':4,
  '^':5
}

def precedence_of(character):
  if precedence_map.has_key(character):
    return precedence_map[character]
  return 6
