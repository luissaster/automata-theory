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

from interface import input_automaton, print_automaton
from misc import check_equivalence, generate_automaton_image, generate_txt_report, simulate_word

def main():
    automaton_instance = None
    converted_automaton = None
    minimized_automaton = None

    while True:
        print("\nMenu:\n")
        print("1. Insert automaton")
        print("2. View automaton (print and create image)")
        print("3. Convert automaton")
        print("4. View converted automaton (print and create image)")
        print("5. Minimize DFA")
        print("6. View minimized DFA (print and create image)")
        print("7. Simulate word acceptance in the inserted automaton")
        print("8. Simulate word acceptance in the converted automaton")
        print("9. Check equivalence between automata")
        print("10. Generate .txt file with the automata")
        print("\n0. Exit")
        option = input("Choose an option: ")

        if option == "1":
            automaton_instance = input_automaton()
        elif option == "2":
            if automaton_instance:
                print_automaton(automaton_instance)
                generate_automaton_image(automaton_instance, image_name="inserted_automaton", image_format="png")
            else:
                print("Automaton not inserted.")
        elif option == "3":
            if automaton_instance:
                converted_automaton = automaton_instance.convert_to_dfa()
                print("Automaton converted successfully.")
            else:
                print("Automaton not inserted.")
        elif option == "4":
            if converted_automaton:
                print_automaton(converted_automaton)
                generate_automaton_image(converted_automaton, image_name="converted_automaton", image_format="png")
            else:
                print("Converted automaton not available.")
        elif option == "5":
            if converted_automaton:
                minimized_automaton = converted_automaton.minimize_dfa()
                print("DFA minimized successfully.")
            else:
                print("Converted automaton not available.")
        elif option == "6":
            if minimized_automaton:
                print_automaton(minimized_automaton)
                generate_automaton_image(minimized_automaton, image_name="minimized_automaton", image_format="png")
            else:
                print("Minimized DFA not available.")
        elif option == "7":
            if automaton_instance:
                word = input("Enter the word to be simulated: ")
                if simulate_word(automaton_instance, word):
                    print("Word accepted by the inserted automaton.")
                else:
                    print("Word not accepted by the inserted automaton.")
            else:
                print("Automaton not inserted.")
        elif option == "8":
            if converted_automaton:
                word = input("Enter the word to be simulated: ")
                if simulate_word(converted_automaton, word):
                    print("Word accepted by the converted automaton.")
                else:
                    print("Word not accepted by the converted automaton.")
            else:
                print("Converted automaton not available.")
        elif option == "9":
            if automaton_instance and converted_automaton:
                if check_equivalence(automaton_instance, converted_automaton):
                    print("The automata are equivalent.")
                else:
                    print("The automata are not equivalent.")
            else:
                print("Inserted or converted automaton not available.")
        elif option == "10":
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
