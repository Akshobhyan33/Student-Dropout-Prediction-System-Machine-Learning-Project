import io

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report

MODEL_PATH = "final_dropout_model.pkl"
DATA_PATH = "dropout_data_preprocessed.csv"

CLASS_NAMES = ["Dropout", "Enrolled", "Graduate"]
RISK_BINS = [-0.01, 0.3, 0.6, 1.0]
RISK_LABELS = ["Low", "Medium", "High"]
ID_COLUMNS = ["Student_ID", "Roll_No", "Register_No", "Name", "Student_Name"]
COLLEGE_FORMAT_KEYS = ["CGPA_Sem1", "Subjects_Passed_Sem1", "CGPA1", "Passed_Sem1"]
EXCLUDE_COLUMNS = [
    "Target",
    "Target_encoded",
    "Student_ID",
    "Roll_No",
    "Register_No",
    "Name",
    "Student_Name",
]


def load_artifacts(model_path=MODEL_PATH, data_path=DATA_PATH):
    model = joblib.load(model_path)
    df = pd.read_csv(data_path)
    features = df.drop(columns=["Target", "Target_encoded"])
    feature_defaults = features.mean()
    return model, df, features, feature_defaults


def predict_single(model, feature_defaults, features, values):
    input_row = feature_defaults.copy()
    input_row["approval_rate_2nd_sem"] = values["sem2_approval_rate"]
    input_row["Curricular units 2nd sem (approved)"] = values["sem2_units_approved"]
    input_row["Curricular units 2nd sem (grade)"] = values["sem2_grade"] * 2
    input_row["total_units_approved"] = values["total_units_approved"]
    input_row["approval_rate_1st_sem"] = values["sem1_approval_rate"]
    input_row["Tuition fees up to date"] = 1 if values["tuition_up_to_date"] == "Yes" else 0
    input_row["Scholarship holder"] = 1 if values["scholarship"] == "Yes" else 0
    input_row["Age at enrollment"] = values["age"]

    input_df = pd.DataFrame([input_row])[features.columns]
    predicted_class = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0]

    return {
        "outcome": CLASS_NAMES[predicted_class],
        "probabilities": probabilities,
        "confidence": float(max(probabilities)) * 100,
    }


def read_uploaded_csv(uploaded_file):
    try:
        content = uploaded_file.getvalue().decode("utf-8")
        if ";" in content.split("\n")[0]:
            return pd.read_csv(io.StringIO(content), sep=";")
        return pd.read_csv(io.StringIO(content))
    except Exception:
        return pd.read_csv(uploaded_file)


def detect_format(students_df):
    return any(col in students_df.columns for col in COLLEGE_FORMAT_KEYS)


def _identifier_column(students_df):
    for col in ID_COLUMNS:
        if col in students_df.columns:
            return col
    return None


def _add_engineered_features(proc):
    proc["total_units_approved"] = (
        proc["Curricular units 1st sem (approved)"]
        + proc["Curricular units 2nd sem (approved)"]
    )
    proc["approval_rate_1st_sem"] = (
        proc["Curricular units 1st sem (approved)"]
        / (proc["Curricular units 1st sem (enrolled)"] + 1e-6)
    )
    proc["approval_rate_2nd_sem"] = (
        proc["Curricular units 2nd sem (approved)"]
        / (proc["Curricular units 2nd sem (enrolled)"] + 1e-6)
    )
    proc["grade_drop_sem1_to_sem2"] = (
        proc["Curricular units 1st sem (grade)"]
        - proc["Curricular units 2nd sem (grade)"]
    )
    proc["financial_risk_flag"] = (proc["Tuition fees up to date"] == 0).astype(int)
    return proc


def predict_batch(model, students_df, college_to_uci, add_engineered_features, feature_order):
    is_college_format = detect_format(students_df)
    id_col = _identifier_column(students_df)
    fallback_ids = [f"Student_{i + 1}" for i in range(len(students_df))]

    if is_college_format:
        uci_df = college_to_uci(students_df)
        uci_df = add_engineered_features(uci_df)
        X_batch = uci_df[feature_order]
    else:
        proc = _add_engineered_features(students_df.copy())
        feature_cols = [c for c in proc.columns if c not in EXCLUDE_COLUMNS]
        X_batch = proc[feature_cols]

    predictions = model.predict(X_batch)
    probabilities = model.predict_proba(X_batch)

    results = pd.DataFrame()
    results["Student_ID"] = students_df[id_col] if id_col else fallback_ids
    if "Name" in students_df.columns:
        results["Name"] = students_df["Name"]
    if is_college_format:
        if "CGPA_Sem1" in students_df.columns:
            results["CGPA_Sem1"] = students_df["CGPA_Sem1"]
            results["CGPA_Sem2"] = students_df["CGPA_Sem2"]
        if "Attendance_Pct" in students_df.columns:
            results["Attendance_%"] = students_df["Attendance_Pct"]
        if "Fees_Paid" in students_df.columns:
            results["Fees_Paid"] = students_df["Fees_Paid"]

    results["Predicted"] = [CLASS_NAMES[p] for p in predictions]
    results["Dropout_Prob_%"] = (probabilities[:, 0] * 100).round(1)
    results["Enrolled_Prob_%"] = (probabilities[:, 1] * 100).round(1)
    results["Graduate_Prob_%"] = (probabilities[:, 2] * 100).round(1)
    results["Risk_Level"] = pd.cut(
        probabilities[:, 0], bins=RISK_BINS, labels=RISK_LABELS
    ).astype(str)
    results = results.sort_values("Dropout_Prob_%", ascending=False).reset_index(drop=True)

    risk_counts = {label: int((results["Risk_Level"] == label).sum()) for label in RISK_LABELS}

    actual_col = None
    for candidate in ("Target", "Actual_Outcome"):
        if candidate in students_df.columns:
            actual_col = candidate
            break

    accuracy = None
    report = None
    if actual_col:
        accuracy = accuracy_score(students_df[actual_col], results["Predicted"])
        report = classification_report(
            students_df[actual_col], results["Predicted"], zero_division=0
        )

    return {
        "results": results,
        "format": "college" if is_college_format else "uci",
        "risk_counts": risk_counts,
        "accuracy": accuracy,
        "report": report,
        "actual_col": actual_col,
    }