#!/usr/bin/env python3
"""Claude Code hook that nudges Claude to save lessons after real work.

  self_improve_hook.py start   (SessionStart) records the repo state.
  self_improve_hook.py stop    (Stop) if the repo changed since the last
                               check, asks Claude once to run the
                               self-improve skill before finishing.

Never fails the session: any error just exits 0.
"""
import hashlib
import json
import os
import subprocess
import sys

REASON = (
    "Self-improve check: before you finish, use the `self-improve` skill. "
    "Look back at this turn: user corrections, mistakes you fixed, commands "
    "that took several tries, project conventions you discovered. If any of "
    "it would help a future session, save it to this repo's CLAUDE.md or "
    ".claude/skills/ and commit it with the rest of the work. If nothing is "
    "worth saving, finish without mentioning this check."
)


def git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, timeout=10
    ).stdout


def repo_state(cwd):
    head = git("rev-parse", "HEAD", cwd=cwd)
    status = git("status", "--porcelain", cwd=cwd)
    diff = git("diff", "HEAD", cwd=cwd)
    return hashlib.sha256((head + status + diff).encode()).hexdigest()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stop"
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    cwd = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    git_dir = git("rev-parse", "--absolute-git-dir", cwd=cwd).strip()
    if not git_dir:
        return  # not a git repo
    session = "".join(c for c in data.get("session_id", "default") if c.isalnum() or c in "-_")
    state_dir = os.path.join(git_dir, "claude-self-improve")
    os.makedirs(state_dir, exist_ok=True)
    marker = os.path.join(state_dir, session or "default")

    current = repo_state(cwd)
    if mode == "start" or data.get("stop_hook_active") or not os.path.exists(marker):
        # Baseline, or Claude already ran the check this turn: record and pass.
        with open(marker, "w") as f:
            f.write(current)
        return

    with open(marker) as f:
        previous = f.read().strip()
    if previous != current:
        print(json.dumps({"decision": "block", "reason": REASON}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
