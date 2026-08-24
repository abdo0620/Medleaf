"""Helpers for counting tokens locally """

import tiktoken

_enc = tiktoken.get_encoding("cl100k_base")  

def count_tokens_ollama(text):
    """Return an estimated token count for `text`"""
    return len(_enc.encode(text))