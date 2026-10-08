# College data (Indian context) -> UCI features -> predict
# Constants for Indian bachelor's context, mappings for available fields
import pandas as pd
import joblib
import numpy as np

model = joblib.load("final_dropout_model.pkl")
train_df = pd.read_csv("dropout_data_preprocessed.csv")

# Training stats for filling truly unknown features
train_mode = train_df.mode().iloc[0]
train_median = train_df.select_dtypes(include=[np.number]).median()

# Model expects these 41 features in this exact order
FEATURE_ORDER = [
    'Marital status', 'Application mode', 'Application order', 'Course',
    'Daytime/evening attendance\t', 'Previous qualification',
    'Previous qualification (grade)', 'Nacionality', "Mother's qualification",
    "Father's qualification", "Mother's occupation", "Father's occupation",
    'Admission grade', 'Displaced', 'Educational special needs', 'Debtor',
    'Tuition fees up to date', 'Gender', 'Scholarship holder',
    'Age at enrollment', 'International',
    'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)',
    'Curricular units 1st sem (evaluations)', 'Curricular units 1st sem (approved)',
    'Curricular units 1st sem (grade)', 'Curricular units 1st sem (without evaluations)',
    'Curricular units 2nd sem (credited)', 'Curricular units 2nd sem (enrolled)',
    'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (approved)',
    'Curricular units 2nd sem (grade)', 'Curricular units 2nd sem (without evaluations)',
    'Unemployment rate', 'Inflation rate', 'GDP',
    'total_units_approved', 'approval_rate_1st_sem', 'approval_rate_2nd_sem',
    'grade_drop_sem1_to_sem2', 'financial_risk_flag'
]

class_names = ["Dropout", "Enrolled", "Graduate"]

# India 2024 macro constants
INDIA_UNEMPLOYMENT = 8.5
INDIA_INFLATION = 5.5
INDIA_GDP = 6.5

