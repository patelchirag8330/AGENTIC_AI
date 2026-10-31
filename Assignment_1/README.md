# Assignment 1 — Student Support Agent

Flask + LangChain + Groq (`openai/gpt-oss-20b`) + SQLite + BM25 policy retrieval.

## Setup (Windows)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your Groq key to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
SECRET_KEY=replace_with_a_long_random_secret
```

## Included student accounts

The cleaned database already contains only two student profiles: **001 — Chirag Patel** and **002 — Abhi Patel**. Their existing password hashes and current profile/fee/scholarship records are retained. Previous tickets, memories and activity history have been cleared.

If you need to provision another account, run:

```powershell
python database.py
```

Do not share the database or `.env` publicly.

## Run

```powershell
python app.py
```

Open http://127.0.0.1:5000.

## Student-facing features

- Use the **Memory** button in the top bar to add, review, forget or clear your own saved facts.
- Expand **Agent run details** under an assistant response to inspect tool calls, runtime and trace ID when available.
- Start a new conversation with **New chat**; recent turns are supplied to the agent as context.

## Evaluate

```powershell
python evaluate.py
```

Evaluation uses temporary fictional records in a separate test database; it does not add sample students to the live application database.

## Project files

- `app.py` — Flask routes and session login
- `agent.py` — Groq agent loop
- `tools.py` — approved agent tools
- `database.py` — SQLite schema, account provisioning and login checks
- `retrieval.py` — BM25 policy search
- `memory.py` — student-scoped memory
- `context_manager.py` — conversation context
- `tracing.py` — run tracing
- Assignment 2 additionally includes `privacy.py`, `authz.py`, `approvals.py`, and `audit.py`.

Assignment 2 retains student-specific authorization, approval for sensitive changes, privacy protections and audit logging.
