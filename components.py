from html import escape

import streamlit as st


def render_sidebar(conversations, active_conversation_id, default_top_k=3, default_threshold=0.2):
    st.sidebar.markdown(
        """
        <div class="app-logo">
            <div class="app-logo-mark">ST</div>
            <div>
                <p class="app-logo-title">Support Ticket AI</p>
                <div class="app-logo-subtitle">Support intelligence console</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    new_chat_clicked = st.sidebar.button(
        "New Chat",
        key="new_chat_button",
        use_container_width=True,
    )

    st.sidebar.markdown(
        '<div class="sidebar-label">Previous conversations</div>',
        unsafe_allow_html=True,
    )

    selected_conversation_id = None

    if conversations:
        for conversation in conversations:
            title = conversation.get("title") or "Untitled conversation"
            label = title if len(title) <= 38 else f"{title[:35]}..."
            is_active = conversation.get("id") == active_conversation_id

            if st.sidebar.button(
                label,
                key=f"conversation_{conversation.get('id')}",
                use_container_width=True,
                disabled=is_active,
            ):
                selected_conversation_id = conversation.get("id")
    else:
        st.sidebar.markdown(
            '<div class="conversation-empty">No saved conversations yet.</div>',
            unsafe_allow_html=True,
        )

    st.sidebar.markdown(
        '<div class="sidebar-label">Settings</div>',
        unsafe_allow_html=True,
    )

    top_k = st.sidebar.slider(
        "Retrieved tickets",
        min_value=1,
        max_value=5,
        value=default_top_k,
        step=1,
    )

    threshold = st.sidebar.slider(
        "Similarity threshold",
        min_value=0.0,
        max_value=1.0,
        value=default_threshold,
        step=0.05,
    )

    st.sidebar.markdown(
        '<div class="sidebar-caption">Gemini response generation with ticket retrieval.</div>',
        unsafe_allow_html=True,
    )

    return {
        "new_chat_clicked": new_chat_clicked,
        "selected_conversation_id": selected_conversation_id,
        "top_k": top_k,
        "threshold": threshold,
    }


def render_empty_state(ticket_count):
    st.markdown(
        f"""
        <section class="empty-state">
            <div class="empty-state-inner">
                <div class="eyebrow">Support Ticket AI</div>
                <h1>Ready to troubleshoot.</h1>
                <p>Bring a customer issue into focus with answers grounded in your existing support history.</p>
                <div class="stat-grid">
                    <div class="stat-tile">
                        <div class="stat-value">{ticket_count}</div>
                        <div class="stat-label">Tickets indexed</div>
                    </div>
                    <div class="stat-tile">
                        <div class="stat-value">TF-IDF</div>
                        <div class="stat-label">Retrieval layer</div>
                    </div>
                    <div class="stat-tile">
                        <div class="stat-value">Gemini</div>
                        <div class="stat-label">Answer engine</div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_message_bubble(message):
    role = message.get("role", "assistant")

    # Let Streamlit provide the role avatar; plain text is interpreted as an image path.
    with st.chat_message(role):
        st.markdown(message.get("content", ""))

        tickets = message.get("tickets")
        if role == "assistant" and tickets is not None:
            render_retrieved_tickets(tickets)


def render_chat_window(messages, ticket_count):
    if not messages:
        render_empty_state(ticket_count)
        return

    for message in messages:
        render_message_bubble(message)


def render_chat_input():
    return st.chat_input("Describe your technical problem...")


def render_loading_indicator(label, placeholder=None):
    safe_label = escape(label)
    markup = f"""
    <div class="loading-card" role="status" aria-live="polite">
        <span class="loading-dot"></span>
        <span>{safe_label}</span>
    </div>
    """

    if placeholder is None:
        st.markdown(markup, unsafe_allow_html=True)
        return

    placeholder.markdown(markup, unsafe_allow_html=True)


def render_retrieved_tickets(tickets):
    st.markdown(
        """
        <div class="ticket-summary">
            <div class="ticket-field-label">Retrieved support tickets</div>
            <div class="meta-text">Expand a match to inspect the source ticket used for this answer.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not tickets:
        st.caption("No relevant support tickets found.")
        return

    for ticket in tickets:
        score = _format_similarity(ticket.get("similarity", 0))
        ticket_id = escape(str(ticket.get("ticket_id", "Unknown")))
        issue = escape(str(ticket.get("issue", "Untitled issue")))

        with st.expander(f"Ticket #{ticket_id} | {issue} | Similarity {score}", expanded=False):
            render_ticket_card(ticket)


def render_ticket_card(ticket):
    ticket_id = escape(str(ticket.get("ticket_id", "Unknown")))
    issue = escape(str(ticket.get("issue", "")))
    problem = escape(str(ticket.get("description", "")))
    solution = escape(str(ticket.get("solution", "")))
    score = _format_similarity(ticket.get("similarity", 0))

    st.markdown(
        f"""
        <article class="ticket-card">
            <div class="ticket-card-header">
                <span class="ticket-id">Ticket #{ticket_id}</span>
                <span class="score-pill">Similarity {score}</span>
            </div>
            <div class="ticket-field">
                <div class="ticket-field-label">Issue</div>
                <div class="ticket-field-body">{issue}</div>
            </div>
            <div class="ticket-field">
                <div class="ticket-field-label">Problem</div>
                <div class="ticket-field-body">{problem}</div>
            </div>
            <div class="ticket-field">
                <div class="ticket-field-label">Previous Solution</div>
                <div class="ticket-field-body">{solution}</div>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def _format_similarity(value):
    try:
        return f"{float(value):.2f}"
    except (TypeError, ValueError):
        return "0.00"
