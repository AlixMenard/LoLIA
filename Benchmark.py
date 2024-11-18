import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lolmodels import *
from data_get import *

years = [2022, 2023, 2024]
leagues = ["lec", "worlds"]

models = [Dense.NeuralNetwork, RNN.SimpleRNN, random_forest.RandomForest(), GBC.GBC(), KNN.KNN(), SGD.SGD()]
names = ["Dense", "RNN", "RandomForest", "GBC", "KNN", "SGD"]
names = [f"{n}_{t}" for n in names for t in ["train", "val"]]

results = np.zeros((len(years) * len(leagues), len(models)*2+1))

for i_league, league in enumerate(leagues):
    print(league)
    for i_year, year in enumerate(years):
        print(f"\t{year}")
        results[i_year + i_league * len(years), 0] = f"{league}-{year}"
        r, p = get_league_season(league, year)
        r_seq, p_seq = get_league_season(league, year, seq = True)
        for i_model, model in enumerate(models):
            print(f"\t\t{model}")
            if type(model) == type: # Dense or RNN
                m = model()
                if type(m) == Dense.NeuralNetwork:
                    m.format(r, p)
                    m.fit()
                    training_acc, training_mse = m.test(m.X_train, m.y_train)
                    validation_acc, validation_mse = m.test(m.X_val, m.y_val)
                    results[i_year + i_league*len(years), 2*i_model+1] = training_acc
                    results[i_year + i_league*len(years), 2*i_model+2] = validation_acc
                else:
                    m.format(r_seq, p_seq)
                    m.fit()
                    training_acc, training_mse = m.test(m.X_train, m.y_train)
                    validation_acc, validation_mse = m.test(m.X_val, m.y_val)
                    results[i_year + i_league*len(years), 2*i_model+1] = training_acc
                    results[i_year + i_league*len(years), 2*i_model+2] = validation_acc
                    del r_seq, p_seq
            else:
                m = model.create()
                training, validation = model.train(m, r, p, full_eval = True)
                results[i_year + i_league*len(years), 2*i_model+1] = training
                results[i_year + i_league*len(years), 2*i_model+2] = validation


pd_results = pd.DataFrame(results, columns=names)
pd_results.to_csv("benchmark.csv")
print(pd_results.to_markdown())