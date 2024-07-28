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
import os
from itertools import product

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

        # Step 2: Distinguish states using the Myhill-Nerode theorem
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
    dot = graphviz.Digraph()
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

    # Create the directory if it doesn't exist
    output_dir = "img"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = dot.render(filename=os.path.join(output_dir, image_name), format=image_format, view=True)
    print(f"Graph saved as {output_path}")

def simulate_word(automaton_instance, word):
    current_states = {automaton_instance.initial_state}
    for symbol in word:
        next_states = set()
        for state in current_states:
            next_states.update(automaton_instance.get_next_states(state, symbol))
        current_states = next_states
    return any(state in automaton_instance.final_states for state in current_states)

def check_equivalence(automaton1, automaton2):
    # Checking equivalence is complex; here we only check if both accept the same words up to a given length
    for word_length in range(5):
        for word in product(automaton1.alphabet, repeat=word_length):
            word = ''.join(word)
            if simulate_word(automaton1, word) != simulate_word(automaton2, word):
                return False
    return True

def generate_txt_report(automaton1, automaton2, minimized_automaton, filename="report_automaton.txt"):
    with open(filename, 'w') as file:
        file.write("Automaton 1:\n")
        file.write(f"States: {', '.join(automaton1.states)}\n")
        file.write(f"Alphabet: {', '.join(automaton1.alphabet)}\n")
        file.write("Transitions:\n")
        for state in automaton1.states:
            for symbol in automaton1.alphabet:
                next_states = automaton1.get_next_states(state, symbol)
                file.write(f"  {state} --{symbol}--> {', '.join(next_states)}\n")
        file.write(f"Initial State: {automaton1.initial_state}\n")
        file.write(f"Final States: {', '.join(automaton1.final_states)}\n\n")

        file.write("Automaton 2:\n")
        file.write(f"States: {', '.join(automaton2.states)}\n")
        file.write(f"Alphabet: {', '.join(automaton2.alphabet)}\n")
        file.write("Transitions:\n")
        for state in automaton2.states:
            for symbol in automaton2.alphabet:
                next_states = automaton2.get_next_states(state, symbol)
                file.write(f"  {state} --{symbol}--> {', '.join(next_states)}\n")
        file.write(f"Initial State: {automaton2.initial_state}\n")
        file.write(f"Final States: {', '.join(automaton2.final_states)}\n\n")

        file.write("Minimized Automaton:\n")
        file.write(f"States: {', '.join(minimized_automaton.states)}\n")
        file.write(f"Alphabet: {', '.join(minimized_automaton.alphabet)}\n")
        file.write("Transitions:\n")
        for state in minimized_automaton.states:
            for symbol in minimized_automaton.alphabet:
                next_states = minimized_automaton.get_next_states(state, symbol)
                file.write(f"  {state} --{symbol}--> {', '.join(next_states)}\n")
        file.write(f"Initial State: {minimized_automaton.initial_state}\n")
        file.write(f"Final States: {', '.join(minimized_automaton.final_states)}\n")

def main():
    automaton_instance = None
    converted_automaton = None
    minimized_automaton = None

    while True:
        print("\nMenu:\n")
        print("1. Inserir automato")
        print("2. Visualizar automato (print e criar imagem)")
        print("3. Converter automato")
        print("4. Visualizar automato convertido (print e criar imagem)")
        print("5. Minimizar AFD")
        print("6. Visualizar AFD minimizado (print e criar imagem)")
        print("7. Simular aceitação de palavra no automato inserido")
        print("8. Simular aceitação de palavra no automato convertido")
        print("9. Checar equivalencia entre os automatos")
        print("10. Gerar arquivo .txt com os automatos")
        print("\n0. Sair")
        option = input("Escolha uma opção: ")

        if option == "1":
            automaton_instance = input_automaton()
        elif option == "2":
            if automaton_instance:
                print_automaton(automaton_instance)
                generate_automaton_image(automaton_instance, image_name="inserted_automaton", image_format="png")
            else:
                print("Automato não inserido.")
        elif option == "3":
            if automaton_instance:
                converted_automaton = automaton_instance.convert_to_dfa()
                print("Automato convertido com sucesso.")
            else:
                print("Automato não inserido.")
        elif option == "4":
            if converted_automaton:
                print_automaton(converted_automaton)
                generate_automaton_image(converted_automaton, image_name="converted_automaton", image_format="png")
            else:
                print("Automato convertido não disponível.")
        elif option == "5":
            if converted_automaton:
                minimized_automaton = converted_automaton.minimize_dfa()
                print("AFD minimizado com sucesso.")
            else:
                print("Automato convertido não disponível.")
        elif option == "6":
            if minimized_automaton:
                print_automaton(minimized_automaton)
                generate_automaton_image(minimized_automaton, image_name="minimized_automaton", image_format="png")
            else:
                print("AFD minimizado não disponível.")
        elif option == "7":
            if automaton_instance:
                word = input("Digite a palavra a ser simulada: ")
                if simulate_word(automaton_instance, word):
                    print("Palavra aceita pelo automato inserido.")
                else:
                    print("Palavra não aceita pelo automato inserido.")
            else:
                print("Automato não inserido.")
        elif option == "8":
            if converted_automaton:
                word = input("Digite a palavra a ser simulada: ")
                if simulate_word(converted_automaton, word):
                    print("Palavra aceita pelo automato convertido.")
                else:
                    print("Palavra não aceita pelo automato convertido.")
            else:
                print("Automato convertido não disponível.")
        elif option == "9":
            if automaton_instance and converted_automaton:
                if check_equivalence(automaton_instance, converted_automaton):
                    print("Os automatos são equivalentes.")
                else:
                    print("Os automatos não são equivalentes.")
            else:
                print("Automato inserido ou convertido não disponível.")
        elif option == "10":
            if automaton_instance and converted_automaton and minimized_automaton:
                generate_txt_report(automaton_instance, converted_automaton, minimized_automaton)
                print("Relatório gerado com sucesso.")
            else:
                print("Automato inserido, convertido ou minimizado não disponível.")
        elif option == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
