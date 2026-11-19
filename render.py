"""Repository card. Compact is the top repo. Regular is the list. Wide adds bars."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import public_repos
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    if size == "mini":
        return _mini(mode, colors, data)
    if size == "compact":
        return _compact(mode, colors, data)
    if size == "wide":
        return _list(mode, colors, data, 896, True)
    return _list(mode, colors, data, 495, False)


def _mini(mode, colors, data):
    repo, stars = data["repos"][0]
    name, _ = dots("REPOS", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} repositories", mark=6, margin=14),
        name,
        label(16, 100, repo, colors["fg"], 16, 0),
        label(16, 124, f"{stars} stars", colors["muted"], 12, 0.2),
        "</svg>",
    ])


def _compact(mode, colors, data):
    repo, stars = data["repos"][0]
    name, _ = dots("REPOS", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} repositories"),
        name,
        label(20, 96, repo, colors["fg"], 22, 0),
        label(20, 118, f"{stars} stars · @{data['login']}", colors["muted"], 13, 0.2),
        "</svg>",
    ])


def _list(mode, colors, data, width, bars):
    rows = data["repos"]
    height = 72 + len(rows) * 30 + 24
    name, _ = dots("REPOS", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, width, height, f"{data['login']} repositories"), name]
    peak = max(stars for _, stars in rows) or 1
    for index, (repo, stars) in enumerate(rows):
        y = 78 + index * 30
        parts.append(label(20, y, repo, colors["fg"], 15, 0.1))
        if bars:
            bar = max(4, 460 * (stars / peak))
            parts.append(f'<rect x="280" y="{y - 11}" width="460" height="6" fill="{colors["rule"]}"/>')
            parts.append(f'<rect x="280" y="{y - 11}" width="{bar:.1f}" height="6" fill="{colors["figure"]}"/>')
            parts.append(label(760, y, str(stars), colors["figure"], 15, 0.2))
        else:
            parts.append(label(width - 56, y, str(stars), colors["figure"], 15, 0.2))
    parts.append("</svg>")
    return "\n".join(parts)


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/{card}?username={login}&theme={mode}&size={size}"
    return [
        f"**{card}** · {mode} · {size}",
        "",
        f"`{url}`",
        "",
        f"![{card} {mode} {size}](dist/{login}/{filename})",
        "",
    ]


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = public_repos(login)
    data["login"] = login
    out = ROOT / "dist" / login
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {login}", "", "Compact is the top repository. Regular is the list. Wide adds the bars.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += _variant("repos", login, mode, size, filename)
            print(login, mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
