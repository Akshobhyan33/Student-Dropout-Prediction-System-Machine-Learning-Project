ICONS = {
    "graduation-cap": (
        '<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/>'
        '<path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>'
    ),
    "upload": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
        '<polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/>'
    ),
    "users": (
        '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
        '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "chart-column": (
        '<path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>'
    ),
    "triangle-alert": (
        '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/>'
        '<path d="M12 9v4"/><path d="M12 17h.01"/>'
    ),
    "circle-check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "refresh-cw": (
        '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>'
        '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>'
    ),
    "alert-circle": (
        '<circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/>'
        '<line x1="12" x2="12.01" y1="16" y2="16"/>'
    ),
}


def icon(name, size=16, cls="", stroke=1.8):
    body = ICONS.get(name, ICONS["info"])
    return (
        f'<svg class="ico {cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="{stroke}" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{body}</svg>'
    )


BASE_CSS = """
<style>
:root{
  --bg:#080a0f;
  --surface:#181c25;
  --surface-2:#11151d;
  --border:rgba(255,255,255,0.07);
  --border-2:rgba(255,255,255,0.12);
  --text:#f4f6fa;
  --muted:#98a2b3;
  --dim:#6b7484;
  --accent:#ef4444;
  --accent-2:#fb7185;
  --accent-deep:#b91c1c;
  --cyan:#38bdf8;
  --radius:14px;
  --radius-sm:11px;
  --shadow:0 16px 34px -24px rgba(0,0,0,.95);
}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"],section.main,.main,.block-container{
  background-color:var(--bg);
}
.stApp{
  background-image:
    radial-gradient(1000px 560px at 10% -12%, rgba(239,68,68,.10), transparent 62%),
    radial-gradient(820px 520px at 92% -8%, rgba(56,189,248,.05), transparent 60%),
    radial-gradient(900px 620px at 50% 108%, rgba(239,68,68,.05), transparent 62%),
    repeating-linear-gradient(0deg, rgba(255,255,255,.022) 0 1px, transparent 1px 72px),
    repeating-linear-gradient(90deg, rgba(255,255,255,.022) 0 1px, transparent 1px 72px);
  background-attachment:fixed;
}
.stApp::after{
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    radial-gradient(circle at 22% 28%, rgba(255,255,255,.45) 0 1px, transparent 1.4px),
    radial-gradient(circle at 68% 62%, rgba(255,255,255,.32) 0 1px, transparent 1.4px),
    radial-gradient(circle at 86% 18%, rgba(255,255,255,.26) 0 1px, transparent 1.4px);
  background-size:360px 360px,440px 440px,520px 520px;
  opacity:.45;
  -webkit-mask-image:linear-gradient(180deg, rgba(0,0,0,.85), transparent 62%);
  mask-image:linear-gradient(180deg, rgba(0,0,0,.85), transparent 62%);
}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > *,
[data-testid="stAppViewContainer"] .main,
[data-testid="stMain"], section.main, .stMain, .main, .block-container{
  position:relative; z-index:1;
}
#MainMenu, footer, header[data-testid="stHeader"], [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], [data-testid="collapsedControl"]{
  visibility:hidden; height:0; display:none;
}
.block-container, .main .block-container{
  padding:1.5rem clamp(1rem,3vw,2.75rem) 2.5rem; max-width:1320px;
}
h1,h2,h3,h4,h5{ letter-spacing:-.02em; }
.ico{ vertical-align:-.14em; flex:0 0 auto; }
[data-testid="stAppViewContainer"] .stMarkdown p{ margin:0; }
hr{ border-color:var(--border); }
::-webkit-scrollbar{ width:9px; height:9px; }
::-webkit-scrollbar-track{ background:#0b0d11; }
::-webkit-scrollbar-thumb{ background:#232935; border-radius:8px; border:2px solid #0b0d11; }
</style>
"""

