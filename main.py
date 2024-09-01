# Projeto da disciplina SIN 131 - INTRODUÇÃO À TEORIA DA COMPUTAÇÃO
# Universidade Federal de Viçosa - Campus Rio Paranaíba
# -----------------------------------------------------------------
# Desenvolvimento de um programa que realize a conversão de autômatos finitos não determinísticos
# em autômatos finitos determinísticos.
#
# Desenvolver um programa que receba a especificação de uma Máquina de Turing (MT) e uma palavra 
# de entrada, e determine se essa palavra pertence ou não à linguagem reconhecida por essa máquina.
# -----------------------------------------------------------------
# Conceitos:
# NFA (Nondeterministic finite automaton) -> Autômato finito não determinístico.
# DFA (Deterministic finite automaton) -> Autômato finito determinístico.
# -----------------------------------------------------------------
# Luís Fernando Almeida - 8102 - T1
# Pedro Augusto Simões da Cruz - 8116 - T1
# -----------------------------------------------------------------

from functions import Automaton, TuringMachine_BinaryIncrement, TuringMachine_BalanceParantheses
from interface import input_automaton, print_automaton
from misc import check_equivalence, generate_automaton_image, generate_txt_report, simulate_word
        
def main():
    """
    Main program loop that shows a menu to the user and asks for input.
    """
    while True:
        print("\nMenu:\n")
        print("1. Insert automaton")
        print("2. Convert automaton to DFA")
        print("3. Minimize DFA")
        print("4. Simulate word acceptance (Inserted and converted automaton)")
        print("5. Check equivalence between automata (Inserted and converted automaton)")
        print("6. Generate .txt file")
        print("7. Run binary increment Turing machine")
        print("8. Run parentheses balance Turing machine")
        print("\n0. Exit")
        option = input("Choose an option: ")

        if option == "1":
            automaton = input_automaton()
            if automaton:
                print_automaton(automaton)
                generate_automaton_image(automaton, image_name="inserted_automaton.png", image_format="png")
        elif option == "2":
            if automaton:
                converted_automaton = automaton.convert_to_dfa()
                print("Automaton converted successfully.")
                if converted_automaton:
                    print_automaton(converted_automaton)
                    generate_automaton_image(converted_automaton, image_name="converted_automaton.png", image_format="png")
        elif option == "3":
            if converted_automaton:
                minimized_automaton = converted_automaton.minimize_dfa()
                print("DFA minimized successfully.")
                if minimized_automaton:
                    print_automaton(minimized_automaton)
                    generate_automaton_image(minimized_automaton, image_name="minimized_automaton.png", image_format="png")
        elif option == "4":
            if automaton or converted_automaton:
                word = input("Enter the word to be simulated: ")
                if automaton:
                    result = simulate_word(automaton, word)
                    print(f"Word acceptance by the inserted automaton: {'Accepted' if result else 'Not accepted'}")
                if converted_automaton:
                    result = simulate_word(converted_automaton, word)
                    print(f"Word acceptance by the converted automaton: {'Accepted' if result else 'Not accepted'}")
        elif option == "5":
            if automaton and converted_automaton:
                if check_equivalence(automaton, converted_automaton):
                    print("The automata are equivalent.")
                else:
                    print("The automata are not equivalent.")
        elif option == "6":
            if automaton and converted_automaton and minimized_automaton:
                generate_txt_report(automaton, converted_automaton, minimized_automaton)
                print("Report generated successfully.")
        elif option == "7":
            input_tape = input("Enter the binary number to be incremented: ")
            tmBinary = TuringMachine_BinaryIncrement(input_tape)
            tmBinary.run()
            print("Result after increment:", tmBinary.get_tape())
        elif option == "8":
            input_tape = input("Enter the parentheses: ")
            tmBalance = TuringMachine_BalanceParantheses(input_tape)
            result = tmBalance.run()
            print("The result is:", result)
        elif option == "0":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

