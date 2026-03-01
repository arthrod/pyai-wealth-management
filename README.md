# Research Blog Drafting Multi-Agent Example using Pydantic AI Framework

This project demonstrates how to use [Pydantic AI Framework](https://ai.pydantic.dev/) 
with multiple agents working together. It uses a supervisor pattern to hand off work across a research and writing pipeline.

You will find a version of just using the Pydantic AI Framework and another version
that leverages [Temporal](https://temporal.io) to wrap the agentic flow with Temporal.

![](images/architecture.png)

The vanilla Pydantic AI framework version of this example is located [here](src/py_supervisor/README.md).

The Temporal version of this example is located [here](src/temporal_supervisor/README.md)

Scenarios currently implemented include:
* Topic Intake - supervisor captures the user blog topic and routes the request
* Research Brief Creation - researcher generates structured notes and outline ideas
* Blog Draft Creation - writer converts research notes into a complete blog post draft
* Revision Loop - writer can route back to supervisor when clarification is needed

You can run through the orchestration with the Temporal version using a [Web Application](src/frontend/README.md) 

## Prerequisities
* [uv](https://docs.astral.sh/uv/) - Python package and project manager
* [OpenAI API Key] (https://platform.openai.com/api-keys) - Your key to accessing OpenAI's LLM
* [Temporal CLI](https://docs.temporal.io/cli#install) - Local Temporal service
* [Redis](https://redis.io/downloads/) - Stores conversation history

## Set up Python Environment
```bash
uv sync
```

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

## Getting Started

See the Pydantic AI Framework version [here](src/py_supervisor/README.md)
And the Temporal version of this example [here](src/temporal_supervisor/README.md)

Stay tuned! More to come!
