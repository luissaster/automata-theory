import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from functions import Automaton, TuringMachine_BinaryIncrement, TuringMachine_BalanceParantheses
from misc import check_equivalence, generate_automaton_image, generate_txt_report, simulate_word


class AutomatonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI")
        self.root.geometry("400x400")

        self.testAutomaton = Automaton(
            states=['q0', 'q1', 'q2'],
            initial_state='q0',
            final_states=['q2'],
            alphabet=['a', 'b'],
            transitions={
                'q0': {'a': ['q0', 'q1'], 'b':['q2']},  # On 'a', q0 can stay in q0 or move to q1
                'q1': {'b': ['q2']},        # On 'b', q1 moves to q2
                'q2': {'a': ['q0'], 'b': ['q2']}  # q2 loops on 'a' or 'b'
            },
            is_dfa=False  # Indicating it's an NFA
        )

        self.automaton = None
        self.converted_automaton = None
        self.minimized_automaton = None
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.root, text="Run Test Automaton", command=self.run_test_automaton).pack(pady=10)
        tk.Button(self.root, text="Insert Automaton", command=self.insert_automaton).pack(pady=10)
        tk.Button(self.root, text="Convert to DFA", command=self.convert_to_dfa).pack(pady=10)
        tk.Button(self.root, text="Minimize DFA", command=self.minimize_dfa).pack(pady=10)
        tk.Button(self.root, text="Simulate Word Acceptance", command=self.simulate_word).pack(pady=10)
        tk.Button(self.root, text="Check Equivalence", command=self.check_equivalence).pack(pady=10)
        tk.Button(self.root, text="Generate .txt File", command=self.generate_txt_file).pack(pady=10)
        tk.Button(self.root, text="Run Turing Machines", command=self.run_turing_machines).pack(pady=10)

    def run_test_automaton(self):
        self.show_automaton(self.testAutomaton)
        generate_automaton_image(self.testAutomaton, image_name="inserted_automaton")
        self.automaton = self.testAutomaton
        self.convert_to_dfa()
        self.minimize_dfa()
    
    def insert_automaton(self):
        states = simpledialog.askstring("Input", "Enter states separated by commas (e.g.: q0,q1,...):").split(",")
        alphabet = simpledialog.askstring("Input", "Enter alphabet separated by commas (e.g.: a,b,...):").split(",")
        transitions = {}
        for state in states:
            transitions[state] = {}
            for symbol in alphabet:
                next_states = simpledialog.askstring("Input", f"Enter next states for {state} and {symbol} separated by commas (leave blank for an empty transition):").split(",")
                transitions[state][symbol] = next_states if next_states != [''] else []
        initial_state = simpledialog.askstring("Input", "Enter initial state (e.g.: q0):")
        final_states = simpledialog.askstring("Input", "Enter final states separated by commas (e.g.: q0,q1,...):").split(",")
        is_dfa = simpledialog.askstring("Input", "Is it a DFA (Deterministic Finite Automaton)?\nY for yes, N for no:").lower() == "y"
        self.automaton = Automaton(states, alphabet, transitions, initial_state, final_states, is_dfa)
        self.show_automaton(self.automaton)
        generate_automaton_image(self.automaton, image_name="inserted_automaton") 

    def convert_to_dfa(self):
        if self.automaton:
            self.converted_automaton = self.automaton.convert_to_dfa()
            messagebox.showinfo("Success", "Automaton converted successfully.")
            self.show_automaton(self.converted_automaton)
            generate_automaton_image(self.converted_automaton, image_name="converted_automaton")
        else:
            messagebox.showwarning("Error", "No automaton to convert.")

    def minimize_dfa(self):
        if self.converted_automaton:
            self.minimized_automaton = self.converted_automaton.minimize_dfa()
            messagebox.showinfo("Success", "DFA minimized successfully.")
            self.show_automaton(self.minimized_automaton)
            generate_automaton_image(self.minimized_automaton, image_name="minimized_automaton")
        else:
            messagebox.showwarning("Error", "No DFA to minimize.")

    def simulate_word(self):
        if self.automaton or self.converted_automaton:
            word = simpledialog.askstring("Input", "Enter the word to be simulated:")
            results = []
            if self.automaton:
                result = simulate_word(self.automaton, word)
                results.append(f"Word acceptance by the inserted automaton: {'Accepted' if result else 'Not accepted'}")
            if self.converted_automaton:
                result = simulate_word(self.converted_automaton, word)
                results.append(f"Word acceptance by the converted automaton: {'Accepted' if result else 'Not accepted'}")
            messagebox.showinfo("Word Acceptance", "\n".join(results))
        else:
            messagebox.showwarning("Error", "No automaton available for simulation.")

    def check_equivalence(self):
        if self.automaton and self.converted_automaton:
            if check_equivalence(self.automaton, self.converted_automaton):
                messagebox.showinfo("Equivalence Check", "The automata are equivalent.")
            else:
                messagebox.showinfo("Equivalence Check", "The automata are not equivalent.")
        else:
            messagebox.showwarning("Error", "Both automata must be available for equivalence check.")

    def generate_txt_file(self):
        if self.automaton and self.converted_automaton and self.minimized_automaton:
            generate_txt_report(self.automaton, self.converted_automaton, self.minimized_automaton)
            messagebox.showinfo("Report Generation", "Report generated successfully.")
        else:
            messagebox.showwarning("Error", "All required automata must be available to generate the report.")

    def run_turing_machines(self):
        tm_option = simpledialog.askstring("Input", "Select a Turing Machine to run:\n1. Binary increment\n2. Parentheses balance")
        if tm_option == "1":
            input_tape = simpledialog.askstring("Input", "Enter the binary number to be incremented:")
            tmBinary = TuringMachine_BinaryIncrement(input_tape)
            tmBinary.run()
            messagebox.showinfo("Result", "Result after increment: " + tmBinary.get_tape())
        elif tm_option == "2":
            input_tape = simpledialog.askstring("Input", "Enter the parentheses:")
            tmBalance = TuringMachine_BalanceParantheses(input_tape)
            result = tmBalance.run()
            messagebox.showinfo("Result", "The result is: " + ("Balanced" if result else "Not balanced"))
        else:
            messagebox.showwarning("Error", "Invalid option. Try again.")

    def show_automaton(self, automaton_instance):
        info = f"States: {', '.join(automaton_instance.states)}\n"
        info += f"Alphabet: {', '.join(automaton_instance.alphabet)}\n"
        info += "Transitions:\n"
        for state in automaton_instance.states:
            info += f"  {state}:\n"
            for symbol in automaton_instance.alphabet:
                next_states = automaton_instance.get_next_states(state, symbol)
                info += f"    {symbol} ---> {', '.join(next_states)}\n"
        info += f"Initial state: {automaton_instance.initial_state}\n"
        info += f"Final states: {', '.join(automaton_instance.final_states)}\n"
        info += f"Is it a DFA: {automaton_instance.is_dfa}\n"
        messagebox.showinfo("Automaton Information", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonApp(root)
    root.mainloop()
