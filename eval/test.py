"""
📊 Benchmark DeepEval pour Medleaf (Chroma + Google Gemini)

Adapté du script original -- remplace Ollama par Gemini (deepeval.models.GeminiModel),
en gardant la même structure : Golden_dataset.json (queries / corpus / ground_truth),
génération via ta pipeline RAG existante, puis évaluation avec 4 métriques DeepEval.

Place ce fichier dans: Evaluation/RAG/ (à côté de Golden_dataset.json)
"""

import json
import os
import sys
from pathlib import Path

import pandas as pd
from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
)
from deepeval.models import GeminiModel
from deepeval.test_case import LLMTestCase
from dotenv import load_dotenv



# -------------------------------------------------
# Racine du projet -- adapte le nombre de parents
# si tu places ce fichier ailleurs que Evaluation/RAG/
# -------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR / "Rag"))

from retreival import retreive_chunks
from agent import ask_mia
# -------------------------------------------------
# Ta fonction de retrieval réelle (Chroma).
# ⚠️ Adapte "retrieval" si ton fichier a un autre nom
# dans le dossier Rag/ (ex: Rag.retriever, Rag.query, etc.)
# -------------------------------------------------

# Génération de la réponse finale avec Gemini, à partir
# des chunks récupérés. Utilise google-genai comme le
# reste du projet (déjà dans requirements.txt).
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_GEN_MODEL = os.getenv("GEMINI_GEN_MODEL", "gemini-2.5-flash-lite")
gen_client = genai.Client(api_key=GEMINI_API_KEY)


# def generate_with_gemini(question, chunks):
#     context_text = "\n\n".join(chunks)
#     prompt = f"""
#     Tu es un assistant factuel. Réponds à la question UNIQUEMENT à partir
#     des extraits fournis. N'invente rien. Si l'information n'apparaît pas
#     dans les extraits, réponds exactement :
#     "L'information demandée n'apparaît pas dans les extraits fournis."

#     Question : {question}

#     Extraits :
#     {context_text}
#     """
#     response = gen_client.models.generate_content(
#         model=GEMINI_GEN_MODEL,
#         contents=prompt,
#     )
#     return response.text.strip()


# -------------------------------------------------
# CHARGEMENT DES DONNÉES
# -------------------------------------------------
def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


dataset_path = ROOT_DIR / "eval" / "eval_data.json"
dataset = load_json(dataset_path)
queries = dataset["queries"]
corpus = dataset["corpus"]
ground_truth = dataset["ground_truth"]

corpus_ids = [d["id"] for d in corpus]
corpus_texts = [d["text"] for d in corpus]


# -------------------------------------------------
# GÉNÉRATION DE LA RÉPONSE (ta pipeline Chroma + Gemini)
# -------------------------------------------------
def generate_answer(question):
    """
    1. Récupère les chunks pertinents depuis Chroma via retreive_chunks().
    2. Génère la réponse finale avec Gemini à partir de ces chunks.

    Retourne (reponse_finale: str, chunks_recuperes: list[str]).
    """
    return      ask_mia(question)



# -------------------------------------------------
# ÉVALUATION GÉNÉRATION (DeepEval + Gemini comme juge)
# -------------------------------------------------
load_dotenv(ROOT_DIR / "Rag" / ".env")  # même .env que ton app (GEMINI_API_KEY)

GEMINI_EVAL_MODEL_NAME = os.getenv("GEMINI_API_KEY", "gemini-2.5-flash-lite")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

eval_llm = GeminiModel(
    api_key=GEMINI_API_KEY
)


def evaluate_generation(queries, ground_truth):
    print("\n🔹 Évaluation avec DeepEval (juge: Gemini)...")
    print(f"📌 Total de questions : {len(queries)}\n")

    test_cases = []

    for idx, q in enumerate(queries[:1]):
        print(f"⏳ Traitement question {idx + 1}/{len(queries)}: {q['text'][:150]}...")

        qid = q["id"]
        relevant_docs = [c for c in corpus if c["id"] in ground_truth.get(qid, [])]

        response, chunks_list = generate_answer(q["text"])
        expected_answer = "\n".join([d["text"] for d in relevant_docs])
        time.sleep(0)

        test_case = LLMTestCase(
            input=q["text"],
            actual_output=response,
            expected_output=expected_answer,
            retrieval_context=chunks_list,
        )
        test_cases.append(test_case)

    metrics = [
        FaithfulnessMetric(model=eval_llm),
        ContextualPrecisionMetric(model=eval_llm),
        ContextualRecallMetric(model=eval_llm),
        AnswerRelevancyMetric(model=eval_llm),
    ]

    _ = evaluate(test_cases, metrics=metrics, async_config=AsyncConfig(run_async=False))

    deepeval_file = ROOT_DIR / ".deepeval" / ".latest_test_run.json"

    if deepeval_file.exists():
        with open(deepeval_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        metrics_summary = data["testRunData"]["metricsScores"]

        results_dict = {
            "total_questions": len(test_cases),
            "evaluation_time_seconds": data["testRunData"]["runDuration"],
            "timestamp": pd.Timestamp.now().isoformat(),
            "metrics": {},
        }

        for metric_data in metrics_summary:
            metric_name = metric_data["metric"]
            scores = metric_data["scores"]
            passed = metric_data["passes"]
            total = passed + metric_data["fails"]
            avg_score = sum(scores) / len(scores) if scores else 0
            pass_rate = (passed / total * 100) if total > 0 else 0

            results_dict["metrics"][metric_name] = {
                "pass_rate_percent": round(pass_rate, 2),
                "passed": passed,
                "total": total,
                "average_score": round(avg_score, 4),
                "scores": scores,
            }

            print(f"{metric_name}: {pass_rate:.2f}% pass rate")

        all_avg = [
            results_dict["metrics"][m]["average_score"] for m in results_dict["metrics"]
        ]
        global_score = sum(all_avg) / len(all_avg) if all_avg else 0
        results_dict["global_average_score"] = round(global_score, 4)

        print("\n" + "=" * 80)
        print(f"Score Global Moyen: {global_score:.4f}")
        print("=" * 80 + "\n")

        output_path = ROOT_DIR / "Evaluation" / "RAG" / "evaluation_results.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results_dict, f, indent=2, ensure_ascii=False)

        print(f"✅ Résultats sauvegardés dans: {output_path}")
        print(f"✅ Résultats DeepEval complets dans: {deepeval_file}\n")
        return results_dict
    else:
        print(f"❌ ERREUR: Fichier {deepeval_file} introuvable!")
        return None


if __name__ == "__main__":
    evaluate_generation(queries, ground_truth)

