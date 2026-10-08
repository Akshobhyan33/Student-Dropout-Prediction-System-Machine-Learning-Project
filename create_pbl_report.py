# Create filled PBL report for Student Dropout Prediction project
from docx import Document
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

doc = Document('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL Template (Machine Learning).docx')

# Remove all placeholder paragraphs and rebuild content
# First, get all paragraphs
paragraphs = doc.paragraphs

# Helper functions
def clear_all_paragraphs(doc):
    """Remove all body element paragraphs"""
    body = doc.element.body
    for p in body.findall(qn('w:p')):
        body.remove(p)

def add_para(doc, text, bold=False, size=11, align=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    run.font.name = 'Times New Roman'
    return p

def add_heading(doc, text, level=1):
    from docx.enum.style import WD_STYLE_TYPE
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14 if level == 1 else (12 if level == 2 else 11))
    run.font.name = 'Times New Roman'
    run.font.color.rgb = RGBColor(0, 0, 0)
    return p

def add_bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Times New Roman'
    return p

# Clear existing content and rebuild
body = doc.element.body
# Remove all paragraphs
for p in list(body.findall(qn('w:p'))):
    body.remove(p)

# ============ TITLE PAGE ============
add_para(doc, '', size=12)
add_para(doc, '', size=12)
add_heading(doc, 'A PROJECT BASED LEARNING (PBL) REPORT', level=1)
add_para(doc, '', size=12)
add_para(doc, 'Student Dropout Prediction Using Machine Learning', bold=True, size=16)
add_para(doc, '', size=12)
add_para(doc, 'Submitted by', bold=True, size=12)
add_para(doc, '[YOUR NAME]', size=12)
add_para(doc, '[PARTNER NAME if any]', size=12)
add_para(doc, '', size=12)
add_para(doc, 'Submitted in partial fulfilment of the requirements', size=11)
add_para(doc, 'for the', size=11)
add_para(doc, 'Project-Based Learning component of Machine Learning', size=11)
add_para(doc, 'BACHELOR OF ENGINEERING', size=11)
add_para(doc, 'in', size=11)
add_para(doc, 'COMPUTER SCIENCE AND ENGINEERING', bold=True, size=11)
add_para(doc, '', size=12)
add_para(doc, 'CHENNAI INSTITUTE OF TECHNOLOGY, CHENNAI', size=11)
add_para(doc, 'Affiliated to Anna University, Chennai', size=11)
add_para(doc, '(Autonomous)', size=11)
add_para(doc, 'OCTOBER 2026', size=11)
add_para(doc, '', size=12)
add_heading(doc, 'Vision of the Institute:', level=2)
add_para(doc, '[To be filled from institute website]')
add_heading(doc, 'Mission of the Institute:', level=2)
add_para(doc, '[To be filled from institute website]')

# ============ DEPARTMENT HEADER ============
add_para(doc, '', size=12)
add_heading(doc, 'DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING', level=1)
add_heading(doc, 'Vision of the Department:', level=2)
add_para(doc, '[To be filled from department website]')
add_heading(doc, 'Mission of the Department:', level=2)
add_para(doc, '[To be filled from department website]')

# ============ BONAFIDE CERTIFICATE ============
add_para(doc, '', size=12)
add_heading(doc, 'BONAFIDE CERTIFICATE', level=1)
add_para(doc, 'This is to certify that the Project-Based Learning report titled "Student Dropout Prediction Using Machine Learning" is a Bonafide record of work carried out by [YOUR NAME, REGISTER NO.] of the Department of Computer Science and Engineering, Chennai Institute of Technology, as part of the continuous, mentor-guided Project-Based Learning (PBL) component of the Machine Learning course during the academic year [2026-2027] under my supervision.')
add_para(doc, 'Submitted for the final review held on [DATE].')
add_para(doc, '', size=12)
add_para(doc, 'Internal Examiner', size=11)
add_para(doc, '', size=20)
add_para(doc, '', size=12)

# ============ DECLARATION ============
add_heading(doc, 'DECLARATION', level=1)
add_para(doc, 'I/We jointly declare that the PBL report on "Student Dropout Prediction Using Machine Learning" is the result of original work done by us and best of our knowledge, similar work has not been submitted to ANNA UNIVERSITY, CHENNAI for the requirement of Degree of BACHELOR OF ENGINEERING. This PBL report is submitted on the partial fulfilment of the requirement of the award of Degree of COMPUTER SCIENCE AND ENGINEERING.')
add_para(doc, '', size=12)
add_para(doc, 'Signature', bold=True, size=11)
add_para(doc, '[YOUR NAME]', size=11)
add_para(doc, '[PARTNER NAME]', size=11)
add_para(doc, 'Place: Chennai', size=11)
add_para(doc, 'Date: [DATE]', size=11)

