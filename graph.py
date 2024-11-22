import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

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
    colors = ["red", "blue", "green", "orange", "purple"] * 5 # Extend if you have more models
    color_map = {model: color for model, color in zip(stats["Model"], colors)}

    for _, row in stats.iterrows():
        # Ellipse 1: Range (min to max)
        x_center_range = (row["AccMin"] + row["AccMax"]) / 2
        y_center_range = (row["MSEMin"] + row["MSEMax"]) / 2
        width_range = row["AccMax"] - row["AccMin"]
        height_range = row["MSEMax"] - row["MSEMin"]

        ellipse_range = Ellipse(
            (x_center_range, y_center_range), width_range, height_range,
            color=color_map[row["Model"]], alpha=0.4, label=f"{row['Model']} Range"
        )
        plt.gca().add_patch(ellipse_range)

        # Ellipse 2: Standard Deviation around the Mean
        x_center_mean = row["AccMean"]
        y_center_mean = row["MSEMean"]
        width_std = 2 * row["AccStd"]  # 2 * std to cover one standard deviation
        height_std = 2 * row["MSEStd"]

        ellipse_std = Ellipse(
            (x_center_mean, y_center_mean), width_std, height_std,
            edgecolor=color_map[row["Model"]], facecolor="none", linestyle="--", linewidth=1.5,
            alpha=0.8
        )
        plt.gca().add_patch(ellipse_std)

        # Add model name at the center of the range ellipse
        plt.text(x_center_range, y_center_range, row["Model"], color="black", ha="center", va="center", fontsize=10)

    # Aesthetics
    plt.title("Model Accuracy vs MSE with Ranges", fontsize=16)
    plt.xlabel("Accuracy", fontsize=12)
    plt.ylabel("MSE", fontsize=12)
    plt.legend(title="Model", loc="lower left")
    plt.grid(True)
    plt.xlim(0.65, 0.8)  # Adjust based on your data
    plt.ylim(0.15, 0.35)  # Adjust based on your data
    plt.show()
