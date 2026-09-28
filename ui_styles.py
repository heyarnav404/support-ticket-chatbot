import streamlit as st


APP_CSS = """
<style>
:root {
    --bg: #080b12;
    --surface: #0d111c;
    --surface-soft: #121827;
    --surface-raised: #161d2e;
    --border: rgba(148, 163, 184, 0.18);
    --border-strong: rgba(148, 163, 184, 0.34);
    --text: #edf2ff;
    --muted: #94a3b8;
    --muted-strong: #c7d2fe;
    --accent: #5eead4;
    --accent-2: #60a5fa;
    --warning: #facc15;
    --shadow: 0 18px 54px rgba(0, 0, 0, 0.38);
    --radius: 8px;
}

html,
body,
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at top left, rgba(94, 234, 212, 0.10), transparent 28rem),
        linear-gradient(145deg, #080b12 0%, #0c1020 48%, #090d16 100%);
    color: var(--text);
}

.stApp {
    background: transparent;
}

header[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1120px;
    padding: 2rem 2.25rem 7.5rem;
}

section[data-testid="stSidebar"] {
    background: rgba(8, 11, 18, 0.94);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    min-height: 2.65rem;
    border-radius: var(--radius);
    border: 1px solid var(--border);
    background: rgba(18, 24, 39, 0.82);
    color: var(--text);
    font-weight: 650;
    transition: transform 160ms ease, border-color 160ms ease, background 160ms ease;
}

[data-testid="stSidebar"] .stButton > button:hover {
    border-color: rgba(94, 234, 212, 0.55);
    background: rgba(20, 31, 48, 0.95);
    transform: translateY(-1px);
}

.stButton > button {
    border-radius: var(--radius);
}

.app-logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.1rem 0 1.1rem;
}

.app-logo-mark {
    display: grid;
    width: 2.45rem;
    height: 2.45rem;
    place-items: center;
    border: 1px solid rgba(94, 234, 212, 0.42);
    border-radius: var(--radius);
    background: linear-gradient(145deg, rgba(94, 234, 212, 0.18), rgba(96, 165, 250, 0.16));
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.42);
    color: var(--accent);
    font-weight: 800;
}

.app-logo-title {
    margin: 0;
    color: var(--text);
    font-size: 1.02rem;
    font-weight: 760;
    letter-spacing: 0;
}

.app-logo-subtitle,
.sidebar-caption,
.meta-text {
    color: var(--muted);
    font-size: 0.78rem;
}

.sidebar-label {
    margin: 1.25rem 0 0.55rem;
    color: #cbd5e1;
    font-size: 0.74rem;
    font-weight: 780;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.conversation-empty {
    padding: 0.9rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--muted);
    background: rgba(15, 23, 42, 0.45);
    font-size: 0.86rem;
}

.chat-shell {
    min-height: calc(100vh - 10rem);
}

.empty-state {
    display: grid;
    min-height: calc(100vh - 15rem);
    place-items: center;
    animation: rise-in 320ms ease both;
}

.empty-state-inner {
    width: min(680px, 100%);
    padding: 2.2rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: linear-gradient(160deg, rgba(22, 29, 46, 0.86), rgba(13, 17, 28, 0.70));
    box-shadow: var(--shadow);
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.9rem;
    color: var(--accent);
    font-size: 0.8rem;
    font-weight: 760;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.empty-state h1 {
    margin: 0;
    color: var(--text);
    font-size: clamp(2rem, 4vw, 3.45rem);
    line-height: 1.02;
    letter-spacing: 0;
}

.empty-state p {
    max-width: 46rem;
    margin: 1rem 0 0;
    color: var(--muted);
    font-size: 1.03rem;
    line-height: 1.65;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1.35rem;
}

.stat-tile {
    min-height: 5.4rem;
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: rgba(8, 13, 23, 0.62);
}

.stat-value {
    color: var(--text);
    font-size: 1.22rem;
    font-weight: 780;
}

.stat-label {
    margin-top: 0.35rem;
    color: var(--muted);
    font-size: 0.8rem;
}

[data-testid="stChatMessage"] {
    gap: 0.75rem;
    padding: 0.92rem 0;
    animation: message-in 220ms ease both;
}

[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(145deg, rgba(94, 234, 212, 0.20), rgba(96, 165, 250, 0.18));
    color: var(--accent);
}

[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    background: rgba(96, 165, 250, 0.16);
    color: #bfdbfe;
}

[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] {
    line-height: 1.65;
}

[data-testid="stChatMessage"] pre {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: #070a11;
}

[data-testid="stChatMessage"] code {
    font-size: 0.9rem;
}

.ticket-summary {
    margin-top: 0.85rem;
    padding: 0.95rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: rgba(8, 13, 23, 0.68);
}

.ticket-card {
    padding: 0.95rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: rgba(12, 18, 30, 0.74);
}

.ticket-card + .ticket-card {
    margin-top: 0.75rem;
}

.ticket-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}

.ticket-id {
    color: var(--accent);
    font-size: 0.82rem;
    font-weight: 780;
}

.score-pill {
    flex: 0 0 auto;
    border: 1px solid rgba(94, 234, 212, 0.32);
    border-radius: 999px;
    padding: 0.25rem 0.55rem;
    color: var(--accent);
    background: rgba(94, 234, 212, 0.08);
    font-size: 0.78rem;
    font-weight: 760;
}

.ticket-field {
    margin-top: 0.7rem;
}

.ticket-field-label {
    color: #cbd5e1;
    font-size: 0.74rem;
    font-weight: 760;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.ticket-field-body {
    margin-top: 0.18rem;
    color: #e5e7eb;
    font-size: 0.91rem;
    line-height: 1.55;
}

.loading-card {
    display: inline-flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.75rem 0;
    padding: 0.75rem 0.95rem;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: rgba(15, 23, 42, 0.78);
    color: var(--muted-strong);
    box-shadow: 0 12px 34px rgba(0, 0, 0, 0.20);
}

.loading-dot {
    width: 0.58rem;
    height: 0.58rem;
    border-radius: 999px;
    background: var(--accent);
    box-shadow: 0 0 0 0 rgba(94, 234, 212, 0.42);
    animation: pulse 1.15s ease-in-out infinite;
}

.stChatFloatingInputContainer {
    padding-bottom: 1.35rem;
    background: linear-gradient(180deg, transparent, rgba(8, 11, 18, 0.92) 32%);
}

[data-testid="stChatInput"] {
    border-radius: 18px;
    border: 1px solid var(--border-strong);
    background: rgba(12, 18, 30, 0.96);
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.35);
}

[data-testid="stChatInput"] textarea {
    min-height: 3.25rem;
    color: var(--text);
}

[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    background: rgba(12, 18, 30, 0.58);
}

[data-testid="stExpander"] details summary {
    font-weight: 700;
}

@keyframes message-in {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes rise-in {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% {
        transform: scale(0.92);
        box-shadow: 0 0 0 0 rgba(94, 234, 212, 0.42);
    }
    70% {
        transform: scale(1);
        box-shadow: 0 0 0 10px rgba(94, 234, 212, 0);
    }
    100% {
        transform: scale(0.92);
        box-shadow: 0 0 0 0 rgba(94, 234, 212, 0);
    }
}

@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.35rem 1rem 7rem;
    }

    .empty-state {
        min-height: calc(100vh - 13rem);
        place-items: start;
        padding-top: 1rem;
    }

    .empty-state-inner {
        padding: 1.25rem;
    }

    .stat-grid {
        grid-template-columns: 1fr;
    }

    .ticket-card-header {
        align-items: flex-start;
        flex-direction: column;
    }
}

@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] {
        padding-left: 0.75rem;
        padding-right: 0.75rem;
    }

    .empty-state h1 {
        font-size: 2rem;
    }

    .empty-state p {
        font-size: 0.95rem;
    }
}
</style>
"""


def inject_styles():
    st.markdown(APP_CSS, unsafe_allow_html=True)
