from sklearn.ensemble import GradientBoostingClassifier
import matplotlib.pyplot as plt
from torch.ao.nn.quantized import Dropout


class GBC:

    def create(self, n_estimators=10000, max_depth=13, random_state=0, max_features:float|str|int=0.9):
        return GradientBoostingClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, max_features=max_features)

    def train(self, forest, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        forest.fit(X_train, y_train)
        return forest.score(X_val, y_val)

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #? n_estimators ! 10000
        """x = list(range(5000, 16000, 1000))
        accuracy = []
        for n in x:
            print(n)
            forest = self.create(n_estimators=n)
            forest.fit(X_train, y_train)
            accuracy.append(forest.score(X_val, y_val))
        plt.plot(x, accuracy)
        plt.show()"""

        #? max_depth ! 13
        """x = list(range(10, 20, 1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                forest = self.create(max_depth=n)
                forest.fit(X_train, y_train)
                score += forest.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? max_features ! 0.9
        """x = [0.85, 0.9, 0.95]
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                forest = self.create(max_features=n)
                forest.fit(X_train, y_train)
                score += forest.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""