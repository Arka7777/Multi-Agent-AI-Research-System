import time
import streamlit as st
from pipeline import run_pipeline

st.set_page_config(
    page_title="ResearchMind",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------------------------------
# STYLES
# --------------------------------------------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #0a0a0a; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* ---- Hero ---- */
.kicker {
    text-align: center;
    color: #f97316;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}
.wordmark {
    text-align: center;
    font-family: 'Archivo Black', sans-serif;
    font-size: 3.6rem;
    line-height: 1.05;
    margin: 0 0 1.1rem 0;
}
.wordmark .w1 { color: #f5f3ef; }
.wordmark .w2 {
    background: linear-gradient(90deg, #fb923c, #f97316);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 1rem;
    max-width: 560px;
    margin: 0 auto 2rem auto;
    line-height: 1.55;
}
.hairline {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 0 0 2.4rem 0;
}

/* ---- Section labels ---- */
.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #f97316;
    margin-bottom: 0.6rem;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #f5f3ef;
    margin-bottom: 1rem;
}

/* ---- Text input ---- */
.stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #f5f3ef !important;
    padding: 0.85rem 1.1rem !important;
    font-size: 0.95rem !important;
}
.stTextInput input::placeholder { color: #6b7280 !important; }
.stTextInput input:focus { border-color: #f97316 !important; }

/* ---- Run button ---- */
div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #fb923c, #ea580c);
    color: #0a0a0a;
    border: none;
    border-radius: 10px;
    padding: 0.85rem 1.5rem;
    font-weight: 700;
    font-size: 0.95rem;
    width: 100%;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 6px 24px rgba(249,115,22,0.25);
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 30px rgba(249,115,22,0.4);
}

/* ---- Chip row label ---- */
.chip-row-label {
    color: #6b7280;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin: 1.2rem 0 0.5rem 0;
    text-transform: uppercase;
}

/* ---- Pipeline cards ---- */
.pcard {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.3s ease, background 0.3s ease;
}
.pcard.active {
    border-color: rgba(249,115,22,0.5);
    background: rgba(249,115,22,0.06);
}
.pcard.done {
    border-color: rgba(74,222,128,0.35);
    background: rgba(74,222,128,0.04);
}
.pcard-left { display: flex; align-items: center; gap: 14px; }
.pcard-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    font-weight: 600;
    color: #f97316;
    width: 26px;
}
.pcard.done .pcard-num { color: #4ade80; }
.pcard-title { color: #f5f3ef; font-weight: 600; font-size: 0.95rem; margin-bottom: 2px; }
.pcard-desc { color: #6b7280; font-size: 0.8rem; }
.pcard-status {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 999px;
    color: #6b7280;
    background: rgba(255,255,255,0.04);
    white-space: nowrap;
}
.pcard.active .pcard-status {
    color: #f97316;
    background: rgba(249,115,22,0.12);
    animation: fade 1.3s ease-in-out infinite;
}
.pcard.done .pcard-status {
    color: #4ade80;
    background: rgba(74,222,128,0.12);
}
@keyframes fade { 0%,100% {opacity:1;} 50% {opacity:0.4;} }

/* ---- Results panels ---- */
.panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.panel h4 {
    margin-top: 0;
    color: #f5f3ef;
    font-weight: 700;
}
.report-body {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.88rem;
    line-height: 1.7;
    color: #d1d5db;
    white-space: pre-wrap;
}
.status-line {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #4ade80;
    font-size: 0.85rem;
    margin: 0 0 1.4rem 0;
}
.status-line .dot { width: 6px; height: 6px; border-radius: 50%; background: #4ade80; }

.stTabs [data-baseweb="tab"] { color: #6b7280; font-weight: 500; }
.stTabs [aria-selected="true"] { color: #f97316 !important; }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# HERO
# --------------------------------------------------------------------------
st.markdown('<div class="kicker">Multi-Agent AI System</div>', unsafe_allow_html=True)
st.markdown('<div class="wordmark"><span class="w1">Research</span><span class="w2">Mind</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Four specialized AI agents collaborate — searching, scraping, writing, '
    'and critiquing — to deliver a polished research report on any topic.</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="hairline">', unsafe_allow_html=True)

# --------------------------------------------------------------------------
# TWO COLUMN LAYOUT: input (left) / pipeline (right)
# --------------------------------------------------------------------------
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
if "history" not in st.session_state:
    st.session_state.history = []

left, right = st.columns([1, 1], gap="large")

SUGGESTIONS = ["LLM agents 2025", "Quantum computing breakthroughs", "Solid-state batteries", "CRISPR gene editing"]

with left:
    st.markdown('<div class="section-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research topic",
        value=st.session_state.topic_input,
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
        key="topic_field",
    )
    run_clicked = st.button("⚡ Run Research Pipeline", use_container_width=True)

    st.markdown('<div class="chip-row-label">Try →</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTIONS))
    for i, s in enumerate(SUGGESTIONS):
        with chip_cols[i]:
            if st.button(s, key=f"chip_{i}"):
                st.session_state.topic_input = s
                st.rerun()

STAGES = [
    ("search", "01", "Search Agent", "Gathers recent web information"),
    ("read", "02", "Reader Agent", "Scrapes & extracts deep content"),
    ("write", "03", "Writer Chain", "Drafts a structured report"),
    ("critique", "04", "Critic Chain", "Scores and stress-tests the draft"),
]

with right:
    st.markdown('<div class="section-title">Pipeline</div>', unsafe_allow_html=True)
    pipeline_placeholder = st.empty()


def render_pipeline(stage_states):
    html = ""
    status_word = {"pending": "WAITING", "active": "RUNNING", "done": "DONE"}
    for key, num, title, desc in STAGES:
        state = stage_states.get(key, "pending")
        html += f'''
        <div class="pcard {state}">
            <div class="pcard-left">
                <div class="pcard-num">{num}</div>
                <div>
                    <div class="pcard-title">{title}</div>
                    <div class="pcard-desc">{desc}</div>
                </div>
            </div>
            <div class="pcard-status">{status_word[state]}</div>
        </div>'''
    pipeline_placeholder.markdown(html, unsafe_allow_html=True)


stage_states = {key: "pending" for key, _, _, _ in STAGES}
with right:
    render_pipeline(stage_states)

results_placeholder = st.container()

# --------------------------------------------------------------------------
# RUN PIPELINE
# --------------------------------------------------------------------------
if run_clicked:
    if not topic.strip():
        st.warning("Enter a topic first.")
        st.stop()

    def on_progress(stage_key, status, payload):
        if status == "start":
            stage_states[stage_key] = "active"
        elif status == "done":
            stage_states[stage_key] = "done"
        with right:
            render_pipeline(stage_states)

    start_time = time.time()
    with st.spinner(""):
        state = run_pipeline(topic, on_progress=on_progress)
    elapsed = time.time() - start_time

    st.session_state.history.append(topic)
    st.session_state["last_state"] = state
    st.session_state["last_elapsed"] = elapsed
    st.session_state["last_topic"] = topic

# --------------------------------------------------------------------------
# RESULTS
# --------------------------------------------------------------------------
if "last_state" in st.session_state:
    state = st.session_state["last_state"]
    elapsed = st.session_state.get("last_elapsed", 0)
    topic_done = st.session_state.get("last_topic", "")

    with results_placeholder:
        st.markdown('<hr class="hairline">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="status-line"><span class="dot"></span>'
            f'Completed in {elapsed:.1f}s — "{topic_done}"</div>',
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3 = st.tabs(["Report", "Critique", "Raw Research"])

        with tab1:
            st.markdown(f'<div class="panel"><h4>Research Report</h4>'
                        f'<div class="report-body">{state["report"]}</div></div>',
                        unsafe_allow_html=True)
            st.download_button(
                "Download report (.md)",
                data=state["report"],
                file_name=f"{topic_done.replace(' ', '_')}_report.md",
                mime="text/markdown",
            )

        with tab2:
            st.markdown(f'<div class="panel"><h4>Critic Verdict</h4>'
                        f'<div class="report-body">{state["feedback"]}</div></div>',
                        unsafe_allow_html=True)

        with tab3:
            with st.expander("Search Agent Output", expanded=False):
                st.markdown(f'<div class="report-body">{state["search_results"]}</div>', unsafe_allow_html=True)
            with st.expander("Scraped Content (Reader Agent)", expanded=False):
                st.markdown(f'<div class="report-body">{state["scraped_content"]}</div>', unsafe_allow_html=True)