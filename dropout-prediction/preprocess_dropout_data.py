# Student Dropout Prediction - Data Preprocessing
# Dataset: "Predict Students' Dropout and Academic Success" (UCI ML Repository)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the dataset
df = pd.read_csv("data.csv", sep=";")

print("Shape of dataset (rows, columns):", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nTarget column value counts (Dropout / Enrolled / Graduate):")
print(df["Target"].value_counts())

# Check for missing values
print("\nMissing values per column:")
print(df.isnull().sum().sum(), "total missing cells")

# Feature engineering - create useful new columns from existing data
# total_units_approved = total subjects passed across both semesters
df["total_units_approved"] = (
    df["Curricular units 1st sem (approved)"]
    + df["Curricular units 2nd sem (approved)"]
)

# What fraction of enrolled subjects were passed each semester
df["approval_rate_1st_sem"] = (
    df["Curricular units 1st sem (approved)"]
    / (df["Curricular units 1st sem (enrolled)"] + 1e-6)
)
df["approval_rate_2nd_sem"] = (
    df["Curricular units 2nd sem (approved)"]
    / (df["Curricular units 2nd sem (enrolled)"] + 1e-6)
)

# Did the student's grade drop from sem 1 to sem 2?
df["grade_drop_sem1_to_sem2"] = (
    df["Curricular units 1st sem (grade)"]
    - df["Curricular units 2nd sem (grade)"]
)

# 1 if tuition is NOT up to date (financial risk)
df["financial_risk_flag"] = (df["Tuition fees up to date"] == 0).astype(int)

# Convert text labels (Dropout/Enrolled/Graduate) into numbers
target_encoder = LabelEncoder()
df["Target_encoded"] = target_encoder.fit_transform(df["Target"])

print("\nTarget classes mapped as:",
      dict(zip(target_encoder.classes_,
                target_encoder.transform(target_encoder.classes_))))

# Separate features (X) and target (y)
X = df.drop(columns=["Target", "Target_encoded"])
y = df["Target_encoded"]

# 80% training, 20% testing, stratified to keep same class ratio in both
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("\nTraining set size:", X_train.shape)
print("Testing set size:", X_test.shape)

# Save the cleaned data for the next step
df.to_csv("dropout_data_preprocessed.csv", index=False)
print("\nSaved cleaned dataset as 'dropout_data_preprocessed.csv'")
