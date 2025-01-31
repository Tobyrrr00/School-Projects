import numpy as np
from random import random
#save activations and derivatives
#implement backpropagation
#implement gradient descent
#implement train
#train our net with some dummy datasets
#make some predictions

class MLP:
    def __init__(self, num_inputs = 3, num_hidden = [3,3], num_outputs = 2):

        self.num_inupts = num_inputs
        self.num_hidden = num_hidden
        self.num_outputs = num_outputs
        
        #create generic representation of the layer
        layers = [num_inputs] + num_hidden + [num_outputs]
        
        #initiate random weights
        self.weights = []
        for i in range(len(layers) - 1):
            w = np.random.rand(layers[i], layers[i + 1])
            self.weights.append(w)

        self.activations = []
        for i in range(len(layers)):
            a = np.zeros(layers[i])
            self.activations.append(a)

        self.derivatives = []
        for i in range(len(layers) - 1):
            d = np.zeros((layers[i], layers[i + 1]))
            self.derivatives.append(d)
        


    def forward_propogate(self, inputs):
        activations = inputs
        self.activations[0] = inputs

        for i, w in enumerate(self.weights):
            #calculate net inputs
            net_inputs = np.dot(activations, w)

            #calculate the activations
            activations = self._sigmoid(net_inputs)
            self.activations[i+1] = activations

        return activations

    def back_propagate(self, error):

        
        # iterate backwareds through the network layers
        for i in reversed(range(len(self.derivatives))):
            #get activation for previous layer
            activations = self.activations[i+1]
            #apply sigmoid derivative function
            delta = error * self._sigmoid_derivative(activations)
            #reshape delta as to have it as a 2d array
            delta_reshaped = delta.reshape(delta.shape[0], -1).T
            #get activations for current layer
            current_activations = self.activations[i]
            #reshape activations as to have them as a 2d column matrix
            current_activations_reshaped = current_activations.reshape(current_activations.shape[0], -1)
            #save derivative afteklr applying matrix multiplication(dot product)
            self.derivatives[i] = np.dot(current_activations_reshaped, delta_reshaped)
            #backpropogate the next error
            error = np.dot(delta, self.weights[i].T)

            
            #print("Derivatives for W{}: {}".format(i, self.derivatives[i]))
        return error

    def gradient_descent(self, learning_rate):
        for i in range(len(self.weights)):
            weights = self.weights[i]
            derivatives = self.derivatives[i]
            weights += derivatives * learning_rate


    def train(self, inputs, targets, epochs, learning_rate):
        for i in range(epochs):
            sum_error = 0
            for input, target in zip(inputs, targets):
                #forward propagation
                output = self.forward_propogate(input)
                #calculate error
                error = target - output
                #back propagation 
                self.back_propagate(error)
                #apply gradient descent
                self.gradient_descent(learning_rate)
                
                sum_error += self._mse(target, output)
            
            #report error
            print("Error: {} at epoch {}".format(sum_error/len(inputs),i))

    def _mse(self, target, output):
        return np.average((target - output)**2)

    def _sigmoid_derivative(self, x):
        return x * (1.0 - x) 

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

if __name__ == "__main__":
    # create a dataset to train a network for the sum operation
    inputs = np.array([[random()/2 for _ in range(2)] for _ in range(1000)])
    targets = np.array([[i[0] + i[1]] for i in inputs])
    #create an MLP
    mlp = MLP(2, [5], 1)
    #train our mlp
    #You can the Edit epochs (currently 50). less = less accurate. more = more accurate
    mlp.train(inputs, targets, 50, 0.1)

    #dummy data
    input = np.array([.3, .1])
    target = np.array([.4])
    #get a prediction
    output = mlp.forward_propogate(input)
    print()
    print("Our network believes that {} + {} is equal to {}".format(input[0], input[1], output[0]))
