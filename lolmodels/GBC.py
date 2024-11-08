from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
from torch.ao.nn.quantized import Dropout


class GBC:

    def create(self, n_estimators=100, max_depth=3, learning_rate=0.1, subsample=1.0):
        return GradientBoostingClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, subsample=subsample)

    def train(self, gbc, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        gbc.fit(X_train, y_train)
        return gbc.score(X_val, y_val)

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #? n_estimators ! 500
        """x = [10,50,100,200,500,1000,5000,10000]
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
        plt.show()"""

        #? learning_rate !
        x = list(i/ 10 for i in range(1, 10, 1))
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
        plt.show()

        #? max_depth !
        x = list(range(1, 15, 1))
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
        plt.show()

        #? subsample !
        x = list(i/ 10 for i in range(1, 10, 1))
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
        plt.show()