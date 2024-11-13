from numpy.ma.core import argmax

from data_get import *
from lolmodels.Dense import *
from torch import nn

r, p = get_league_season('worlds', 2024)

LR = list(i/1000 for i in range(0,200,10))
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
            acc = NN.test()
            results.append((acc, lr, dropout, layer))
            count += 1
            print(f"{count}/{tot}")

best = argmax(results, key=lambda x: x[0])