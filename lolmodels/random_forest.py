from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

class RandomForest:

    def create(self, n_estimators=100, max_depth=25, random_state=0, max_features:float|str|int=0.85):
        return RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, max_features=max_features)

    def train(self, forest, train_set, validation_set, full_eval = False):
        np.random.shuffle(train_set)
        np.random.shuffle(validation_set)

        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        forest.fit(X_train, y_train)
        if full_eval:
            return forest.score(X_train, y_train), forest.score(X_val, y_val)
        return forest.score(X_val, y_val)

    def search_params(self, train_set, validation_set):
        X_train, y_train = train_set[:,1:], train_set[:,0]
        X_val, y_val = validation_set[:,1:], validation_set[:,0]

        #? n_estimators ! 100
        """x = list(range(100, 160, 10))
        accuracy = []
        for n in x:
            print(n)
            forest = self.create(n_estimators=n)
            forest.fit(X_train, y_train)
            accuracy.append(forest.score(X_val, y_val))
        plt.plot(x, accuracy)
        plt.show()"""

        #? max_depth ! 25
        """x = list(range(20, 30, 1))
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

        #? max_features ! 0.85
        """x = list(i/100 for i in range(75, 100, 5))
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