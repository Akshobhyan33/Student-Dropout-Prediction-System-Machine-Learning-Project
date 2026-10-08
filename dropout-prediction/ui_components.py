import streamlit as st

from ui_theme import icon

OUTCOME_STYLE = {
    "Dropout": ("#f87171", "rgba(239,68,68,0.14)", "rgba(239,68,68,0.36)", "triangle-alert"),
    "Enrolled": ("#fbbf24", "rgba(251,191,36,0.13)", "rgba(251,191,36,0.34)", "refresh-cw"),
    "Graduate": ("#34d399", "rgba(52,211,153,0.13)", "rgba(52,211,153,0.32)", "circle-check"),
}

PROB_STYLE = {
    "Dropout": ("#f87171", "triangle-alert"),
    "Enrolled": ("#fbbf24", "refresh-cw"),
    "Graduate": ("#34d399", "circle-check"),
}


def app_header(title, subtitle):
    st.markdown(
        f"""
<div class="app-header">
  <div class="brand-mark">{icon('graduation-cap', 21)}</div>
  <div class="brand-text">
    <h1>{title}</h1>
    <p>{subtitle}</p>
  </div>
</div>""",
        unsafe_allow_html=True,
    )


def section_head(icon_name, title, tone="accent"):
    color = "#38bdf8" if tone == "cyan" else "#fb7185"
    bg = "rgba(56,189,248,0.1)" if tone == "cyan" else "rgba(239,68,68,0.1)"
    border = "rgba(56,189,248,0.24)" if tone == "cyan" else "rgba(239,68,68,0.26)"
    st.markdown(
        f"""
<div class="sec-head">
  <span class="sec-ico" style="color:{color};background:{bg};border-color:{border}">{icon(icon_name, 16)}</span>
  <span class="sec-title">{title}</span>
</div>""",
        unsafe_allow_html=True,
    )


def segmented_nav(key="nav"):
    return st.radio(
        " ",
        ["Single Student", "Batch Analysis"],
        horizontal=True,
        key=key,
        label_visibility="collapsed",
    )


def stat_cards(items):
    cards = []
    for label, value, tint in items:
        cards.append(
            f"""
<div class="stat-card" style="--tint:{tint}">
  <p class="stat-label">{label}</p>
  <p class="stat-value">{value}</p>
</div>"""
        )
    st.markdown(f'<div class="stat-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def result_card(outcome, confidence, class_names, probabilities):
    tint, soft, border, ic = OUTCOME_STYLE[outcome]

    bars = []
    for name, prob in zip(class_names, probabilities):
        color, bic = PROB_STYLE[name]
        pct = float(prob) * 100
        bars.append(
            f"""
<div class="prob-row">
  <div class="prob-meta">
    <span class="prob-name" style="color:{color}">{icon(bic, 12)} {name}</span>
    <span class="prob-pct">{pct:.1f}%</span>
  </div>
  <div class="prob-track"><span class="prob-fill" style="--pc:{color};width:{pct:.2f}%"></span></div>
</div>"""
        )

    st.markdown(
        f"""
<div class="result" style="--tint:{tint};--tint-soft:{soft};--tint-bd:{border}">
  <div class="result-glow"></div>
  <div class="result-main">
    <p class="result-label">{icon(ic, 13)} Predicted Outcome</p>
    <p class="result-outcome">{outcome}</p>
    <p class="result-conf">Confidence <b>{confidence:.1f}%</b></p>
  </div>
  <div class="result-side">{"".join(bars)}</div>
</div>""",
        unsafe_allow_html=True,
    )


def drop_area_title(text):
    st.markdown(
        f'<div class="drop-title">{icon("upload", 18)}<span>{text}</span></div>',
        unsafe_allow_html=True,
    )


def supported_formats():
    st.markdown(
        f"""
<div class="fmt">
  <p class="fmt-row"><b>College format</b> (recommended):<br>
    <code>Student_ID, Name, CGPA_Sem1, CGPA_Sem2, Subjects_Passed_Sem1, Subjects_Passed_Sem2, Fees_Paid, ...</code></p>
  <p class="fmt-row"><b>UCI format</b> (original): 37 columns like
    <code>Curricular units 1st sem (approved)</code>, <code>Tuition fees up to date</code>, etc.</p>
  <p class="fmt-row">File can be comma or semicolon separated.</p>
</div>""",
        unsafe_allow_html=True,
    )


DEFAULT_TONE_ICON = {"info": "info", "ok": "circle-check", "warn": "alert-circle", "err": "triangle-alert"}


def note(text, tone="info", icon_name=None):
    tone = tone if tone in DEFAULT_TONE_ICON else "info"
    st.markdown(
        f'<div class="note {tone}">{icon(icon_name or DEFAULT_TONE_ICON[tone], 14)}<span>{text}</span></div>',
        unsafe_allow_html=True,
    )
