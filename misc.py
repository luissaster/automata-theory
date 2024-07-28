# This file includes miscellaneous functions used in the program.
# That is: generate_automaton_image(), simulate_word(), check_equivalence(), generate_txt_report()

import os
import graphviz
from itertools import product

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
    
    # Cleanup = True
    output_path = dot.render(filename=os.path.join(output_dir, image_name), format=image_format, view=True, cleanup=True)
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