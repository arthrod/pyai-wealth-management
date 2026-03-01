from dataclasses import dataclass
from typing import Optional

from pydantic_ai import Agent, ModelRetry, RunContext

from common.agent_constants import (
    AGENT_MODEL,
    SUPERVISOR_AGENT_NAME,
    SUPERVISOR_INSTRUCTIONS,
    RESEARCHER_AGENT_NAME,
    RESEARCHER_INSTRUCTIONS,
    WRITER_AGENT_NAME,
    WRITER_INSTRUCTIONS,
)

DEBUG_MODE = False


def debug_print(message: str):
    """Print debug messages only when DEBUG_MODE is enabled."""
    if DEBUG_MODE:
        print(message)


@dataclass
class AgentDependencies:
    blog_topic: Optional[str] = None
    research_notes: Optional[str] = None
    next_agent: Optional[str] = None
    trigger_message: Optional[str] = None
    current_agent_name: str = SUPERVISOR_AGENT_NAME
    message_history: list = None

    def __post_init__(self):
        if self.message_history is None:
            self.message_history = []


# Supervisor Output Functions
async def respond_to_user(ctx: RunContext[AgentDependencies], response: str) -> str:
    debug_print(f"[{ctx.deps.current_agent_name}] Responding to user")
    return response


async def route_to_researcher_agent(ctx: RunContext[AgentDependencies], topic: str) -> str:
    clean_topic = topic.strip()
    if not clean_topic:
        raise ModelRetry("Provide a non-empty blog topic before routing to the researcher.")

    debug_print(f"[{ctx.deps.current_agent_name}] Routing to {RESEARCHER_AGENT_NAME}")
    ctx.deps.blog_topic = clean_topic
    ctx.deps.next_agent = RESEARCHER_AGENT_NAME
    ctx.deps.trigger_message = (
        "Research the topic and prepare structured notes for a blog draft. "
        f"Topic: {clean_topic}"
    )
    return ""


# Researcher Output Functions
async def respond_with_research(ctx: RunContext[AgentDependencies], response: str) -> str:
    debug_print(f"[{ctx.deps.current_agent_name}] Responding with research")
    return response


async def route_research_to_writer(
    ctx: RunContext[AgentDependencies],
    topic: str,
    research_notes: str,
) -> str:
    clean_topic = topic.strip() or (ctx.deps.blog_topic or "").strip()
    clean_notes = research_notes.strip()

    if not clean_topic:
        raise ModelRetry("Missing blog topic. Ask supervisor for a clear topic before drafting.")

    if not clean_notes:
        raise ModelRetry("Research notes are empty. Provide detailed notes before routing to writer.")

    debug_print(f"[{ctx.deps.current_agent_name}] Routing to {WRITER_AGENT_NAME}")
    ctx.deps.blog_topic = clean_topic
    ctx.deps.research_notes = clean_notes
    ctx.deps.next_agent = WRITER_AGENT_NAME
    ctx.deps.trigger_message = (
        "Draft a polished blog post using the prepared research notes.\n"
        f"Topic: {clean_topic}\n"
        f"Research notes:\n{clean_notes}"
    )
    return ""


async def route_from_researcher_to_supervisor(
    ctx: RunContext[AgentDependencies],
    message: str,
) -> str:
    follow_up = message.strip() or "Please provide a clear blog topic to continue."
    debug_print(f"[{ctx.deps.current_agent_name}] Routing back to {SUPERVISOR_AGENT_NAME}")
    ctx.deps.next_agent = SUPERVISOR_AGENT_NAME
    ctx.deps.trigger_message = follow_up
    return ""


# Writer Output Functions
async def deliver_blog_draft(ctx: RunContext[AgentDependencies], draft: str) -> str:
    clean_draft = draft.strip()
    if not clean_draft:
        raise ModelRetry("The blog draft cannot be empty. Provide a complete draft.")

    debug_print(f"[{ctx.deps.current_agent_name}] Delivering blog draft")
    return clean_draft


async def route_from_writer_to_supervisor(
    ctx: RunContext[AgentDependencies],
    message: str,
) -> str:
    follow_up = message.strip() or "Please share the topic or revision request."
    debug_print(f"[{ctx.deps.current_agent_name}] Routing back to {SUPERVISOR_AGENT_NAME}")
    ctx.deps.next_agent = SUPERVISOR_AGENT_NAME
    ctx.deps.trigger_message = follow_up
    return ""


# Agents
supervisor_agent = Agent(
    AGENT_MODEL,
    name=SUPERVISOR_AGENT_NAME,
    deps_type=AgentDependencies,
    output_type=[
        respond_to_user,
        route_to_researcher_agent,
    ],
    system_prompt=SUPERVISOR_INSTRUCTIONS,
)

researcher_agent = Agent(
    AGENT_MODEL,
    name=RESEARCHER_AGENT_NAME,
    deps_type=AgentDependencies,
    output_type=[
        respond_with_research,
        route_research_to_writer,
        route_from_researcher_to_supervisor,
    ],
    system_prompt=RESEARCHER_INSTRUCTIONS,
)

writer_agent = Agent(
    AGENT_MODEL,
    name=WRITER_AGENT_NAME,
    deps_type=AgentDependencies,
    output_type=[
        deliver_blog_draft,
        route_from_writer_to_supervisor,
    ],
    system_prompt=WRITER_INSTRUCTIONS,
)


# Tools
@supervisor_agent.tool
async def get_blog_topic(context: RunContext[AgentDependencies]) -> str:
    if context.deps.blog_topic:
        return context.deps.blog_topic
    return "No blog topic is currently stored."


@supervisor_agent.tool
async def set_blog_topic(context: RunContext[AgentDependencies], topic: str) -> str:
    clean_topic = topic.strip()
    if not clean_topic:
        raise ModelRetry("Cannot store an empty blog topic.")

    context.deps.blog_topic = clean_topic
    return f"Stored blog topic: {clean_topic}"


@researcher_agent.tool
async def save_research_notes(context: RunContext[AgentDependencies], notes: str) -> str:
    clean_notes = notes.strip()
    if not clean_notes:
        raise ModelRetry("Cannot save empty research notes.")

    context.deps.research_notes = clean_notes
    return "Research notes saved."
