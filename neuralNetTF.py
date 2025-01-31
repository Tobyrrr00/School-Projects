import numpy as np
from random import random
import tensorflow as tf
from sklearn.model_selection import train_test_split

def generate_dataset(num_samples, test_size):
    
    # build inputs/targets for sum operation: y[0][0] = x[0][0] + x[0][1]
    x = np.array([[random()/2 for _ in range(2)] for _ in range(num_samples)])
    y = np.array([[i[0] + i[1]] for i in x])
    # split dataset into test and training sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    return x_train, x_test, y_train, y_test

if __name__ == "__main__":
    x_train, x_test, y_train, y_test = generate_dataset(5000, 0.3)
    #print("x_test \n".format(x_test))
    #print("y_test \n".format(y_test))

    #build model: 
    model = tf.keras.Sequential([
        #input layers. 2 neurons, 5 hidden layers,
        tf.keras.layers.Dense(5, input_dim = 2, activation="sigmoid"),
        #output layers. 1 output layers
        tf.keras.layers.Dense(1, activation = "sigmoid")
    ])
    
    #compile model
    optimizer = tf.keras.optimizers.SGD(learning_rate = 0.1)
    #mse = Min Squared Error
    model.compile(optimizer = optimizer, loss = "MSE")

    #fit model
    model.fit(x_train, y_train, epochs = 100)

    #evaluate model 
    print("\nModel Evaluation:")
    model.evaluate(x_test, y_test)

    #make predictions
    data = np.array([[0.1, 0.2],[0.2, 0.2]])
    predictions = model.predict(data)

    print("\nSome predictions:")
    for d, p in zip(data, predictions):
        print("{} + {} = {}".format(d[0], d[1], p[0]))
