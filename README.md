# physicsgpt

PhysicsGPT is a lightweight web app that can answer physics questions for competitive exams and read answers aloud.

## Features
- Supports exam-oriented responses for **JEE, NEET, BITSAT, Olympiad, and General physics prep**.
- Accepts student level (middle school, high school, college) to tune explanations.
- Generates structured answers from an LLM backend.
- Speaks answers aloud in the browser using Web Speech API.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_key_here"   # optional but recommended
python app.py
```

Open http://localhost:8000.

## Notes
- If `OPENAI_API_KEY` is not set, the app returns a fallback coaching response.
- You can override the model with `OPENAI_MODEL` (default: `gpt-4.1-mini`).
