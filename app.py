import os
from dataclasses import dataclass
from flask import Flask, jsonify, render_template, request
from openai import OpenAI


app = Flask(__name__)


EXAM_CONTEXT = {
    "JEE": "JEE Main and Advanced: emphasize conceptual depth, quick methods, and common traps.",
    "NEET": "NEET: focus on NCERT-aligned explanations, accurate fundamentals, and elimination strategies.",
    "BITSAT": "BITSAT: concise, exam-speed reasoning with formula-first problem solving.",
    "Olympiad": "Physics Olympiad: rigorous derivations, multi-step reasoning, and advanced insight.",
    "General": "General physics learning: adapt to student's level with clear stepwise guidance.",
}


@dataclass
class PhysicsRequest:
    question: str
    exam: str
    level: str

    @classmethod
    def from_payload(cls, payload: dict) -> "PhysicsRequest":
        question = (payload.get("question") or "").strip()
        exam = payload.get("exam", "General")
        level = payload.get("level", "high-school")
        return cls(question=question, exam=exam, level=level)


def build_prompt(req: PhysicsRequest) -> str:
    exam_context = EXAM_CONTEXT.get(req.exam, EXAM_CONTEXT["General"])
    return (
        "You are PhysicsGPT, an expert physics tutor for competitive exams. "
        f"Student level: {req.level}. "
        f"Exam context: {exam_context} "
        "Answer with: (1) core concept, (2) step-by-step solution, "
        "(3) final answer, and (4) quick exam tip. Keep language clear and friendly. "
        f"Question: {req.question}"
    )


def generate_answer(req: PhysicsRequest) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "I can explain this once an API key is configured. "
            "Set OPENAI_API_KEY to enable full oral physics answers. "
            f"Meanwhile, try this framing: identify known quantities, pick the governing law, and solve stepwise for: {req.question}"
        )

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=build_prompt(req),
        temperature=0.2,
    )
    return response.output_text.strip()


@app.get("/")
def index():
    return render_template("index.html", exam_options=sorted(EXAM_CONTEXT.keys()))


@app.post("/api/answer")
def answer():
    payload = request.get_json(silent=True) or {}
    req = PhysicsRequest.from_payload(payload)

    if not req.question:
        return jsonify({"error": "Please enter a physics question."}), 400

    try:
        answer_text = generate_answer(req)
    except Exception as exc:  # surface model/provider issues safely
        return jsonify({"error": f"Failed to generate answer: {exc}"}), 500

    return jsonify({"answer": answer_text})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
