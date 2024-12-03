from sklearn.linear_model import SGDClassifier
import numpy as np
import matplotlib.pyplot as plt

class SGD:

    def __init__(self):
        self.name = "SGD"

    def create(self, loss = "log_loss", penatly = "l1", alpha=0.00008):
        return SGDClassifier(loss = loss, penalty = penatly, alpha = alpha)
        # loss : ‘hinge’, ‘log_loss’, ‘modified_huber’, ‘squared_hinge’, ‘perceptron’, ‘squared_error’, ‘huber’, ‘epsilon_insensitive’, ‘squared_epsilon_insensitive’
        #        c
        # penalty : ‘l2’, ‘l1’, ‘elasticnet’


    def train(self, sgd, train_set, validation_set, full_eval = False):
        np.random.shuffle(train_set)
        if validation_set is not None:
            np.random.shuffle(validation_set)

        X_train, y_train = train_set[:,1:], train_set[:,0]
        if validation_set is not None:
            X_val, y_val = validation_set[:,1:], validation_set[:,0]

        sgd.fit(X_train, y_train)
        if full_eval and validation_set is not None:
            return sgd.score(X_train, y_train), sgd.score(X_val, y_val)
        if validation_set is not None:
            return sgd.score(X_val, y_val)

    def eval(self, sgd, *sets):
        res = []
        for set in sets:
            X, y = set[:, 1:], set[:, 0]
            predi = sgd.predict_proba(X)[:,1]
            mse = ((predi - y)**2).mean().item()
            res.append(mse)
        return res

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #loss = "hinge", penatly = "l2", alpha=0.0001,

        #? loss ! log_loss
        l = ["hinge", "log_loss", "modified_huber", "squared_hinge", "perceptron",
             "squared_error", "huber", "epsilon_insensitive", "squared_epsilon_insensitive"]
        x = list(range(9))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(loss = l[n])
                np.random.shuffle(train_set)
                np.random.shuffle(validation_set)
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()

        #? penatly ! l1
        """p = ['l1', 'l2', 'elasticnet']
        x = [0,1,2]
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(penatly=p[n])
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""

        #? alpha ! 0.00008
        """x = list(i/100000 for i in range(1,11))
        accuracy = []
        for n in x:
            print(n)
            score = 0
            for _ in range(10):
                knn = self.create(alpha=n)
                knn.fit(X_train, y_train)
                score += knn.score(X_val, y_val)
            accuracy.append(score/10)
        plt.plot(x, accuracy)
        plt.show()"""