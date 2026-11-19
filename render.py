"""Public repository card. Five Nothing modes. Private names stay off the card."""

import json
from pathlib import Path

from frame import dots, label, open_svg
from nothing import MODES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, data):
    colors = theme(mode)
    rows = data["repos"]
    height = 78 + len(rows) * 32 + 36
    name, _ = dots("REPOS", 46, 22, colors["fg"], scale=2.2)
    parts = [
        open_svg(mode, 640, height, "Public repositories by stars"),
        name,
    ]
    for index, (repo, stars) in enumerate(rows):
        y = 96 + index * 32
        parts.append(label(28, y, repo, colors["fg"], 16, 0.2))
        parts.append(label(520, y, str(stars), colors["figure"], 16, 0.4))
    parts.append(label(28, height - 18, "Public repositories", colors["muted"], 12, 0.8))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    data = json.loads((ROOT / "sample.json").read_text())
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    for mode in MODES:
        (out / f"{mode}.svg").write_text(render(mode, data))
        print(mode)


if __name__ == "__main__":
    main()
