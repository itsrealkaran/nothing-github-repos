"""Public repository card for any GitHub username."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
from github_user import public_repos
from nothing import MODES, SCALE, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    scale = SCALE[size]
    colors = theme(mode)
    rows = data["repos"]
    width = int(640 * scale)
    height = int((88 + len(rows) * 34 + 36) * scale)

    def n(value):
        return round(value * scale, 1)

    name, _ = dots("REPOS", n(46), n(22), colors["fg"], scale=2.2 * scale)
    parts = [open_svg(mode, width, height, f"{data['login']} repositories"), name]
    for index, (repo, stars) in enumerate(rows):
        y = n(100 + index * 34)
        parts.append(label(n(28), y, repo, colors["fg"], n(16), 0.2))
        parts.append(label(width - n(48), y, str(stars), colors["figure"], n(16), 0.4))
    parts.append(label(n(28), height - n(18), f"@{data['login']} · public repositories", colors["muted"], n(12), 0.6))
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = public_repos(login)
    data["login"] = login
    out = ROOT / "dist" / login
    out.mkdir(parents=True, exist_ok=True)
    lines = [f"# {login}", "", "Username, mode, and size.", ""]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += [f"### {size}", "", f"![{mode} {size}](dist/{login}/{filename})", ""]
            print(login, mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
