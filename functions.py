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
        # Initialize DFA components
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
        # Fita de entrada inicial com símbolos de branco nas extremidades
        self.tape = list(tape) + [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head_position = len(tape) - 1  # Começa na última posição da fita
        self.current_state = "q0"  # Estado inicial
        self.transitions = self._define_transitions()

    def _define_transitions(self):
        # Definindo as regras de transição para a máquina de Turing
        return {
            ("q0", "1"): ("q0", "0", "L"),  # Troque '1' por '0' e continue para a esquerda
            ("q0", "0"): ("q1", "1", "R"),  # Troque '0' por '1' e mude para o estado final
            ("q0", "B"): ("q1", "1", "R"),  # Se chegar ao início da fita, adicione '1'
        }

    def step(self):
        # Executa um passo da máquina de Turing
        current_symbol = self.tape[self.head_position]
        if (self.current_state, current_symbol) in self.transitions:
            new_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol  # Escreve o símbolo
            self.current_state = new_state  # Atualiza o estado
            self.head_position += 1 if direction == "R" else -1  # Move o cabeçote

    def run(self):
        # Executa a máquina até atingir o estado de parada 'q1'
        while self.current_state != "q1":
            self.step()

    def get_tape(self):
        # Retorna o conteúdo atual da fita
        return "".join(self.tape).rstrip(self.blank_symbol)

class TuringMachine_BalanceParantheses:
    def __init__(self, tape, blank_symbol="B"):
        # Inicializa a fita e a máquina de Turing
        self.tape = list(tape) + [blank_symbol]
        self.blank_symbol = blank_symbol
        self.head_position = 0  # Cabeçote começa na primeira posição da fita
        self.current_state = "q0"  # Estado inicial
        self.transitions = self._define_transitions()

    def _define_transitions(self):
        # Definindo as regras de transição para a máquina de Turing
        return {
            # Estado q0: Procura o próximo '(' para marcar
            ("q0", "("): ("q1", "X", "R"),  # Marca '(' como 'X' e move para a direita
            ("q0", "X"): ("q0", "X", "R"),  # Ignora 'X' e continua para a direita
            ("q0", "Y"): ("q0", "Y", "R"),  # Ignora 'Y' e continua para a direita
            ("q0", ")"): ("q_reject", ")", "R"),  # Rejeita se ')' não tiver um '(' correspondente
            ("q0", "B"): ("q_accept", "B", "R"),  # Aceita se chegar ao fim sem parênteses desbalanceados
            
            # Estado q1: Procura o próximo ')' para marcar
            ("q1", "("): ("q1", "(", "R"),  # Ignora '(' e continua para a direita
            ("q1", "X"): ("q1", "X", "R"),  # Ignora 'X' e continua para a direita
            ("q1", "Y"): ("q1", "Y", "R"),  # Ignora 'Y' e continua para a direita
            ("q1", ")"): ("q2", "Y", "L"),  # Marca ')' como 'Y' e volta para a esquerda
            ("q1", "B"): ("q_reject", "B", "L"),  # Rejeita se não encontrar um ')'
            
            # Estado q2: Retorna ao início para procurar o próximo '('
            ("q2", "("): ("q2", "(", "L"),  # Move para a esquerda sobre '('
            ("q2", ")"): ("q2", ")", "L"),  # Move para a esquerda sobre ')'
            ("q2", "X"): ("q0", "X", "R"),  # Retorna ao estado q0 ao encontrar um 'X'
            ("q2", "Y"): ("q2", "Y", "L"),  # Move para a esquerda sobre 'Y'
        }

    def step(self):
        # Executa um passo da máquina de Turing
        current_symbol = self.tape[self.head_position]
        if (self.current_state, current_symbol) in self.transitions:
            new_state, write_symbol, direction = self.transitions[(self.current_state, current_symbol)]
            self.tape[self.head_position] = write_symbol  # Escreve o símbolo
            self.current_state = new_state  # Atualiza o estado
            self.head_position += 1 if direction == "R" else -1  # Move o cabeçote

    def run(self):
        # Executa a máquina até atingir um estado de aceitação ou rejeição
        while self.current_state not in ["q_accept", "q_reject"]:
            self.step()
        return self.current_state == "q_accept"

    def get_tape(self):
        # Retorna o conteúdo atual da fita
        return "".join(self.tape).rstrip(self.blank_symbol)

