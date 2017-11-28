import random
import math

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 3.5
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <The course is very interesting, but I find the chapter about temporal probability models a little bit confusing. Maybe we can do more review in class. >
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        # Start your code
        logp = math.log(0.5)
        for i,gene in enumerate(sequence):
            if i>0:
                logp += math.log(self.transition[states[i-1]][states[i]])
            logp += math.log(self.emission[states[i]][gene])
        return logp
        # End your code
        ###########################################


    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        size = len(sequence)
        print(size)
        v = [[0 for k in range(size)] for t in range(2)]
        prev = [[0 for k in range(size)] for t in range(2)]
        for t in range(size):
            for k in range(2):
                if t == 0:
                    v[k][t]=math.log(self.emission[k][sequence[t]])+math.log(self.prior[k])
                else:
                    prev0=math.log(self.transition[0][k])+v[0][t-1]
                    prev1=math.log(self.transition[1][k])+v[1][t-1]
                    if prev0>= prev1:
                        v[k][t]=math.log(self.emission[k][sequence[t]])+prev0
                        prev[k][t] = 0
                    else:
                        v[k][t]=math.log(self.emission[k][sequence[t]])+prev1
                        prev[k][t] = 1
        states=[]
        index=0
        if v[0][size-1]<v[1][size-1]:
            index=1
        for k in range(size):
            states.append(index)
            index = prev[index][size-1-k]
        states.reverse()
        return states
        # End your code
        ###########################################

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

#sequence = read_sequence("small.txt")
#viterbi = hmm.viterbi(sequence)
#logprob = hmm.logprob(sequence, viterbi)
#write_output("my_small_output.txt", logprob, viterbi)


sequence = read_sequence("ecoli.txt")
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
write_output("ecoli_output.txt", logprob, viterbi)


