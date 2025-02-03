Title = 'Multi Layer Perceptron from scratch'
Image = 'img/ANN-Graph.webp'
arch = 'img/mlparch.png'
intro = '''A Multilayer Perceptron has input and output layers, and one or more hidden layers with many neurons stacked
together. And while in the Perceptron the neuron must have an activation function that imposes a threshold, like ReLU or
sigmoid, neurons in a Multilayer Perceptron can use any arbitrary activation function.'''


head = [Title, Image, arch, intro]

content = [
    ['Feed Forward Algorthim', '''Multilayer Perceptron falls under the category of <strong>feedforward algorithms</strong>
because inputs are combined with the initial weights in a weighted sum and subjected to the activation function, just
like in the Perceptron.But the difference is that each linear combination is propagated to the next layer.
Each layer is feeding the next one with the result of their computation, their internal representation of the data.This
goes all the way through the hidden layers to the output layer.

''', '''
def forward_propagate(self, inputs):
    """
    Computes forward propagation of the network based on input signals.

    Args:
    inputs (ndarray): Input signals
    Returns:
    activations (ndarray): Output values
    """

    # the input layer activation is just the input itself
    activations = inputs

    # save the activations for backpropogation
    self.activations[0] = activations

    # iterate through the network layers
    for i, w in enumerate(self.weights):
    # calculate matrix multiplication between previous activation and weight matrix
    net_inputs = np.dot(activations, w)

    # apply sigmoid activation function
    activations = self._sigmoid(net_inputs)

    # save the activations for backpropogation
    self.activations[i + 1] = activations

    # return output layer activation
    return activations
'''],
    ['Calculate Mean-squared error (MSE)', """
After the forward propagation, compare the predicted output with the actual target values.
Calculate the error for each output neuron by finding the difference between the predicted and actual values.
Square each of these differences to ensure positive contributions and emphasize larger errors.
Sum up the squared errors and divide by the number of output neurons to get the mean squared error (MSE).
""", '''
def _mse(self, target, output):
    """
    Mean Squared Error loss function
    Args:
    target (ndarray): The ground trut
    output (ndarray): The predicted values
    Returns:
    (float): Output
    """
    return np.average((target - output) ** 2)
'''],
    ['backpropogation', '''
If the algorithm only computed the weighted sums in each neuron, propagated results to the output layer, and stopped
there, it wouldn’t be able to learn the weights that minimize the cost function. If the algorithm only computed one
iteration, there would be no actual learning.
Backpropagation is the learning mechanism that allows the Multilayer Perceptron to iteratively adjust the weights in the
network, with the goal of minimizing the cost function.
''',
     '''
def back_propagate(self, error):
    """
    Backpropogates an error signal.
    Args:
    error (ndarray): The error to backprop.
    Returns:
    error (ndarray): The final error of the input
    """

    # iterate backwards through the network layers
    for i in reversed(range(len(self.derivatives))):

    # get activation for previous layer
    activations = self.activations[i+1]

    # apply sigmoid derivative function
    delta = error * self._sigmoid_derivative(activations)

    # reshape delta as to have it as a 2d array
    delta_re = delta.reshape(delta.shape[0], -1).T

    # get activations for current layer
    current_activations = self.activations[i]

    # reshape activations as to have them as a 2d column matrix
    current_activations = current_activations.reshape(current_activations.shape[0],-1)

    # save derivative after applying matrix multiplication
    self.derivatives[i] = np.dot(current_activations, delta_re)

    # backpropogate the next error
    error = np.dot(delta, self.weights[i].T)
'''], ['Gradient Descent', '''
The gradient is the partial derivative of the error with respect to each weight in the network.
For each weight, calculate the gradient by taking the derivative of the error with respect to that weight.
The gradient indicates the direction and magnitude in which the weight should be adjusted to reduce the error.
There is one hard requirement for backpropagation to work properly.The function that combines inputs and weights in a
neuron, for instance the weighted sum, and the threshold function, for instance ReLU, must be differentiable.These
functions must have a bounded derivative, because Gradient Descent is typically the optimization function used in
MultiLayer Perceptron.
''', '''
def gradient_descent(self, learningRate=1):
    """
    Learns by descending the gradient
    Args:
    learningRate (float): How fast to learn.
    """
    # update the weights by stepping down the gradient
    for i in range(len(self.weights)):
    weights = self.weights[i]
    derivatives = self.derivatives[i]
    weights += derivatives * learningRate
'''],
    ['Train process', '''
The training process of a neural network involves adjusting its weights and biases to minimize the difference between
predicted outputs and actual targets.
''', '''
 def train(self, inputs, targets, epochs, learning_rate):
        """
        Trains model running forward prop and backprop
        Args:
            inputs (ndarray): X
            targets (ndarray): Y
            epochs (int): Num. epochs we want to train the network for
            learning_rate (float): Step to apply to gradient descent
        """
        # now enter the training loop
        for i in range(epochs):
            sum_errors = 0

            # iterate through all the training data
            for j, input in enumerate(inputs):
                target = targets[j]

                # activate the network!
                output = self.forward_propagate(input)

                error = target - output

                self.back_propagate(error)

                # now perform gradient descent on the derivatives
                # (this will update the weights
                self.gradient_descent(learning_rate)

                # keep track of the MSE for reporting later
                sum_errors += self._mse(target, output)

            # Epoch complete, report the training error
            print("Error: {} at epoch {}".format(sum_errors / len(items), i+1))

        print("Training complete!")
        print("=====")
''']
]
project = 'mlp.ipynb'
