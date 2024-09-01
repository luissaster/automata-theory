# This file includes functions related to the user interface.
# That is: input_automaton() and print_automaton()

from functions import Automaton

def input_automaton():
    states = input("Enter states separated by commas (e.g.: q0,q1,...): ").split(",")
    alphabet = input("Enter alphabet separated by commas (e.g.: a,b,...): ").split(",")
    transitions = {}
    for state in states:
        transitions[state] = {}
        for symbol in alphabet:
            next_states = input(f"Enter next states for {state} and {symbol} separated by commas (leave blank for an empty transition): ").split(",")
            transitions[state][symbol] = next_states if next_states != [''] else []
    initial_state = input("Enter initial state (e.g.: q0): ")
    final_states = input("Enter final states separated by commas (e.g.: q0,q1,...): ").split(",")
    is_dfa = input("Is it a DFA (Deterministic Finite Automaton)?\nY for yes, N for no: ").lower() == "y"
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
    print(f"Initial state: {automaton_instance.initial_state}")
    print(f"Final states: {', '.join(automaton_instance.final_states)}")
    print(f"Is it a DFA: {automaton_instance.is_dfa}")

