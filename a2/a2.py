import random
import time
import copy

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################

# define file size
file_size = "big"

# A clause consists of a set of symbols, each of which is negated
# or not. A clause where
# clause.symbols = {"a": 1, "b": -1, "c": 1}
# corresponds to the statement: a OR (NOT b) OR c .
class Clause:
    def __init__(self):
        pass

    def from_str(self, s):
        s = s.split()
        self.symbols = {}
        for token in s:
            if token[0] == "-":
                sign = -1
                symbol = token[1:]
            else:
                sign = 1
                symbol = token
            self.symbols[symbol] = sign

    def __str__(self):
        tokens = []
        for symbol,sign in self.symbols.items():
            token = ""
            if sign == -1:
                token += "-"
            token += symbol
            tokens.append(token)
        return " ".join(tokens)

# A SAT instance consists of a set of CNF clauses. All clauses
# must be satisfied in order for the SAT instance to be satisfied.
class SatInstance:
    def __init__(self):
        pass

    def from_str(self, s):
        self.symbols = set()
        self.clauses = []
        for line in s.splitlines():
            clause = Clause()
            clause.from_str(line)
            self.clauses.append(clause)
            for symbol in clause.symbols:
                self.symbols.add(symbol)
        self.symbols = sorted(self.symbols)

    def __str__(self):
        s = ""
        for clause in self.clauses:
            s += str(clause)
            s += "\n"
        return s

    # Takes as input an assignment to symbols and returns True or
    # False depending on whether the instance is satisfied.
    # Input:
    # - assignment: Dictionary of the format {symbol: sign}, where sign
    #       is either 1 or -1.
    # Output: True or False
    def is_satisfied(self, assignment):
        ###########################################
        # Start your code
        instance_satisfied = True
        for clause in self.clauses:
            clause_satisfied = False
            for symbol,sign in clause.items():
               if assignment[symbol]*sign == 1:
                   clause_satisfied=True
                   break
            if clause_satisfied is False:
                instance_satisfied=False
                break
        return instance_satisfied
        # End your code
        ###########################################
    
    # check if there are unit clausese and update the solution
    def unit_propagate(self,solution):
        while True:
            new_assigment = {}
            for clause in self.clauses:
                if(len(clause.symbols)==1):
                    new_assigment.update(clause.symbols)
            for symbol,sign in new_assigment.items():
                for i,clause in enumerate(self.clauses):
                    if clause is not None and symbol in clause.symbols:
                        if sign == clause.symbols[symbol]:
                            self.clauses[i] = None
                        else:
                            clause.symbols.pop(symbol)
            # delete always true clauses
            if len(new_assigment)>0:
                self.clauses = list(filter(None, self.clauses))
                solution.update(new_assigment)
            else:
                break
    # check if there are pure literals and update the solution
    def pure_literal_assign(self,solution):
        pure_symbols = {}
        for symbol in self.symbols:
            sign = None
            is_pure = True
            for clause in self.clauses:
                if symbol in clause.symbols:
                    if sign is not None and sign!=clause.symbols[symbol]:
                        is_pure = False
                        break
                    elif sign is None:
                        sign = clause.symbols[symbol]
            if is_pure and sign is not None:
                pure_symbols[symbol]=sign
        if len(pure_symbols)==0:
            return
        for i,clause in enumerate(self.clauses):
            for symbol,sign in pure_symbols.items():
                if symbol in clause.symbols:
                    if sign == clause.symbols[symbol]:
                        self.clauses[i] = None
                    else:
                        clause.symbols.pop(symbol)
        self.clauses = list(filter(None, self.clauses))
        solution.update(pure_symbols)
    
    # check if there are False clauses in the instance
    def check_valid(self):
        for clause in self.clauses:
            if len(clause.symbols)==0:
                return False
        return True

    # assign a symbol to either true or false in the instance
    def assign_symbol(self,symbol,sign):
        instance = copy.deepcopy(self)
        for i,clause in enumerate(instance.clauses):
            if clause is not None and symbol in clause.symbols:
                if sign == clause.symbols[symbol]:
                    instance.clauses[i] = None
                else:
                    clause.symbols.pop(symbol)
        instance.clauses = list(filter(None, instance.clauses))
        return instance

# Finds a satisfying assignment to a SAT instance,
# using the DPLL algorithm.
# Input: SAT instance
# Output: Dictionary of the format {symbol: sign}, where sign
#         is either 1 or -1.
def solve_dpll(instance):
    ###########################################
    # Start your code
    assignment = {}
    instance_stack = [instance]
    assignment_stack = [{}]
    while len(instance_stack)!=0:
        # pop out new problem
        new_instance = instance_stack.pop()
        new_assign = assignment_stack.pop()
        # if every symbol is assigned, we're done!
        
        if len(new_assign)==len(instance.symbols):
            assignment = new_assign
            break
        new_instance.unit_propagate(new_assign)
        new_instance.pure_literal_assign(new_assign)
        if len(new_assign)==len(instance.symbols):
            if new_instance.check_valid():
                assignment = new_assign
                break
            else:
                continue
        # get an unassigned symbol
        for symbol in new_instance.symbols:
            if symbol not in new_assign:
                for sign in (-1,1):
                    next_instance = new_instance.assign_symbol(symbol,sign)
                    if next_instance.check_valid():
                        instance_stack.append(next_instance)
                        next_assign = copy.deepcopy(new_assign)
                        next_assign.update({symbol:sign})
                        assignment_stack.append(next_assign)
                break
        

    return assignment
    # End your code
    ###########################################

# the input and output code are modified so that the program reads only one line into memory each time
# better to handle large input file
instance_str = ""
with open(file_size + "_assignments_inferred.txt", "w") as output_file:
    with open(file_size + "_instances.txt", "r") as input_file:
        for line in input_file:
            if line == "\n":
                if instance_str.strip() == "":
                    continue
                instance = SatInstance()
                instance.from_str(instance_str)
                assignment = solve_dpll(instance)
                for symbol_index, (symbol, sign) in enumerate(assignment.items()):
                    if symbol_index != 0:
                        output_file.write(" ")
                    token = ""
                    if sign == -1:
                        token += "-"
                    token += symbol
                    output_file.write(token)
                output_file.write("\n")
                instance_str = ""
            else:
                instance_str+=line
