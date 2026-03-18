import streamlit as st
import requests
import json
import sqlite3
import os
import base64
import tempfile
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RaMsAI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'DM Mono', monospace;
}

[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e;
}

[data-testid="stSidebar"] > div { padding: 0 !important; }

.sidebar-logo {
    padding: 2rem 1.5rem 1.5rem;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 1rem;
}

.sidebar-logo h1 {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #fff;
}

.sidebar-logo span { color: #5b6af0; }

.sidebar-logo p {
    font-size: 0.65rem;
    color: #4a4a6a;
    margin-top: 0.25rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.nav-section {
    padding: 0 1rem;
    margin-bottom: 0.5rem;
}

.nav-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #3a3a5a;
    padding: 0.5rem 0.5rem 0.25rem;
    font-weight: 500;
}

.stRadio > div { gap: 0 !important; }

.stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 0.6rem 0.75rem !important;
    border-radius: 8px !important;
    font-size: 0.8rem !important;
    color: #6a6a8a !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    margin: 1px 0 !important;
}

.stRadio label:hover { background: #15151f !important; color: #b0b0d0 !important; }

.page-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid #1a1a2a;
    margin-bottom: 2rem;
}

.page-header h2 {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
    letter-spacing: -0.02em;
}

.page-header p { font-size: 0.75rem; color: #4a4a6a; margin-top: 0.4rem; }

.card {
    background: #0f0f18;
    border: 1px solid #1a1a2a;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    color: #5b6af0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 1rem;
}

.msg-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1rem;
    align-items: flex-start;
}

.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 600;
    flex-shrink: 0;
    margin-top: 2px;
}