def college_to_uci(college_df):
    """
    Convert college-format DataFrame to UCI feature matrix.
    
    Required college columns (flexible names accepted):
    - Student_ID / Roll_No / Name
    - CGPA_Sem1, CGPA_Sem2 (0-10 scale)
    - Subjects_Passed_Sem1, Subjects_Passed_Sem2 (or just Passed_Sem1/2)
    - Subjects_Enrolled_Sem1, Subjects_Enrolled_Sem2 (default 6)
    - Fees_Paid (1=yes, 0=no) or Fees_Status ("Paid"/"Unpaid")
    - Attendance_Pct (0-100) - optional, used to adjust approval rates
    - Scholarship (1/0) - optional
    - Debtor (1/0) - optional, default 0
    - Age - optional, default 19
    - Gender (0=M, 1=F) - optional, default 1
    - Parent_Income - optional, used for Debtor/Scholarship proxy
    - Admission_Grade - optional, default 130
    - Mother_Qual, Father_Qual - optional, default 19 (secondary)
    - Mother_Occ, Father_Occ - optional, default 5
    - Course_Code - optional, default 9119 (engineering)
    - Previous_Qual - optional, default 1 (high school)
    - Prev_Qual_Grade - optional, default 130
    """
    n = len(college_df)
    uci = pd.DataFrame(index=range(n))
    c = college_df  # shorthand
    
    # Helper to get column with flexible names
    def get_col(*names, default=None):
        for name in names:
            if name in c.columns:
                return c[name]
        return pd.Series([default] * n, index=c.index)
    
    # ---- CONSTANTS for Indian bachelor's context ----
    uci["Marital status"] = 1                    # 1 = single (virtually all)
    uci["Application mode"] = 1                  # 1 = general admission
    uci["Application order"] = 1                 # 1 = first choice
    uci["Daytime/evening attendance\t"] = 1      # 1 = daytime (full-time)
    uci["Displaced"] = 1                         # 1 = not displaced
    uci["Educational special needs"] = 0         # 0 = no
    uci["International"] = 0                     # 0 = domestic
    uci["Nacionality"] = 1                       # 1 = Portuguese in original, use 1 as default category
    uci["Unemployment rate"] = INDIA_UNEMPLOYMENT
    uci["Inflation rate"] = INDIA_INFLATION
    uci["GDP"] = INDIA_GDP
    
    # ---- MAPPED from college data ----
    uci["Course"] = get_col("Course_Code", "Course", "course_code", default=9119)
    uci["Previous qualification"] = get_col("Previous_Qual", "Prev_Qual", "previous_qual", default=1)
    uci["Previous qualification (grade)"] = get_col("Prev_Qual_Grade", "Prev_Qual_Grade", "prev_qual_grade", default=130)
    
    # Parent background (use training median if not provided)
    uci["Mother's qualification"] = get_col("Mother_Qual", "Mother_qual", "mother_qual", default=int(train_median["Mother's qualification"]))
    uci["Father's qualification"] = get_col("Father_Qual", "Father_qual", "father_qual", default=int(train_median["Father's qualification"]))
    uci["Mother's occupation"] = get_col("Mother_Occ", "Mother_occ", "mother_occ", default=int(train_median["Mother's occupation"]))
    uci["Father's occupation"] = get_col("Father_Occ", "Father_occ", "father_occ", default=int(train_median["Father's occupation"]))
    
    uci["Admission grade"] = get_col("Admission_Grade", "Admission_grade", "admission_grade", default=130)
    
    # Financial
    fees_paid = get_col("Fees_Paid", "Fees_paid", "fees_paid", "Fees_Status", "fees_status")
    # Handle "Paid"/"Unpaid" strings
    if fees_paid.dtype == object:
        fees_paid = fees_paid.map({"Paid": 1, "paid": 1, "Yes": 1, "yes": 1, "1": 1, "Unpaid": 0, "unpaid": 0, "No": 0, "no": 0, "0": 0}).fillna(1)
    uci["Tuition fees up to date"] = fees_paid.fillna(1).astype(int)
    
    uci["Debtor"] = get_col("Debtor", "debtor", default=0).fillna(0).astype(int)
    uci["Scholarship holder"] = get_col("Scholarship", "scholarship", default=0).fillna(0).astype(int)
    
    # Demographics
    uci["Gender"] = get_col("Gender", "gender", "Sex", "sex", default=1).fillna(1).astype(int)
    uci["Age at enrollment"] = get_col("Age", "age", default=19).fillna(19).astype(int)
    
    # ---- ACADEMICS: CGPA (0-10) -> Grade (0-20) ----
    cgpa1 = get_col("CGPA_Sem1", "CGPA1", "cgpa_sem1", "cgpa1", default=7.0)
    cgpa2 = get_col("CGPA_Sem2", "CGPA2", "cgpa_sem2", "cgpa2", default=7.0)
    uci["Curricular units 1st sem (grade)"] = cgpa1 * 2
    uci["Curricular units 2nd sem (grade)"] = cgpa2 * 2
    
    # Subjects passed/enrolled
    passed1 = get_col("Subjects_Passed_Sem1", "Passed_Sem1", "passed_sem1", default=6)
    passed2 = get_col("Subjects_Passed_Sem2", "Passed_Sem2", "passed_sem2", default=6)
    enrolled1 = get_col("Subjects_Enrolled_Sem1", "Enrolled_Sem1", "enrolled_sem1", default=6)
    enrolled2 = get_col("Subjects_Enrolled_Sem2", "Enrolled_Sem2", "enrolled_sem2", default=6)
    
    uci["Curricular units 1st sem (approved)"] = passed1
    uci["Curricular units 2nd sem (approved)"] = passed2
    uci["Curricular units 1st sem (enrolled)"] = enrolled1
    uci["Curricular units 2nd sem (enrolled)"] = enrolled2
    
    # Evaluations = enrolled (all subjects have exams)
    uci["Curricular units 1st sem (evaluations)"] = enrolled1
    uci["Curricular units 2nd sem (evaluations)"] = enrolled2
    
    # Credited / without evaluations = 0 (no credit transfers typically)
    uci["Curricular units 1st sem (credited)"] = 0
    uci["Curricular units 2nd sem (credited)"] = 0
    uci["Curricular units 1st sem (without evaluations)"] = 0
    uci["Curricular units 2nd sem (without evaluations)"] = 0
    
    # ---- TARGET placeholder ----
    if "Actual_Outcome" in c.columns:
        uci["Target"] = c["Actual_Outcome"]
    else:
        uci["Target"] = "Graduate"
    
    return uci

def add_engineered_features(df):
    df = df.copy()
    df["total_units_approved"] = (
        df["Curricular units 1st sem (approved)"] + df["Curricular units 2nd sem (approved)"]
    )
    df["approval_rate_1st_sem"] = (
        df["Curricular units 1st sem (approved)"] / (df["Curricular units 1st sem (enrolled)"] + 1e-6)
    )
    df["approval_rate_2nd_sem"] = (
        df["Curricular units 2nd sem (approved)"] / (df["Curricular units 2nd sem (enrolled)"] + 1e-6)
    )
    df["grade_drop_sem1_to_sem2"] = (
        df["Curricular units 1st sem (grade)"] - df["Curricular units 2nd sem (grade)"]
    )
    df["financial_risk_flag"] = (df["Tuition fees up to date"] == 0).astype(int)
    return df

