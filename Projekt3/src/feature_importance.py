import matplotlib.pyplot as plt
import pandas as pd
import os


def plot_feature_importance(
        model,
        feature_names,
        model_name
):
    # tylko modele z importance
    if not hasattr(
            model,
            "feature_importances_"
    ):
        return

    importance = (
        model.feature_importances_
    )

    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importance
    })

    importance_df = (
        importance_df
        .sort_values(
            by="importance",
            ascending=False
        )
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        importance_df["feature"],
        importance_df["importance"]
    )

    plt.xlabel("Importance")

    plt.title(
        f"Feature Importance - "
        f"{model_name}"
    )

    plt.gca().invert_yaxis()

    os.makedirs(
        "results/feature_importance",
        exist_ok=True
    )

    plt.savefig(
        f"results/"
        f"feature_importance/"
        f"{model_name}.png"
    )

    plt.close()

    print(
        f"\nTop features "
        f"for {model_name}:"
    )

    print(
        importance_df.head(10)
    )