COMPONENT_CSS = """
<style>
.app-header{
  display:flex; align-items:center; gap:.8rem;
  padding:.85rem 1.1rem; margin-bottom:.75rem;
  background:
    radial-gradient(420px 90px at 0% 0%, rgba(255,255,255,.03), transparent 70%),
    linear-gradient(135deg, rgba(28,32,40,.8) 0%, rgba(15,18,24,.62) 100%);
  border:1px solid var(--border); border-radius:var(--radius);
  box-shadow:var(--shadow); position:relative; overflow:hidden;
}
.app-header::before{
  content:""; position:absolute; left:0; top:0; height:2px; width:100%;
  background:linear-gradient(90deg, var(--accent-deep), var(--accent) 30%, rgba(56,189,248,.45) 70%, transparent);
}
.brand-mark{
  width:36px; height:36px; flex:0 0 36px; border-radius:var(--radius-sm);
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(140deg, rgba(239,68,68,.2), rgba(239,68,68,.05));
  border:1px solid rgba(239,68,68,.3); color:var(--accent-2);
}
.brand-text h1{
  margin:0; font-size:clamp(1.12rem,1.7vw,1.42rem); font-weight:700; color:#fff; line-height:1.2;
}
.brand-text p{ margin:.12rem 0 0; color:var(--muted); font-size:.785rem; line-height:1.35; }
.sec-head{ display:flex; align-items:center; gap:.5rem; margin-bottom:.7rem; }
.sec-ico{
  width:26px; height:26px; flex:0 0 26px; border-radius:8px;
  display:inline-flex; align-items:center; justify-content:center; border:1px solid;
}
.sec-title{ font-size:.92rem; font-weight:650; color:#fff; letter-spacing:-.012em; }
.stat-grid{ display:grid; gap:.7rem; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); }
.stat-card{
  position:relative; overflow:hidden;
  background:
    radial-gradient(300px 80px at 0% 0%, rgba(255,255,255,.026), transparent 70%),
    linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:var(--radius);
  padding:.8rem .95rem; box-shadow:var(--shadow);
}
.stat-card::before{
  content:""; position:absolute; inset:0 auto 0 0; width:3px;
  background:linear-gradient(180deg,var(--tint,var(--accent)),transparent);
}
.stat-label{
  margin:0 0 .3rem; font-size:.715rem; font-weight:600; letter-spacing:.04em;
  text-transform:uppercase; color:var(--muted);
}
.stat-value{ margin:0; font-size:1.45rem; font-weight:700; color:#fff; line-height:1.1; font-variant-numeric:tabular-nums; }
.result{
  position:relative; overflow:hidden;
  display:grid; grid-template-columns:minmax(0,.85fr) minmax(0,1fr); gap:1.6rem; align-items:center;
  background:linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--tint-bd,var(--border-2)); border-radius:var(--radius);
  padding:1.35rem 1.5rem; box-shadow:var(--shadow);
}
.result::before{
  content:""; position:absolute; inset:0 0 auto 0; height:3px;
  background:linear-gradient(90deg,var(--tint),transparent 82%);
}
.result-glow{
  position:absolute; right:-80px; top:-80px; width:250px; height:250px; border-radius:50%;
  background:radial-gradient(circle, var(--tint) 0%, transparent 68%); opacity:.14; pointer-events:none;
}
.result-main{ position:relative; min-width:0; }
.result-label{
  display:flex; align-items:center; gap:.4rem; margin:0 0 .5rem;
  font-size:.7rem; font-weight:650; letter-spacing:.1em; text-transform:uppercase; color:var(--dim);
}
.result-outcome{
  margin:0; font-size:clamp(1.7rem,3.4vw,2.4rem); font-weight:800; line-height:1.04;
  color:var(--tint); letter-spacing:-.03em;
}
.result-conf{ margin:.5rem 0 0; color:var(--muted); font-size:.86rem; }
.result-conf b{ color:#fff; font-weight:650; font-variant-numeric:tabular-nums; }
.result-side{ position:relative; min-width:0; }
.prob-row + .prob-row{ margin-top:.72rem; }
.prob-meta{ display:flex; justify-content:space-between; align-items:center; margin-bottom:.3rem; }
.prob-name{ display:inline-flex; align-items:center; gap:.4rem; font-size:.8rem; font-weight:550; }
.prob-pct{ color:#fff; font-size:.8rem; font-weight:650; font-variant-numeric:tabular-nums; }
.prob-track{ height:8px; border-radius:999px; background:rgba(5,7,10,.9); border:1px solid var(--border); overflow:hidden; }
.prob-fill{
  display:block; height:100%; border-radius:999px; background-color:var(--pc);
  background-image:linear-gradient(90deg,var(--pc),color-mix(in srgb,var(--pc) 50%, #ffffff));
  transition:width .5s cubic-bezier(.22,.8,.3,1);
}
.drop-title{
  display:flex; align-items:center; justify-content:center; gap:.5rem; margin:0 0 .65rem;
  color:var(--text); font-size:.95rem; font-weight:600; text-align:center;
}
.drop-title .ico{ color:var(--accent-2); }
.fmt{
  background:
    radial-gradient(400px 90px at 0% 0%, rgba(255,255,255,.022), transparent 70%),
    linear-gradient(180deg, var(--surface-2) 0%, rgba(12,15,20,.5) 100%);
  border:1px solid var(--border); border-radius:var(--radius);
  padding:.85rem 1rem;
}
.fmt-row{ margin:0 0 .5rem; color:var(--muted); font-size:.775rem; line-height:1.55; }
.fmt-row:last-child{ margin-bottom:0; }
.fmt-row b{ color:#dfe5ee; font-weight:600; }
.fmt-row code{
  font-family:'JetBrains Mono',ui-monospace,SFMono-Regular,Consolas,monospace;
  font-size:.715rem; color:#a9b6c8; background:rgba(5,7,10,.6);
  border:1px solid var(--border); border-radius:5px; padding:.06rem .28rem;
}
.note{
  display:flex; align-items:flex-start; gap:.55rem;
  background:rgba(56,189,248,.055); border:1px solid rgba(56,189,248,.16);
  border-radius:var(--radius-sm); padding:.7rem .85rem;
  color:#bcd3e4; font-size:.785rem; line-height:1.5;
}
.note .ico{ color:var(--cyan); flex:0 0 auto; margin-top:.12rem; }
.note.ok{ background:rgba(52,211,153,.06); border-color:rgba(52,211,153,.18); color:#b6e8d5; }
.note.ok .ico{ color:#34d399; }
.note.warn{ background:rgba(251,191,36,.06); border-color:rgba(251,191,36,.2); color:#e5d3a3; }
.note.warn .ico{ color:#fbbf24; }
.note.err{ background:rgba(239,68,68,.07); border-color:rgba(239,68,68,.22); color:#f3c2c2; }
.note.err .ico{ color:var(--accent-2); }
.lead{ margin:0 0 .7rem; color:var(--muted); font-size:.85rem; line-height:1.5; }
.section-label{
  margin:.2rem 0 .55rem; color:#dfe5ee; font-size:.9rem; font-weight:600;
}
@media (max-width:1080px){
  .result{ grid-template-columns:1fr; gap:1.1rem; }
}
@media (max-width:760px){
  .app-header{ padding:.9rem 1rem; }
  .result{ padding:1.1rem 1.05rem; }
  .block-container,.main .block-container{ padding-left:.9rem; padding-right:.9rem; }
}
</style>
"""

