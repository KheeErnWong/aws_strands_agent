from strands import tool
from pathlib import Path
from datetime import datetime
import json

REPORTS_DIR = Path("./outputs/reports")
NOTES_DIR = Path("./outputs/notes")


@tool
def generate_report(
    title: str, sections: list[str], conclusion: str, include_notes: bool = True
) -> str:
    """
    Generate a markdown research report from findings.

    Use this at the end of a research session to compile all findings into a formatted, shareable report.

    Args:
        title: The report title
        sections: List of section contents (each becomes an H2 section)
        conclusion: The concluding summary
        include_notes: Whether to append saved notes at the end

    Returns:
        Path to the generated report file
    """
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.md"

    # Build report content
    content = f"# {title}\n\n"
    content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    content += "---\n\n"

    for i, section in enumerate(sections, start=1):
        content += f"## Section {i}\n\n{section}\n\n"

    content += f"## Conclusion\n\n{conclusion}\n\n"

    # Optionally include notes
    if include_notes and NOTES_DIR.exists():
        notes = list(NOTES_DIR.glob("*.json"))
        if notes:
            content += "---\n\n## Appendix: Research Notes\n\n"
            for note_file in sorted(notes):
                note = json.loads(note_file.read_text())
                content += f"### {note['topic']}\n\n"
                content += f"*{note['timestamp']}*\n\n"
                content += f"{note['content']}\n\n"

    report_path = REPORTS_DIR / filename
    report_path.write_text(content)

    return f"Report generated: {report_path}"
