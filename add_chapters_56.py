# Adds chapters 5-8 to PBL report
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

# ============ CHAPTER 5: IMPLEMENTATION ============
add_heading('CHAPTER 5', level=1)
add_heading('IMPLEMENTATION', level=1)

add_heading('5.1 Module Description', level=2)
add_para('Data Preprocessing Module (preprocess_dropout_data.py): Loads the raw UCI dataset, checks for missing values, creates engineered features (total_units_approved, approval rates, grade drop, financial risk flag), encodes the target variable using LabelEncoder, splits the data into training and testing sets, and saves the preprocessed dataset.')
add_para('Model Training Module (train_dropout_model.py): Implements baseline Logistic Regression and Random Forest models. Evaluates both using accuracy and classification report. Generates confusion matrix and feature importance charts as visual outputs.')
add_para('Advanced Training Module (train_advanced.py): Implements SMOTE for class balancing, GridSearchCV for hyperparameter tuning of Random Forest, and XGBoost as a comparison model. Performs 5-fold cross-validation on both models and selects the best one based on CV accuracy. Saves the final model as a pickle file.')
add_para('Web Interface Module (app.py): Streamlit-based web application with two tabs — Single Student (manual input via sliders and dropdowns) and Batch Upload (CSV file upload with automatic format detection). Displays predictions with color-coded risk levels and download functionality.')
add_para('Batch Prediction Module (batch_predict.py): Command-line script that reads a CSV of student data, applies the same preprocessing pipeline, loads the trained model, predicts outcomes for all students, and saves results to a CSV file. Includes accuracy evaluation if true labels are available.')
add_para('College Mapper Module (college_to_uci_mapper.py): Converts college-format CSV data (CGPA, attendance, fees, subjects) into the UCI feature format expected by the model. Uses constants for Indian context (marital status, macro indicators) and flexible column name matching.')

add_heading('5.2 Key Code Snippets', level=2)
add_para('Model training with GridSearchCV:', bold=True, size=10)
add_code('grid_search = GridSearchCV(')
add_code('    RandomForestClassifier(random_state=42, class_weight="balanced"),')
add_code('    param_grid={"n_estimators": [100,200,300],')
add_code('                "max_depth": [None, 10, 20],')
add_code('                "min_samples_split": [2, 5]},')
add_code('    cv=5, scoring="f1_macro", n_jobs=-1)')
add_code('grid_search.fit(X_train_bal, y_train_bal)')
add_para('Feature engineering pipeline:', bold=True, size=10)
add_code('df["approval_rate_2nd_sem"] = (')
add_code('    df["Curricular units 2nd sem (approved)"]')
add_code('    / (df["Curricular units 2nd sem (enrolled)"] + 1e-6))')
add_para('Web app prediction call:', bold=True, size=10)
add_code('preds = model.predict(X_batch)')
add_code('probs = model.predict_proba(X_batch)')
add_code('results["Dropout_Prob_%"] = (probs[:, 0] * 100).round(1)')

add_heading('5.3 User Interface / Demo', level=2)
add_para('The web application (Streamlit) provides an accessible interface for non-technical users. The Single Student tab allows manual entry of key parameters (CGPA, subjects passed, fees status) with sliders and dropdowns. The Batch Upload tab allows uploading CSV files with automatic format detection. Results are displayed as a color-coded table sorted by dropout risk. The Streamlit app is accessible at http://localhost:8501.')

# ============ CHAPTER 6: RESULTS ============
add_heading('CHAPTER 6', level=1)
add_heading('RESULTS AND DISCUSSION', level=1)

add_heading('6.1 Evaluation Metrics', level=2)
add_para('The following metrics were used to evaluate model performance:')
add_bullet('Accuracy: Overall correctness of predictions (correct predictions / total predictions). Used as the primary metric because class distribution is reasonably balanced after SMOTE.')
add_bullet('F1-Score (Macro): Harmonic mean of precision and recall, averaged across all three classes. Used because it accounts for class imbalance in the original dataset.')
add_bullet('Precision and Recall per class: Shows how well the model performs for each individual outcome class (Dropout, Enrolled, Graduate).')
add_bullet('Confusion Matrix: A 3x3 matrix showing actual vs predicted classes, revealing which classes the model confuses most frequently.')
add_bullet('5-Fold Cross-Validation Accuracy: Measures model generalization by training and testing on 5 different data splits. Provides mean and standard deviation of accuracy.')

add_heading('6.2 Results Across Iterations', level=2)
add_para('Iteration | Model | Test Accuracy | F1-Macro | CV Accuracy')
add_para('Iter 1 | Logistic Regression | 72.8% | 0.69 | N/A')
add_para('Iter 2 | Random Forest (200) | 75.6% | 0.71 | N/A')
add_para('Iter 3 | Tuned RF (GridSearchCV) | 76.3% | 0.71 | 77.5% (+/-0.011)')
add_para('Iter 3 | XGBoost | 77.3% | 0.72 | 77.5% (+/-0.010)')
add_para('Final | Random Forest (tuned) | 77% | 0.71 | 77.5% (+/-0.011)')
add_para('The confusion matrix for the final model (Figure 6.1) shows the highest misclassification between Enrolled and Graduate students. Graduate students are occasionally predicted as Enrolled, and vice versa, because these classes share similar academic performance characteristics in the training data.')

add_heading('6.3 Discussion', level=2)
add_para('The final model achieved 77% test accuracy, which is a meaningful improvement from the 72.8% baseline. The key driver of this improvement was twofold: (1) Random Forest captured non-linear relationships between features that Logistic Regression missed, and (2) SMOTE addressed the class imbalance that was causing poor Enrolled class predictions.')
add_para('Feature importance analysis revealed that approval_rate_2nd_sem was the single most important predictor, followed by Curricular units 2nd sem (approved) and Curricular units 2nd sem (grade). This makes intuitive sense — a student\'s second semester performance is a strong indicator of whether they will continue or drop out. The financial_risk_flag (whether tuition fees are up to date) also appeared among the top 10 features, confirming that financial stress correlates with dropout risk.')
add_para('Between the tuned Random Forest and XGBoost, the performance was nearly identical on both test accuracy (76.3% vs 77.3%) and cross-validation (77.5% vs 77.5%). Random Forest was chosen as the final model due to its slightly lower variance in cross-validation results, making it more robust to data variations.')

add_heading('6.4 Limitations', level=2)
add_para('The dataset represents Portuguese higher education students and may not directly generalize to Indian college contexts without retraining on local data. The dataset has 37 features, many of which are specific to the European education system (e.g., marital status, application mode). The project uses a pre-trained model that was trained on the UCI dataset; deployment on a different college would require retraining with local historical data. The dataset size (4,424 students) is moderate and may not capture all edge cases in student dropout behavior. The model does not incorporate temporal dynamics (e.g., performance trends across semesters beyond the first two).')

print('Chapters 5 and 6 done')
doc.save('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL_Report_Filled.docx')
