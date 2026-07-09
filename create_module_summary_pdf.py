from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


INPUT_FILE = Path("module_summary.md")
OUTPUT_FILE = Path("module_summary.pdf")


def clean_line(line):
    line = line.strip()

    if line.startswith("# "):
        return ("title", line[2:].strip())

    if line.startswith("## "):
        return ("heading", line[3:].strip())

    if line.startswith(":::"):
        return ("skip", "")

    return ("body", line)


def write_page(pdf, page_items):
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor("white")
    plt.axis("off")

    y = 0.94

    for item_type, text in page_items:
        if item_type == "title":
            fig.text(0.08, y, text, fontsize=16, weight="bold", va="top")
            y -= 0.055

        elif item_type == "heading":
            fig.text(0.08, y, text, fontsize=12.5, weight="bold", va="top")
            y -= 0.04

        elif item_type == "blank":
            y -= 0.018

        else:
            for wrapped_line in wrap(text, width=92):
                fig.text(0.08, y, wrapped_line, fontsize=9.5, va="top")
                y -= 0.022

    pdf.savefig(fig)
    plt.close(fig)


def main():
    raw_lines = INPUT_FILE.read_text(encoding="utf-8").splitlines()

    pages = []
    current_page = []
    y_remaining = 0.86

    for raw_line in raw_lines:
        item_type, text = clean_line(raw_line)

        if item_type == "skip":
            continue

        if text == "":
            item = ("blank", "")
            height = 0.018
        elif item_type == "title":
            item = (item_type, text)
            height = 0.055
        elif item_type == "heading":
            item = (item_type, text)
            height = 0.04
        else:
            wrapped_count = max(1, len(wrap(text, width=92)))
            item = ("body", text)
            height = wrapped_count * 0.022

        if y_remaining - height < 0.06:
            pages.append(current_page)
            current_page = []
            y_remaining = 0.88

        current_page.append(item)
        y_remaining -= height

    if current_page:
        pages.append(current_page)

    with PdfPages(OUTPUT_FILE) as pdf:
        for page_items in pages:
            write_page(pdf, page_items)

    print(f"Created formatted PDF: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()