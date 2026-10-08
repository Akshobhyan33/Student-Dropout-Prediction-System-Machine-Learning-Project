import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier

# Load preprocessed data
df = pd.read_csv("dropout_data_preprocessed.csv")
X = df.drop(columns=["Target", "Target_encoded"])
y = df["Target_encoded"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

class_names = ["Dropout", "Enrolled", "Graduate"]

# SMOTE creates extra samples for the minority classes so the model isn't biased
print("Before SMOTE:", y_train.value_counts().to_dict())
smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)
print("After SMOTE:", y_train_bal.value_counts().to_dict())

# Search for the best settings for Random Forest
param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [None, 10, 20],
    "min_samples_split": [2, 5],
}

print("\nRunning hyperparameter search (this may take a minute)...")
grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42, class_weight="balanced"),
    param_grid,
    cv=5,
    scoring="f1_macro",
    n_jobs=-1,
)
grid_search.fit(X_train_bal, y_train_bal)

print("Best parameters found:", grid_search.best_params_)
best_rf = grid_search.best_estimator_

rf_preds = best_rf.predict(X_test)
print("\n" + "=" * 50)
print("TUNED RANDOM FOREST RESULTS")
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, rf_preds))
print(classification_report(y_test, rf_preds, target_names=class_names))

# XGBoost - a gradient boosting model that often performs very well
xgb_model = XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric="mlogloss",
)
xgb_model.fit(X_train_bal, y_train_bal)
xgb_preds = xgb_model.predict(X_test)

print("\n" + "=" * 50)
print("XGBOOST RESULTS")
print("=" * 50)
print("Accuracy:", accuracy_score(y_test, xgb_preds))
print(classification_report(y_test, xgb_preds, target_names=class_names))

# Cross-validation checks how well each model generalizes on unseen data
cv_scores_rf = cross_val_score(best_rf, X, y, cv=5, scoring="accuracy")
cv_scores_xgb = cross_val_score(xgb_model, X, y, cv=5, scoring="accuracy")

print("\nRandom Forest 5-fold CV accuracy: {:.3f} (+/- {:.3f})".format(
    cv_scores_rf.mean(), cv_scores_rf.std()))
print("XGBoost 5-fold CV accuracy: {:.3f} (+/- {:.3f})".format(
    cv_scores_xgb.mean(), cv_scores_xgb.std()))

# Pick whichever model performs better on cross-validation
final_model, final_name = (
    (xgb_model, "XGBoost") if cv_scores_xgb.mean() > cv_scores_rf.mean()
    else (best_rf, "Random Forest")
)
print(f"\nFinal chosen model: {final_name}")

# Save the best model so the Streamlit app can use it
joblib.dump(final_model, "final_dropout_model.pkl")
print("Saved best model as 'final_dropout_model.pkl'")

final_preds = final_model.predict(X_test)
cm = confusion_matrix(y_test, final_preds)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap="Blues")
plt.title(f"{final_name} (Tuned) - Confusion Matrix")
plt.tight_layout()
plt.savefig("confusion_matrix_final.png")
print("Saved 'confusion_matrix_final.png'")
