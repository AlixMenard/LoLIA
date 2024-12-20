import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import seaborn as sns
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import CubicSpline


def global_results():
    # Example DataFrames (same as before)
    df_acc = pd.read_csv("data/benchmarks/benchmark_acc.csv")
    df_mse = pd.read_csv("data/benchmarks/benchmark_mse.csv")

    # Melt DataFrames for merging
    df_acc_melted = df_acc.melt(id_vars="Season", var_name="Model", value_name="Accuracy")
    df_mse_melted = df_mse.melt(id_vars="Season", var_name="Model", value_name="MSE")

    # Merge the DataFrames
    df = pd.merge(df_acc_melted, df_mse_melted, on=["Season", "Model"])
    df = df[df["Model"].str.endswith("_val")]

    stats = df.groupby("Model").agg({
        "Accuracy": ["min", "max", "mean", "std"],
        "MSE": ["min", "max", "mean", "std"]
    })
    stats.columns = ["AccMin", "AccMax", "AccMean", "AccStd", "MSEMin", "MSEMax", "MSEMean", "MSEStd"]
    stats = stats.reset_index()

    # Plot
    plt.figure(figsize=(10, 6))

    # Define colors for models
    cmap = plt.cm.get_cmap("tab10", 10)  # "tab10" is a good default choice
    colors = [cmap(i) for i in range(cmap.N)]
    color_map = {model: color for model, color in zip(stats["Model"], colors)}

    for _, row in stats.iterrows():
        """# Ellipse 1: Range (min to max)
        x_center_range = (row["AccMin"] + row["AccMax"]) / 2
        y_center_range = (row["MSEMin"] + row["MSEMax"]) / 2
        width_range = row["AccMax"] - row["AccMin"]
        height_range = row["MSEMax"] - row["MSEMin"]

        ellipse_range = Ellipse(
            (x_center_range, y_center_range), width_range, height_range,
            color=color_map[row["Model"]], alpha=0.4, label=f"{row['Model']} Range"
        )
        plt.gca().add_patch(ellipse_range)"""

        # Ellipse 2: Standard Deviation around the Mean
        x_center_mean = row["AccMean"]
        y_center_mean = row["MSEMean"]
        width_std = 2 * row["AccStd"]  # 2 * std to cover one standard deviation
        height_std = 2 * row["MSEStd"]

        ellipse_std = Ellipse(
            (x_center_mean, y_center_mean), width_std, height_std,
            edgecolor=color_map[row["Model"]], facecolor="none", linestyle="-", linewidth=1.5,
            alpha=0.8, label=f"{row['Model'][:-4]}"
        )
        plt.gca().add_patch(ellipse_std)

        # Add model name at the center of the range ellipse
        plt.text(x_center_mean, y_center_mean, row["Model"], color=color_map[row["Model"]], ha="center", va="center", fontsize=10)

    # Aesthetics
    plt.title("Model Accuracy vs MSE with Ranges", fontsize=16)
    plt.xlabel("Accuracy", fontsize=12)
    plt.ylabel("MSE", fontsize=12)
    plt.legend(title="Model", loc="lower left")
    plt.grid(True)
    plt.xlim(0.55, 0.925)  # Adjust based on your data
    plt.ylim(0.075, 0.4)  # Adjust based on your data
    plt.show()

def timelessness(model_type):
    df = pd.read_csv(rf"data/benchmarks/timelessness_{model_type}.csv")

    # Set "Years" column as the index
    df.set_index("Years", inplace=True)

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df,
        annot=True,  # Show accuracy values in the cells
        fmt=".2f",  # Format to 2 decimal places
        cmap="YlGnBu",  # Colormap
        cbar_kws={'label': 'Accuracy'},  # Label for the color bar
        linewidths=0.5,  # Line width between cells
        square=True,  # Square cells
        vmin=0,
        vmax=1
    )

    # Add titles and labels
    plt.title("Model Accuracy by Training and Testing Years", fontsize=16)
    plt.xlabel("Testing Year", fontsize=12)
    plt.ylabel("Training Year", fontsize=12)

    # Show the plot
    plt.tight_layout()
    plt.show()

def cross_region_compatibility(model_type):
    df = pd.read_csv(rf"data/benchmarks/CRC_{model_type}.csv")

    # Set "Years" column as the index
    df.set_index("Leagues", inplace=True)

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df,
        annot=True,  # Show accuracy values in the cells
        fmt=".2f",  # Format to 2 decimal places
        cmap="YlGnBu",  # Colormap
        cbar_kws={'label': 'Accuracy'},  # Label for the color bar
        linewidths=0.5,  # Line width between cells
        square=True,  # Square cells
        vmin=0,
        vmax=1
    )

    # Add titles and labels
    plt.title("Model Accuracy by Training and Testing League", fontsize=16)
    plt.xlabel("Testing League", fontsize=12)
    plt.ylabel("Training League", fontsize=12)

    # Show the plot
    plt.tight_layout()
    plt.show()

def stability(model_type):
    df = pd.read_csv(rf"data/benchmarks/stability_{model_type}.csv", header=None)

    deltas = df[0]
    averages = df[1]
    energies = df[2]

    plt.plot(averages, energies, "x")
    plt.title("Relative energy of high frequency variations\nvs\nAverage winning probabilty (game based)", fontsize=10)
    plt.ylabel("Relative energy of high frequency variations", fontsize=10)
    plt.xlabel("Average winning probability", fontsize=10)
    plt.tight_layout()
    plt.show()

    plt.plot(deltas, energies, "x")
    plt.title("Relative energy of high frequency variations\nvs\nMaximum winning probability variation (game based)", fontsize=10)
    plt.ylabel("Relative energy of high frequency variations", fontsize=10)
    plt.xlabel("Maximum winning probability variation", fontsize=10)
    plt.tight_layout()
    plt.show()

def plot_smoothing_methods(data, time_interval=10):
    # Generate x values based on the time interval
    x = np.arange(0, len(data) * time_interval, time_interval)

    # Gaussian Smoothing
    sigma = 2
    gaussian_smooth = gaussian_filter1d(data, sigma=sigma)
    # Gaussian Smoothing
    sigma = 1
    gaussian_smooth1 = gaussian_filter1d(data, sigma=sigma)
    gaussian_smooth12 = gaussian_filter1d(gaussian_smooth1, sigma=sigma)


    # Plotting
    plt.figure(figsize=(12, 6))

    # Original scatter plot
    plt.scatter(x, data, color='gray', alpha=0.5, label='Original Data (Scatter)')

    # Gaussian Smoothing
    plt.plot(x, gaussian_smooth, color='green', label='Gaussian Smoothing 2')
    plt.plot(x, gaussian_smooth12, color='red', label='Gaussian Smoothing 1 *2')

    # Labels and legend
    plt.title('Game outcome chances vs time')
    plt.xlabel('Time (s)')
    plt.ylabel('Winning probability')
    plt.legend()
    plt.grid(True)
    plt.show()

    return gaussian_smooth

