from strands import Agent
from strands.models import BedrockModel
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.session.file_session_manager import FileSessionManager
from strands.tools.executors import ConcurrentToolExecutor

# Prebuilt tools from strands_tools
from strands_tools import tavily_search

# Custom tools
from research_assistant.tools import save_note, list_notes
from research_assistant.tools import generate_report

# Hooks
from research_assistant.hooks.logging_hook import ToolLoggingHook
from research_assistant.hooks.rate_limiter import RateLimitHook

# Structured output mode
from research_assistant.models.research_output import ResearchOutput

SYSTEM_PROMPT = """
    Act as an expert, highly meticulous, and unbiased research assistant.
    Your primary function is to deliver accurate, objective, and synthesized
    information based on factual evidence. You are a specialist in rapid
    information retrieval and structured reporting.

    Your workflow:
    1. When given a research topic, use tavily_search to find relevant information
    2. Save important findings as notes using save_note with appropriate tags
    3. Use list_notes to review what you've collected
    4. When asked, compile findings into a report using generate_report

    Always cite sources and indicate confidence levels in your findings.
    Mark critical discoveries with [IMPORTANT] for preservation.
"""


def create_agent(session_id: str = "default") -> Agent:
    return Agent(
        # Model configuration
        model=BedrockModel(model_id="anthropic.claude-sonnet-4-20250514"),
        # System prompt
        system_prompt=SYSTEM_PROMPT,
        # Specify tools
        tools=[tavily_search, save_note, list_notes, generate_report],
        # Conversation management
        # Keeps last 40 messages (user + assistant combined)
        # Drops oldest when exceeded, preserves tool call pairs
        conversation_manager=SlidingWindowConversationManager(window_size=40),
        # Session persistence.
        # Specify conversation thread. Different id = fresh conversation.
        session_manager=FileSessionManager(session_id=session_id),
        # Hooks for logging and rate limiting
        hooks=[ToolLoggingHook(), RateLimitHook(limits={"tavily_search": 10})],
        # Structure output schema (default for all calls)
        structured_output_model=ResearchOutput,
        # Agent identity
        agent_id="research-assistant",
        name="Research Assistant",
        description="Searches and summarizes research topics",
        # Persistent state across session
        state={"topics_researched": [], "total_searches": 0},
        # Callbacks. For displaying/streaming output as the agent runs
        callback_handler=None,
        # Tool execution to let multiple tools run in parallel
        tool_executor=ConcurrentToolExecutor(),
        # Misc
        record_direct_tool_call=True,  # Log tool calls in message history
        load_tools_from_directory=False,  # Don't auto-load from ./tools/
    )
