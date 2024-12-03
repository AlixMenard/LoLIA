from filterpy.kalman import predict
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
from torch.ao.nn.quantized import Dropout
import numpy as np


class GBC:

    def __init__(self):
        self.name = "GBC"

    def create(self, n_estimators=500, max_depth=6, learning_rate=0.6, subsample=1.0):
        return GradientBoostingClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, subsample=subsample)

    def train(self, gbc, train_set, validation_set, full_eval = False):
        np.random.shuffle(train_set)
        if validation_set is not None:
            np.random.shuffle(validation_set)

        X_train, y_train = train_set[:,1:], train_set[:,0]
        if validation_set is not None:
            X_val, y_val = validation_set[:,1:], validation_set[:,0]

        gbc.fit(X_train, y_train)
        if full_eval and validation_set is not None:
            return gbc.score(X_train, y_train), gbc.score(X_val, y_val)
        if validation_set is not None:
            return gbc.score(X_val, y_val)

    def eval(self, gbc:GradientBoostingClassifier, *sets):
        res = []
        for set in sets:
            X, y = set[:, 1:], set[:, 0]
            predi = gbc.predict_proba(X)[:,1]
            mse = ((predi - y)**2).mean().item()
            res.append(mse)
        return res

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #? n_estimators ! 500
        x = list(range(2,9,1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                gbc = self.create(n_estimators=n)
                gbc.fit(X_train, y_train)
                score += gbc.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()

        #? learning_rate !0.6
        """x = list(i/ 100 for i in range(55, 66, 1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                gbc = self.create(learning_rate=n)
                gbc.fit(X_train, y_train)
                score += gbc.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? max_depth ! 6
        """x = list(range(1, 15, 1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                gbc = self.create(max_depth=n)
                gbc.fit(X_train, y_train)
                score += gbc.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? subsample ! 1
        """x = list(i/ 10 for i in range(1, 10, 1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                gbc = self.create(subsample=n)
                gbc.fit(X_train, y_train)
                score += gbc.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""