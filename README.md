# AI Assistant Showcase

A minimal, production-oriented showcase of a **Pydantic AI–based action agent** with structured outputs, tool usage, and real database interaction.

The project demonstrates how to build a deterministic, tool-augmented AI assistant that can **reason, act, and persist state** using modern Python tooling.

---

## Overview

This repository showcases an AI assistant built with:

- **pydantic-ai** for strongly typed agent behavior
- **Tool-based actions** (database access, web search)
- **Supabase** as a real persistence layer
- **Streamlit** as a lightweight UI layer
- Pluggable LLM backends (OpenAI / Mistral)

The assistant can:
- List existing customers
- Create or update customer records
- Use external tools when required
- Return validated, structured responses

This is a **showcase project**, not a generic framework.

---

## Architecture

**Core components:**

- `ActionAgent`
  - Typed agent using `pydantic-ai`
  - Strict response models (`AgentResponseModel`)
  - System-prompt–driven behavior
- **Tool layer**
  - Database tools (Supabase)
  - External search (Tavily)
- **Dependency injection**
  - Explicit runtime dependencies via `RunContext`
- **Model abstraction**
  - Central `ModelFactory` for LLM selection

The agent operates synchronously and is designed to be **deterministic, inspectable, and extendable**.

---

## Tech Stack

- Python `>=3.13,<4.0"`
- pydantic-ai (OpenAI & Mistral support)
- Supabase
- Streamlit
- Tavily Search
- Pandas

---

## Environment Requirements

The following environment variables must be set inside a 'secrets.toml' file located at 'src/streamlit/.streamlit/' :

```bash
TAVILY_API_KEY=

LLM_MISTRAL_MODEL=
MISTRAL_API_KEY=

OPENAI_MODEL=
OPENAI_API_KEY=

SUPABASE_URL=
SUPABASE_KEY=
```

---

## Example Capabilities

* Natural language → structured action
* LLM-driven tool selection
* Database writes with validation
* Typed agent responses (no free-text output)
* Safe extension via new tools and models

---

## Purpose

This repository exists to demonstrate:

* How to build production-grade AI agents
* How to avoid prompt-only or text-only architectures
* How to combine AI reasoning with real system actions

It is intended as a technical reference and showcase, not as an end-user product.

---

## Author

Lukas Hamm

🔗 [https://www.lukashamm.dev](https://lukashamm.dev)  
📧 [lukas@lukashamm.dev](lukas@lukashamm.dev)  
💼 [https://www.linkedin.com/in/lukashamm-dev](https://www.linkedin.com/in/lukashamm-dev)

---
