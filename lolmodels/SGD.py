from sklearn.linear_model import SGDClassifier
import numpy as np
import matplotlib.pyplot as plt

class SGD:

    def create(self, loss = "perceptron", penatly = "l1", alpha=0.00008):
        return SGDClassifier(loss = loss, penalty = penatly, alpha = alpha)
        # loss : ‘hinge’, ‘log_loss’, ‘modified_huber’, ‘squared_hinge’, ‘perceptron’, ‘squared_error’,
        #        c
        # penalty : ‘l2’, ‘l1’, ‘elasticnet’


    def train(self, sgd, train_set, validation_set):
        np.random.shuffle(train_set)
        np.random.shuffle(validation_set)

        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        sgd.fit(X_train, y_train)
        return sgd.score(X_val, y_val)

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #loss = "hinge", penatly = "l2", alpha=0.0001,

        #? loss ! perceptron
        """l = ["hinge", "log_loss", "modified_huber", "squared_hinge", "perceptron", "squared_error", "hinge",
             "log_loss", "modified_huber", "squared_hinge", "perceptron", "squared_error"]
        x = list(range(12))
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
        plt.show()"""

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