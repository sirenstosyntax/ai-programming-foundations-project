from pathlib import Path

path = Path("module_summary.md")
text = path.read_text(encoding="utf-8", errors="replace")

replacements = {
    "\ufeff": "",
    "\\#": "#",
    "\\_": "_",
    "\\`": "`",
    "â€”": "-",
    "â€“": "-",
    "â€™": "'",
    "â€œ": '"',
    "â€": '"',
    "â€": '"',
    "“": '"',
    "”": '"',
    "’": "'",
    "—": "-",
    "–": "-",
}

for old, new in replacements.items():
    text = text.replace(old, new)

text = "".join(
    character
    if character in "\r\n\t" or 32 <= ord(character) <= 126
    else ""
    for character in text
)

path.write_text(text, encoding="utf-8")
print("Sanitized module_summary.md")