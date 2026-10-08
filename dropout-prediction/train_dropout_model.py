# Student Dropout Prediction - Model Training & Evaluation
# Run this AFTER preprocess_dropout_data.py

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

# Load preprocessed data
df = pd.read_csv("dropout_data_preprocessed.csv")

X = df.drop(columns=["Target", "Target_encoded"])
y = df["Target_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

class_names = ["Dropout", "Enrolled", "Graduate"]

# Model 1: Logistic Regression (simple baseline)
log_model = LogisticRegression(max_iter=2000, class_weight="balanced")
log_model.fit(X_train, y_train)
log_preds = log_model.predict(X_test)

print("=" * 50)
print("LOGISTIC REGRESSION RESULTS")
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, log_preds))
print(classification_report(y_test, log_preds, target_names=class_names))

# Model 2: Random Forest (better at capturing non-linear patterns)
rf_model = RandomForestClassifier(
    n_estimators=200, class_weight="balanced", random_state=42
)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

print("=" * 50)
print("RANDOM FOREST RESULTS")
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, rf_preds))
print(classification_report(y_test, rf_preds, target_names=class_names))

# Confusion matrix - shows where the model gets confused
cm = confusion_matrix(y_test, rf_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap="Blues")
plt.title("Random Forest - Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix.png")
print("\nSaved confusion matrix chart as 'confusion_matrix.png'")

# Which features matter most for the prediction?
importances = pd.Series(rf_model.feature_importances_, index=X.columns)
top_features = importances.sort_values(ascending=False).head(10)

plt.figure(figsize=(8, 5))
top_features.sort_values().plot(kind="barh", color="#2E7D32")
plt.title("Top 10 Features Driving Dropout Prediction")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig("feature_importance.png")
print("Saved feature importance chart as 'feature_importance.png'")

print("\nTop 10 most important features:")
print(top_features.sort_values(ascending=False))
