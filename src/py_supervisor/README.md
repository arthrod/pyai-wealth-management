# Research Blog Drafting Multi-Agent Example using Pydantic AI Framework

Demonstrates how to use Pydantic AI Framework with a supervisor, researcher, and writer orchestration.

The Temporal version of this example is located [here](src/temporal_supervisor/README.md)

Scenarios currently implemented include
* Topic Intake - supervisor captures the blog topic
* Research Briefing - researcher builds structured notes
* Blog Drafting - writer produces a complete draft
* Clarification Routing - specialized agents can route back to supervisor when needed

## Prerequisites
* [uv](https://docs.astral.sh/uv/) - Python package and project manager

## Set up your OpenAI API Key

```bash
cp setoaikey.example setoaikey.sh
chmod +x setoaikey.sh
```

Now edit the setoaikey.sh file and paste in your OpenAI API Key.
It should look something like this:
```text
export OPENAI_API_KEY=sk-proj-....
```

## Running the agent
```bash
cd src/py_supervisor
source ../../setoaikey.sh
uv run python -m py_supervisor.main
```

Example Output
```
Welcome to the blog drafting studio. Share a topic to begin.

[Supervisor Agent] Enter your message: Draft a blog post about agent orchestration for startup founders.
# Agent Orchestration for Startup Founders: A Practical Guide

## Introduction
Startup founders are increasingly using AI agents to speed up research, decision-making, and content creation. A simple three-agent pattern can improve quality without adding process overhead.

## Why a Supervisor-Researcher-Writer Pattern Works
1. The supervisor captures the request and keeps workflow state consistent.
2. The researcher gathers structured notes, arguments, and evidence ideas.
3. The writer converts those notes into a coherent, publication-ready narrative.

## Implementation Tips
- Keep role boundaries strict so each agent has one job.
- Persist intermediate notes to avoid losing context on retries.
- Route ambiguous requests back to the supervisor for clarification.

## Conclusion
This orchestration pattern gives founders faster first drafts with better structure and fewer hallucinations than a single-agent flow.

[Writer Agent] Enter your message: end
Agent loop complete.
```
