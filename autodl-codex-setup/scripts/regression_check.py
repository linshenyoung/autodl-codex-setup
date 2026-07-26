"""Static regression checks for the public autodl-codex-setup Skill.

This script never contacts a server, reads credentials, or runs SSH. It checks
that the published Skill retains the safeguards learned from real regressions.
"""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"

REQUIRED = (
    "unique SSH alias",
    "ExitOnForwardFailure=yes",
    "PowerShell does not use backslash",
    "PowerShell single-quoted string",
    "ClearAllForwardings=yes",
    "HTTP 403",
    "HTTP 421",
    "return `405`",
    "Do not use `POST`",
    "codex login --device-auth",
    "chmod 600",
    "exact local SSH PID",
    "remote port is released",
)

FORBIDDEN = re.compile(
    r"Your" + r"God|example" + r"\.org|connect\." +
    r"(?:west|bjb|cqa)\.seetacloud\.com|A6000" + r"Pro",
    re.IGNORECASE,
)


def main() -> int:
    if not SKILL.is_file():
        print(f"missing {SKILL}")
        return 1

    text = SKILL.read_text(encoding="utf-8")
    missing = [phrase for phrase in REQUIRED if phrase not in text]
    if missing:
        print("missing safeguards:")
        for phrase in missing:
            print(f"- {phrase}")
        return 1

    violations = []
    for path in ROOT.parents[0].rglob("*"):
        if path.is_file() and ".git" not in path.parts:
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if FORBIDDEN.search(content):
                violations.append(path.relative_to(ROOT.parents[0]))
    if violations:
        print("private-looking strings found in:")
        for path in violations:
            print(f"- {path}")
        return 1

    print("autodl-codex-setup regression checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
