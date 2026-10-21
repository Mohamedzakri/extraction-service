from dataclasses import dataclass

@dataclass(frozen=True)
class AskResult:
    text: str
    status: str
    incomplete_reason: str
    model: str
    input_tokens: str
    output_tokens: str