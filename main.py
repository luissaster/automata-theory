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
# Pedro Augusto Simões da Cruz - 8116 - T1
# -----------------------------------------------------------------

from automaton import Automaton
from interface import input_automaton, print_automaton
from misc import check_equivalence, generate_automaton_image, generate_txt_report, simulate_word

def main():
    """
    Example of how to define an automaton
    states = ['q0', 'q1', 'q2', 'q3', 'q4']
    alphabet = ['a', 'b']
    transitions = {
        'q0': {'a': ['q1']},
        'q1': {'a': ['q3'], 'b': ['q2']},
        'q2': {'a': ['q4'], 'b': ['q2']},
        'q3': {'a': ['q3'], 'b': ['q2']},
        'q4': {'a': ['q3'], 'b': ['q2']}
    }

    initial_state = 'q0'
    final_states = ['q3', 'q4']
    is_dfa = True

    definido = Automaton(states, alphabet, transitions, initial_state, final_states, is_dfa)
    """
    
    automaton_instance = None
    converted_automaton = None
    minimized_automaton = None

    while True:
        print("\nMenu:\n")
        print("1. Insert automaton")
        print("2. Convert automaton to DFA")
        print("3. Minimize DFA")
        print("4. Simulate word acceptance (Inserted and converted automaton)")
        print("5. Check equivalence between automata (Inserted and converted automaton)")
        print("6. Generate .txt file")
        print("\n0. Exit")
        option = input("Choose an option: ")

        if option == "1":
            automaton_instance = input_automaton()
            if automaton_instance:
                print_automaton(automaton_instance)
                image_name = "inserted_automaton.png"
                generate_automaton_image(automaton_instance, image_name=image_name, image_format="png")
        elif option == "2":
            if automaton_instance:
                converted_automaton = automaton_instance.convert_to_dfa()
                print("Automaton converted successfully.")
                if converted_automaton:
                    print_automaton(converted_automaton)
                    image_name = "converted_automaton.png"
                    generate_automaton_image(converted_automaton, image_name=image_name, image_format="png")
            else:
                print("Automaton not inserted.")
        elif option == "3":
            if converted_automaton:
                minimized_automaton = converted_automaton.minimize_dfa()
                print("DFA minimized successfully.")
                if minimized_automaton:
                    print_automaton(minimized_automaton)
                    image_name = "minimized_automaton.png"
                    generate_automaton_image(minimized_automaton, image_name=image_name, image_format="png")
            else:
                print("Converted automaton not available.")
        elif option == "4":
            if automaton_instance or converted_automaton:
                word = input("Enter the word to be simulated: ")
                if automaton_instance:
                    result_instance = simulate_word(automaton_instance, word)
                    print(f"Word acceptance by the inserted automaton: {'Accepted' if result_instance else 'Not accepted'}")
                if converted_automaton:
                    result_converted = simulate_word(converted_automaton, word)
                    print(f"Word acceptance by the converted automaton: {'Accepted' if result_converted else 'Not accepted'}")
            else:
                print("Automaton not available.")
        elif option == "5":
            if automaton_instance and converted_automaton:
                if check_equivalence(automaton_instance, converted_automaton):
                    print("The automata are equivalent.")
                else:
                    print("The automata are not equivalent.")
            else:
                print("Inserted or converted automaton not available.")
        elif option == "6":
            if automaton_instance and converted_automaton and minimized_automaton:
                generate_txt_report(automaton_instance, converted_automaton, minimized_automaton)
                print("Report generated successfully.")
            else:
                print("Inserted, converted, or minimized automaton not available.")
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

