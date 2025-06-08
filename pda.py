def load_pda(filename):
    states, symbols, stack_alphabet = [], [], []
    rules = []
    start_state = None
    accept_states = []
    section = None

    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line
                continue
            if section == "[states]":
                states.extend(line.split())
            elif section == "[symbols]":
                symbols.extend(line.split())
            elif section == "[stack]":
                stack_alphabet.extend(line.split())
            elif section == "[rules]":
                parts = line.split("→")
                lhs = parts[0].strip().split()
                rhs = parts[1].strip().split()
                rules.append((lhs[0], lhs[1], lhs[2], rhs[0], rhs[1]))
            elif section == "[start]":
                start_state = line.strip()
            elif section == "[accept]":
                accept_states.extend(line.split())
    return states, symbols, stack_alphabet, rules, start_state, accept_states


def simulate_pda(states, symbols, stack_alphabet, rules, start_state, accept_states, input_str):
    from collections import deque
    stack = []
    queue = deque()
    visited = set()  # Track visited (state, input, stack snapshot)

    queue.append((start_state, input_str, stack[:]))

    while queue:
        state, remaining_input, current_stack = queue.popleft()

        # If already seen this exact configuration, skip
        config_key = (state, remaining_input, tuple(current_stack))
        if config_key in visited:
            continue
        visited.add(config_key)

        if not remaining_input and state in accept_states:
            return True

        for rule in rules:
            cur_state, input_sym, stack_top, next_state, push_stack = rule
            if state != cur_state:
                continue
            if input_sym != "ε" and (not remaining_input or input_sym != remaining_input[0]):
                continue
            if stack_top != "ε":
                if not current_stack or current_stack[-1] != stack_top:
                    continue
                temp_stack = current_stack[:-1]
            else:
                temp_stack = current_stack[:]

            new_stack = temp_stack[:]
            if push_stack != "ε":
                for symbol in reversed(push_stack):
                    new_stack.append(symbol)

            new_input = remaining_input
            if input_sym != "ε":
                new_input = remaining_input[1:]

            queue.append((next_state, new_input, new_stack))

    return False


states, symbols, stack_alphabet, rules, start_state, accept_states = load_pda("[pda]")

tests = [
    "000111111",  # 3 < 6 - 2 → ACCEPTED
    "00001111",   # 4 = 4 → REJECTED
    "01",         # 1 < 1 + 2 → REJECTED
    "0011111",    # 2 < 5 → 5 > 2 + 2 → ACCEPTED
]

for test in tests:
    result = simulate_pda(states, symbols, stack_alphabet, rules, start_state, accept_states, test)
    print(f"Input: {test} → {'ACCEPTED' if result else 'REJECTED'}")

