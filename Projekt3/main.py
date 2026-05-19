import os

from src.preprocessing import (
    load_and_preprocess_data
)

from src.models import (
    get_models
)

from src.evaluation import (
    evaluate_model,
    save_metrics
)

from src.visualization import (
    plot_confusion_matrix,
    plot_learning_curve
)

from src.eda import run_eda

from src.tuning import (
    get_tuned_models
)

from src.feature_importance import (
    plot_feature_importance
)

import joblib
def create_folders():
    os.makedirs(
        "results/confusion_matrices",
        exist_ok=True
    )

    os.makedirs(
        "results/learning_curves",
        exist_ok=True
    )


def main():
    create_folders()
    run_eda("data/heart.csv")
    (
        X_train,
        X_test,
        y_train,
        y_test,
        feature_names
    ) = (
        load_and_preprocess_data(
            "data/heart.csv"
        )
    )

    models = get_tuned_models(
        X_train,
        y_train
    )

    results = []

    best_model = None
    best_score = -1
    best_name = ""

    for name, model in models.items():
        print(f"Training {name}...")

        model.fit(
            X_train,
            y_train
        )

        metrics, matrix = evaluate_model(
            model,
            X_test,
            y_test
        )

        print(f"\n{name}")
        print(matrix)

        metrics["model"] = name
        metrics["combined_score"] = (
                0.5 * metrics["recall"]
                + 0.3 * metrics["f1"]
                + 0.2 * metrics["accuracy"]
                - 0.1 * metrics["loss"]
        )
        if metrics["combined_score"] > best_score:
            best_score = metrics["combined_score"]
            best_model = model
            best_name = name
        results.append(metrics)

        plot_confusion_matrix(
            matrix,
            name
        )

        plot_learning_curve(
            model,
            X_train,
            y_train,
            name
        )

        plot_feature_importance(
            model,
            feature_names,
            name
        )

    save_metrics(results)

    joblib.dump(
        best_model,
        "results/best_model.pkl"
    )

    print(
        f"\nBest model: "
        f"{best_name}"
    )

    print(
        f"Combined score: "
        f"{best_score:.4f}"
    )

    print("Done!")


if __name__ == "__main__":
    main()