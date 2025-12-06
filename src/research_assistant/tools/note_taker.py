from strands import tool
from pathlib import Path
import json
from datetime import datetime

NOTES_DIR = Path("./outputs/notes")


@tool
def save_note(topic: str, content: str, tags: list[str] = None) -> str:
    """
    Save a research note to persistant storage.

    Use this to record important findings, summaries, or insights
    that should be preserved for the final report.

    Args:
        topic: The topic or title for this note
        content: Note content (can be multiple paragraphs)
        tags: Optional list of tags for categorization

    Returns:
        Confirmation message with the saved noted ID
    """
    NOTES_DIR.mkdir(parents=True, exist_ok=True)

    note_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    note = {
        "id": note_id,
        "topic": topic,
        "content": content,
        "tags": tags or [],
        "timestamp": datetime.now().isoformat(),
    }

    note_path = NOTES_DIR / f"{note_id}.json"
    note_path.write_text(json.dumps(note, indent=2))

    return f"Note saved with ID: {note_id}"


def list_notes(tag_filter: str = None) -> str:
    """
    List all saved research notes, optionally filtering by tag.

    Use this to review what notes have been collected before generating a report.

    Args:
        tag_filer: Optional tag to filter notes by

    Returns:
        Formatted list of notes with their topics, IDs and preview
    """

    if not NOTES_DIR.exists():
        return "No notes found."

    notes = []

    for note_file in sorted(NOTES_DIR.glob("*.json")):
        note = json.loads(note_file.read_text())

        # Include the note if user did not specify tag, or if filter matches the note's tag
        if tag_filter is None or tag_filter in note.get("tags", []):
            preview = (
                note["content"][:100] + "..."
                if len(note["content"]) > 100
                else note["content"]
            )
            tags_str = ", ".join(note.get("tags", [])) or "no tags"
            notes.append(
                f"[{note['id']}] {note['topic']}\n    Tags: {tags_str}\n    {preview}"
            )
    return "\n\n.join(notes)" if notes else "No matching notes found"
