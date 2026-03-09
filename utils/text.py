import tiktoken


def get_tokenizer(model: str):
    try:
        encoding = tiktoken.encoding_for_model(model)
        return
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")
        return encoding.encode
    
def count_tokens(text: str, model: str) -> int:
    tokenizer = get_tokenizer(model)
    if tokenizer:
        return len(tokenizer(text))
    return estimate_tokens(text)

def estimate_tokens(text: str) -> int:
    # Simple heuristic: 1 token is approximately 4 characters
    return max(1, len(text) // 4)