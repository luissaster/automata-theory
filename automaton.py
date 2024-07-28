# This file includes the Automaton class and its methods.
# That is: get_next_states(), convert_to_dfa(), minimize_dfa()

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
        if self.is_dfa:
            return self

        # Initialize DFA components
        dfa_states = []
        dfa_transitions = {}
        dfa_initial_state = frozenset([self.initial_state])
        dfa_final_states = set()

        # Queue for processing states
        queue = [dfa_initial_state]
        dfa_states.append(dfa_initial_state)

        while queue:
            current = queue.pop(0)
            dfa_transitions[current] = {}
            
            for symbol in self.alphabet:
                next_states = set()
                
                for state in current:
                    next_states.update(self.get_next_states(state, symbol))
                
                next_states = frozenset(next_states)
                
                if next_states not in dfa_states:
                    dfa_states.append(next_states)
                    queue.append(next_states)
                
                dfa_transitions[current][symbol] = next_states
            
            # Check for final states
            if current & set(self.final_states):
                dfa_final_states.add(current)
        
        # Convert state sets to strings
        dfa_state_names = {state: str(index) for index, state in enumerate(dfa_states)}
        dfa_transitions_named = {dfa_state_names[state]: {symbol: dfa_state_names[next_state] for symbol, next_state in trans.items()} for state, trans in dfa_transitions.items()}
        dfa_initial_state_named = dfa_state_names[dfa_initial_state]
        dfa_final_states_named = {dfa_state_names[state] for state in dfa_final_states}

        return Automaton(
            states=list(dfa_state_names.values()),
            alphabet=self.alphabet,
            transitions=dfa_transitions_named,
            initial_state=dfa_initial_state_named,
            final_states=list(dfa_final_states_named),
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