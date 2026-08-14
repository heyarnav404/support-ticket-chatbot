import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from google import genai

# Page setup

st.set_page_config(
    page_title="Support Ticket AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Support Ticket AI Assistant")
st.write(
    "Ask about a technical problem and the AI will "
    "use previous support tickets to help answer it."
)

# Gemini

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# Load support tickets

tickets = pd.read_csv("tickets.csv")

tickets["search_text"] = (
    tickets["issue"] + " " +
    tickets["description"]
)

# Create TF-IDF vectors

vectorizer = TfidfVectorizer()

ticket_vectors = vectorizer.fit_transform(
    tickets["search_text"]
)


# Search similar tickets

def search_tickets(question, top_k=3):

    question_vector = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        question_vector,
        ticket_vectors
    ).flatten()

    top_indices = similarities.argsort()[
        -top_k:
    ][::-1]

    return tickets.iloc[top_indices]

 
# Generate AI answer

def generate_answer(question, results):

    context = ""

    for _, ticket in results.iterrows():

        context += f"""
Ticket #{ticket['ticket_id']}
Issue: {ticket['issue']}
Problem: {ticket['description']}
Previous Solution: {ticket['solution']}
---
"""

    prompt = f"""
You are a helpful technical support assistant.

Answer the user's question using the previous
support tickets provided below.

Only use the information from the tickets.
Do not invent solutions.

If the tickets do not contain enough information,
say that clearly.

Previous support tickets:
{context}

User question:
{question}

Give a short, clear and helpful answer.
"""

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )

    return response.text


# Chat interface

question = st.text_input(
    "💬 Describe your problem:"
)

if st.button("🤖 Ask AI"):

    if question.strip():

        with st.spinner("Searching previous tickets..."):

            results = search_tickets(question)

        with st.spinner("Generating AI response..."):

            answer = generate_answer(
                question,
                results
            )

        st.subheader("🤖 AI Response")

        st.success(answer)

        # Show retrieved tickets
        with st.expander(
            "🔎 View retrieved support tickets"
        ):

            for _, ticket in results.iterrows():

                st.write(
                    f"### Ticket #{ticket['ticket_id']}"
                )

                st.write(
                    f"**Issue:** {ticket['issue']}"
                )

                st.write(
                    f"**Problem:** {ticket['description']}"
                )

                st.write(
                    f"**Previous Solution:** "
                    f"{ticket['solution']}"
                )

                st.divider()

    else:

        st.warning(
            "Please describe your problem first."
        )