# alpaca

A simple command-line tool to list available LLM models from various providers (OpenAI, Google, Anthropic, xAI).

## Installation

1. Clone the repository:
```bash
$ git clone git@github.com:ljbuturovic/alpaca.git
$ cd alpaca
```

2. Create a virtual environment:
```bash
$ python3 -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
$ pip install -r requirements.txt
```

## Usage

The tool requires API keys set as environment variables:
- `OPENAI_API_KEY` for OpenAI
- `GOOGLE_API_KEY` for Google Gemini API, or `GOOGLE_CLOUD_PROJECT` for Vertex AI API
- `ANTHROPIC_API_KEY` for Anthropic
- `XAI_API_KEY` for xAI

### Examples

List OpenAI models:
```bash
$ ./llm_models.py --provider OpenAI
```

List Google models using Gemini API:
```bash
$ ./llm_models.py --provider Google
```

List Google models using Vertex AI API (with regional endpoint):
```bash
$ ./llm_models.py --provider Google --vertexai --region us-central1
```

List Anthropic models:
```bash
$ ./llm_models.py --provider Anthropic
```

List xAI models:
```bash
$ ./llm_models.py --provider xAI
```

## Requirements

- Python 3.7+
- See `requirements.txt` for package dependencies
- tested on Ubuntu 24.04
