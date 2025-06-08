#!/usr/bin/env python3
import sys
from collections import deque

EPSILON_SYMBOLS = {"ε", "epsilon"}

class FiniteAutomaton:
    def __init__(self):
        self.states = set()
        self.symbols = set()
        self.transitions = {}            # (state, symbol) -> set of next states
        self.epsilon_transitions = {}    # state -> set of next states (ε only)
        self.start_state = None
        self.accept_states = set()
        self.type = "DFA"

    def load_from_file(self, path: str) -> str | None:
        try:
            with open(path, "r", encoding="utf8") as f:
                content = f.read()
        except FileNotFoundError:
            return f"[ERROR] File '{path}' not found"

        sections = self._parse_sections(content)

        required = {"states", "symbols", "rules", "start", "accept"}
        missing = required - sections.keys()
        if missing:
            return f"[ERROR] Missing sections: {', '.join(missing)}"

        self.states = set(sections["states"])
        self.symbols = set(sections["symbols"])

        if len(sections["start"]) != 1:
            return "[ERROR] Exactly one start state required"
        self.start_state = sections["start"][0]
        if self.start_state not in self.states:
            return f"[ERROR] Start state '{self.start_state}' not listed in [states]"

        self.accept_states = set(sections["accept"])
        bad_accept = self.accept_states - self.states
        if bad_accept:
            return f"[ERROR] Accept states not in [states]: {', '.join(bad_accept)}"

        self._process_rules(sections["rules"])

        if "epsilon" in sections and sections["epsilon"]:
            self._process_epsilon(sections["epsilon"])
            self.type = "NFA"

        return None

    def _parse_sections(self, text: str) -> dict[str, list[str]]:
        sections = {}
        current = None
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                current = line[1:-1].strip().lower()
                sections[current] = []
            elif current:
                sections[current].append(line)
        return sections

    def _process_rules(self, lines: list[str]) -> None:
        for rule in lines:
            tokens = rule.split()
            if len(tokens) < 3:
                continue
            from_state = tokens[0]
            symbol = tokens[1]
            to_state = " ".join(tokens[2:])

            if from_state not in self.states or to_state not in self.states:
                continue

            if symbol in EPSILON_SYMBOLS:
                self.epsilon_transitions.setdefault(from_state, set()).add(to_state)
                self.type = "NFA"
            else:
                if symbol not in self.symbols:
                    continue
                key = (from_state, symbol)
                self.transitions.setdefault(key, set()).add(to_state)
                if len(self.transitions[key]) > 1:
                    self.type = "NFA"

    def _process_epsilon(self, lines: list[str]) -> None:
        for line in lines:
            tokens = line.split()
            if len(tokens) < 2:
                continue
            frm, to = tokens[0], " ".join(tokens[1:])
            if frm in self.states and to in self.states:
                self.epsilon_transitions.setdefault(frm, set()).add(to)

    def _epsilon_closure(self, states: set[str]) -> set[str]:
        closure = set(states)
        q = deque(states)
        while q:
            state = q.popleft()
            for nxt in self.epsilon_transitions.get(state, ()):
                if nxt not in closure:
                    closure.add(nxt)
                    q.append(nxt)
        return closure

    def _move(self, states: set[str], symbol: str) -> set[str]:
        next_states = set()
        for s in states:
            next_states.update(self.transitions.get((s, symbol), ()))
        return next_states

    def _next(self, states: set[str], symbol: str) -> set[str]:
        after = self._move(states, symbol)
        return self._epsilon_closure(after) if self.type == "NFA" else after

    def get_possible_transitions(self, current_states: set[str], symbol: str) -> set[str]:
        return self._next(current_states, symbol)

    def run(self, input_string: str) -> tuple[bool, set[str]]:
        states = self._epsilon_closure({self.start_state}) if self.type == "NFA" else {self.start_state}
        for ch in input_string:
            if ch not in self.symbols:
                return False, states
            states = self._next(states, ch)
            if not states:
                return False, states
        return bool(states & self.accept_states), states

    def interactive(self):
        print(f"\n=== Interactive {self.type} === (start: {self.start_state})")
        print("Allowed symbols:", ", ".join(sorted(self.symbols)))
        print("Commands:  reset | status | quit")
        print("-" * 50)

        states = self._epsilon_closure({self.start_state}) if self.type == "NFA" else {self.start_state}
        tape = ""

        def status():
            acc = states & self.accept_states
            print(f"[states] {sorted(states)}   [tape] '{tape or '(empty)'}'" +
                  ("   ✅ ACCEPTING" if acc else ""))

        status()
        while True:
            inp = input(">> ").strip().lower()
            if inp in {"quit", "exit"}:
                break
            if inp == "reset":
                states = self._epsilon_closure({self.start_state}) if self.type == "NFA" else {self.start_state}
                tape = ""
                status()
                continue
            if inp == "status":
                status()
                continue
            if len(inp) != 1:
                print("Enter exactly one symbol.")
                continue
            sym = inp
            if sym not in self.symbols:
                print("Invalid symbol.")
                continue

            next_states = self.get_possible_transitions(states, sym)
            if not next_states:
                print("❌  No transition: stuck.")
                continue

            states = next_states
            tape += sym
            status()

            if states & self.accept_states:
                print("\n🎉  String accepted!\n")
                break


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python fa_sim.py  <file>            # interactive")
        print("  python fa_sim.py  <file>  <string>  # test a string")
        return

    fa = FiniteAutomaton()
    err = fa.load_from_file(sys.argv[1])
    if err:
        print(err)
        return

    print(f"Loaded {fa.type}: {len(fa.states)} states, "
          f"{len(fa.symbols)} symbols, start={fa.start_state}, "
          f"accept={', '.join(fa.accept_states)}")

    if len(sys.argv) == 3:
        s = sys.argv[2]
        ok, end = fa.run(s)
        print("ACCEPTED" if ok else "REJECTED", "-- ended in", sorted(end))
    else:
        fa.interactive()


if __name__ == "__main__":
    main()
