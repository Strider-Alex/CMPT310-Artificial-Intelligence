import random
import math
import time
import copy

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################


def logistic(x):
    return 1.0 / (1.0 + math.exp(-x))

def logistic_derivative(x):
    return logistic(x) * (1-logistic(x))

class Neuron:
    def __init__(self, attribute_weights, neuron_weights, bias_weight):
        # neuron.attribute_weights[i] = Weight of input attribute i as input to this neuron
        self.attribute_weights = attribute_weights
        # neuron.neuron_weights[i] = Weight of neuron j as input to this neuron
        self.neuron_weights = neuron_weights
        self.bias_weight = bias_weight

class ANN:
    def __init__(self, num_attributes, neurons):
        # Number of input attributes.
        self.num_attributes = num_attributes
        # Number of neurons. neurons[-1] is the output neuron.
        self.neurons = neurons
        for neuron_index, neuron in enumerate(self.neurons):
            for input_neuron, input_weight in neuron.neuron_weights.items():
                assert(input_neuron < neuron_index)

    # Calculates the output of the output neuron for given input attributes.
    def calculate(self, attributes):
        ###########################################
        # Start your code
        print("My code here")
        # End your code
        ###########################################

    # Returns the squared error of a collection of examples:
    # Error = 0.5 * sum_i ( example_labels[i] - ann.calculate(example_attributes) )**2
    def squared_error(self, example_attributes, example_labels):
        ###########################################
        # Start your code
        print("My code here")
        # End your code
        ###########################################

    # Runs backpropagation on a single example in order to
    # update the network weights appropriately.
    def backpropagate_example(self, attributes, label, learning_rate=1.0):
        ###########################################
        # Start your code
        print("My code here")
        # End your code
        ###########################################

    # Runs backpropagation on each example, repeating this process
    # num_epochs times.
    def learn(self, example_attributes, example_labels, learning_rate=1.0, num_epochs=100):
        ###########################################
        # Start your code
        print("My code here")
        # End your code
        ###########################################


example_attributes = [ [0,0], [0,1], [1,0], [1,1] ]
example_labels = [0,1,1,0]

def random_ann(num_attributes=2, num_hidden=2):
    neurons = []
    # hidden neurons
    for i in range(num_hidden):
        attribute_weights = {attribute_index: random.uniform(-1.0,1.0) for attribute_index in range(num_attributes)}
        bias_weight = random.uniform(-1.0,1.0)
        neurons.append(Neuron(attribute_weights,{},bias_weight))
    # output neuron
    neuron_weights = {input_neuron: random.uniform(-1.0,1.0) for input_neuron in range(num_hidden)}
    bias_weight = random.uniform(-1.0,1.0)
    neurons.append(Neuron({},neuron_weights,bias_weight))
    ann = ANN(num_attributes, neurons)
    return ann

best_ann = None
best_error = float("inf")
for instance_index in range(10):
    ann = random_ann()
    ann.learn(example_attributes, example_labels, learning_rate=10.0, num_epochs=10000)
    error = ann.squared_error(example_attributes, example_labels)
    if error < best_error:
        best_error = error
        best_ann = ann


#####################################################
#####################################################
# Please hard-code your learned ANN here:
learned_ann = random_ann()
learned_ann.neurons[0].attribute_weights[0] = 0.0
learned_ann.neurons[0].attribute_weights[1] = 0.0
learned_ann.neurons[0].bias_weight = 0.0
learned_ann.neurons[1].attribute_weights[0] = 0.0
learned_ann.neurons[1].attribute_weights[1] = 0.0
learned_ann.neurons[1].bias_weight = 0.0
learned_ann.neurons[2].neuron_weights[0] = 0.0
learned_ann.neurons[2].neuron_weights[1] = 0.0
learned_ann.neurons[2].bias_weight = 0.0
# Enter the squared error of this network here:
final_squared_error = 0.0
#####################################################
#####################################################


