from postfix_utils import regex_to_postfix
from automaton_utils import StateCounter, NFAState, Automaton


def generate_nfa(regex):
  #try:
  sc = StateCounter('nfa')
  postfix = regex_to_postfix(regex)
  stack = []

  # doesn't support intervals yet
  for c in postfix:

    if c == '*':
      nfa = stack.pop()
      # push new nfa which accepts zero or more of nfa
      accepting = NFAState(sc, {})
      nfa.start_state.add_transitions('epsilon', accepting)
      nfa.end_state.add_transitions('epsilon', nfa.start_state)
      new_nfa = Automaton(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '+': # one or more
      nfa = stack.pop()
      # push new nfa which accepts one or more of nfa
      accepting = NFAState(sc, {})
      nfa.end_state.add_transitions('epsilon', nfa.start_state)
      nfa.end_state.add_transitions('epsilon', accepting)
      new_nfa = Automaton(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '?': # zero or one
      nfa = stack.pop()
      # push new nfa which accepts zero or one of nfa
      accepting = NFAState(sc, {})
      nfa.start_state.add_transitions('epsilon', accepting)
      nfa.end_state.add_transitions('epsilon', accepting)
      new_nfa = Automaton(nfa.start_state, accepting)
      stack.append(new_nfa)

    elif c == '|':
      nfa2 = stack.pop()
      nfa1 = stack.pop()
      # push new nfa which accepts alternation of nfa1 or nfa2
      accepting = NFAState(sc, {})
      state = NFAState(sc, {'epsilon':[nfa1.start_state, nfa2.start_state]})
      nfa1.end_state.add_transitions('epsilon', accepting)
      nfa2.end_state.add_transitions('epsilon', accepting)
      new_nfa = Automaton(state, accepting)
      stack.append(new_nfa)

    elif c == chr(8):
      nfa2 = stack.pop()
      nfa1 = stack.pop()
      # push new nfa which accepts concatenation of nfa1 and nfa2
      nfa1.end_state.add_transitions('epsilon', nfa2.start_state)
      new_nfa = Automaton(nfa1.start_state, nfa2.end_state)
      stack.append(new_nfa)

    else:
      # push nfa which accepts character c
      accepting = NFAState(sc, {})
      state = NFAState(sc, {c:[accepting]})
      new_nfa = Automaton(state, accepting)
      stack.append(new_nfa)

  if len(stack) != 1:
    raise RuntimeError("%s is not a supported regular expression" % regex)

  return stack[0]
