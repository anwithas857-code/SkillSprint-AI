# SkillSprint AI — Complete MVP

This version avoids the frontend/backend mismatch by having FastAPI serve the frontend.

## Run on Windows

1. Open Command Prompt inside `backend`.
2. Activate your existing virtual environment if you have one:
   `.venv\Scripts\activate`
3. Install packages:
   `pip install -r requirements.txt`
4. Start:
   `uvicorn main:app --reload`
5. Open Chrome:
   `http://127.0.0.1:8000`

Do NOT double-click `frontend/index.html`. Open the localhost address above.

## What works

- Student profile + target career
- Assessment questions
- Skill scoring
- Weak-area detection
- Course recommendations
- Course-start tracking
- Career readiness percentage
- Improvement target
- Reminders
- SQLite persistence while the server/database remain available

The scoring engine is a prototype. It is ready to be upgraded to an LLM-based evaluator with an API key later.
