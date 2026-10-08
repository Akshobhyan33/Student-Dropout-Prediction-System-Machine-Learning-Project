# A3 Landscape PBL Poster - PIL-based for proper text sizing
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 4961, 3508
img = Image.new('RGB', (W, H), '#F0F4F8')
draw = ImageDraw.Draw(img)

# Try to load fonts
def get_font(size, bold=False):
    font_paths = [
        'C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/segoeui.ttf',
        'C:/Windows/Fonts/calibrib.ttf' if bold else 'C:/Windows/Fonts/calibri.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

# Colors
NAVY = '#1B2A4A'
DARK_BLUE = '#1E3A5F'
CYAN = '#06B6D4'
MED_BLUE = '#2563EB'
WHITE = '#FFFFFF'
LIGHT_BG = '#EFF6FF'
DARK_TEXT = '#1E293B'
GRAY = '#475569'
GREEN = '#10B981'

def rounded_rect(draw, xy, fill, outline=None, radius=15, width=2):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def section_header(x, y, w, h, text):
    rounded_rect(draw, (x, y, x+w, y+h), fill=NAVY, radius=10)
    font = get_font(28, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w-tw)//2, y + (h-28)//2), text, fill=WHITE, font=font)

def draw_bullet(x, y, text, fs=20):
    font = get_font(fs)
    draw.ellipse((x, y+6, x+12, y+18), fill=CYAN)
    draw.text((x+20, y), text, fill=DARK_TEXT, font=font)

def draw_text(x, y, text, fs=20, color=DARK_TEXT, bold=False):
    font = get_font(fs, bold)
    draw.text((x, y), text, fill=color, font=font)

# ============ HEADER ============
draw.rectangle((0, 0, W, 320), fill=NAVY)
draw.rectangle((0, 320, W, 330), fill=CYAN)

font_inst = get_font(32, bold=True)
draw.text((W//2 - 350, 30), 'CHENNAI INSTITUTE OF TECHNOLOGY, CHENNAI', fill=WHITE, font=font_inst)
font_sub = get_font(20)
draw.text((W//2 - 300, 75), 'Department of Computer Science and Engineering  |  Affiliated to Anna University', fill='#93C5FD', font=font_sub)
draw.text((W//2 - 250, 105), 'Project-Based Learning (PBL) — Machine Learning  |  Academic Year 2026-2027', fill='#93C5FD', font=font_sub)

font_title = get_font(48, bold=True)
draw.text((W//2 - 500, 150), 'STUDENT DROPOUT PREDICTION USING MACHINE LEARNING', fill=WHITE, font=font_title)
font_sub2 = get_font(18)
draw.text((W//2 - 350, 220), 'Predicting Dropout, Enrolled, and Graduate outcomes using Random Forest, XGBoost, and SMOTE', fill='#BFDBFE', font=font_sub2)

# Team
font_team = get_font(18, bold=True)
font_member = get_font(17)
draw.text((W-350, 30), 'PROJECT TEAM', fill='#93C5FD', font=font_team)
draw.text((W-350, 60), '[Your Name]', fill=WHITE, font=font_member)
draw.text((W-350, 85), '[Partner Name]', fill=WHITE, font=font_member)
draw.text((W-350, 120), 'FACULTY GUIDE:', fill='#93C5FD', font=font_team)
draw.text((W-350, 145), '[Mentor Name]', fill=WHITE, font=font_member)

print("Header done")

# ============ COLUMNS ============
COL1_X, COL1_W = 40, 1560
COL2_X, COL2_W = 1630, 1700
COL3_X, COL3_W = 3360, 1560
TOP = 360
BOT = 40
COL_H = H - TOP - BOT

for cx, cw in [(COL1_X, COL1_W), (COL2_X, COL2_W), (COL3_X, COL3_W)]:
    rounded_rect(draw, (cx, BOT, cx+cw, H-TOP), fill=WHITE, outline='#CBD5E1', radius=12)

# ==================== LEFT COLUMN ====================
y = TOP + 20

# ABSTRACT
section_header(COL1_X+10, y, COL1_W-20, 40, 'ABSTRACT')
y += 55
abstract = [
    'Student dropout is a critical problem in higher education',
    'institutions worldwide. This project builds a machine learning',
    'pipeline to predict whether a student will Dropout, Stay',
    'Enrolled, or Graduate using the UCI dataset (4,424 students,',
    '37 features). We applied feature engineering, SMOTE for class',
    'balancing, and trained Logistic Regression (72.8%), Random',
    'Forest (75.6%), and tuned Random Forest with SMOTE (77%).',
    'The system is deployed as a Streamlit web app and CLI tool.',
]
for line in abstract:
    draw_text(COL1_X+25, y, line, fs=19)
    y += 28
y += 20

# INTRODUCTION
section_header(COL1_X+10, y, COL1_W-20, 40, 'INTRODUCTION / PROBLEM STATEMENT')
y += 55
intro = [
    'Higher education institutions lose significant resources when',
    'students leave without completing their degrees.',
    'Early identification of at-risk students enables timely',
    'intervention through academic counseling and financial aid.',
    'Existing ML approaches often ignore class imbalance and',
    'feature engineering critical for accurate prediction.',
    'This project addresses these gaps with an end-to-end pipeline.',
]
for b in intro:
    draw_bullet(COL1_X+25, y, b, fs=19)
    y += 28
y += 20

# OBJECTIVES
section_header(COL1_X+10, y, COL1_W-20, 40, 'OBJECTIVES')
y += 55
objs = [
    ('01', 'Preprocess and engineer features from the UCI dataset'),
    ('02', 'Build baseline models (Logistic Regression, Random Forest)'),
    ('03', 'Apply SMOTE to address class imbalance in training data'),
    ('04', 'Tune hyperparameters using GridSearchCV with 5-fold CV'),
    ('05', 'Compare Random Forest vs XGBoost and select best model'),
    ('06', 'Deploy via Streamlit web app and batch prediction CLI'),
]
for num, obj in objs:
    draw_text(COL1_X+25, y, num, fs=22, color=CYAN, bold=True)
    draw_text(COL1_X+70, y, obj, fs=19)
    y += 32
y += 20

# METHODOLOGY
section_header(COL1_X+10, y, COL1_W-20, 40, 'METHODOLOGY')
y += 55
steps = [
    ('UCI\nDataset', NAVY),
    ('Preprocess\n& Feature Eng.', DARK_BLUE),
    ('SMOTE\nBalancing', MED_BLUE),
    ('Model\nTraining', CYAN),
    ('GridSearchCV\nTuning', MED_BLUE),
    ('Deploy\n(Streamlit)', GREEN),
]
bw = (COL1_W - 50) // len(steps)
for i, (label, color) in enumerate(steps):
    bx = COL1_X + 20 + i * bw
    rounded_rect(draw, (bx, y, bx+bw-10, y+80), fill=color, radius=8)
    lines = label.split('\n')
    font_s = get_font(15, bold=True)
    for j, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_s)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (bw-10-tw)//2, y + 15 + j*22), line, fill=WHITE, font=font_s)
    if i < len(steps) - 1:
        draw.text((bx+bw-8, y+30), '→', fill=NAVY, font=get_font(28, bold=True))

y += 100
method_pts = [
    '80-20 train-test split with stratification',
    '5 engineered features: approval rates, grade drop, financial risk',
    'SMOTE balanced classes to 1767 each from imbalanced originals',
    'GridSearchCV: n_estimators [100,200,300], max_depth [None,10,20]',
    '5-fold cross-validation for final model selection',
]
for mp in method_pts:
    draw_bullet(COL1_X+25, y, mp, fs=18)
    y += 26

print("Left column done")

# ==================== CENTER COLUMN ====================
y = TOP + 20

# SYSTEM ARCHITECTURE
section_header(COL2_X+10, y, COL2_W-20, 40, 'SYSTEM ARCHITECTURE')
y += 55

arch = [
    ('DATA INPUT', ['CSV Upload', 'UCI/College Format', 'Auto Detection'], NAVY),
    ('PREPROCESSING', ['Missing Values', 'Label Encoding', 'Train/Test Split'], DARK_BLUE),
    ('FEATURE ENG.', ['Approval Rates', 'Grade Drop', 'Financial Risk'], MED_BLUE),
    ('MODEL', ['Random Forest', 'XGBoost', 'SMOTE Balancing'], CYAN),
    ('OUTPUT', ['Predictions CSV', 'Web App UI', 'Risk Scores'], GREEN),
]
abw = (COL2_W - 60) // len(arch)
for i, (title, items, color) in enumerate(arch):
    bx = COL2_X + 20 + i * abw
    rounded_rect(draw, (bx, y, bx+abw-12, y+130), fill=color, radius=10)
    font_t = get_font(18, bold=True)
    bbox = draw.textbbox((0, 0), title, font=font_t)
    tw = bbox[2] - bbox[0]
    draw.text((bx + (abw-12-tw)//2, y+10), title, fill=WHITE, font=font_t)
    font_i = get_font(14)
    for j, item in enumerate(items):
        bbox = draw.textbbox((0, 0), item, font=font_i)
        tw = bbox[2] - bbox[0]
        draw.text((bx + (abw-12-tw)//2, y+45 + j*26), item, fill='#E0F2FE', font=font_i)
    if i < len(arch) - 1:
        draw.text((bx+abw-10, y+50), '→', fill=NAVY, font=get_font(24, bold=True))

y += 155

# TECHNOLOGIES
section_header(COL2_X+10, y, COL2_W-20, 40, 'TECHNOLOGIES / TOOLS')
y += 55
techs = [
    ('Python 3.14', 'Language'), ('scikit-learn', 'ML Framework'),
    ('pandas', 'Data Processing'), ('XGBoost', 'Gradient Boosting'),
    ('imblearn (SMOTE)', 'Class Balancing'), ('Streamlit', 'Web Application'),
    ('matplotlib', 'Visualization'), ('joblib', 'Model Persistence'),
]
tw = (COL2_W - 50) // 4
for i, (name, cat) in enumerate(techs):
    tx = COL2_X + 20 + (i % 4) * tw
    ty = y + (i // 4) * 55
    rounded_rect(draw, (tx, ty, tx+tw-10, ty+50), fill=LIGHT_BG, outline=MED_BLUE, radius=8)
    font_n = get_font(17, bold=True)
    font_c = get_font(13)
    bbox = draw.textbbox((0, 0), name, font=font_n)
    ntw = bbox[2] - bbox[0]
    draw.text((tx + (tw-10-ntw)//2, ty+8), name, fill=NAVY, font=font_n)
    bbox = draw.textbbox((0, 0), cat, font=font_c)
    ctw = bbox[2] - bbox[0]
    draw.text((tx + (tw-10-ctw)//2, ty+30), cat, fill=GRAY, font=font_c)

y += 130

# DATASET
section_header(COL2_X+10, y, COL2_W-20, 40, 'DATASET')
y += 55
ds = [
    ('Source:', 'UCI ML Repository — Predict Students\' Dropout and Academic Success'),
    ('Samples:', '4,424 students'),
    ('Features:', '37 original + 5 engineered = 41 total features'),
    ('Classes:', 'Dropout (1,421)  |  Enrolled (794)  |  Graduate (2,209)'),
    ('Split:', '80% Training (3,539)  |  20% Testing (885)'),
    ('Key Features:', 'approval_rate, total_units_approved, grade_drop, financial_risk_flag'),
]
for label, val in ds:
    draw_text(COL2_X+25, y, label, fs=19, color=NAVY, bold=True)
    draw_text(COL2_X+165, y, val, fs=19)
    y += 30
y += 20

# IMPLEMENTATION
section_header(COL2_X+10, y, COL2_W-20, 40, 'IMPLEMENTATION')
y += 55
impl = [
    'preprocess_dropout_data.py — Data cleaning, feature engineering, encoding',
    'train_dropout_model.py — Baseline models: Logistic Regression + Random Forest',
    'train_advanced.py — SMOTE + GridSearchCV + XGBoost + cross-validation',
    'batch_predict.py — Command-line batch prediction with risk scoring',
    'app.py — Streamlit web UI with Single Student and Batch Upload tabs',
    'college_to_uci_mapper.py — Maps college CSV format to UCI features',
]
for s in impl:
    draw_bullet(COL2_X+25, y, s, fs=18)
    y += 26

print("Center column done")

# ==================== RIGHT COLUMN ====================
y = TOP + 20

# RESULTS
section_header(COL3_X+10, y, COL3_W-20, 40, 'RESULTS & PERFORMANCE')
y += 55

# Bar chart
chart_x, chart_y = COL3_X+25, y
chart_w, chart_h = COL3_W-60, 300
rounded_rect(draw, (chart_x, chart_y, chart_x+chart_w, chart_y+chart_h), fill=LIGHT_BG, outline=MED_BLUE, radius=10)

# Draw bar chart manually
models = ['Logistic\nRegression', 'Random\nForest', 'Tuned RF\n+SMOTE', 'XGBoost']
accs = [72.8, 75.6, 76.3, 77.3]
colors_b = ['#6B7280', MED_BLUE, CYAN, GREEN]
bar_area_x = chart_x + 80
bar_area_y = chart_y + 40
bar_area_w = chart_w - 160
bar_area_h = chart_h - 80

# Title
font_chart = get_font(20, bold=True)
bbox = draw.textbbox((0, 0), 'Model Accuracy Comparison', font=font_chart)
tw = bbox[2] - bbox[0]
draw.text((chart_x + (chart_w-tw)//2, chart_y + 10), 'Model Accuracy Comparison', fill=NAVY, font=font_chart)

# Y axis labels
for pct in [68, 70, 72, 74, 76, 78, 80]:
    py = bar_area_y + bar_area_h - (pct - 68) / 12 * bar_area_h
    draw.text((chart_x + 10, py - 8), f'{pct}%', fill=GRAY, font=get_font(12))
    draw.line((bar_area_x, py, chart_x + chart_w - 40, py), fill='#E5E7EB', width=1)

# Bars
bar_w = bar_area_w // 5
for i, (model, acc, color) in enumerate(zip(models, accs, colors_b)):
    bx = bar_area_x + i * (bar_w + 20)
    bh = (acc - 68) / 12 * bar_area_h
    by = bar_area_y + bar_area_h - bh
    draw.rounded_rectangle((bx, by, bx+bar_w, bar_area_y+bar_area_h), radius=6, fill=color)
    # Value on top
    font_v = get_font(16, bold=True)
    draw.text((bx + bar_w//2 - 15, by - 22), f'{acc}%', fill=DARK_TEXT, font=font_v)
    # Model name below
    lines = model.split('\n')
    font_m = get_font(13)
    for j, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_m)
        mtw = bbox[2] - bbox[0]
        draw.text((bx + (bar_w-mtw)//2, bar_area_y + bar_area_h + 8 + j*16), line, fill=DARK_TEXT, font=font_m)

y += chart_h + 15

# Key Metrics
rounded_rect(draw, (COL3_X+25, y, COL3_X+COL3_W-35, y+90), fill=NAVY, radius=10)
metrics = [('77.5%', 'CV Accuracy'), ('0.71', 'F1-Macro'), ('0.011', 'CV Std Dev'), ('77.3%', 'Best Test')]
mw = (COL3_W-60) // 4
for i, (val, label) in enumerate(metrics):
    mx = COL3_X + 25 + i * mw + mw//2
    font_v = get_font(30, bold=True)
    font_l = get_font(16)
    bbox = draw.textbbox((0, 0), val, font=font_v)
    vtw = bbox[2] - bbox[0]
    draw.text((mx - vtw//2, y+10), val, fill=WHITE, font=font_v)
    bbox = draw.textbbox((0, 0), label, font=font_l)
    ltw = bbox[2] - bbox[0]
    draw.text((mx - ltw//2, y+50), label, fill='#93C5FD', font=font_l)

y += 110

# Confusion Matrix + Feature Importance side by side
half_w = (COL3_W - 70) // 2

# Confusion Matrix
rounded_rect(draw, (COL3_X+25, y, COL3_X+25+half_w, y+220), fill=LIGHT_BG, outline=MED_BLUE, radius=10)
font_cm = get_font(18, bold=True)
bbox = draw.textbbox((0, 0), 'Confusion Matrix', font=font_cm)
tw = bbox[2] - bbox[0]
draw.text((COL3_X+25+(half_w-tw)//2, y+8), 'Confusion Matrix', fill=NAVY, font=font_cm)

cm_data = [[208, 23, 53], [27, 84, 48], [14, 27, 401]]
cm_labels = ['Drop', 'Enr', 'Grad']
cm_x, cm_y = COL3_X+50, y+45
cell = 55

# Color maps
def cm_color(val, is_diag):
    if is_diag:
        intensity = val / 401
        r = int(30 + 50 * (1-intensity))
        g = int(100 + 155 * intensity)
        b = int(200 + 55 * intensity)
    else:
        intensity = val / 53
        r = int(200 + 55 * intensity)
        g = int(80 + 50 * (1-intensity))
        b = int(80 + 50 * (1-intensity))
    return (min(r,255), min(g,255), min(b,255))

for i in range(3):
    for j in range(3):
        val = cm_data[i][j]
        is_diag = (i == j)
        color = cm_color(val, is_diag)
        draw.rounded_rectangle((cm_x+j*cell, cm_y+i*cell, cm_x+(j+1)*cell-4, cm_y+(i+1)*cell-4),
                                radius=6, fill=color)
        font_cv = get_font(20, bold=True)
        text_color = WHITE if val > 100 else DARK_TEXT
        draw.text((cm_x+j*cell+15, cm_y+i*cell+15), str(val), fill=text_color, font=font_cv)

for i, label in enumerate(cm_labels):
    draw.text((cm_x-5, cm_y+i*cell+18), label, fill=DARK_TEXT, font=get_font(14))
    draw.text((cm_x+i*cell+15, cm_y-18), label, fill=DARK_TEXT, font=get_font(14))

# Feature Importance
fi_x = COL3_X + 25 + half_w + 20
rounded_rect(draw, (fi_x, y, fi_x+half_w, y+220), fill=LIGHT_BG, outline=MED_BLUE, radius=10)
font_fi = get_font(18, bold=True)
bbox = draw.textbbox((0, 0), 'Top 5 Features', font=font_fi)
tw = bbox[2] - bbox[0]
draw.text((fi_x+(half_w-tw)//2, y+8), 'Top 5 Features', fill=NAVY, font=font_fi)

features = ['2nd Sem Pass Rate', '2nd Sem Approved', '2nd Sem Grade',
            'Total Units Passed', '1st Sem Pass Rate']
importances = [9.96, 6.39, 5.76, 5.42, 4.92]
fiy = y + 45
max_bar = half_w - 120
for i, (feat, imp) in enumerate(zip(features, importances)):
    fy = fiy + i * 34
    bar_w = int(imp / 10.5 * max_bar)
    draw.text((fi_x+5, fy+2), feat, fill=DARK_TEXT, font=get_font(13))
    draw.rounded_rectangle((fi_x+100, fy, fi_x+100+bar_w, fy+22), radius=4, fill=CYAN)
    draw.text((fi_x+105+bar_w, fy+2), f'{imp}%', fill=NAVY, font=get_font(13, bold=True))

y += 240

# KEY FINDINGS
section_header(COL3_X+10, y, COL3_W-20, 40, 'KEY FINDINGS')
y += 55
findings = [
    '2nd semester approval rate is the single strongest predictor (9.96%)',
    'SMOTE improved Enrolled F1 from 0.50 to 0.71 — class balancing is critical',
    'Financial risk flag (unpaid fees) ranks among top 10 features',
    'Random Forest preferred over XGBoost due to lower CV variance',
    'Feature engineering contributed ~2% accuracy gain over raw features',
]
for f in findings:
    draw_bullet(COL3_X+25, y, f, fs=18)
    y += 26
y += 15

# CONCLUSION
section_header(COL3_X+10, y, COL3_W-20, 40, 'CONCLUSION')
y += 55
conclusion = (
    'Built an end-to-end ML pipeline predicting student outcomes with 77% accuracy '
    'using tuned Random Forest on the UCI dataset (4,424 students). Feature '
    'engineering and SMOTE for class imbalance were key to performance. Deployed '
    'as a Streamlit web application with batch prediction and college-format CSV '
    'mapper for Indian institutions.'
)
# Wrap conclusion text
words = conclusion.split()
lines = []
line = ''
for word in words:
    test = line + ' ' + word if line else word
    bbox = draw.textbbox((0, 0), test, font=get_font(18))
    if bbox[2] - bbox[0] < COL3_W - 60:
        line = test
    else:
        lines.append(line)
        line = word
if line:
    lines.append(line)
for l in lines:
    draw_text(COL3_X+25, y, l, fs=18)
    y += 26

y += 15

# FUTURE SCOPE
section_header(COL3_X+10, y, COL3_W-20, 40, 'FUTURE ENHANCEMENTS')
y += 55
future = [
    'Retrain on college-specific historical data for local deployment',
    'Deploy to cloud platform (Streamlit Cloud / Heroku) for wider access',
    'Add deep learning models for larger datasets and complex patterns',
    'Build admin dashboard showing at-risk students with intervention plans',
    'Incorporate LMS logs, library usage, and attendance records',
]
for f in future:
    draw_bullet(COL3_X+25, y, f, fs=18)
    y += 26
y += 15

# REFERENCES
section_header(COL3_X+10, y, COL3_W-20, 40, 'REFERENCES')
y += 50
refs = [
    '[1] UCI ML Repository — Predict Students\' Dropout and Academic Success',
    '[2] Pedregosa et al., Scikit-learn, JMLR 12, 2011',
    '[3] Lemaitre et al., Imbalanced-learn, JMLR 18, 2017',
    '[4] Chen & Guestrin, XGBoost, KDD 2016',
    '[5] Streamlit Documentation, streamlit.io',
]
for r in refs:
    draw_text(COL3_X+25, y, r, fs=15, color=GRAY)
    y += 22

print("Right column done")

# ============ FOOTER ============
draw.rectangle((0, H-35, W, H), fill=NAVY)
font_footer = get_font(14)
draw.text((W//2 - 400, H-28), 'Student Dropout Prediction Using Machine Learning  |  Chennai Institute of Technology  |  PBL 2026-27', fill='#93C5FD', font=font_footer)

# ============ SAVE ============
out = 'C:/My Code/COLLEGE/ML PROJECT/Poster/PBL_Poster.png'
img.save(out, 'PNG', dpi=(300, 300))
print(f"Saved: {out}")
print(f"Size: {W}x{H} pixels")
print(f"File: {os.path.getsize(out)/1024/1024:.1f} MB")
