# collect.py — lance sur ton PC
import json
import agent  # ton fichier agent.py existant

test_questions = [
    "how much tamsulosin should i take",
    "what is betamethasone used for",
    "what are the side effects of venlafaxine",
    "what is tamsulosin used for",
    "can betamethasone be used on skin",
]

ground_truths = [
    "The recommended dose of tamsulosin hydrochloride is 0.4 mg once daily",
    "Betamethasone dipropionate is a topical corticosteroid used to treat skin conditions",
    "Venlafaxine side effects include nausea, dizziness, insomnia, and increased blood pressure",
    "Tamsulosin is used to treat symptoms of benign prostatic hyperplasia BPH",
    "Betamethasone dipropionate cream is applied topically to treat inflammatory skin conditions",
]

questions_out, answers_out, contexts_out = [], [], []

for i, q in enumerate(test_questions):
    print(f"[{i+1}/{len(test_questions)}] {q}")
    try:
        answer, chunks = agent.ask_mia(q, [])
        questions_out.append(q)
        answers_out.append(answer)
        contexts_out.append(chunks)
        print(f"  ✓ done")
    except Exception as e:
        print(f"  ✗ erreur: {e}")
        questions_out.append(q)
        answers_out.append("")
        contexts_out.append([""])

data = {
    "question":     questions_out,
    "answer":       answers_out,
    "contexts":     contexts_out,
    "ground_truth": ground_truths,
}

with open("eval_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ eval_data.json créé ! Upload ce fichier sur Colab.")