def load():
    states = []
    alphabet = []
    transitions = {}
    final_states = []
    start_state = None
    epsilon_transitions = {}
    sections = []

    with open("[nfa2]") as file:
        for line in file:
            line = line.strip()
            if line.startswith("[") and line.endswith("]"):
                sections.append(line)
    
    section = None
    with open("[nfa2]") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line in sections:
                section = line
                continue

            if section == "[states]":
                states.extend(line.split())

            elif section == "[symbols]":
                alphabet.extend(line.split())

            elif section == "[rules]":
                parts = line.split()
                if len(parts) == 3:
                    state, symbol, next_state = parts
                    if state not in states or next_state not in states:
                        print(f"Wrong rule!! {state} {symbol} {next_state}")
                        continue
                    if symbol == "ε":
                        if state not in epsilon_transitions:
                            epsilon_transitions[state] = set()
                        epsilon_transitions[state].add(next_state)
                    else:
                        if symbol not in alphabet:
                            print(f"Wrong rule!! {state} {symbol} {next_state}")
                            continue
                        if state not in transitions:
                            transitions[state] = {}
                        if symbol not in transitions[state]:
                            transitions[state][symbol] = set()
                        transitions[state][symbol].add(next_state)

            elif section == "[start]":
                if line not in states:
                    print("start_state not in states")
                    continue
                start_state = line

            elif section == "[accept]":
                final_states.extend(line.split())

    return states, alphabet, transitions, epsilon_transitions, final_states, start_state
def epsilon_closure(state, epsilon_transitions):
    closure = set()
    stack = [state]
    
    while stack:
        current = stack.pop()
        if current not in closure:
            closure.add(current)
            if current in epsilon_transitions:
                stack.extend(epsilon_transitions[current])
    
    return closure


def process_nfa(states, alphabet, transitions, epsilon_transitions, final_states, start_state, input):
    current_states = epsilon_closure(start_state, epsilon_transitions)
    for symbol in input:
        next_states = set()
        
        for state in current_states:
            if state in transitions and symbol in transitions[state]:
                for next_state in transitions[state][symbol]:
                    next_states.update(epsilon_closure(next_state, epsilon_transitions))
        
        current_states = next_states
    print(current_states)
    return any(state in final_states for state in current_states)


states, alphabet, transitions, epsilon_transitions, final_states, start_state = load()
test_inputs = ["", "0", "01", "001", "110", "1010", "0101", "111", "000", "000111"]
for test_input in test_inputs:
    result = process_nfa(states, alphabet, transitions, epsilon_transitions, final_states, start_state, test_input)
    print(f"Input: {test_input} → {'Accepted' if result else 'Rejected'}")


