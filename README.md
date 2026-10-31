# AIDTM Agentic AI Engineering — Final Project Package

This package contains Assignment 1 and Assignment 2 of the Student Support Portal.

- **Assignment 1:** Intelligent Student Support Agent.
- **Assignment 2:** Student Support Agent with privacy, authorization, approval workflows and tamper-evident audit logging.

Both assignments use Flask, LangChain, Groq (`openai/gpt-oss-20b`), SQLite, BM25 policy retrieval and a web chat interface.

## Cleaned project data

The included application databases contain only these two student accounts:

| Student ID | Student name |
|---|---|
| 001 | Chirag Patel |
| 002 | Abhi Patel |

Existing password hashes and the current fee, scholarship and contact profile rows for these two accounts are retained. Previous support tickets, saved memories, approval requests, audit history, and trace/evaluation outputs have been cleared. No other student accounts remain in the supplied databases.

The original passwords are not included in this README. If either account's password is unknown, use the account-provisioning/reset procedure in the assignment's database code rather than sharing passwords.

## Security setup

The original `.env` files containing a Groq API key and Flask secret have been removed. The `.env.example` files are safe templates.

1. Open `Assignment_1` or `Assignment_2`.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Copy `.env.example` to `.env`.
5. Add your own Groq API key and generate a new Flask secret key.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Put the generated value in `SECRET_KEY` in `.env`. Never share `.env` or commit it to Git.

**Security action:** The API key in the uploaded project was exposed in the archive. Revoke that key in Groq and create a replacement before running the app.

## Run an assignment

From the selected assignment folder:

```powershell
python app.py
```

Open http://127.0.0.1:5000.

## Run evaluations

Run `python evaluate.py` separately in each assignment folder. Evaluation outputs will be generated afresh in that assignment's `reports` folder. Assignment 2 uses temporary evaluation records and keeps the live student database unchanged.

## Project structure

```text
agentic-student-support-portal-main/
├── Assignment_1/
└── Assignment_2/
```

Each assignment includes its application code, policy data, evaluation scripts, static UI files, requirements, safe environment template and cleaned SQLite database.
