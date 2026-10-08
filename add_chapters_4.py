# Adds chapters 4-8 to PBL report
from docx import Document
from docx.shared import Pt, RGBColor
from docx.oxml.ns import qn

doc = Document('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL_Report_Filled.docx')

def add_para(text, bold=False, size=11, after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return p

def add_heading(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14 if level == 1 else (12 if level == 2 else 11))
    run.font.name = 'Times New Roman'
    return p

def add_bullet(text, size=11):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Pt(12)
    run = p.add_run('• ' + text)
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return p

def add_code(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Courier New'
    run.font.size = Pt(9)
    return p

# ============ CHAPTER 4: ITERATIVE DESIGN ============
add_heading('CHAPTER 4', level=1)
add_heading('ITERATIVE DESIGN AND DEVELOPMENT', level=1)

add_heading('4.1 System Architecture', level=2)
add_para('The end-to-end pipeline consists of six main blocks:')
add_bullet('Data Input: Raw student dataset loaded from CSV file.')
add_bullet('Preprocessing: Handling missing values, encoding categorical labels, splitting into training and testing sets.')
add_bullet('Feature Engineering: Creating new features from existing ones (approval rates, total units, financial risk flag).')
add_bullet('Model Training: Training classification models using different algorithms with hyperparameter tuning.')
add_bullet('Evaluation: Measuring accuracy, precision, recall, F1-score, and cross-validation scores.')
add_bullet('Output/Deployment: Saving predictions as CSV files and displaying results via Streamlit web interface.')
add_para('This pipeline is represented as Figure 4.1 and shows the flow from raw data through preprocessing, feature engineering, model selection, and final deployment as a web application.')

add_heading('4.2 Iteration 1 — Baseline (Logistic Regression)', level=2)
add_para('The simplest working version used Logistic Regression with max_iter=2000 and class_weight="balanced". The dataset was preprocessed with basic feature engineering (total_units_approved, approval_rate_1st_sem, approval_rate_2nd_sem, grade_drop_sem1_to_sem2, financial_risk_flag) and LabelEncoder for the target variable. The training-test split was 80-20 with stratification to maintain class ratios.')
add_para('Results: Accuracy of 72.8%, Dropout F1-score of 0.74, Graduate F1-score of 0.82, Enrolled F1-score of 0.51. The low Enrolled performance indicated that class imbalance was a significant problem. This limitation motivated the next iteration.')

add_heading('4.3 Iteration 2 — Refinement (Random Forest)', level=2)
add_para('Based on mentor feedback about the poor Enrolled class performance in Iteration 1, the team moved to Random Forest with 200 estimators and class_weight="balanced". Random Forest captures non-linear relationships between features and the target variable that logistic regression cannot model. The same feature engineering pipeline was reused with no changes to the preprocessing logic.')
add_para('Results: Accuracy improved to 75.6%. Dropout F1-score improved to 0.78, Graduate F1-score to 0.85, Enrolled F1-score to 0.50. The confusion matrix showed that the model was confusing Enrolled and Graduate students most frequently. Feature importance analysis revealed that approval_rate_2nd_sem was the most important predictor.')

add_heading('4.4 Iteration 3 — Advanced Refinement (SMOTE + GridSearchCV + XGBoost)', level=2)
add_para('Mentor feedback identified class imbalance as the root cause of poor Enrolled class predictions. The team implemented SMOTE (Synthetic Minority Over-sampling Technique) to balance the training classes from {Graduate: 1767, Dropout: 1137, Enrolled: 635} to {Graduate: 1767, Dropout: 1767, Enrolled: 1767}. Additionally, GridSearchCV with 5-fold cross-validation was used to systematically search optimal hyperparameters for Random Forest (n_estimators: [100, 200, 300], max_depth: [None, 10, 20], min_samples_split: [2, 5]).')
add_para('XGBoost was also implemented as a comparison model with 300 estimators, max_depth=6, learning_rate=0.1. Both models were trained on SMOTE-balanced data.')
add_para('Results: Tuned Random Forest achieved 76.3% accuracy (F1-macro: 0.71). XGBoost achieved 77.3% test accuracy (F1-macro: 0.72). 5-fold cross-validation showed both models at approximately 77.5% accuracy (RF: 0.775 +/- 0.011, XGBoost: 0.775 +/- 0.010). Random Forest was chosen as the final model due to slightly lower variance in cross-validation.')

add_heading('4.5 Final Approach', level=2)
add_para('The final model is a Random Forest classifier with the following key hyperparameters: n_estimators=200, max_depth=20, min_samples_split=2, class_weight="balanced", random_state=42. The model uses the engineered features alongside the original 37 features, totaling 41 input features. The rationale for choosing Random Forest includes its ability to handle non-linear feature interactions, robustness to outliers, built-in feature importance calculation, and strong performance on tabular data with class imbalance when combined with SMOTE.')

add_heading('4.5 Training Procedure', level=2)
add_para('Training Procedure: Data split 80-20 (train-test) with stratify=y to maintain class distribution. Features were standardized implicitly by Random Forest (no scaling needed for tree-based models). Hyperparameters were optimized using GridSearchCV with 5-fold cross-validation and f1_macro scoring on SMOTE-balanced training data. Cross-validation was performed on the full dataset (5 folds) with accuracy scoring.')
add_code('# Key training configuration')
add_code('X_train, X_test, y_train, y_test = train_test_split(')
add_code('    X, y, test_size=0.2, random_state=42, stratify=y)')
add_code('smote = SMOTE(random_state=42)')
add_code('X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)')
add_code('grid_search = GridSearchCV(')
add_code('    RandomForestClassifier(random_state=42, class_weight="balanced"),')
add_code('    param_grid={"n_estimators": [100,200,300],')
add_code('                "max_depth": [None, 10, 20],')
add_code('                "min_samples_split": [2, 5]},')
add_code('    cv=5, scoring="f1_macro", n_jobs=-1)')
add_code('grid_search.fit(X_train_bal, y_train_bal)')

print('Chapter 4 done')
doc.save('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL_Report_Filled.docx')
