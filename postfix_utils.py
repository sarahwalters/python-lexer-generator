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
