import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import learning_curve
import numpy as np


def plot_confusion_matrix(matrix, model_name):
    plt.figure(figsize=(6, 5))

    sns.heatmap(
        matrix,
        annot=True,
        fmt="d"
    )

    plt.title(
        f"Confusion Matrix - {model_name}"
    )

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig(
        f"results/confusion_matrices/"
        f"{model_name}.png"
    )

    plt.close()


def plot_learning_curve(
        model,
        X,
        y,
        model_name
):
    train_sizes, train_scores, test_scores = learning_curve(
        model,
        X,
        y,
        cv=5,
        scoring="accuracy"
    )

    train_mean = np.mean(
        train_scores,
        axis=1
    )

    test_mean = np.mean(
        test_scores,
        axis=1
    )

    plt.figure(figsize=(8, 5))

    plt.plot(
        train_sizes,
        train_mean,
        label="Training Score"
    )

    plt.plot(
        train_sizes,
        test_mean,
        label="Validation Score"
    )

    plt.title(
        f"Learning Curve - {model_name}"
    )

    plt.xlabel("Training examples")
    plt.ylabel("Accuracy")

    plt.legend()

    plt.savefig(
        f"results/learning_curves/"
        f"{model_name}.png"
    )

    plt.close()