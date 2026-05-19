Program do znajdywania najlepszego modelu do przewidywania chorób serca.
Dataset: https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset/data

14 kolumn:
age
sex
chest pain type (4 values)
resting blood pressure
serum cholestoral in mg/dl
fasting blood sugar > 120 mg/dl
resting electrocardiographic results (values 0,1,2)
maximum heart rate achieved
exercise induced angina
oldpeak = ST depression induced by exercise relative to rest
the slope of the peak exercise ST segment
number of major vessels (0-3) colored by flourosopy
thal: 0 = normal; 1 = fixed defect; 2 = reversable defect
target: 0 = normall; 1 = ill


Etapy:

I Preprocessing:
src/preprocessing.py
Usunięcie duplikatów (około 700)
Podział na cechy i etykiety
Podział trening 80% / test 20%
Imputacja danych (nie potrzebna bo nie ma NULLi, ale dana dla przykładu)
Skalowanie danych, istotne dla Logistic Regression, KNN, SVM, Neural Network

II EDA (Exploratory Data Analysis):
src/eda.py
Wyświetla informacje o danych wstępnych, mediana, średnia itp.

III Strojenie hiperparametrów:
src/tuning.py
GridSearchCV do sprawdzenia jaka kombinacja parametrów daje najlepsze wyniki dla każdego modelu na danych treningowych
Logistic Regression - C (regularyzacja modelu)
KNN - liczba sąsiadów i sposób głosowania
Decision Tree - maksymalna głębokość drzewa i minimalna liczba próbek do podziału
Random Forest - maksymalna głębokość drzewa, minimalna liczba próbek do podziału i ilość drzew
SVM - C i jądro
Neural Network - architektura sieci, funkcja aktywacji i learning rate

IV Trenowanie modeli:
main.py
Dla każdego dostrojonego modelu dajemy model.fit z danymi treningowymi

V Ewaluacja:
src/evaluation.py
Accuracy
Precision
Recall
F1-score
Log Loss
Confusion Matrix:
TN FP
FN TP

VI
