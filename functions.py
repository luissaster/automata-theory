class Automaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states, is_dfa):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states
        self.is_dfa = is_dfa
    
    def get_next_states(self, state, symbol):
        next_states = set()
        if state in self.transitions and symbol in self.transitions[state]:
            next_states.update(self.transitions[state][symbol])
        return next_states
    
    def convert_to_dfa(self):
        dfa_states = []
        dfa_transitions = {}
        initial_state = frozenset([self.initial_state])
        final_states = set()

        # Queue for processing states
        queue = [initial_state]
        dfa_states.append(initial_state)

        while queue:
            current_state = queue.pop(0)
            dfa_transitions[current_state] = {}

            for symbol in self.alphabet:
                next_states = set()

                for state in current_state:
                    next_states.update(self.get_next_states(state, symbol))

                next_state = frozenset(next_states)

                if next_state not in dfa_states:
                    dfa_states.append(next_state)
                    queue.append(next_state)

                dfa_transitions[current_state][symbol] = next_state

            # Check for final states
            if current_state & set(self.final_states):
                final_states.add(current_state)

        # Convert state sets to strings
        state_map = {state: str(index) for index, state in enumerate(dfa_states)}
        transitions_named = {state_map[state]: {symbol: state_map[next_state] for symbol, next_state in trans.items()} for state, trans in dfa_transitions.items()}
        initial_state_named = state_map[initial_state]
        final_states_named = {state_map[state] for state in final_states}

        return Automaton(
            states=list(state_map.values()),
            alphabet=self.alphabet,
            transitions=transitions_named,
            initial_state=initial_state_named,
            final_states=list(final_states_named),
            is_dfa=True
        )
    
    def minimize_dfa(self):
        if not self.is_dfa:
            raise ValueError("Minimization can only be applied to DFA.")

        # Step 1: Remove unreachable states
        reachable_states = {self.initial_state}
        queue = [self.initial_state]
        
        while queue:
            state = queue.pop(0)
            for symbol in self.alphabet:
                next_state = self.transitions[state][symbol]
                if next_state not in reachable_states:
                    reachable_states.add(next_state)
                    queue.append(next_state)
        
        self.states = list(reachable_states)
        self.transitions = {state: trans for state, trans in self.transitions.items() if state in reachable_states}
        self.final_states = [state for state in self.final_states if state in reachable_states]

        # Step 2: Applying the Myhill-Nerode theorem
        partition = [set(self.final_states), set(self.states) - set(self.final_states)]
        
        while True:
            new_partition = []
            for group in partition:
                grouped_states = {}
                for state in group:
                    signature = tuple(sorted([(symbol, self.transitions[state][symbol]) for symbol in self.alphabet]))
                    if signature not in grouped_states:
                        grouped_states[signature] = set()
                    grouped_states[signature].add(state)
                new_partition.extend(grouped_states.values())
            if len(new_partition) == len(partition):
                break
            partition = new_partition
        
        # Step 3: Create the new minimized DFA
        state_map = {state: idx for idx, group in enumerate(partition) for state in group}
        minimized_states = [str(idx) for idx in range(len(partition))]
        minimized_transitions = {str(idx): {} for idx in range(len(partition))}
        minimized_final_states = {str(state_map[state]) for state in self.final_states}
        minimized_initial_state = str(state_map[self.initial_state])
        
        for group in partition:
            representative = next(iter(group))
            for symbol in self.alphabet:
                next_state = self.transitions[representative][symbol]
                minimized_transitions[str(state_map[representative])][symbol] = str(state_map[next_state])

        return Automaton(
            states=minimized_states,
            alphabet=self.alphabet,
            transitions=minimized_transitions,
            initial_state=minimized_initial_state,
            final_states=list(minimized_final_states),
            is_dfa=True
        )

class TuringMachine_BinaryIncrement:
    def __init__(self, tape, blank_symbol="B"):
        self.tape = list(tape) + [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head_position = len(tape) - 1          # Start at the last position of the tape
        self.current_state = "q0"  
        self.transitions = self._define_transitions()

    def _define_transitions(self):
        return {
            ("q0", "1"): ("q0", "0", "L"),          # Replace '1' with '0' and go to the left
            ("q0", "0"): ("q1", "1", "R"),          # Replace '0' with '1' and go to the final state
            ("q0", "B"): ("q1", "1", "R"),          # If you reach the beginning of the tape, add '1'
        }

    def step(self):
        current_symbol = self.tape[self.head_position]
        if (self.current_state, current_symbol) in self.transitions:
            new_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol            # Write the symbol
            self.current_state = new_state                          # Update the state
            self.head_position += 1 if direction == "R" else -1     # Move the head

    def run(self):
        while self.current_state != "q1":
            self.step()

    def get_tape(self):
        return "".join(self.tape).rstrip(self.blank_symbol)

class TuringMachine_BalanceParantheses:
    def __init__(self, tape, blank_symbol="B"):
        self.tape = list(tape) + [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head_position = 0                      # Start at the first position of the tape
        self.current_state = "q0" 
        self.transitions = self._define_transitions()

    def _define_transitions(self):
        return {

            # State q0: Search for the next '(' to mark

            ("q0", "("): ("q1", "X", "R"),          # Mark '(' as 'X' and move right
            ("q0", "X"): ("q0", "X", "R"),          # Ignore 'X' and continue right
            ("q0", "Y"): ("q0", "Y", "R"),          # Ignore 'Y' and continue right
            ("q0", ")"): ("q_reject", ")", "R"),    # Reject if ')' doesn't have a corresponding '('
            ("q0", "B"): ("q_accept", "B", "R"),    # Accept if there are no unbalanced parentheses at the end
            
            # State q1: Search for the next ')' to mark

            ("q1", "("): ("q1", "(", "R"),          # Ignore '(' and continue right
            ("q1", "X"): ("q1", "X", "R"),          # Ignore 'X' and continue right
            ("q1", "Y"): ("q1", "Y", "R"),          # Ignore 'Y' and continue right
            ("q1", ")"): ("q2", "Y", "L"),          # Mark ')' as 'Y' and go back to the left
            ("q1", "B"): ("q_reject", "B", "L"),    # Reject if there is no ')' to mark
            
            # State q2: Go back to the beginning to search for the next '('

            ("q2", "("): ("q2", "(", "L"),          # Go back to the left over '('
            ("q2", ")"): ("q2", ")", "L"),          # Go back to the left over ')'
            ("q2", "X"): ("q0", "X", "R"),          # Go back to state q0 when you find an 'X'
            ("q2", "Y"): ("q2", "Y", "L"),          # Go back to the left over 'Y'

        }

    def step(self):
        current_symbol = self.tape[self.head_position]
        if (self.current_state, current_symbol) in self.transitions:
            new_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol            # Write the symbol
            self.current_state = new_state                          # Update the state
            self.head_position += 1 if direction == "R" else -1     # Move the head

    def run(self):
        while self.current_state not in ["q_accept", "q_reject"]:
            self.step()
        return self.current_state == "q_accept"

    def get_tape(self):
        return "".join(self.tape).rstrip(self.blank_symbol)

