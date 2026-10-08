import streamlit as st

import ui_components as ui
from prediction_engine import (
    CLASS_NAMES,
    load_artifacts,
    predict_batch,
    predict_single,
    read_uploaded_csv,
)
from ui_theme import apply_theme

st.set_page_config(
    page_title="Student Dropout Risk Predictor",
    page_icon="favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner=False)
def get_artifacts():
    return load_artifacts()


@st.cache_resource(show_spinner=False)
def get_mapper():
    from college_to_uci_mapper import FEATURE_ORDER, add_engineered_features, college_to_uci

    return college_to_uci, add_engineered_features, FEATURE_ORDER


def single_student_page(model, features, feature_defaults):
    st.markdown(
        "<p class=\"lead\">Enter a student's details to predict whether they will "
        "Dropout, Stay Enrolled, or Graduate.</p>",
        unsafe_allow_html=True,
    )

    left, right = st.columns(2, gap="medium")

    with left:
        with st.container(key="sec_academic"):
            ui.section_head("chart-column", "Academic Performance")
            sem2_grade = st.slider(
                "2nd Sem Grade (CGPA, 0-10)", 0.0, 10.0, 6.0, step=0.1,
                help="Average grade in 2nd semester on a 0-10 CGPA scale",
            )
            sem2_units_approved = st.slider(
                "2nd Sem Subjects Passed", 0, 10, 5,
                help="How many subjects did the student pass in 2nd semester?",
            )
            total_units_approved = st.slider(
                "Total Subjects Passed (both semesters)", 0, 20, 10,
                help="Total subjects passed across 1st and 2nd semester combined",
            )
            sem2_approval_rate = st.slider(
                "2nd Sem Pass Rate", 0.0, 1.0, 0.6, step=0.01, format="%.2f",
                help="What fraction of enrolled subjects were passed in 2nd sem",
            )
            sem1_approval_rate = st.slider(
                "1st Sem Pass Rate", 0.0, 1.0, 0.6, step=0.01, format="%.2f",
                help="What fraction of enrolled subjects were passed in 1st sem",
            )

    with right:
        with st.container(key="sec_profile"):
            ui.section_head("users", "Student &amp; Financial Information", tone="cyan")
            age = st.slider("Age at Enrollment", 17, 50, 20)
            tuition_up_to_date = st.selectbox(
                "Tuition Fees Up to Date?", ["Yes", "No"],
                help="Unpaid tuition is one of the strongest financial risk flags",
            )
            scholarship = st.selectbox("Scholarship Holder?", ["Yes", "No"])

    action, _ = st.columns([1, 1.7], gap="medium")
    with action:
        if st.button("Predict Outcome", key="single_predict"):
            st.session_state["single_result"] = predict_single(
                model,
                feature_defaults,
                features,
                {
                    "sem2_grade": sem2_grade,
                    "sem2_units_approved": sem2_units_approved,
                    "total_units_approved": total_units_approved,
                    "sem2_approval_rate": sem2_approval_rate,
                    "sem1_approval_rate": sem1_approval_rate,
                    "tuition_up_to_date": tuition_up_to_date,
                    "scholarship": scholarship,
                    "age": age,
                },
            )

    result = st.session_state.get("single_result")
    if result:
        ui.result_card(
            result["outcome"],
            result["confidence"],
            CLASS_NAMES,
            result["probabilities"],
        )


def render_results(batch):
    results = batch["results"]

    ui.stat_cards(
        [
            ("High Dropout Risk (&gt;60%)", batch["risk_counts"].get("High", 0), "#f87171"),
            ("Medium Risk (30-60%)", batch["risk_counts"].get("Medium", 0), "#fbbf24"),
            ("Low Risk (&lt;30%)", batch["risk_counts"].get("Low", 0), "#34d399"),
        ]
    )

    st.markdown(
        '<p class="section-label">Students ranked by dropout risk (highest first):</p>',
        unsafe_allow_html=True,
    )

    styled = results.style.apply(
        lambda row: [
            "background-color: rgba(239,68,68,0.15); color: #fecaca"
            if row["Dropout_Prob_%"] > 60
            else "background-color: rgba(251,191,36,0.12); color: #fde68a"
            if row["Dropout_Prob_%"] >= 30
            else "background-color: rgba(52,211,153,0.1); color: #bbf7d0"
        ]
        * len(row),
        axis=1,
    )
    st.dataframe(
        styled,
        width="stretch",
        hide_index=True,
        height=max(160, min(480, 62 + 35 * len(results))),
        column_config={
            "Predicted": st.column_config.TextColumn("Predicted", width="small"),
            "Dropout_Prob_%": st.column_config.ProgressColumn(
                "Dropout_Prob_%", min_value=0.0, max_value=100.0, format="%.1f%%", width="medium"
            ),
            "Enrolled_Prob_%": st.column_config.NumberColumn("Enrolled_Prob_%", format="%.1f"),
            "Graduate_Prob_%": st.column_config.NumberColumn("Graduate_Prob_%", format="%.1f"),
            "Risk_Level": st.column_config.TextColumn("Risk_Level", width="small"),
        },
    )

    left, right = st.columns([1, 1.6], gap="medium")
    with left:
        with st.container(key="sec_secondary"):
            st.download_button(
                "Download Predictions as CSV",
                data=results.to_csv(index=False).encode("utf-8"),
                file_name="dropout_predictions.csv",
                mime="text/csv",
                width="stretch",
            )
    with right:
        if batch["accuracy"] is not None:
            ui.note(
                f"Model Accuracy on this file: <b>{batch['accuracy'] * 100:.1f}%</b>",
                tone="ok",
                icon_name="trending-up",
            )

    if batch["report"]:
        with st.expander("Show detailed classification report"):
            st.code(batch["report"], language="text")


def batch_page(model):
    spacer_left, middle, spacer_right = st.columns([1, 1.5, 1], gap="medium")

    with middle:
        with st.container(key="sec_upload"):
            ui.drop_area_title("Upload a CSV file with student data.")
            uploaded_file = st.file_uploader(
                "Choose CSV file",
                type=["csv"],
                label_visibility="collapsed",
                key="batch_upload",
            )

    with st.container(key="sec_formats"):
        ui.supported_formats()

    if uploaded_file is None:
        return

    college_to_uci, add_engineered_features, feature_order = get_mapper()

    try:
        students_df = read_uploaded_csv(uploaded_file)
        if students_df.empty:
            ui.note(
                "This file has no data rows. Export the sheet with a header row and "
                "at least one student record.",
                tone="warn",
                icon_name="alert-circle",
            )
            return
        batch = predict_batch(
            model, students_df, college_to_uci, add_engineered_features, feature_order
        )
    except Exception as exc:
        ui.note(
            f"Could not process this file. {exc} Check that the columns match one of "
            "the supported formats.",
            tone="err",
            icon_name="triangle-alert",
        )
        return

    detected = (
        "Detected <b>college format</b> &mdash; converting to model features automatically."
        if batch["format"] == "college"
        else "Detected <b>UCI format</b> &mdash; using original features."
    )
    ui.note(f"Loaded {len(students_df)} students &nbsp;&middot;&nbsp; {detected}", tone="ok")

    render_results(batch)


def main():
    apply_theme()

    model, _df, features, feature_defaults = get_artifacts()

    ui.app_header(
        "Student Dropout Risk Predictor",
        "AI-powered early warning system for student academic outcomes",
    )

    page = ui.segmented_nav()

    if page == "Single Student":
        single_student_page(model, features, feature_defaults)
    else:
        batch_page(model)


main()