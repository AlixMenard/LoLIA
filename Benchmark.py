import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpmath.libmp import trailing

from lolmodels import *
from data_get import *

from colorama import Fore, Back, Style

leagues = ["lcs", "lec", "worlds"]
years = [2022, 2023, 2024]
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
    years_train = years[:]
    years_eval = years[:]

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
                        r1, r2 = get_league_season(l, yt, seq = True)
                        r = np.vstack((r1, r2))
                        p1, p2 = get_league_season(l, ye, seq = True)
                        p = np.vstack((p1, p2))
                    else:
                        r1, r2 = get_league_season(l, yt)
                        r = np.vstack((r1, r2))
                        p1, p2 = get_league_season(l, ye)
                        p = np.vstack((p1, p2))
                    model.format(r, p)
                    model.fit()

                    validation_acc, _ = model.test(model.X_val, model.y_val)
                    results[i_l, i_yt, i_ye] = validation_acc/100
                else:
                    model = model_type.create()
                    r1, r2 = get_league_season(l, yt)
                    r = np.vstack((r1, r2))
                    p1, p2 = get_league_season(l, ye)
                    p = np.vstack((p1, p2))

                    _, validation_acc = model_type.train(model, r, p, full_eval=True)
                    results[i_l, i_yt, i_ye] = validation_acc
            print("", flush=True)


    results = np.mean(results, axis=0)
    results2 = np.zeros((len(years_train), len(years_eval)+1), dtype=object)
    for i in range(len(years_train)):
        results2[i, 0] = years_train[i]
        results2[i, 1:] = results[i, :]
    df = pd.DataFrame(results2, columns=["Years"] + years_eval)
    df.to_csv(fr"data/benchmarks/timelessness_{model_type.name}.csv", index=False)

def cross_region_compatibility(model_type):
    leagues_train = leagues[:]
    leagues_eval = leagues[:]

    results = np.zeros((len(years), len(leagues_train), len(leagues_eval)), dtype=object)

    for i_y, y in enumerate(years):
        print(y, flush=True)
        for i_lt, lt in enumerate(leagues_train):
            print(f"\t{lt}", end = "", flush=True)
            for i_le, le in enumerate(leagues_eval):
                print(".", end = "", flush=True)
                if type(model_type) == type:
                    model = model_type()
                    if type(model) == RNN.SimpleRNN:
                        r1, r2 = get_league_season(lt, y, seq = True)
                        r = np.vstack((r1, r2))
                        p1, p2 = get_league_season(le, y, seq = True)
                        p = np.vstack((p1, p2))
                    else:
                        r1, r2 = get_league_season(lt, y)
                        r = np.vstack((r1, r2))
                        p1, p2 = get_league_season(le, y)
                        p = np.vstack((p1, p2))
                    model.format(r, p)
                    model.fit()

                    validation_acc, _ = model.test(model.X_val, model.y_val)
                    results[i_y, i_lt, i_le] = validation_acc/100
                else:
                    model = model_type.create()
                    r1, r2 = get_league_season(lt, y)
                    r = np.vstack((r1, r2))
                    p1, p2 = get_league_season(le, y)
                    p = np.vstack((p1, p2))

                    _, validation_acc = model_type.train(model, r, p, full_eval=True)
                    results[i_y, i_lt, i_le] = validation_acc
            print("", flush=True)


    results = np.mean(results, axis=0)
    results2 = np.zeros((len(leagues_train), len(leagues_eval)+1), dtype=object)
    for i in range(len(leagues_train)):
        results2[i, 0] = leagues_train[i]
        results2[i, 1:] = results[i, :]
    df = pd.DataFrame(results2, columns=["Leagues"] + leagues_eval)
    df.to_csv(fr"data/benchmarks/CRC_{model_type.name}.csv", index=False)

def stability(model_type):
    matches = get_random_matches(200) #! 100
    training = get_samples() #! default
    results = []

    if type(model_type) == type:
        model = model_type()
        model.format(training, training)
        model.fit()
    else:
        model = model_type.create()
        model_type.train(model, training, None)

    for m in matches:
        m_x, m_y = format(m)
        if type(model_type) == type:
            res = [float(i[0]) for i in model(m_x)]
            results.append(res)
        else:
            res = model.predict_proba(m_x)[:,1]
            results.append(res)

    def compute_fft(probabilities):
        N = len(probabilities)
        fft_vals = np.fft.fft(probabilities)
        freqs = np.fft.fftfreq(N, d=10)  # d=10 for 10-second intervals
        return fft_vals, freqs, N

    averages = [np.mean(res) for res in results]
    deltas = [np.max(res)-np.min(res) for res in results]
    plot = [res[:] for res in results]

    results = [compute_fft(res) for res in results]

    def plot_magnitude_spectrum(freqs, fft_vals, game_l, title="Magnitude Spectrum"):

        N = len(freqs)  # Total number of frequency components
        half_N = N // 2

        # Use only the positive frequencies
        positive_freqs = freqs[:half_N]
        positive_magnitude = np.abs(fft_vals[:half_N])
        #positive_magnitude[0] /= game_l
        normalized_magnitudes = positive_magnitude #/ np.max(positive_magnitude)

        plt.figure(figsize=(10, 6))
        plt.bar(positive_freqs, normalized_magnitudes, width=0.001)
        plt.title("Frequency Spectrum (Positive Frequencies)")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Magnitude")
        plt.show()

    for i, m in enumerate(results):
        magnitudes, freqs, N = m
        N = len(freqs)  # Total number of frequency components
        half_N = N // 2

        positive_freqs = freqs[:half_N]
        positive_magnitude = np.abs(magnitudes[:half_N])
        positive_magnitude[0] /= N
        normalized_magnitudes = positive_magnitude / np.max(positive_magnitude)

        high_freq = np.where(positive_freqs>0.01)
        #print(high_freq, positive_freqs[high_freq])

        energy_ratio = np.sum(normalized_magnitudes[high_freq]**2) / np.sum(normalized_magnitudes**2)
        results[i] = energy_ratio

    """plt.plot(averages, results, ".")
    plt.show()
    plt.plot(deltas, results, ".")
    plt.show()

    for i, energy in enumerate(results):
        if energy > 0.8:
            plt.plot(plot[i])
            fft_vals, freqs, N = compute_fft(plot[i])
            plot_magnitude_spectrum(freqs, fft_vals, N)"""


    deltas = np.array(deltas)
    averages = np.array(averages)
    results = np.array(results)
    data = list(zip(deltas, averages, results))
    with open(fr"data/benchmarks/stability_{model_type.name}.csv", "w") as f:
        for line in data:
            f.write(f"{line[0]}, {line[1]}, {line[2]}\n")


if __name__ == "__main__":
    print(Fore.RED + "Global :" + Style.RESET_ALL)
    global_results()
    models = models[:-1]
    print("\n"*3)
    for m_t in models:
        print(Fore.RED + f"Timelessness {m_t.name} :" + Style.RESET_ALL)
        timelessness(m_t)
        print("\n"*3)
        print(Fore.RED + f"CR compatibility {m_t.name} :" + Style.RESET_ALL)
        cross_region_compatibility(m_t)
        print("\n"*3)
    models.pop(1)
    for m_t in models:
        print(Fore.RED + f"Timelessness {m_t.name} :" + Style.RESET_ALL)
        stability(m_t)
        print("\n"*3)