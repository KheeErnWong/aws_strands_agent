from dotenv import load_dotenv

import asyncio
import sys
from pathlib import Path

from research_assistant.agent import create_agent

load_dotenv()


def list_session(sessions_dir: str = "./session") -> list[str]:
    """List of available session IDs."""
    session_path = Path(sessions_dir)
    if not session_path.exists():
        return []

    return [
        d.name.replace("session_", "")
        for d in session_path.iterdir()
        if d.is_dir() and d.name.startswith("session_")
    ]


async def interactive_session(agent):
    """Run interactive research session with streaming."""
    print("\n" + "=" * 50)
    print("Research Assistant ready.")
    print("Commands: 'quit' to exit, 'notes' to list notes")
    print("\n" + "=" * 50)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if user_input.lower() in ["quit", "exit", "q"]:
            break

        if not user_input:
            continue

        print("\nAssistant: ", end="", flush=True)

        async for event in agent.stream_async(user_input):
            if "data" in event:
                print(event["data"], end="", flush=True)
            if "current_tool_use" in event:
                name = event["current_tool_use"].get("name")
                if name:
                    print(f"\n [Using {name}]", flush=True)

        print("\n")


def main():
    # Get session ID from args or prompt
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        sessions = list_session()

        if sessions:
            print("Available sessions:")
            for i, sid in enumerate(sessions, start=1):
                print(f"  {i}. {sid}")
            print(f"  {len(sessions) + 1}. Create new session")

            choice = input("\nSelection session (number or new name): ").strip()

            if choice.isdigit() and int(choice) <= len(sessions):
                session_id = sessions[int(choice) - 1]
            else:
                session_id = choice if choice else "default"
        else:
            session_id = input(
                "Enter session name (or press Enter for 'default'):"
            ).strip()
            session_id = session_id if session_id else "default"

    print(f"\nUsing session: {session_id}")

    agent = create_agent(session_id=session_id)

    try:
        asyncio.run(interactive_session(agent))
    finally:
        agent.cleanup()
        print("\nSession saved. Goodbye!")


if __name__ == "__main__":
    main()