# ============ ACKNOWLEDGEMENT ============
add_heading(doc, 'ACKNOWLEDGEMENT', level=1)
add_para(doc, 'We wish to express our sincere gratitude to our honorable Chairman SHRI. P. SRIRAM for providing immense facilities at our institution.')
add_para(doc, 'We are very proudly rendering our thanks to our Principal Dr.A.RAMESH M.E, Ph.D., for the facilities and the encouragement given by him to the progress and completion of our project.')
add_para(doc, 'We would like to express special thanks of gratitude to our Dean Dr. V. SRINIVASA RAO, M.E., Ph.D., who has been the key spring of motivation to us throughout the completion of our course and project work.')
add_para(doc, 'We proudly render our immense gratitude to the Head of the Department Dr. S. PAVITHRA M.E, Ph.D., for her effective leadership, encouragement and guidance in the project.')
add_para(doc, 'We would like to extend our thanks to the Project Co-ordinator [MENTOR NAME], Department of Computer Science and Engineering, for their valuable suggestions throughout this project.')
add_para(doc, 'We wish to acknowledge the help received from the class advisors [CLASS ADVISOR NAME] of the Department of Computer Science and Engineering and others for providing valuable suggestions and for the successful completion of the project.')
add_para(doc, '', size=12)
add_para(doc, '[YOUR NAME] ([REG.NO])', size=11)
add_para(doc, '[PARTNER NAME] ([REG.NO])', size=11)

# ============ ABSTRACT ============
add_heading(doc, 'ABSTRACT', level=1)
add_para(doc, 'Student dropout is a critical problem in higher education institutions worldwide. This project addresses the problem of predicting student dropout using machine learning techniques applied to the publicly available dataset "Predict Students\' Dropout and Academic Success" from the UCI Machine Learning Repository. The dataset contains academic, demographic, and financial information of 4,424 students across 37 features. We implemented a complete machine learning pipeline including data preprocessing, feature engineering, and model training using multiple algorithms. Baseline Logistic Regression achieved 72.8% accuracy, while Random Forest achieved 75.6%. After addressing class imbalance using SMOTE and hyperparameter tuning with GridSearchCV, the final Random Forest model (max_depth=20, n_estimators=200) achieved 77% test accuracy and 77.5% cross-validation accuracy with a standard deviation of only 0.011. The system is deployed as a web application using Streamlit, allowing users to input student details and receive real-time dropout risk predictions with confidence scores. A batch prediction script and a college-format CSV mapper were also developed for practical deployment scenarios.', bold=False)
add_para(doc, 'Keywords: [Machine Learning, Student Dropout Prediction, Random Forest, SMOTE, Streamlit, Feature Engineering, Imbalanced Classification]')

# ============ TABLE OF CONTENTS ============
add_heading(doc, 'TABLE OF CONTENTS', level=1)
add_para(doc, '')
add_para(doc, '1. INTRODUCTION .................................................... Page X')
add_para(doc, '2. CONCEPT EXPLORATION .................................... Page X')
add_para(doc, '3. PROJECT PLANNING AND TEAM ORGANISATION ........... Page X')
add_para(doc, '4. ITERATIVE DESIGN AND DEVELOPMENT .................. Page X')
add_para(doc, '5. IMPLEMENTATION ......................................... Page X')
add_para(doc, '6. RESULTS AND DISCUSSION ............................ Page X')
add_para(doc, '7. TEAM REFLECTION AND LEARNING OUTCOMES ............. Page X')
add_para(doc, '8. CONCLUSION AND FUTURE SCOPE ....................... Page X')
add_para(doc, 'REFERENCES .................................................. Page X')
add_para(doc, 'APPENDIX .................................................... Page X')

# ============ LIST OF FIGURES ============
add_heading(doc, 'LIST OF FIGURES', level=1)
add_para(doc, 'Figure 4.1  System architecture diagram ................ Page X')
add_para(doc, 'Figure 4.2  Feature importance bar chart ............... Page X')
add_para(doc, 'Figure 6.1  Random Forest confusion matrix ............. Page X')
add_para(doc, 'Figure 6.2  Iteration comparison accuracy plot ........ Page X')

# ============ LIST OF TABLES ============
add_heading(doc, 'LIST OF TABLES', level=1)
add_para(doc, 'Table 3.1 Weekly PBL progress log .................... Page X')
add_para(doc, 'Table 3.2 Hardware and software requirements ......... Page X')
add_para(doc, 'Table 6.1 Model evaluation results ................. Page X')
add_para(doc, 'Table 6.2 Feature importance rankings .............. Page X')
add_para(doc, 'Table 6.3 Confusion matrix for final model ........... Page X')

# ============ LIST OF ABBREVIATIONS ============
add_heading(doc, 'LIST OF ABBREVIATIONS', level=1)
add_para(doc, 'ML — Machine Learning')
add_para(doc, 'RF — Random Forest')
add_para(doc, 'XGB — XGBoost')
add_para(doc, 'PBL — Project-Based Learning')
add_para(doc, 'SMOTE — Synthetic Minority Over-sampling Technique')
add_para(doc, 'GCV — Grid Cross Validation')
add_para(doc, 'CV — Cross Validation')
add_para(doc, 'F1 — F1-Score (harmonic mean of precision and recall)')
add_para(doc, 'UCI — University of California, Irvine (ML Repository)')

print("Part 1 of PBL document created. Continuing...")
doc.save('C:/My Code/COLLEGE/ML PROJECT/documentation/PBL_Report_Filled.docx')
