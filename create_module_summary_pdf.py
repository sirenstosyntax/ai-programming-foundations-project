from pathlib import Path
from textwrap import wrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


INPUT_FILE = Path("module_summary.md")
OUTPUT_FILE = Path("module_summary.pdf")


def draw_wrapped_text_page(pdf, title, lines, max_chars=95):
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor("white")
    plt.axis("off")

    y = 0.96

    if title:
        fig.text(0.08, y, title, fontsize=14, weight="bold", va="top")
        y -= 0.04

    for line in lines:
        if y < 0.07:
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor("white")
            plt.axis("off")
            y = 0.96

        if line.startswith("# "):
            text = line.replace("# ", "").strip()
            fig.text(0.08, y, text, fontsize=14, weight="bold", va="top")
            y -= 0.04
        elif line.startswith("## "):
            text = line.replace("## ", "").strip()
            fig.text(0.08, y, text, fontsize=12, weight="bold", va="top")
            y -= 0.035
        elif line.strip() == "":
            y -= 0.018
        else:
            wrapped = wrap(line, width=max_chars)
            for wrapped_line in wrapped:
                if y < 0.07:
                    pdf.savefig(fig, bbox_inches="tight")
                    plt.close(fig)
                    fig = plt.figure(figsize=(8.5, 11))
                    fig.patch.set_facecolor("white")
                    plt.axis("off")
                    y = 0.96

                fig.text(0.08, y, wrapped_line, fontsize=9.5, va="top")
                y -= 0.022

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def main():
    text = INPUT_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    with PdfPages(OUTPUT_FILE) as pdf:
        draw_wrapped_text_page(pdf, "", lines)

    print(f"Created {OUTPUT_FILE}")


if __name__ == "__main__":
    main()