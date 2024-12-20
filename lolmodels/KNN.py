from sklearn.neighbors import KNeighborsClassifier as NN
import numpy as np
import matplotlib.pyplot as plt

class KNN:

    def __init__(self):
        self.name = "KNN"

    def create(self, n_neighbours=40, weights='uniform', algorithm='ball_tree', metric='minkowski', p=2):
        return NN(n_neighbors=n_neighbours, weights=weights, algorithm=algorithm, metric=metric, p=p)
        #weights : ‘uniform’, ‘distance’
        #algo : ‘ball_tree’, ‘kd_tree’, ‘brute’

    def train(self, knn, train_set, validation_set, full_eval = False):
        np.random.shuffle(train_set)
        if validation_set is not None:
            np.random.shuffle(validation_set)

        X_train, y_train = train_set[:,1:], train_set[:,0]
        if validation_set is not None:
            X_val, y_val = validation_set[:,1:], validation_set[:,0]

        knn.fit(X_train, y_train)
        if full_eval and validation_set is not None:
            return knn.score(X_train, y_train), knn.score(X_val, y_val)
        if validation_set is not None:
            return knn.score(X_val, y_val)

    def eval(self, knn, *sets):
        res = []
        for set in sets:
            X, y = set[:, 1:], set[:, 0]
            predi = knn.predict_proba(X)[:,1]
            mse = ((predi - y)**2).mean().item()
            res.append(mse)
        return res

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #? n_neighbours ! 40
        """x = list(range(37,42,1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(20):
                knn = self.create(n_neighbours=n)
                np.random.shuffle(train_set)
                np.random.shuffle(validation_set)
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/20)
        plt.plot(x, accuracy)
        plt.show()"""

        #? weights ! uniform
        """w = ['uniform', 'distance']
        x = [0,1]
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(weights=w[n])
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? algorithm ! idem
        """a = ['ball_tree', 'kd_tree', 'brute']
        x = [0,1,2]
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(algorithm=a[n])
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? p ! 1.6 -> 2
        """x = list(range(16,20,1))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(p=n/10)
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""