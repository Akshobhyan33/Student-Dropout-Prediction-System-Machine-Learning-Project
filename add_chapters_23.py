# Adds all remaining chapters to the PBL report
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
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return p

# ============ CHAPTER 2: CONCEPT EXPLORATION ============
add_heading('CHAPTER 2', level=1)
add_heading('CONCEPT EXPLORATION', level=1)

add_heading('2.1 Related Approaches', level=2)

add_para('2.1.1 Classical ML Approaches', bold=True, size=11)
add_para('Logistic Regression is one of the simplest and most widely used classification algorithms. It models the probability of a categorical outcome using a logistic function. In student dropout prediction, logistic regression serves as a strong baseline because it is interpretable, fast to train, and performs well on tabular data with mixed numerical and categorical features. Studies using the same UCI dataset have reported baseline logistic regression accuracy in the range of 70-75%.')
add_para('Decision Trees partition the feature space into regions based on feature thresholds. They are easy to interpret but prone to overfitting. Random Forest addresses this by building an ensemble of decision trees and averaging their predictions, reducing variance and improving generalization.')

add_para('2.1.2 Ensemble and Boosting Methods', bold=True, size=11)
add_para('Random Forest is an ensemble learning method that constructs multiple decision trees during training and outputs the mode of the classes (classification). It uses bagging (bootstrap aggregating) and random feature selection to reduce correlation between trees. It performs well on imbalanced datasets when class_weight="balanced" is used.')
add_para('XGBoost (Extreme Gradient Boosting) builds trees sequentially, where each new tree corrects errors made by the previous one. It uses gradient descent optimization and regularization to prevent overfitting. XGBoost has become a dominant algorithm in structured/tabular data competitions due to its high predictive accuracy and built-in handling of missing values.')

add_para('2.1.3 Handling Class Imbalance', bold=True, size=11)
add_para('In the UCI dataset, the number of students in each class is imbalanced: Graduate (2209), Dropout (1421), and Enrolled (794). This imbalance can bias models toward predicting the majority class. SMOTE (Synthetic Minority Over-sampling Technique) generates synthetic samples for minority classes by interpolating between existing data points, balancing the class distribution without simply duplicating data. This approach has been widely adopted in educational data mining for dropout prediction tasks.')

add_para('2.1.4 Deep Learning and Neural Network Approaches', bold=True, size=11)
add_para('Neural networks and deep learning models have been applied to student performance prediction with promising results. However, for tabular data with moderate size (thousands of samples), classical ML methods like Random Forest and XGBoost often outperform deep learning due to their ability to capture non-linear relationships with fewer parameters and less risk of overfitting. Given the project scope and available computational resources, classical ensemble methods were chosen over deep learning.')

add_heading('2.2 Summary Table', level=2)
add_para('The following table summarizes the approaches explored:', bold=True, size=11)
add_para('Algorithm | Pros | Cons | Suitability for this task', bold=True, size=10)
add_para('Logistic Regression | Interpretable, fast baseline | Limited non-linear modeling | Baseline (73% accuracy)')
add_para('Random Forest | Handles non-linearity, robust to outliers | Less interpretable than LR | Primary candidate (76% accuracy)')
add_para('XGBoost | Highest accuracy, handles missing data | More hyperparameters, slower training | Secondary candidate (77% accuracy)')
add_para('SMOTE | Balances imbalanced classes | May introduce noise | Used for data preprocessing')
add_para('GridSearchCV | Systematic hyperparameter tuning | Computationally expensive | Used for model optimization')

add_heading('2.3 What This Told Us', level=2)
add_para('Based on this exploration, the team decided to start with Logistic Regression as the baseline (Iteration 1) to establish a reference point, then move to Random Forest (Iteration 2) for improved performance through non-linear modeling and ensemble averaging. Finally, after mentor feedback on class imbalance, the team implemented SMOTE and hyperparameter tuning with XGBoost as a comparison (Iteration 3). The decision was driven by the tabular nature of the data, moderate dataset size, and the need for interpretable results that could be explained during the project viva.')

# ============ CHAPTER 3: PROJECT PLANNING ============
add_heading('CHAPTER 3', level=1)
add_heading('PROJECT PLANNING AND TEAM ORGANISATION', level=1)

add_heading('3.1 Weekly PBL Progress Log', level=2)
add_para('The following table shows the week-by-week progress through the PBL cycle.', bold=True, size=11)
add_para('Week 1: Explored the dataset, understood features, set up Python environment with required libraries (pandas, scikit-learn, matplotlib).', size=11)
add_para('Week 2: Implemented data preprocessing and feature engineering. Created total_units_approved, approval rates, grade drop, and financial risk flag. Encoded categorical labels.', size=11)
add_para('Week 3: Built baseline model (Logistic Regression). Achieved 72.8% accuracy. Identified class imbalance as a key issue.', size=11)
add_para('Week 4: Implemented Random Forest model. Achieved 75.6% accuracy. Generated confusion matrix and feature importance charts.', size=11)
add_para('Week 5: Added SMOTE for class balancing, implemented GridSearchCV for hyperparameter tuning, compared XGBoost. Final model: Random Forest with 77% accuracy.', size=11)
add_para('Week 6: Built web application using Streamlit (Single Student + Batch Upload tabs). Added college-format CSV mapper.', size=11)
add_para('Week 7: Created batch prediction script, tested with 20 student samples, documented the project (this PBL report).', size=11)

add_heading('3.2 Requirements', level=2)
add_para('Dataset: UCI Machine Learning Repository — "Predict Students\' Dropout and Academic Success" (https://archive.ics.uci.edu/dataset/697/), containing 4,424 students with 37 features and 3 target classes.', size=11)
add_para('Features: 37 input features spanning demographics (marital status, gender, age), academic records (credits, grades, enrollments per semester), financial information (tuition fees status), and macroeconomic indicators (unemployment rate, inflation rate, GDP).', size=11)
add_para('Classes: Dropout (1421), Enrolled (794), Graduate (2209). Class ratio approximately 32:18:50.', size=11)
add_para('Tools: Python 3.14, pandas, scikit-learn, imbalanced-learn, XGBoost, matplotlib, joblib, Streamlit.', size=11)
add_para('Hardware: Standard laptop with sufficient RAM for training ensemble models on ~4000 samples.', size=11)

add_heading('3.3 Feasibility', level=2)
add_para('This project was achievable within the PBL timeframe given the availability of a well-documented public dataset, mature Python libraries for machine learning, and a clear problem definition. The dataset required no data collection phase, allowing immediate focus on preprocessing and modeling. The iterative build-test-learn cycle was feasible because each iteration produced measurable improvements in accuracy. The web deployment using Streamlit required minimal infrastructure as it runs as a local server. The project scope was kept focused on classical ML methods to ensure completion within the academic semester timeline.')

print('Chapters 2 and 3 done')
doc.save('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL_Report_Filled.docx')
