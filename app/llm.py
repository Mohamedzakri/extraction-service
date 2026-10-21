#from dataclasses import fields
#from http import client
from openai import OpenAI

from app.models.AskResult import AskResult

client = OpenAI()

def ask(prompt: str, max_output_tokens: int) -> AskResult:
    print(f"prompt => {prompt} , max tokens => {max_output_tokens}")
    resp = client.responses.create(model="gpt-4o-mini", input=prompt, max_output_tokens=int(max_output_tokens))
    text = resp.output_text
    status = resp.status
    incomplete_reason = getattr(resp, "incomplete_details", "") or ""
    model = resp.model
    
    input_tokens = str(resp.usage.input_tokens) if hasattr(resp, "usage") else "0"
    output_tokens = str(resp.usage.output_tokens) if hasattr(resp, "usage") else "0"

    '''
        allowed_keys = {r.name for r in fields(AskResult)}
        filtered_response = {k: v for k, v in resp.items() if k in allowed_keys}
        return AskResult(**filtered_response)
    '''

    return AskResult(
        text=text,
        status=status,
        incomplete_reason=str(incomplete_reason),
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens
    )

    
'''

 Write app/llm.py with an ask(prompt: str, max_output_tokens: int) function.
It returns a frozen dataclass AskResult with these fields: text, status, incomplete_reason (or None), model, input_tokens and output_tokens.
It sends model="gpt-4o-mini" explicitly.
The worked example from the M0 briefing is your starting point.


import sys
from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from the environment
resp = client.responses.create(
    model="gpt-4o-mini",
    input="Name one use of a vector database in one sentence.",
    max_output_tokens=60,
)
print(resp.output_text)
print("status:", resp.status, "| incomplete:", resp.incomplete_details)
print("tokens in/out:", resp.usage.input_tokens, resp.usage.output_tokens)
sys.exit(0 if resp.status == "completed" else 2)
'''