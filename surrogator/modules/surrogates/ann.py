"""
 Title:         ANN
 Description:   Contains the DNN for the Surrogate Model 
 Author:        Janzen Choi

"""

# Libraries
from modules.surrogates.__surrogate__ import SurrogateTemplate
import numpy as np
import os; os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3" # disable warnings
import tensorflow.keras as kr

# ANN Class
class Surrogate(SurrogateTemplate):

    # Prepares the surrogate
    def prepare(self):
        
        # Define neural network
        self.model = kr.Sequential()
        self.model.add(kr.layers.InputLayer(input_shape=(self.input_size,)))
        self.model.add(kr.layers.Dense(units=128))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=64))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=32))
        self.model.add(kr.layers.Activation("relu"))
        self.model.add(kr.layers.Dense(units=self.output_size))
        self.model.add(kr.layers.Activation("relu"))
        
        # Define optimiser and compile
        opt = kr.optimizers.SGD(
            learning_rate=0.1,
            momentum=0.1,
        )
        self.model.compile(optimizer=opt, loss="mse")

    # Fits the model
    def fit(self, x_train, y_train, epochs=100, batch_size=None, verbose=False):
        x_train = np.array(x_train)
        y_train = np.array(y_train)
        verbose = 1 if verbose else 0
        batch_size = batch_size if batch_size != None else round(len(x_train)/2)
        self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=verbose)

    # Makes a single prediction
    def predict(self, x_test):
        x_test = np.array([x_test])
        y_pred = self.model.predict(x_test, batch_size=10)
        return y_pred