.msg-avatar.ai { background: #1a1a3a; color: #5b6af0; border: 1px solid #2a2a4a; }
.msg-avatar.user-av { background: #1a2a1a; color: #5af078; border: 1px solid #2a4a2a; }

.msg-bubble {
    max-width: 80%;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-size: 0.82rem;
    line-height: 1.6;
}

.msg-bubble.ai { background: #12121e; border: 1px solid #1e1e30; color: #c8c8e0; }
.msg-bubble.user { background: #131f30; border: 1px solid #1e2e42; color: #a8c8e8; }

.reasoning-box {
    background: #0c0c16;
    border: 1px solid #1a1a2a;
    border-left: 3px solid #5b6af0;
    border-radius: 6px;
    padding: 0.75rem 1rem;
    margin-top: 0.5rem;
    font-size: 0.72rem;
    color: #4a4a6a;
    line-height: 1.5;
}

.reasoning-box .label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3a3a5a;
    margin-bottom: 0.4rem;
}

.history-item {
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #13131e;
    cursor: pointer;
    transition: background 0.1s;
}

.history-item:hover { background: #13131e; }
.history-item .hi-role { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.1em; color: #3a3a5a; margin-bottom: 0.2rem; }
.history-item .hi-text { font-size: 0.78rem; color: #7a7a9a; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.history-item .hi-time { font-size: 0.6rem; color: #2a2a3a; margin-top: 0.2rem; }

.model-badge {
    display: inline-block;
    background: #12121e;
    border: 1px solid #2a2a3a;
    border-radius: 4px;
    padding: 0.15rem 0.5rem;
    font-size: 0.65rem;
    color: #5b6af0;
    margin-bottom: 0.5rem;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0c0c16 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #5b6af0 !important;
    box-shadow: 0 0 0 2px rgba(91, 106, 240, 0.12) !important;
}

.stButton > button {
    background: #5b6af0 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.15s ease !important;
}

.stButton > button:hover { background: #4a59e0 !important; transform: translateY(-1px) !important; }

.stSelectbox > div > div {
    background: #0c0c16 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e8f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

.stSlider > div > div { color: #5b6af0 !important; }

div[data-testid="stMetric"] {
    background: #0c0c16;
    border: 1px solid #1a1a2a;
    border-radius: 8px;
    padding: 1rem !important;
}

div[data-testid="stMetric"] label { color: #4a4a6a !important; font-size: 0.7rem !important; }
div[data-testid="stMetric"] div { color: #5b6af0 !important; font-family: 'Syne', sans-serif !important; }

.stExpander {
    background: #0f0f18 !important;
    border: 1px solid #1a1a2a !important;
    border-radius: 8px !important;
}

.stSpinner > div { border-color: #5b6af0 transparent transparent transparent !important; }

hr { border-color: #1a1a2a !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = "/tmp/nexusai.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        role TEXT,
        content TEXT,
        reasoning TEXT,
        model TEXT,
        mode TEXT,
        timestamp TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        timestamp TEXT
    )""")
    conn.commit()
    conn.close()

def save_message(session_id, role, content, reasoning="", model="", mode="chat"):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO conversations VALUES (NULL,?,?,?,?,?,?,?)",
              (session_id, role, content, reasoning, model, mode, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history(session_id, limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content, reasoning, model, timestamp FROM conversations WHERE session_id=? ORDER BY id DESC LIMIT ?",
              (session_id, limit))
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))

def get_all_sessions():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT session_id, MAX(timestamp), COUNT(*) as cnt
                 FROM conversations GROUP BY session_id ORDER BY MAX(timestamp) DESC LIMIT 20""")
    rows = c.fetchall()
    conn.close()
    return rows

def get_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM conversations")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(DISTINCT session_id) FROM conversations")
    sessions = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM documents")
    docs = c.fetchone()[0]
    conn.close()
    return total, sessions, docs

def save_document(title, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO documents VALUES (NULL,?,?,?)",
              (title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_documents():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, title, content, timestamp FROM documents ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ── Session state ─────────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_reasoning" not in st.session_state:
    st.session_state.show_reasoning = False

# ── OpenRouter API ────────────────────────────────────────────────────────────
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

FREE_MODELS = {
    "Auto (Free Router)": "openrouter/free",
    "DeepSeek R1": "deepseek/deepseek-r1:free",
    "Gemini 2.0 Flash": "google/gemini-2.0-flash-exp:free",
    "Llama 3.3 70B": "meta-llama/llama-3.3-70b-instruct:free",
    "Qwen 2.5 72B": "qwen/qwen-2.5-72b-instruct:free",
    "Mistral 7B": "mistralai/mistral-7b-instruct:free",
}

def call_openrouter(api_key, messages, model="openrouter/free", reasoning=False, temperature=0.7, max_tokens=1000):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://nexusai.streamlit.app",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if reasoning:
        payload["reasoning"] = {"enabled": True}
    try:
        r = requests.post(OPENROUTER_URL, headers=headers, data=json.dumps(payload), timeout=60)
        r.raise_for_status()
        data = r.json()
        msg = data["choices"][0]["message"]
        content = msg.get("content") or ""
        reasoning_text = ""
        if reasoning:
            rd = msg.get("reasoning_details") or msg.get("reasoning") or ""
            if isinstance(rd, list):
                reasoning_text = " ".join([x.get("thinking", "") for x in rd if isinstance(x, dict)])
            elif isinstance(rd, str):
                reasoning_text = rd
        model_used = data.get("model", model)
        return content, reasoning_text, model_used
    except Exception as e:
        return f"Error: {str(e)}", "", model

# ── TTS (browser-based) ───────────────────────────────────────────────────────
def tts_html(text):
    safe = text.replace("'", "\\'").replace("\n", " ")[:500]
    return f"""
    <div style="margin-top:0.5rem;">
        <button onclick="speakText()" style="
            background:#12121e; border:1px solid #2a2a3a; border-radius:6px;
            color:#5b6af0; font-size:0.7rem; padding:0.3rem 0.75rem; cursor:pointer;
            font-family:'DM Mono',monospace; transition:all 0.15s;">
            Play audio
        </button>
        <button onclick="stopText()" style="
            background:#12121e; border:1px solid #2a2a3a; border-radius:6px;
            color:#6a4a6a; font-size:0.7rem; padding:0.3rem 0.75rem; cursor:pointer;
            font-family:'DM Mono',monospace; margin-left:0.5rem;">
            Stop
        </button>
    </div>
    <script>
    let utter;
    function speakText() {{
        window.speechSynthesis.cancel();
        utter = new SpeechSynthesisUtterance('{safe}');
        utter.lang = 'fr-FR';
        utter.rate = 0.95;
        window.speechSynthesis.speak(utter);
    }}
    function stopText() {{ window.speechSynthesis.cancel(); }}
    </script>
    """

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h1>Nexus<span>AI</span></h1>
        <p>OpenRouter · Free Tier</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section"><div class="nav-label">Navigation</div></div>', unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "Chat",
        "Reasoning",
        "RAG / Documents",
        "TTS / STT",
        "History",
        "Settings",
    ], label_visibility="collapsed")

    st.markdown("---")

    # ── API Key : .env en local, Secrets sur Streamlit Cloud ─────────────────
    st.markdown('<div class="nav-label" style="padding:0 0.5rem 0.5rem;">API Key</div>', unsafe_allow_html=True)
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY", "")
    except Exception:
        api_key = ""
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")

    if api_key:
        st.markdown('<div style="font-size:0.65rem; color:#5af078; padding:0 0.25rem;">Connected</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="font-size:0.65rem; color:#f05b5b; padding:0 0.25rem;">No key — check .env or Streamlit Secrets</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="nav-label" style="padding:0 0.5rem 0.5rem;">Model</div>', unsafe_allow_html=True)
    selected_model_name = st.selectbox("Model", list(FREE_MODELS.keys()), label_visibility="collapsed")
    selected_model = FREE_MODELS[selected_model_name]

    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max tokens", 256, 2000, 800, 64)

# ── Pages ─────────────────────────────────────────────────────────────────────

# ═══ CHAT ════════════════════════════════════════════════════════════════════
if page == "Chat":
    st.markdown("""
    <div class="page-header">
        <h2>Chat</h2>
        <p>Multi-turn conversation with memory and persistent history</p>
    </div>
    """, unsafe_allow_html=True)

    col_chat, col_info = st.columns([3, 1])

    with col_info:
        st.markdown('<div class="card"><div class="card-title">Session</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.7rem; color:#4a4a6a; margin-bottom:0.5rem;">ID: {st.session_state.session_id[:16]}...</div>', unsafe_allow_html=True)
        total, sessions, docs = get_stats()
        st.metric("Messages", total)
        st.metric("Sessions", sessions)
        if st.button("New session"):
            st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.messages = []
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_chat:
        history = get_history(st.session_state.session_id, 30)
        chat_html = '<div style="max-height:480px; overflow-y:auto; padding-right:0.5rem;">'
        if not history:
            chat_html += '<div style="text-align:center; padding:3rem; color:#2a2a3a; font-size:0.78rem;">Start a conversation below</div>'
        for role, content, reasoning, model, ts in history:
            is_user = role == "user"
            avatar_class = "user-av" if is_user else "ai"
            avatar_label = "You" if is_user else "AI"
            bubble_class = "user" if is_user else "ai"
            row_class = "user" if is_user else ""
            model_badge = f'<div class="model-badge">{model[:30] if model else ""}</div>' if not is_user and model else ""
            content_safe = content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
            reasoning_block = ""
            if reasoning and not is_user:
                reasoning_safe = reasoning[:300].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
                reasoning_block = '<div class="reasoning-box"><div class="label">Reasoning trace</div>' + reasoning_safe + '...</div>'
            align = 'text-align:right;' if is_user else ''
            chat_html += '<div class="msg-row ' + row_class + '">'
            chat_html += '<div class="msg-avatar ' + avatar_class + '">' + avatar_label + '</div>'
            chat_html += '<div>' + model_badge
            chat_html += '<div class="msg-bubble ' + bubble_class + '">' + content_safe + '</div>'
            chat_html += reasoning_block
            chat_html += '<div style="font-size:0.6rem; color:#2a2a3a; margin-top:0.2rem; ' + align + '">' + ts[11:16] + '</div>'
            chat_html += '</div></div>'
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        st.markdown("---")
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area("Message", placeholder="Type your message...", height=80, label_visibility="collapsed")
            col_send, col_clear = st.columns([5, 1])
            with col_send:
                submitted = st.form_submit_button("Send", use_container_width=True)
            with col_clear:
                cleared = st.form_submit_button("Clear")

        if cleared:
            st.session_state.messages = []
            st.rerun()

        if submitted and user_input.strip():
            if not api_key:
                st.error("No API key found. Add OPENROUTER_API_KEY to your .env file.")
            else:
                save_message(st.session_state.session_id, "user", user_input, model=selected_model)
                hist = get_history(st.session_state.session_id, 20)
                api_messages = [{"role": r, "content": c} for r, c, _, _, _ in hist]
                with st.spinner("Generating..."):
                    reply, reasoning_text, model_used = call_openrouter(
                        api_key, api_messages, selected_model, False, temperature, max_tokens
                    )
                save_message(st.session_state.session_id, "assistant", reply, reasoning_text, model_used)
                st.rerun()

# ═══ REASONING ═══════════════════════════════════════════════════════════════
elif page == "Reasoning":
    st.markdown("""
    <div class="page-header">
        <h2>Reasoning Mode</h2>
        <p>Extended thinking — model shows its reasoning chain before answering</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Reasoning prompt</div>', unsafe_allow_html=True)
    reasoning_prompt = st.text_area("Prompt", placeholder="Ask something complex: math, logic, analysis...", height=100, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        follow_up = st.text_input("Follow-up (optional)", placeholder="Are you sure? Think again...")
    with col2:
        run_btn = st.button("Run reasoning", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if run_btn and reasoning_prompt.strip():
        if not api_key:
            st.error("No API key found. Add OPENROUTER_API_KEY to your .env file.")
        else:
            messages_r = [{"role": "user", "content": reasoning_prompt}]
            with st.spinner("Reasoning..."):
                reply1, reasoning1, model1 = call_openrouter(api_key, messages_r, selected_model, True, temperature, max_tokens)

            save_message(st.session_state.session_id, "user", reasoning_prompt, model=selected_model, mode="reasoning")
            save_message(st.session_state.session_id, "assistant", reply1, reasoning1, model1, mode="reasoning")

            st.markdown('<div class="card"><div class="card-title">First response</div>', unsafe_allow_html=True)
            if reasoning1:
                with st.expander("Reasoning trace", expanded=True):
                    st.markdown(f'<div style="font-size:0.78rem; color:#6a6a8a; line-height:1.7;">{reasoning1}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="msg-bubble ai" style="max-width:100%;">{reply1}</div>', unsafe_allow_html=True)
            st.markdown(tts_html(reply1), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            if follow_up.strip():
                messages_r2 = [
                    {"role": "user", "content": reasoning_prompt},
                    {"role": "assistant", "content": reply1, "reasoning_details": reasoning1},
                    {"role": "user", "content": follow_up},
                ]
                with st.spinner("Continuing reasoning..."):
                    reply2, reasoning2, model2 = call_openrouter(api_key, messages_r2, selected_model, True, temperature, max_tokens)

                save_message(st.session_state.session_id, "user", follow_up, model=selected_model, mode="reasoning")
                save_message(st.session_state.session_id, "assistant", reply2, reasoning2, model2, mode="reasoning")

                st.markdown('<div class="card"><div class="card-title">Follow-up response</div>', unsafe_allow_html=True)
                if reasoning2:
                    with st.expander("Reasoning trace", expanded=False):
                        st.markdown(f'<div style="font-size:0.78rem; color:#6a6a8a; line-height:1.7;">{reasoning2}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="msg-bubble ai" style="max-width:100%;">{reply2}</div>', unsafe_allow_html=True)
                st.markdown(tts_html(reply2), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

# ═══ RAG / DOCUMENTS ══════════════════════════════════════════════════════════
elif page == "RAG / Documents":
    st.markdown("""
    <div class="page-header">
        <h2>RAG / Documents</h2>
        <p>Upload documents and query them — retrieval-augmented generation</p>
    </div>
    """, unsafe_allow_html=True)

    col_upload, col_query = st.columns([1, 1])

    with col_upload:
        st.markdown('<div class="card"><div class="card-title">Document store</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload a .txt file", type=["txt"], label_visibility="collapsed")
        if uploaded:
            content = uploaded.read().decode("utf-8", errors="ignore")
            save_document(uploaded.name, content)
            st.success(f"Saved: {uploaded.name}")

        docs = get_documents()
        if docs:
            for doc_id, title, content, ts in docs:
                with st.expander(f"{title} — {ts[:10]}"):
                    st.markdown(f'<div style="font-size:0.75rem; color:#6a6a8a; max-height:120px; overflow:auto;">{content[:600]}...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="font-size:0.75rem; color:#2a2a3a; padding:1rem 0;">No documents yet. Upload a .txt file.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_query:
        st.markdown('<div class="card"><div class="card-title">Query documents</div>', unsafe_allow_html=True)
        rag_question = st.text_area("Question", placeholder="Ask a question about your documents...", height=80, label_visibility="collapsed")
        rag_btn = st.button("Query", use_container_width=True)

        if rag_btn and rag_question.strip():
            if not api_key:
                st.error("No API key found. Add OPENROUTER_API_KEY to your .env file.")
            elif not docs:
                st.warning("No documents uploaded yet.")
            else:
                context = "\n\n---\n\n".join([f"[{t}]\n{c[:1500]}" for _, t, c, _ in docs])
                rag_prompt = f"""You are a precise document assistant. Answer based ONLY on the provided documents.

DOCUMENTS:
{context[:3000]}

QUESTION: {rag_question}

Answer concisely and cite which document supports your answer."""
                messages_rag = [{"role": "user", "content": rag_prompt}]
                with st.spinner("Searching documents..."):
                    rag_reply, _, rag_model = call_openrouter(api_key, messages_rag, selected_model, False, 0.3, max_tokens)

                save_message(st.session_state.session_id, "user", rag_question, model=selected_model, mode="rag")
                save_message(st.session_state.session_id, "assistant", rag_reply, "", rag_model, mode="rag")

                st.markdown(f'<div class="model-badge">{rag_model[:40]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="msg-bubble ai" style="max-width:100%; margin-top:0.5rem;">{rag_reply}</div>', unsafe_allow_html=True)
                st.markdown(tts_html(rag_reply), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══ TTS / STT ════════════════════════════════════════════════════════════════
elif page == "TTS / STT":
    st.markdown("""
    <div class="page-header">
        <h2>TTS / STT</h2>
        <p>Text-to-speech and speech-to-text using the Web Speech API — no extra cost</p>
    </div>
    """, unsafe_allow_html=True)

    col_tts, col_stt = st.columns(2)

    with col_tts:
        st.markdown('<div class="card"><div class="card-title">Text to Speech</div>', unsafe_allow_html=True)
        tts_text = st.text_area("Text to speak", placeholder="Enter text to speak aloud...", height=120, label_visibility="collapsed")
        lang_tts = st.selectbox("Language", ["fr-FR", "en-US", "ar-SA", "es-ES", "de-DE"], label_visibility="collapsed")
        if tts_text:
            safe = tts_text.replace("'", "\\'").replace("\n", " ")[:800]
            st.markdown(f"""
            <button onclick="(function(){{
                window.speechSynthesis.cancel();
                let u = new SpeechSynthesisUtterance('{safe}');
                u.lang = '{lang_tts}'; u.rate = 0.95;
                window.speechSynthesis.speak(u);
            }})()" style="
                background:#5b6af0; border:none; border-radius:8px; color:#fff;
                font-size:0.78rem; padding:0.5rem 1.25rem; cursor:pointer;
                font-family:'DM Mono',monospace; margin-top:0.5rem;">
                Speak
            </button>
            <button onclick="window.speechSynthesis.cancel()" style="
                background:#12121e; border:1px solid #2a2a3a; border-radius:8px; color:#9a6a9a;
                font-size:0.78rem; padding:0.5rem 1.25rem; cursor:pointer;
                font-family:'DM Mono',monospace; margin-left:0.5rem;">
                Stop
            </button>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card" style="margin-top:1rem;"><div class="card-title">Voice + AI</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.75rem; color:#4a4a6a; margin-bottom:0.75rem;">Type a prompt and hear the AI speak back.</div>', unsafe_allow_html=True)
        voice_prompt = st.text_input("Voice prompt", placeholder="Ask anything...", label_visibility="collapsed", key="voice_q")
        voice_btn = st.button("Ask and speak", use_container_width=True)
        if voice_btn and voice_prompt and api_key:
            with st.spinner("..."):
                v_reply, _, _ = call_openrouter(api_key, [{"role": "user", "content": voice_prompt}], selected_model, False, temperature, 400)
            st.markdown(f'<div class="msg-bubble ai" style="max-width:100%; margin-bottom:0.5rem;">{v_reply}</div>', unsafe_allow_html=True)
            st.markdown(tts_html(v_reply), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_stt:
        st.markdown('<div class="card"><div class="card-title">Speech to Text</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.75rem; color:#4a4a6a; margin-bottom:0.75rem;">Uses your browser microphone. Chrome recommended.</div>', unsafe_allow_html=True)
        stt_lang = st.selectbox("STT Language", ["fr-FR", "en-US", "ar-SA", "es-ES"], label_visibility="collapsed", key="stt_lang")
        st.markdown(f"""
        <div style="margin-bottom:0.75rem;">
            <button onclick="startRec2()" id="recBtn2" style="
                background:#12121e; border:1px solid #2a2a3a; border-radius:6px;
                color:#5af078; font-size:0.72rem; padding:0.4rem 1rem; cursor:pointer;
                font-family:'DM Mono',monospace;">
                Start recording
            </button>
            <button onclick="stopRec2()" style="
                background:#12121e; border:1px solid #2a2a3a; border-radius:6px;
                color:#f05b5b; font-size:0.72rem; padding:0.4rem 1rem; cursor:pointer;
                font-family:'DM Mono',monospace; margin-left:0.5rem;">
                Stop
            </button>
            <span id="recStatus2" style="font-size:0.65rem; color:#3a3a5a; margin-left:0.75rem;"></span>
        </div>
        <div id="transcript2" style="
            background:#0c0c16; border:1px solid #1e1e2e; border-radius:6px;
            padding:0.75rem 1rem; font-size:0.8rem; color:#8080a0;
            min-height:5rem; font-family:'DM Mono',monospace; line-height:1.6;"></div>
        <script>
        let rec2;
        function startRec2() {{
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {{
                document.getElementById('recStatus2').innerText = 'Not supported.'; return;
            }}
            rec2 = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            rec2.lang = '{stt_lang}';
            rec2.interimResults = true;
            rec2.continuous = true;
            document.getElementById('recStatus2').innerText = 'Listening...';
            rec2.onresult = (e) => {{
                let t = '';
                for (let i = 0; i < e.results.length; i++) t += e.results[i][0].transcript + ' ';
                document.getElementById('transcript2').innerText = t;
            }};
            rec2.onend = () => document.getElementById('recStatus2').innerText = 'Stopped.';
            rec2.start();
        }}
        function stopRec2() {{ if (rec2) rec2.stop(); }}
        </script>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ═══ HISTORY ══════════════════════════════════════════════════════════════════
elif page == "History":
    st.markdown("""
    <div class="page-header">
        <h2>History</h2>
        <p>All conversations stored in local SQLite database</p>
    </div>
    """, unsafe_allow_html=True)

    total, sessions, docs = get_stats()
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Total messages", total)
    with c2: st.metric("Sessions", sessions)
    with c3: st.metric("Documents", docs)

    st.markdown("---")
    all_sessions = get_all_sessions()

    if not all_sessions:
        st.markdown('<div style="color:#2a2a3a; font-size:0.8rem; padding:2rem 0;">No history yet.</div>', unsafe_allow_html=True)
    else:
        for sess_id, last_ts, cnt in all_sessions:
            with st.expander(f"Session {sess_id} — {cnt} messages — {last_ts[:16]}"):
                hist = get_history(sess_id, 20)
                for role, content, reasoning, model, ts in hist:
                    color = "#a8c8e8" if role == "user" else "#c8c8e0"
                    st.markdown(f"""
                    <div class="history-item">
                        <div class="hi-role">{role} {('· ' + model[:30]) if model else ''}</div>
                        <div class="hi-text" style="color:{color};">{content[:200]}</div>
                        <div class="hi-time">{ts[:16]}</div>
                    </div>
                    """, unsafe_allow_html=True)

# ═══ SETTINGS ════════════════════════════════════════════════════════════════
elif page == "Settings":
    st.markdown("""
    <div class="page-header">
        <h2>Settings</h2>
        <p>Model information and configuration</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">Available free models</div>', unsafe_allow_html=True)
    for name, model_id in FREE_MODELS.items():
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:0.6rem 0; border-bottom:1px solid #13131e;">
            <div style="font-size:0.8rem; color:#c8c8e0;">{name}</div>
            <div class="model-badge">{model_id}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:1rem;"><div class="card-title">Capabilities by mode</div>', unsafe_allow_html=True)
    caps = {
        "Chat": "Multi-turn, memory, history, TTS output",
        "Reasoning": "Extended thinking chain, follow-up continuation",
        "RAG / Documents": "Upload .txt, context injection, source citation",
        "TTS / STT": "Browser Web Speech API — no API cost",
    }
    for mode, desc in caps.items():
        st.markdown(f"""
        <div style="padding:0.6rem 0; border-bottom:1px solid #13131e;">
            <div style="font-size:0.75rem; color:#5b6af0; margin-bottom:0.2rem;">{mode}</div>
            <div style="font-size:0.75rem; color:#6a6a8a;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card" style="margin-top:1rem;"><div class="card-title">Database management</div>', unsafe_allow_html=True)
    if st.button("Clear all conversation history"):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM conversations")
        conn.commit()
        conn.close()
        st.success("History cleared.")
    if st.button("Clear all documents"):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM documents")
        conn.commit()
        conn.close()
        st.success("Documents cleared.")
    st.markdown("</div>", unsafe_allow_html=True)