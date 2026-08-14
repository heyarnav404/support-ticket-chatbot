# 🤖 Support Ticket AI Assistant

An AI-powered support ticket chatbot built with **Python, Streamlit, Scikit-learn, and Google Gemini**.

The application retrieves relevant historical support tickets using **TF-IDF vectorization and cosine similarity**, then provides the retrieved information to a Gemini LLM to generate a clear support response.

> **Note:** This is a portfolio/learning project demonstrating a RAG-style retrieval and generation workflow using a small support-ticket dataset.

---

## 🎯 Project Overview

Support teams often receive questions that are similar to problems they have already solved.

This project demonstrates how an AI assistant can:

1. Accept a user's technical support question.
2. Search previous support tickets for similar problems.
3. Retrieve the most relevant tickets.
4. Provide those tickets as context to an LLM.
5. Generate a concise answer based on the retrieved information.

### Example

**User:**

> I am not receiving the password reset email.

**AI Assistant:**

> Please check your spam folders and verify that your registered email address is correct.

The application also allows the user to view the support tickets that were retrieved to generate the answer.

---

## 🧠 How It Works

The application follows this workflow:

```text
User Question
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Retrieve Similar Support Tickets
      ↓
Relevant Ticket Context
      ↓
Google Gemini LLM
      ↓
AI-Generated Response
```

### 1. User Question

The user enters a technical support problem through the Streamlit interface.

### 2. Text Vectorization

The application uses **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert the support-ticket text into numerical vectors.

### 3. Similarity Search

**Cosine similarity** compares the user's question with the historical support tickets and identifies the most relevant tickets.

### 4. Context Retrieval

The top relevant tickets, including their previous solutions, are collected as context.

### 5. LLM Generation

The retrieved context is provided to **Google Gemini**, which generates a concise response based on the available support information.

The prompt instructs the model not to invent solutions when the retrieved tickets do not contain enough information.

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **Pandas**
* **Scikit-learn**
* **TF-IDF Vectorization**
* **Cosine Similarity**
* **Google Gemini API**
* **Git & GitHub**

---

## 📁 Project Structure

```text
support-ticket-chatbot/
│
├── app.py
├── tickets.csv
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

### Files

| File               | Purpose                                                  |
| ------------------ | -------------------------------------------------------- |
| `app.py`           | Main Streamlit application                               |
| `tickets.csv`      | Sample historical support-ticket dataset                 |
| `requirements.txt` | Python dependencies                                      |
| `README.md`        | Project documentation                                    |
| `.gitignore`       | Prevents sensitive/unnecessary files from being uploaded |

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/heyarnav404/support-ticket-chatbot.git
```

### 2. Navigate into the project

```bash
cd support-ticket-chatbot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 API Key Setup

This project uses the **Google Gemini API**.

Create a Streamlit secrets file:

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
```

### ⚠️ Security

**Never upload your API key to GitHub.**

The `.streamlit/` directory is included in `.gitignore` so the local secrets file is not committed to the repository.

---

## ▶️ Running the Application

Run:

```bash
python -m streamlit run app.py
```

Streamlit will open the application in your browser.

---

## 🧪 Example Questions

Try questions such as:

```text
I cannot login to my account.
```

```text
My payment was declined.
```

```text
I am not receiving the password reset email.
```

```text
My application is running very slowly.
```

```text
I am getting a server error.
```

The chatbot retrieves similar historical tickets and uses them as context for the AI response.

---

## 📚 What I Learned

Through this project, I practiced:

* Working with CSV datasets using Pandas
* Text preprocessing
* TF-IDF vectorization
* Cosine similarity
* Information retrieval
* RAG concepts
* LLM API integration
* Prompt design
* Streamlit application development
* Git and GitHub
* Protecting API credentials

---

## 🚧 Current Limitations

This is a small learning/portfolio prototype.

Current limitations include:

* Uses a small sample support-ticket dataset.
* Uses TF-IDF and cosine similarity instead of a dedicated vector database.
* The chatbot does not maintain long-term conversational memory.
* The quality of responses depends on the available historical tickets.
* It is not designed for production-scale support systems.

---

## 🚀 Future Improvements

Possible improvements include:

* Replace TF-IDF with modern embedding models.
* Add a vector database such as FAISS, Chroma, or another vector store.
* Implement conversation history.
* Add support for larger ticket datasets.
* Add document/PDF knowledge sources.
* Add better retrieval and ranking.
* Add response evaluation and monitoring.
* Deploy the application online.
* Add authentication and user management.

---

## 👨‍💻 Author

**Arnav Chaudhary**

GitHub:
https://github.com/heyarnav404

---

## 📌 Disclaimer

The support-ticket data used in this project is **sample/demo data created for educational and portfolio purposes**. It does not contain real customer support information.
