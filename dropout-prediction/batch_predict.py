# Batch prediction for student dropout risk
import pandas as pd
import joblib

# Load trained model
model = joblib.load("final_dropout_model.pkl")
class_names = ["Dropout", "Enrolled", "Graduate"]

# Read student data (must have the 37 original columns)
# Try semicolon first (original dataset format), fallback to comma
try:
    df = pd.read_csv("students_to_predict.csv", sep=";")
except:
    df = pd.read_csv("students_to_predict.csv")

# Same preprocessing as training
df["total_units_approved"] = (
    df["Curricular units 1st sem (approved)"]
    + df["Curricular units 2nd sem (approved)"]
)
df["approval_rate_1st_sem"] = (
    df["Curricular units 1st sem (approved)"]
    / (df["Curricular units 1st sem (enrolled)"] + 1e-6)
)
df["approval_rate_2nd_sem"] = (
    df["Curricular units 2nd sem (approved)"]
    / (df["Curricular units 2nd sem (enrolled)"] + 1e-6)
)
df["grade_drop_sem1_to_sem2"] = (
    df["Curricular units 1st sem (grade)"]
    - df["Curricular units 2nd sem (grade)"]
)
df["financial_risk_flag"] = (df["Tuition fees up to date"] == 0).astype(int)

# Features the model expects
feature_cols = [c for c in df.columns if c not in ["Target", "Target_encoded"]]
X = df[feature_cols]

# Predict
preds = model.predict(X)
probs = model.predict_proba(X)

# Build results
results = df[["Target"]].copy() if "Target" in df.columns else pd.DataFrame()
results["Predicted"] = [class_names[p] for p in preds]
results["Confidence_Dropout"] = probs[:, 0]
results["Confidence_Enrolled"] = probs[:, 1]
results["Confidence_Graduate"] = probs[:, 2]
results["Dropout_Risk"] = (preds == 0).astype(int)

# Save
results.to_csv("predictions.csv", index=False)
print("Saved predictions.csv with", len(results), "students")

# If true labels exist, print metrics
if "Target" in df.columns:
    from sklearn.metrics import accuracy_score, classification_report
    print("\nOverall accuracy:", accuracy_score(df["Target"], results["Predicted"]))
    print(classification_report(df["Target"], results["Predicted"]))