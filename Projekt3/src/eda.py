import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_eda_folder():
    os.makedirs(
        "results/eda",
        exist_ok=True
    )


def basic_info(df):
    print("\n=== DATASET INFO ===")
    print(df.info())

    print("\n=== FIRST 5 ROWS ===")
    print(df.head())

    print("\n=== STATISTICS ===")
    print(df.describe())

    print("\n=== MISSING VALUES ===")
    print(df.isnull().sum())



def target_distribution(df):
    plt.figure(figsize=(6, 5))

    sns.countplot(
        x="target",
        data=df
    )

    plt.title(
        "Heart Disease Distribution"
    )

    plt.savefig(
        "results/eda/target_distribution.png"
    )

    plt.close()


def feature_histograms(df):
    df.hist(
        figsize=(16, 12),
        bins=20
    )

    plt.tight_layout()

    plt.savefig(
        "results/eda/feature_histograms.png"
    )

    plt.close()


def correlation_heatmap(df):
    plt.figure(figsize=(12, 8))

    correlation = df.corr()

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title(
        "Feature Correlation Heatmap"
    )

    plt.savefig(
        "results/eda/correlation_heatmap.png"
    )

    plt.close()


def feature_vs_target(df):
    features = [
        column
        for column in df.columns
        if column != "target"
    ]

    for feature in features:
        plt.figure(figsize=(7, 5))

        sns.boxplot(
            x="target",
            y=feature,
            data=df
        )

        plt.title(
            f"{feature} vs target"
        )

        plt.savefig(
            f"results/eda/"
            f"{feature}_vs_target.png"
        )

        plt.close()


def outlier_analysis(df):
    plt.figure(figsize=(16, 10))

    sns.boxplot(data=df)

    plt.xticks(rotation=45)

    plt.title(
        "Outlier Detection"
    )

    plt.savefig(
        "results/eda/outliers.png"
    )

    plt.close()


def run_eda(path):
    create_eda_folder()

    df = pd.read_csv(path)

    # usunięcie duplikatów
    duplicates = df.duplicated().sum()

    print(f"\nRemoved duplicates: {duplicates}")

    df = df.drop_duplicates()

    basic_info(df)

    target_distribution(df)

    feature_histograms(df)

    correlation_heatmap(df)

    feature_vs_target(df)

    outlier_analysis(df)

    print("\nEDA finished!")