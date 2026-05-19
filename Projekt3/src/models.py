from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


def get_models():
    return {
        "Logistic Regression":
            LogisticRegression(max_iter=1000),

        "KNN":
            KNeighborsClassifier(n_neighbors=5),

        "Decision Tree":
            DecisionTreeClassifier(
                max_depth=5,
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=100,
                max_depth=5,
                random_state=42
            ),

        "SVM":
            SVC(
                kernel="rbf",
                probability=True
            ),

        "Neural Network":
            MLPClassifier(
                hidden_layer_sizes=(64, 32),
                activation="relu",
                max_iter=500,
                random_state=42
            )
    }