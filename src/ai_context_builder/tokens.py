from anthropic import Anthropic
from anthropic.types import ModelParam

DEFAULT_MODEL: ModelParam = "claude-sonnet-5-5"


def count_tokens(
    client: Anthropic, text: str, model: ModelParam = DEFAULT_MODEL
) -> int:
    result = client.messages.count_tokens(
        model=model, messages=[{"role": "user", "content": text}]
    )

    return result.input_tokens