WIDGET_CSS = """
<style>
[class*="st-key-sec_"]{
  gap:.5rem !important;
  background:
    radial-gradient(460px 130px at 0% 0%, rgba(255,255,255,.026), transparent 70%),
    linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-top:1.5px solid rgba(239,68,68,.34);
  border-radius:var(--radius); box-shadow:var(--shadow);
  padding:.9rem 1rem .5rem; height:100%;
}
[data-testid="stHorizontalBlock"]:has([class*="st-key-sec_academic"]){ align-items:stretch; }
[data-testid="stHorizontalBlock"]:has([class*="st-key-sec_academic"]) [data-testid="stColumn"]{
  display:flex; flex-direction:column;
}
[data-testid="stHorizontalBlock"]:has([class*="st-key-sec_academic"]) [data-testid="stColumn"] > div{
  flex:1 1 auto; min-height:0;
}
[class*="st-key-sec_profile"]{ border-top-color:rgba(56,189,248,.28); justify-content:space-between; }
[class*="st-key-sec_upload"]{
  border:1.5px dashed rgba(148,163,184,0.26);
  background:
    radial-gradient(420px 150px at 50% 0%, rgba(56,189,248,.06), transparent 70%),
    radial-gradient(460px 130px at 0% 0%, rgba(255,255,255,.026), transparent 70%),
    linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  padding:1.05rem 1rem .85rem; text-align:center;
  transition:border-color .2s ease, background .2s ease;
}
[class*="st-key-sec_upload"]:hover{ border-color:rgba(239,68,68,.4); }
[class*="st-key-sec_formats"]{ padding-bottom:.5rem; }
[class*="st-key-sec_"] [data-testid="stVerticalBlock"]{ gap:.5rem !important; }
[class*="st-key-sec_"] [data-testid="stSlider"]{ margin:0 !important; padding:.05rem 0 .15rem; }
[class*="st-key-sec_"] [data-testid="stWidgetLabel"]{ margin-bottom:.1rem !important; }
.st-key-nav{ margin:0 0 .8rem; }
.st-key-nav [role="radiogroup"]{
  gap:.22rem; flex-wrap:wrap; width:fit-content;
  background:rgba(9,12,17,.6); border:1px solid var(--border);
  border-radius:12px; padding:.26rem;
}
.st-key-nav [role="radiogroup"] > label{
  position:relative; cursor:pointer;
  padding:.46rem 1rem; border-radius:9px;
  background:transparent; border:1px solid transparent;
  transition:background .16s ease, border-color .16s ease;
}
.st-key-nav [role="radiogroup"] > label p{ color:var(--muted) !important; font-size:.845rem !important; font-weight:600 !important; }
.st-key-nav [role="radiogroup"] > label:hover{ background:rgba(255,255,255,.04); }
.st-key-nav [role="radiogroup"] > label:hover p{ color:#fff !important; }
.st-key-nav [role="radiogroup"] > label:has(input:checked){
  background:linear-gradient(135deg, rgba(239,68,68,.9), rgba(185,28,28,.9));
  border-color:rgba(251,113,133,.42);
  box-shadow:0 8px 20px -12px rgba(239,68,68,.95);
}
.st-key-nav [role="radiogroup"] > label:has(input:checked) p{ color:#fff !important; }
.st-key-nav input[type="radio"]{ position:absolute; opacity:0; width:0; height:0; }
.st-key-nav [data-testid="stWidgetLabel"]{ display:none; }
.stButton > button, .stDownloadButton > button{
  width:100%;
  background:linear-gradient(135deg, var(--accent) 0%, var(--accent-deep) 100%);
  color:#fff; border:1px solid rgba(251,113,133,.4);
  border-radius:var(--radius-sm); padding:.72rem 1.3rem;
  font-size:.9rem; font-weight:650; letter-spacing:.005em;
  box-shadow:0 12px 26px -16px rgba(239,68,68,.9), 0 0 24px -14px rgba(239,68,68,.6);
  transition:transform .16s ease, box-shadow .16s ease, filter .16s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover{
  transform:translateY(-2px); filter:brightness(1.08);
  border-color:rgba(251,113,133,.7);
  box-shadow:0 18px 32px -16px rgba(239,68,68,1), 0 0 0 3px rgba(239,68,68,.11);
}
.stButton > button:active, .stDownloadButton > button:active{ transform:translateY(0); }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible{
  outline:2px solid rgba(56,189,248,.7); outline-offset:2px;
}
.st-key-secondary .stButton > button, .st-key-secondary .stDownloadButton > button{
  background:rgba(20,24,31,.85); color:#dbe3ee;
  border:1px solid var(--border-2); box-shadow:none;
}
.st-key-secondary .stButton > button:hover, .st-key-secondary .stDownloadButton > button:hover{
  border-color:rgba(56,189,248,.45); color:#fff; filter:none;
  box-shadow:0 12px 24px -18px rgba(56,189,248,.9);
}
[data-testid="stSlider"] [role="slider"], [data-testid="stSlider"] div[class^="thumb-"] > div{
  background:#fff !important; border:3px solid var(--accent) !important;
  box-shadow:0 0 0 4px rgba(239,68,68,.15), 0 3px 9px rgba(0,0,0,.6) !important;
}
[data-testid="stSlider"] [role="slider"]:focus{ box-shadow:0 0 0 6px rgba(239,68,68,.26) !important; }
[data-testid="stSlider"] div[class^="bar-"]{ box-shadow:0 0 12px rgba(239,68,68,.35); }
[data-testid="stSlider"] [data-testid="stSliderTickBar"], [data-testid="stSliderTickBarMin"],
[data-testid="stSliderTickBarMax"]{ display:none !important; }
[data-testid="stSlider"] [data-testid="stThumbValue"]{
  background:var(--accent); color:#fff; border-radius:6px; padding:.08rem .32rem;
  font-size:.67rem !important; font-weight:700 !important;
  font-variant-numeric:tabular-nums;
}
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label{
  color:#c8d1de !important; font-size:.785rem !important; font-weight:550 !important; line-height:1.35 !important;
}
[data-baseweb="select"] > div{
  background:rgba(11,14,19,.92) !important;
  border:1px solid var(--border-2) !important; border-radius:var(--radius-sm) !important;
  transition:border-color .16s ease, box-shadow .16s ease;
}
[data-baseweb="select"] > div:hover{ border-color:rgba(239,68,68,.42) !important; }
[data-baseweb="select"] > div:focus-within{
  border-color:rgba(56,189,248,.55) !important; box-shadow:0 0 0 3px rgba(56,189,248,.13) !important;
}
[data-baseweb="select"] span, [data-baseweb="select"] input{ color:#e6edf6 !important; font-size:.83rem !important; }
[data-baseweb="popover"] ul{ background:#0f1319 !important; }
[data-baseweb="popover"] li:hover{ background:rgba(239,68,68,.15) !important; }
[data-baseweb="popover"] li[aria-selected="true"]{ background:rgba(239,68,68,.22) !important; }
[data-testid="stFileUploaderDropzone"]{
  background:transparent !important; border:none !important; padding:.2rem !important;
}
[data-testid="stFileUploaderDropzone"] button{
  background:linear-gradient(135deg, var(--accent), var(--accent-deep)) !important;
  color:#fff !important; border:1px solid rgba(251,113,133,.4) !important;
  border-radius:9px !important; font-weight:600 !important; font-size:.8rem !important;
  padding:.45rem .95rem !important;
}
[data-testid="stFileUploaderDropzone"] small, [data-testid="stFileUploaderDropzone"] small div{
  color:var(--dim) !important; font-size:.715rem !important;
}
[data-testid="stFileUploaderFile"]{
  background:rgba(11,14,19,.75) !important; border:1px solid var(--border) !important; border-radius:9px !important;
}
[data-testid="stDataFrame"], [data-testid="stArrowDataFrame"]{
  border:1px solid var(--border) !important; border-radius:var(--radius-sm) !important; overflow:hidden;
}
[data-testid="stExpander"]{
  border:1px solid var(--border) !important; border-radius:var(--radius-sm) !important;
  background:rgba(13,16,21,.5) !important; overflow:hidden;
}
[data-testid="stExpander"] summary{ font-size:.8rem !important; color:#c8d1de !important; }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p{ color:var(--dim) !important; font-size:.72rem !important; }
[data-testid="stAlert"]{ border-radius:var(--radius-sm) !important; border:1px solid var(--border-2) !important; font-size:.78rem !important; }
[data-testid="stAppViewContainer"] .block-container{ overflow-x:clip; }
</style>
"""


def apply_theme():
    import streamlit as st

    st.markdown(
        "<link rel='preconnect' href='https://fonts.googleapis.com'>"
        "<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>"
        "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap' rel='stylesheet'>",
        unsafe_allow_html=True,
    )
    st.markdown(BASE_CSS, unsafe_allow_html=True)
    st.markdown(COMPONENT_CSS, unsafe_allow_html=True)
    st.markdown(WIDGET_CSS, unsafe_allow_html=True)