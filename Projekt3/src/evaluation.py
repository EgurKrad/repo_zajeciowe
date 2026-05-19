import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    roc_auc_score
)


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)
    positive_probabilities = (
        probabilities[:, 1]
    )

    metrics = {
        "accuracy":
            accuracy_score(y_test, predictions),

        "loss":
            log_loss(y_test, probabilities),

        "precision":
            precision_score(y_test, predictions),

        "recall":
            recall_score(y_test, predictions),

        "f1":
            f1_score(y_test, predictions),

        "roc_auc":
            roc_auc_score(
                y_test,
                positive_probabilities
            )
    }

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    return metrics, matrix


def save_metrics(results):
    df = pd.DataFrame(results)

    df["combined_score"] = (
            0.5 * df["recall"]
            + 0.3 * df["f1"]
            + 0.2 * df["accuracy"]
            - 0.1 * df["loss"]
    )

    df = df.sort_values(
        by="combined_score",
        ascending=False
    )

    df["rank"] = range(
        1,
        len(df) + 1
    )

    df.to_csv(
        "results/metrics.csv",
        index=False
    )

    print("\n=== FINAL RANKING ===")
    print(
        df[
            [
                "rank",
                "model",
                "accuracy",
                "precision",
                "recall",
                "f1",
                "loss"
            ]
        ]
    )