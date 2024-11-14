from numpy.ma.core import argmax

from data_get import *
from lolmodels.Dense import *
from torch import nn

import matplotlib.pyplot as plt

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)

r, p = get_league_season('worlds', 2024)

def Dense_tuner():
    LR = list(1/10**i for i in range(3,10,1))
    layers = [(128, 64), (64, 32, 16), (128, 64, 32, 16), (128, 32, 8)]
    dropouts = list(i/10 for i in range(0,5))

    results = []
    tot = len(LR) * len(layers) * len(dropouts)
    count = 0

    for lr in LR:
        for dropout in dropouts:
            for layer in layers:
                seq = nn.Sequential()
                seq.append(nn.Linear(273, layer[0]))
                for i in range(len(layer[1:])):
                    seq.append(nn.ReLU())
                    seq.append(nn.Dropout(dropout))
                    seq.append(nn.Linear(layer[i], layer[i+1]))

                seq.append(nn.ReLU())
                seq.append(nn.Dropout(dropout))
                seq.append(nn.Linear(layer[-1], 1))

                NN = NeuralNetwork(stack = seq, lr = lr)
                NN.format(r , p)
                NN.fit()
                acc, mse = NN.test()
                results.append((acc, mse, lr, dropout, layer))
                count += 1
                print(f"{count}/{tot}")

    best_acc = max(results, key=lambda x: x[0])
    best_mse = min(results, key=lambda x: x[1])
    return best_acc, best_mse, results

best_acc, best_mse, results = Dense_tuner()
print(best_acc)
print(best_mse)
X = [x[0] for x in results]
y = [x[1] for x in results]
plt.plot(X, y, '.')
plt.show()
with open('modeltune.txt', 'w') as f:
    for r in results:
        f.write(f'{r}\n')