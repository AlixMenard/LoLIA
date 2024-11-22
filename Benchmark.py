import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from lolmodels import *
from data_get import *

leagues = ["lec", "worlds"]
models = [Dense.NeuralNetwork, RNN.SimpleRNN, random_forest.RandomForest(), GBC.GBC(), KNN.KNN(), SGD.SGD(), NGD.NGD()]

def global_results():
    years = [2022, 2023, 2024]

    names = ["Dense", "RNN", "RandomForest", "GBC", "KNN", "SGD", "NGD"]
    names = ["Season"] + [f"{n}_{t}" for n in names for t in ["train", "val"]]

    results_acc = np.zeros((len(years) * len(leagues), len(models)*2+1), dtype=object)
    results_mse = np.zeros((len(years) * len(leagues), len(models)*2+1), dtype=object)

    for i_league, league in enumerate(leagues):
        print(league)
        for i_year, year in enumerate(years):
            print(f"\t{year}")
            results_acc[i_year + i_league * len(years), 0] = f"{league}-{year}"
            results_mse[i_year + i_league * len(years), 0] = f"{league}-{year}"
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
                        results_acc[i_year + i_league*len(years), 2*i_model+1] = training_acc/100
                        results_acc[i_year + i_league*len(years), 2*i_model+2] = validation_acc/100
                        results_mse[i_year + i_league*len(years), 2*i_model+1] = training_mse
                        results_mse[i_year + i_league*len(years), 2*i_model+2] = validation_mse

                    else:
                        m.format(r_seq, p_seq)
                        m.fit()
                        training_acc, training_mse = m.test(m.X_train, m.y_train)
                        validation_acc, validation_mse = m.test(m.X_val, m.y_val)
                        results_acc[i_year + i_league*len(years), 2*i_model+1] = training_acc/100
                        results_acc[i_year + i_league*len(years), 2*i_model+2] = validation_acc/100
                        results_mse[i_year + i_league*len(years), 2*i_model+1] = training_mse
                        results_mse[i_year + i_league*len(years), 2*i_model+2] = validation_mse
                        del r_seq, p_seq
                elif type(model) == NGD.NGD:
                    acc, mse = model.evaluate(r)
                    results_acc[i_year + i_league*len(years), 2*i_model+1] = acc
                    results_mse[i_year + i_league*len(years), 2*i_model+1] = mse
                    acc, mse = model.evaluate(p)
                    results_acc[i_year + i_league*len(years), 2*i_model+2] = acc
                    results_mse[i_year + i_league*len(years), 2*i_model+2] = mse
                else:
                    m = model.create()
                    training, validation = model.train(m, r, p, full_eval = True)
                    results_acc[i_year + i_league*len(years), 2*i_model+1] = training
                    results_acc[i_year + i_league*len(years), 2*i_model+2] = validation
                    training, validation = model.eval(m, r, p) #MSE
                    results_mse[i_year + i_league*len(years), 2*i_model+1] = training
                    results_mse[i_year + i_league*len(years), 2*i_model+2] = validation



    pd_results1 = pd.DataFrame(results_acc, columns=names)
    pd_results1.to_csv("benchmark_acc.csv", index=False)
    pd_results2 = pd.DataFrame(results_mse, columns=names)
    pd_results2.to_csv("benchmark_mse.csv", index=False)

def timelessness(model_type):
    years_train = [2022, 2023, 2024]
    years_eval = [2022, 2023, 2024]

    results = np.zeros((len(leagues), len(years_train), len(years_eval)), dtype=object)

    for i_l, l in enumerate(leagues):
        print(l, flush=True)
        for i_yt, yt in enumerate(years_train):
            print(f"\t{yt}", end = "", flush=True)
            for i_ye, ye in enumerate(years_eval):
                print(".", end = "", flush=True)
                if type(model_type) == type:
                    model = model_type()
                    if type(model) == RNN.SimpleRNN:
                        r, _ = get_league_season(l, yt, seq = True)
                        _, p = get_league_season(l, ye, seq = True)
                    else:
                        r, _ = get_league_season(l, yt)
                        _, p = get_league_season(l, ye)
                    model.format(r, p)
                    model.fit()

                    validation_acc, _ = model.test(model.X_val, model.y_val)
                    results[i_l, i_yt, i_ye] = validation_acc/100
                else:
                    model = model_type.create()
                    r, _ = get_league_season(l, yt)
                    _, p = get_league_season(l, ye)

                    _, validation_acc = model_type.train(model, r, p, full_eval=True)
                    results[i_l, i_yt, i_ye] = validation_acc


    results = np.mean(results, axis=0)
    results2 = np.zeros((len(years_train), len(years_eval)+1), dtype=object)
    for i in range(len(years_train)):
        results2[i, 0] = years_train[i]
        results2[i, 1:] = results[i, :]
    df = pd.DataFrame(results, columns=years_eval)
    df.to_csv(f"timelessness_{model_type.name}.csv", index=False)

