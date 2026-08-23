"""Helpers for obtaining token counts from the local Ollama service."""

import requests

def count_tokens_ollama(text, model="nomic-embed-text", url="http://localhost:11434"):
    """Return the number of prompt tokens reported by Ollama for ``text``."""
    resp = requests.post(f"{url}/api/embed", json={"model": model, "input": text})
    resp.raise_for_status()
    return resp.json()["prompt_eval_count"]