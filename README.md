# Extraction Service

A small FastAPI service with an OpenAI-backed `ask()` helper. Today it exposes a
`/health` endpoint and a command-line script that makes a first call to the
`gpt-4o-mini` model and prints the result.

## How to run

The project is run with [uv](https://docs.astral.sh/uv/), which manages the
virtual environment and loads the `.env` file for each command. All commands
below are run from the root of this repository (the folder that contains
`requirements.txt`).

### 0. Prerequisites

- Python 3.10 or newer (the project was set up with Python 3.14).
- uv. Install it with the one-liner from
  <https://docs.astral.sh/uv/getting-started/installation/>, then check it with
  `uv --version`.
- An OpenAI API key. Create one at <https://platform.openai.com/api-keys>.

### 1. Create the virtual environment

```bash
uv venv
```

This creates a `.venv` folder in the project root. `uv run` finds it
automatically, so you do not need to activate it. uv writes a `.gitignore`
inside `.venv`, so the folder is never committed.

Already have a virtual environment under another name? Activate it and
`uv run` will use that one instead of creating `.venv`.

### 2. Install the dependencies

```bash
uv pip install -r requirements.txt
```

### 3. Create the `.env` file

Copy the example file and put your OpenAI key in it:

```bash
cp .env.example .env
```

Open `.env` in an editor and set the value:

```
OPENAI_API_KEY=sk-...
```

`.env` is listed in `.gitignore`, so the key is never committed.

The code reads `OPENAI_API_KEY` from the environment. Every command below is
prefixed with `uv run --env-file .env`, which loads the file for that command
only. There is nothing to export by hand.

### 4. Start the server

```bash
uv run --env-file .env uvicorn app.main:app --reload
```

The server listens on <http://127.0.0.1:8000>. In a second terminal, check it
is up with:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

Interactive API docs are available at <http://127.0.0.1:8000/docs>.
Stop the server with `Ctrl+C`.

### 5. Run the first call

The script sends a prompt to `gpt-4o-mini` and prints the model's answer
together with the status, model name and token usage. It takes two arguments:
the prompt and the maximum number of output tokens.

```bash
uv run --env-file .env python3 -m scripts.first_call "Name one use of a vector database in one sentence." 60
```

Example output:

```
prompt => Name one use of a vector database in one sentence. , max tokens => 60
prompt request successful with status completed, values => AskResult(text='A vector database can be used for efficient similarity search in applications like image or text retrieval, enabling rapid finding of items that are semantically similar to a given query.', status='completed', incomplete_reason='', model='gpt-4o-mini-2024-07-18', input_tokens='18', output_tokens='34')
```

To see the exit code, append `; echo "exit: $?"`. With a cap that is too small
for the answer the model stops early and the script exits with code 2:

```bash
uv run --env-file .env python3 -m scripts.first_call "Explain a context window in one sentence." 16; echo "exit: $?"
```

```
prompt => Explain a context window in one sentence. , max tokens => 16
prompt request failed with status incomplete, reason is IncompleteDetails(reason='max_output_tokens')
exit: 2
```

Exit codes:

| Code | Meaning |
| ---- | ------- |
| 0    | The request completed. |
| 1    | No arguments were given (the usage line is printed), or the script crashed before sending anything, for example because `OPENAI_API_KEY` is not set. |
| 2    | The model stopped early, for example because the token cap was too low. The reason is printed. |

Note: every run makes a real request to the OpenAI API and is billed to your
account. If the key is missing, the script stops at startup with:

```
openai.OpenAIError: Missing credentials. Please pass an `api_key`, ... or set the `OPENAI_API_KEY` ... environment variable.
```

Check that `.env` exists, contains the key, and that the command starts with
`uv run --env-file .env`.

### Running without uv

The same steps work with plain Python. Create and activate the environment,
install the dependencies, and export the `.env` variables in your shell:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
set -a; source .env; set +a
```

Then run the commands from steps 4 and 5 without the `uv run --env-file .env`
prefix, for example `uvicorn app.main:app --reload` and
`python3 -m scripts.first_call "..." 60`.
