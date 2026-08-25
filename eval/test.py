"""Evaluate retrieval-grounded answer quality with DeepEval metrics."""

import json
import os
import dotenv
import sys
import time
from pathlib import Path

import pandas as pd
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
)
from deepeval.models import OpenAIModel
from deepeval.test_case import LLMTestCase

os.environ["DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE"] = "120"
dotenv.load_dotenv()
# Paste your regenerated Groq key here (get one at console.groq.com/keys)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# -------------------------------------------------
# Racine du projet
# -------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR / "Rag" / "retreival"))
sys.path.append(str(ROOT_DIR / "Rag" / "agent"))

from retreival import retreive_chunks
from agent import ask_mia

# -------------------------------------------------
# CHARGEMENT DES DONNÉES
# -------------------------------------------------
def load_json(path):
    """Load and return JSON data from ``path``."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


dataset_path = ROOT_DIR / "eval" / "eval_data.json"
dataset = load_json(dataset_path)
queries = dataset["queries"]
corpus = dataset["corpus"]
ground_truth = dataset["ground_truth"]


def generate_answer(question):
    """Generate one answer through the application's retrieval pipeline."""
    return ask_mia(question)


eval_llm = OpenAIModel(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
)


def evaluate_generation(queries, ground_truth, n_questions=20, sleep_between_calls=65):
    """Evaluate selected queries and persist aggregate and per-question scores."""
    # Evaluate retrieval-grounded answers with separate faithfulness,
    # relevance, precision, and recall signals instead of a single composite
    # score; this makes regressions easier to diagnose.
    print("\n🔹 Évaluation avec DeepEval (juge: Groq gpt-oss-20b)...")
    print(f"📌 Total de questions disponibles : {len(queries)}")
    print(f"📌 Questions évaluées cette run : {n_questions}\n")

    results_dict = {
        "total_questions": 0,
        "timestamp": pd.Timestamp.now().isoformat(),
        "metrics": {
            "Faithfulness": {"scores": [], "passed": 0, "failed": 0},
            "AnswerRelevancy": {"scores": [], "passed": 0, "failed": 0},
            "ContextualPrecision": {"scores": [], "passed": 0, "failed": 0},
            "ContextualRecall": {"scores": [], "passed": 0, "failed": 0},
        },
        "per_question": [],
    }

    start_time = time.time()

    for idx, q in enumerate(queries[:n_questions]):
        print(f"\n⏳ Question {idx + 1}/{n_questions}: {q['text'][:150]}...")

        qid = q["id"]
        relevant_docs = [c for c in corpus if c["id"] in ground_truth.get(qid, [])]

        try:
            response, chunks_list = generate_answer(q["text"])
        except Exception as e:
            print(f"⚠️ Échec génération pour {qid}: {e}")
            continue

        expected_answer = "\n".join([d["text"] for d in relevant_docs])

        test_case = LLMTestCase(
            input=q["text"],
            actual_output=response,
            expected_output=expected_answer,
            retrieval_context=chunks_list,
        )

        metrics = {
            "Faithfulness": FaithfulnessMetric(model=eval_llm),
            "AnswerRelevancy": AnswerRelevancyMetric(model=eval_llm),
            "ContextualPrecision": ContextualPrecisionMetric(model=eval_llm),
            "ContextualRecall": ContextualRecallMetric(model=eval_llm),
        }

        question_result = {"id": qid, "question": q["text"], "scores": {}}

        for name, metric in metrics.items():
            try:
                metric.measure(test_case)
                score = metric.score
                passed = metric.is_successful()
                print(f"  {name}: {score:.2f} {'✅' if passed else '❌'}")

                results_dict["metrics"][name]["scores"].append(score)
                if passed:
                    results_dict["metrics"][name]["passed"] += 1
                else:
                    results_dict["metrics"][name]["failed"] += 1
                question_result["scores"][name] = score

            except Exception as e:
                print(f"  ⚠️ {name} a échoué: {e}")

            # The delay avoids rate-limit failures when the external judge is
            # backed by a provider with a free-tier token budget.
            time.sleep(sleep_between_calls)

        results_dict["per_question"].append(question_result)
        results_dict["total_questions"] += 1

    results_dict["evaluation_time_seconds"] = round(time.time() - start_time, 2)

    # Aggregate per-question measurements only after the run so failed calls
    # do not silently become zero-valued scores.
    for name, data in results_dict["metrics"].items():
        scores = data["scores"]
        total = data["passed"] + data["failed"]
        data["average_score"] = round(sum(scores) / len(scores), 4) if scores else 0
        data["pass_rate_percent"] = round((data["passed"] / total * 100), 2) if total else 0

    all_avgs = [m["average_score"] for m in results_dict["metrics"].values() if m["scores"]]
    results_dict["global_average_score"] = round(sum(all_avgs) / len(all_avgs), 4) if all_avgs else 0

    print("\n" + "=" * 80)
    for name, data in results_dict["metrics"].items():
        print(f"{name}: avg={data['average_score']:.4f} | pass_rate={data['pass_rate_percent']:.2f}%")
    print(f"\nScore Global Moyen: {results_dict['global_average_score']:.4f}")
    print("=" * 80 + "\n")

    output_path = ROOT_DIR / "eval" / "evaluation_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results_dict, f, indent=2, ensure_ascii=False)

    print(f"✅ Résultats sauvegardés dans: {output_path}")
    return results_dict


if __name__ == "__main__":
    # Start small — bump n_questions once this runs clean end-to-end
    evaluate_generation(queries, ground_truth, n_questions=20, sleep_between_calls=65)