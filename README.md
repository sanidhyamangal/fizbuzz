# Fizbuzz
AI agent to interact with YahooFinance API to get all the financial information regarding the stock ticker such as stock information, news related to stock, etc. 
Author: Sanidhya Mangal

## Implementation Approach
Entire project works on two core principles.
- **MCP**: Developed a model context protocol (MCP) server to wrap all the function calls within the YahooFinance API.
- **Agent**: Developed an autonomus `ReActiveAgent` to interact with MCP server and get responses for the given workflow.

### Project Structure
```sh
.
├── pyproject.toml
├── README.md
├── src
│   └── fizbuzz
│       ├── __init__.py
│       ├── agents
│       ├── examples
│       │   └── yahoo_finance_tool.ipynb
│       ├── llms
│       ├── llms.py
│       └── yahoo_finance_mcp
│           ├── __init__.py
│           ├── __main__.py
│           └── server.py
└── uv.lock
```

## Setup and Running Instructions

### Environment Setup
- Requires Python 3.10 or later.
- Uses `uv` for dependency management. Install `uv` as per the instructions [here](https://docs.astral.sh/uv/) and run:
  `uv sync`

#### Environment Variables
You can refer to `.env.template` to setup `.env` file for configuring environ variable or can simple set them using `export` command

### Model and API Setup
- The chatbot uses Ollama to run LLM models. Download and install it from [Ollama](https://ollama.com).
- Download the [`mistral:7b`](https://ollama.com/library/mistral) model with:
  `ollama pull mistral:7b`

### Running MCP Server
To start MCP server you can run following command:
```sh
uv run yf-mcp-server
```

This command will main function within, `server.py` to start MCP server. 
>Entrypoint and command name could be modified within `pyproject.toml`