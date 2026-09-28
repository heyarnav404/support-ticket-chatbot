from copy import deepcopy
from pathlib import Path
from uuid import uuid4

import streamlit as st

from components import (
    render_chat_input,
    render_chat_window,
    render_loading_indicator,
    render_message_bubble,
    render_sidebar,
)
from support_engine import (
    create_gemini_client,
    create_ticket_index,
    fallback_answer,
    generate_answer,
    load_support_tickets,
    search_tickets,
)
from ui_styles import inject_styles


PROJECT_DIR = Path(__file__).resolve().parent
TICKET_PATH = PROJECT_DIR / "tickets.csv"


st.set_page_config(
    page_title="Support Ticket AI",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()


@st.cache_data(show_spinner=False)
def get_tickets(ticket_path, modified_at):
    return load_support_tickets(ticket_path)


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "conversations" not in st.session_state:
        st.session_state.conversations = []

    if "active_conversation_id" not in st.session_state:
        st.session_state.active_conversation_id = str(uuid4())


def upsert_active_conversation():
    if not st.session_state.messages:
        return

    active_id = st.session_state.active_conversation_id
    conversation = {
        "id": active_id,
        "title": make_conversation_title(st.session_state.messages),
        "messages": deepcopy(st.session_state.messages),
    }

    for index, saved_conversation in enumerate(st.session_state.conversations):
        if saved_conversation["id"] == active_id:
            st.session_state.conversations[index] = conversation
            return

    st.session_state.conversations.insert(0, conversation)


def make_conversation_title(messages):
    for message in messages:
        if message.get("role") == "user":
            content = " ".join(message.get("content", "").split())
            return content[:48] if len(content) <= 48 else f"{content[:45]}..."

    return "Untitled conversation"


def start_new_chat():
    upsert_active_conversation()
    st.session_state.active_conversation_id = str(uuid4())
    st.session_state.messages = []


def load_conversation(conversation_id):
    upsert_active_conversation()

    for conversation in st.session_state.conversations:
        if conversation["id"] == conversation_id:
            st.session_state.active_conversation_id = conversation_id
            st.session_state.messages = deepcopy(conversation["messages"])
            return


def tickets_to_records(results):
    records = []

    for _, ticket in results.iterrows():
        records.append(
            {
                "ticket_id": ticket.get("ticket_id", ""),
                "issue": ticket.get("issue", ""),
                "description": ticket.get("description", ""),
                "solution": ticket.get("solution", ""),
                "similarity": float(ticket.get("similarity", 0)),
            }
        )

    return records


def get_gemini_client():
    return create_gemini_client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )


initialize_session_state()

tickets = get_tickets(str(TICKET_PATH), TICKET_PATH.stat().st_mtime)
vectorizer, ticket_vectors = create_ticket_index(tickets)

sidebar_state = render_sidebar(
    conversations=st.session_state.conversations,
    active_conversation_id=st.session_state.active_conversation_id,
)

if sidebar_state["new_chat_clicked"]:
    start_new_chat()
    st.rerun()

if sidebar_state["selected_conversation_id"]:
    load_conversation(sidebar_state["selected_conversation_id"])
    st.rerun()

question = render_chat_input()

if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

render_chat_window(
    messages=st.session_state.messages,
    ticket_count=len(tickets),
)

if question:
    loading_placeholder = st.empty()

    try:
        render_loading_indicator(
            "Searching support tickets...",
            placeholder=loading_placeholder,
        )

        results = search_tickets(
            question=question,
            messages=st.session_state.messages,
            tickets=tickets,
            vectorizer=vectorizer,
            ticket_vectors=ticket_vectors,
            top_k=sidebar_state["top_k"],
            threshold=sidebar_state["threshold"],
        )

        ticket_records = tickets_to_records(results)

        render_loading_indicator(
            "Generating response...",
            placeholder=loading_placeholder,
        )

        try:
            answer = generate_answer(
                question=question,
                results=results,
                messages=st.session_state.messages,
                client=get_gemini_client(),
                model=st.secrets.get("GEMINI_MODEL", "gemini-3.7-flash"),
            )
        except Exception as generation_error:
            answer = (
                "Gemini was unavailable, so here is the closest answer from your "
                "support ticket history.\n\n"
                f"{fallback_answer(results)}"
            )
            st.warning(f"AI response unavailable: {generation_error}")

    except Exception as error:
        loading_placeholder.empty()
        st.error("The backend could not generate a response.")
        st.caption(str(error))
        upsert_active_conversation()
        st.stop()

    loading_placeholder.empty()

    assistant_message = {
        "role": "assistant",
        "content": answer,
        "tickets": ticket_records,
    }

    st.session_state.messages.append(assistant_message)
    render_message_bubble(assistant_message)
    upsert_active_conversation()
