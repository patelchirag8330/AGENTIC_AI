# Assignment 2 — Student Support Agent

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

- Use **My data** in the top bar to manage personal memory, review pending email/phone change requests, and inspect recent security events.
- The security activity panel displays the audit hash-chain verification status.
- Sensitive changes require the separate Approve or Reject action; typing approval in chat does not execute a change.
- Expand **Agent run details** under an assistant response to inspect tool calls, runtime and trace ID when available.

## Evaluate

```powershell
python evaluate.py
```

Evaluation uses temporary records in a separate test database; it does not change the live application database. For name-based privacy tests (including the historical Harsh Shah record), the evaluator copies only student IDs and names from the existing live database into its temporary database. It does not copy fees, scholarship details, contacts, credentials or memories. Keep the existing database available when running Assignment 2 evaluation; the report states whether historical identities were loaded.

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