def predict_college_data(college_csv_path, output_csv="college_predictions.csv"):
    """Main function: read college CSV, predict, save results"""
    college_df = pd.read_csv(college_csv_path)
    
    # Map to UCI
    uci_df = college_to_uci(college_df)
    uci_df = add_engineered_features(uci_df)
    
    # Select features in correct order
    X = uci_df[FEATURE_ORDER]
    
    # Predict
    preds = model.predict(X)
    probs = model.predict_proba(X)
    
    # Build results
    id_col = None
    for c in ["Student_ID", "Roll_No", "Register_No", "Name", "Student_Name"]:
        if c in college_df.columns:
            id_col = c
            break
    
    results = pd.DataFrame()
    results["Student_ID"] = college_df[id_col] if id_col else [f"Student_{i+1}" for i in range(n)]
    if "Name" in college_df.columns:
        results["Name"] = college_df["Name"]
    results["Predicted"] = [class_names[p] for p in preds]
    results["Dropout_Prob_%"] = (probs[:, 0] * 100).round(1)
    results["Enrolled_Prob_%"] = (probs[:, 1] * 100).round(1)
    results["Graduate_Prob_%"] = (probs[:, 2] * 100).round(1)
    results["Risk_Level"] = pd.cut(probs[:, 0], bins=[-0.01, 0.3, 0.6, 1.0], labels=["Low", "Medium", "High"])
    
    if "Actual_Outcome" in college_df.columns:
        results["Actual"] = college_df["Actual_Outcome"]
        from sklearn.metrics import accuracy_score
        acc = accuracy_score(college_df["Actual_Outcome"], results["Predicted"])
        print(f"Accuracy: {acc*100:.1f}%")
    
    results = results.sort_values("Dropout_Prob_%", ascending=False).reset_index(drop=True)
    results.to_csv(output_csv, index=False)
    print(f"Saved {output_csv} with {len(results)} predictions")
    return results


if __name__ == "__main__":
    # Demo with sample data
    sample = pd.DataFrame([
        {"Student_ID": "CS2024001", "Name": "Arjun Sharma", "CGPA_Sem1": 8.5, "CGPA_Sem2": 8.2,
         "Subjects_Passed_Sem1": 6, "Subjects_Passed_Sem2": 6, "Subjects_Enrolled_Sem1": 6, "Subjects_Enrolled_Sem2": 6,
         "Attendance_Pct": 85, "Fees_Paid": 1, "Scholarship": 0, "Debtor": 0, "Age": 19, "Gender": 0,
         "Parent_Income": 800000, "Admission_Grade": 145, "Actual_Outcome": "Graduate"},
        {"Student_ID": "CS2024002", "Name": "Priya Patel", "CGPA_Sem1": 6.2, "CGPA_Sem2": 5.8,
         "Subjects_Passed_Sem1": 4, "Subjects_Passed_Sem2": 3, "Subjects_Enrolled_Sem1": 6, "Subjects_Enrolled_Sem2": 6,
         "Attendance_Pct": 65, "Fees_Paid": 0, "Scholarship": 1, "Debtor": 1, "Age": 20, "Gender": 1,
         "Parent_Income": 300000, "Admission_Grade": 110, "Actual_Outcome": "Dropout"},
        {"Student_ID": "CS2024003", "Name": "Rahul Kumar", "CGPA_Sem1": 7.0, "CGPA_Sem2": 6.5,
         "Subjects_Passed_Sem1": 5, "Subjects_Passed_Sem2": 5, "Subjects_Enrolled_Sem1": 6, "Subjects_Enrolled_Sem2": 6,
         "Attendance_Pct": 75, "Fees_Paid": 1, "Scholarship": 0, "Debtor": 0, "Age": 21, "Gender": 0,
         "Parent_Income": 500000, "Admission_Grade": 125, "Actual_Outcome": "Enrolled"},
        {"Student_ID": "CS2024004", "Name": "Sneha Reddy", "CGPA_Sem1": 9.1, "CGPA_Sem2": 8.9,
         "Subjects_Passed_Sem1": 6, "Subjects_Passed_Sem2": 6, "Subjects_Enrolled_Sem1": 6, "Subjects_Enrolled_Sem2": 6,
         "Attendance_Pct": 92, "Fees_Paid": 1, "Scholarship": 1, "Debtor": 0, "Age": 18, "Gender": 1,
         "Parent_Income": 1200000, "Admission_Grade": 155, "Actual_Outcome": "Graduate"},
        {"Student_ID": "CS2024005", "Name": "Vikram Singh", "CGPA_Sem1": 5.5, "CGPA_Sem2": 4.8,
         "Subjects_Passed_Sem1": 2, "Subjects_Passed_Sem2": 1, "Subjects_Enrolled_Sem1": 6, "Subjects_Enrolled_Sem2": 6,
         "Attendance_Pct": 45, "Fees_Paid": 0, "Scholarship": 0, "Debtor": 1, "Age": 22, "Gender": 0,
         "Parent_Income": 250000, "Admission_Grade": 100, "Actual_Outcome": "Dropout"}
    ])
    
    sample.to_csv("college_format_sample.csv", index=False)
    print("Created college_format_sample.csv")
    
    results = predict_college_data("college_format_sample.csv")
    print("\nPredictions (highest dropout risk first):")
    print(results[["Student_ID", "Name", "Predicted", "Dropout_Prob_%", "Risk_Level"]].to_string(index=False))