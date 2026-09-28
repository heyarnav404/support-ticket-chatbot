import pandas as pd
from google import genai
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_GEMINI_MODEL = "gemini-3.7-flash"


def create_gemini_client(api_key):
    return genai.Client(api_key=api_key)


def load_support_tickets(ticket_path):
    tickets = pd.read_csv(ticket_path)

    for column in ("ticket_id", "issue", "description", "solution"):
        if column not in tickets:
            tickets[column] = ""

    tickets["search_text"] = (
        tickets["issue"].fillna("").astype(str) + " " +
        tickets["description"].fillna("").astype(str)
    ).str.strip()

    return tickets


def create_ticket_index(tickets):
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
        strip_accents="unicode",
    )

    ticket_vectors = vectorizer.fit_transform(
        tickets["search_text"]
    )

    return vectorizer, ticket_vectors


def search_tickets(
    question,
    messages,
    tickets,
    vectorizer,
    ticket_vectors,
    top_k=3,
    threshold=0.2
):
    conversation_context = " ".join(
        message.get("content", "")
        for message in messages[-7:-1]
        if message.get("role") == "user"
    )
    search_query = f"{conversation_context} {question}".strip()

    question_vector = vectorizer.transform(
        [search_query]
    )

    similarities = cosine_similarity(
        question_vector,
        ticket_vectors
    ).flatten()

    tickets_with_scores = tickets.copy()

    tickets_with_scores["similarity"] = similarities

    relevant_tickets = tickets_with_scores[
        tickets_with_scores["similarity"] >= threshold
    ]

    relevant_tickets = relevant_tickets.sort_values(
        by="similarity",
        ascending=False
    )

    if not relevant_tickets.empty:
        return relevant_tickets.head(top_k)

    # Always show the closest source ticket so a paraphrased question does not
    # look as though the ticket database was ignored.
    return tickets_with_scores.nlargest(top_k, "similarity")


def generate_answer(
    question,
    results,
    messages,
    client,
    model=DEFAULT_GEMINI_MODEL,
):
    conversation = ""

    for message in messages[:-1]:
        conversation += f"""
{message['role']}: {message['content']}
"""

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

Conversation history:
{conversation}

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
        model=model,
        contents=prompt
    )

    return (response.text or "").strip()


def fallback_answer(results):
    """Return a useful answer when the external model is unavailable."""
    if results.empty:
        return "I could not find a matching support ticket. Please provide more detail about the problem."

    ticket = results.iloc[0]
    return (
        f"I found a similar support ticket (#{ticket['ticket_id']}). "
        f"Recommended solution: {ticket['solution']}"
    )
