# Projeto da disciplina SIN 131 - INTRODUÇÃO À TEORIA DA COMPUTAÇÃO
# Universidade Federal de Viçosa - Campus Rio Paranaíba
# -----------------------------------------------------------------
# Desenvolvimento de um programa que realize a conversão de autômatos finitos não determinísticos
# em autômatos finitos determinísticos.
# -----------------------------------------------------------------
# Conceitos:
# NFA (Nondeterministic finite automaton) -> Autômato finito não determinístico.
# DFA (Deterministic finite automaton) -> Autômato finito determinístico.
# -----------------------------------------------------------------
# Luís Fernando Almeida - 8102 - T1
# Pedro Augusto - - T1
# -----------------------------------------------------------------

import graphviz

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

def input_automaton():
    states = input("Enter the states separated by comma: ").split(",")
    alphabet = input("Enter the alphabet separated by comma: ").split(",")
    transitions = {}
    for state in states:
        transitions[state] = {}
        for symbol in alphabet:
            next_states = input(f"Enter the next states for {state} and {symbol} separated by comma: ").split(",")
            transitions[state][symbol] = next_states if next_states != [''] else []
    initial_state = input("Enter the initial state: ")
    final_states = input("Enter the final states separated by comma: ").split(",")
    is_dfa = input("Is it a DFA (Deterministic finite automaton)?\nY for yes, N for no: ").lower() == "y"
    return Automaton(states, alphabet, transitions, initial_state, final_states, is_dfa)

def print_automaton(automaton_instance):
    print(f"States: {automaton_instance.states}")
    print(f"Alphabet: {automaton_instance.alphabet}")
    print("Transitions:")
    for state in automaton_instance.states:
        print(f"  {state}:")
        for symbol in automaton_instance.alphabet:
            next_states = automaton_instance.get_next_states(state, symbol)
            print(f"    {symbol} ---> {', '.join(next_states)}")
    print(f"Initial State: {automaton_instance.initial_state}")
    print(f"Final States: {', '.join(automaton_instance.final_states)}")

def generate_automaton_image(automaton_instance, image_name="automaton_image", image_format="png"):
    dot = graphviz.Digraph(comment='Automaton', format=image_format)
    for state in automaton_instance.states:
        if state in automaton_instance.final_states:
            dot.node(state, state, style='filled', fillcolor='green')
        else:
            dot.node(state, state)
        for symbol in automaton_instance.alphabet:
            next_states = automaton_instance.transitions[state].get(symbol, [])
            for next_state in next_states:
                if next_state not in automaton_instance.states:
                    continue
                dot.edge(state, next_state, symbol)
    dot.render(image_name, view=True, format=image_format)

def main():
    automaton_instance = input_automaton()
    print_automaton(automaton_instance)
    generate_automaton_image(automaton_instance, image_name="automato_inserido", image_format="png")

    converted_automaton = automaton_instance.convert_to_dfa()
    print_automaton(converted_automaton)
    generate_automaton_image(converted_automaton, image_name="automato_convertido", image_format="png")

if __name__ == "__main__":
    main()
