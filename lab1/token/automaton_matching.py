import string

class State:
    def __init__(self, is_finishing=False):
        self.is_finishing = is_finishing
        self.transitions = {}

    def add_transition(self, other, symbols):
        self.transitions[symbols] = other

    def transition(self, symbol):
        for k, v in self.transitions.items():
            if symbol in k:
                return v

def build_integer_automaton():
    int_start_state = State()           #initial state
    digit_state = State(True)           #input_is_digit state
    underscore_divisor_state = State()  #allow dividing integers like 1_000_000

    int_start_state.add_transition(digit_state, string.digits)

    #continue reading digits
    digit_state.add_transition(digit_state, string.digits)

    #underscore divisor
    digit_state.add_transition(underscore_divisor_state, "_")

    #int doesn't end with underscore
    underscore_divisor_state.add_transition(digit_state, string.digits)

    return int_start_state

def build_double_automaton():
    double_start_state = build_integer_automaton()
    before_dot_digit_state = double_start_state.transition("0")     #get digit_state of integer
    before_dot_digit_state.is_finishing = False                     #digits before dot are not a complete floating number

    dot_state = State()

    before_dot_digit_state.add_transition(dot_state, ".")

    temp = build_integer_automaton()                                #another integer needed after the dot
    after_dot_digit_state = temp.transition("0")                    #get digit_state of integer
    dot_state.add_transition(after_dot_digit_state, string.digits)  #set transition to final state from dot state

    return double_start_state

def build_identifier_automaton():
    identifier_start_state = State()
    first_symbol_state = State(True)

    allowed_first_symbols = string.ascii_letters + "_"

    #also allow bytes from 128 to 255
    for i in range(128, 256):
        try:
            allowed_first_symbols += i.to_bytes(1, "big").decode("cp1252")
        except UnicodeDecodeError:
            pass            #skip if not decodable

    identifier_start_state.add_transition(first_symbol_state, allowed_first_symbols)

    other_symbols_state = State(True)

    allowed_other_symbols = allowed_first_symbols + string.digits

    first_symbol_state.add_transition(other_symbols_state, allowed_other_symbols)

    other_symbols_state.add_transition(other_symbols_state, allowed_other_symbols)

    return identifier_start_state

integer_automaton_start = build_integer_automaton()
double_automaton_start = build_double_automaton()
identifier_automaton_start = build_identifier_automaton()

def match_against_automaton(input, state):
    for symbol in input:
        state = state.transition(symbol)

        if state == None:
            return False

    return state.is_finishing

integer_match = lambda input: match_against_automaton(input, integer_automaton_start)
double_match = lambda input: match_against_automaton(input, double_automaton_start)
identifier_match = lambda input: match_against_automaton(input, identifier_automaton_start)