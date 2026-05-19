from sklearn.model_selection import GridSearchCV

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    make_scorer
)

from src.scoring import calculate_combined_score

def combined_scorer(
        estimator,
        X,
        y
):

    y_pred = estimator.predict(X)

    if hasattr(estimator, "predict_proba"):
        y_proba = estimator.predict_proba(X)

        loss = log_loss(
            y,
            y_proba
        )
    else:
        loss = 0

    metrics = {
        "accuracy":
            accuracy_score(y, y_pred),

        "precision":
            precision_score(
                y,
                y_pred,
                zero_division=0
            ),

        "recall":
            recall_score(
                y,
                y_pred,
                zero_division=0
            ),

        "f1":
            f1_score(
                y,
                y_pred,
                zero_division=0
            ),

        "loss":
            loss
    }

    return calculate_combined_score(
        metrics
    )

def get_tuned_models(X_train, y_train):

    models_params = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000),
            {
                "C": [0.005, 0.01, 0.02, 0.03, 0.05, 0.1, 1, 10]
            }
        ),

        "KNN": (
            KNeighborsClassifier(),
            {
                "n_neighbors": [3, 5, 7, 8, 9, 10, 11, 12],
                "weights": [
                    "uniform",
                    "distance"
                ]
            }
        ),

        "Decision Tree": (
            DecisionTreeClassifier(
                random_state=42
            ),
            {
                "max_depth": [1, 2, 3, 4, 5, 7, 10],
                "min_samples_split":
                    [2, 3, 5, 10]
            }
        ),

        "Random Forest": (
            RandomForestClassifier(
                random_state=42
            ),
            {
                "n_estimators":
                    [40, 50, 60, 100, 200],

                "max_depth":
                    [1, 2, 3, 5, 10],

                "min_samples_split":
                    [2, 3, 4, 5, 6]
            }
        ),

        "SVM": (
            SVC(probability=True),
            {
                "C": [0.03, 0.04, 0.05, 0.1, 0.2, 1, 10],

                "kernel": [
                    "linear",
                    "rbf"
                ]
            }
        ),

        "Neural Network": (
            MLPClassifier(
                random_state=42,
                max_iter=3000,
                early_stopping=True,
                n_iter_no_change=20
            ),
            {
                "hidden_layer_sizes": [
                    (32,),
                    (64,),
                    (64, 32)
                ],

                "activation": [
                    "relu",
                    "tanh"
                ],

                "learning_rate_init": [
                    0.001,
                    0.01,
                    0.02,
                    0.03
                ]
            }
        )
    }

    best_models = {}

    for name, (
        model,
        params
    ) in models_params.items():

        print(f"\nTuning {name}...")

        grid_search = GridSearchCV(
            estimator=model,
            param_grid=params,
            cv=5,
            scoring=combined_scorer,
            n_jobs=-1
        )

        grid_search.fit(
            X_train,
            y_train
        )

        best_models[name] = (
            grid_search.best_estimator_
        )

        print(
            f"Best params for "
            f"{name}: "
            f"{grid_search.best_params_}"
        )

        print(
            f"Best CV score: "
            f"{grid_search.best_score_:.4f}"
        )

    return best_models