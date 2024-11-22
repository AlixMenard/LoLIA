from calendar import error

import numpy as np

class NGD:

    def __init__(self):
        self.name = "NGD"

    def __init__(self):
        self.X_train = self.y_train = None
        self.X_test = self.y_test = None

    def train(self, *args):
        raise Exception("Why would you want to train that ?")

    def predict(self, X):
        predictions = []
        for frame in X:
            redGold = frame[39] + frame[63] + frame[87] + frame[111] + frame[135]
            blueGold = frame[159] + frame[183] + frame[207] + frame[231] + frame[255]
            predictions.append(int(blueGold > redGold))
        return predictions

    def evaluate(self, frames):
        X, y = frames[:,1:], frames[:,0]
        pred = self.predict(X)
        acc = np.mean(pred == y)
        mse = np.mean((pred-y)**2)
        return acc, mse