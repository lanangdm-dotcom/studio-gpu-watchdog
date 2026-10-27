---
name: self-improve
description: Save what you learned in a coding session so future sessions do better. Use before your final reply on any task in a git project where the user corrected you, you fixed your own mistake, a command or workflow took several tries, or you discovered a project convention, setup step, or gotcha. Also use when a "Self-improve check" hook message appears, and when the user says "ingat ini", "remember this", "jangan ulangi", "lain kali", "update skill", or "improve skill". Writes lessons to the repo's CLAUDE.md or .claude/skills/ and commits them with the work. Skip it for pure Q&A turns that changed nothing.
---

# Self-improve

Goal: every session leaves the project a little easier for the next one. Lessons live in the project's git repo, so they survive cloud sessions and reach every machine.

## 1. Install the hook (first time in a repo only)

The hook makes this skill run automatically after any turn that changed the repo. It is installed when `.claude/settings.json` mentions `self_improve_hook.py`.

If it is not installed, and CLAUDE.md does not say `self-improve: no hook`:

1. Copy this whole skill folder into the repo, unless it is already at `.claude/skills/self-improve/`:
   ```bash
   SRC=$(dirname "$(dirname "$(find ~/.claude /mnt "$CLAUDE_PROJECT_DIR" -path '*self-improve/scripts/self_improve_hook.py' 2>/dev/null | head -1)")")
   ROOT=$(git rev-parse --show-toplevel)
   mkdir -p "$ROOT/.claude/skills" && cp -rn "$SRC" "$ROOT/.claude/skills/self-improve"
   ```
2. Merge these hooks into `.claude/settings.json` (create the file if missing; keep any existing keys and hooks):
   ```json
   {
     "hooks": {
       "SessionStart": [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/self-improve/scripts/self_improve_hook.py\" start"}]}],
       "Stop": [{"hooks": [{"type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/self-improve/scripts/self_improve_hook.py\" stop"}]}]
     }
   }
   ```
3. Commit with the current work, and tell the user in one line that auto-improve is now on for this repo.

To install into another repo the user names, copy this skill folder there and do step 2 in that repo.

## 2. Decide whether there is a lesson

Save something only if a future session would act differently because of it. Good lessons:

- The user corrected you ("bukan begitu", "jangan pakai X", "selalu Y").
- You made a mistake and found the cause (wrong command, wrong file, wrong assumption).
- A command, build, test, or deploy took several tries before the right form was found.
- A project convention, folder layout, naming rule, or gotcha that is not obvious from the code.
- A multi-step workflow you will likely repeat (release, migration, seeding data, debugging a service).

Skip: one-off facts about this task, things obvious from reading the code, secrets, tokens, passwords, personal data, anything already written down.

If nothing qualifies, stop here and say nothing about it.

## 3. Pick where it goes

- **CLAUDE.md** (repo root): short rules that apply to almost every task. One or two lines each, under a fitting heading. Example: `- Run \`npm run check\` before committing; CI fails on lint.`
- **`.claude/skills/<topic>/SKILL.md`**: a workflow with steps, or knowledge only needed for one kind of task (deploy, database migrations, WhatsApp API quirks). Name the folder in kebab-case after the task.

Read what exists first (`CLAUDE.md`, `ls .claude/skills`). Update the closest existing entry instead of adding a near-duplicate. Fix or delete anything you now know is wrong or outdated.

New project skill format:

```markdown
---
name: <topic>
description: <what it covers> Use when <concrete triggers: tasks, files, commands, error messages>.
---

# <Topic>

<Steps or rules, short and concrete. Exact commands in code blocks. Say why when the reason is not obvious.>
```

The description decides when the skill loads, so name the situations and keywords that should trigger it.

## 4. Keep it lean

- Prefer editing over appending. A skill that grows forever stops being read.
- Keep CLAUDE.md under about 150 lines; move detail into a skill when it gets long.
- Keep each SKILL.md under about 300 lines; split by topic if needed.
- Write instructions, not a diary: "Use X because Y", not "Today I tried X".

## 5. Commit and report

- Commit the lesson on the current working branch with the task's work, e.g. `chore(claude): note how to run e2e tests`. Do not open a separate PR just for it. If the task itself made no commit and the user did not ask for commits, leave the change uncommitted and mention it.
- In your final reply add one short line, in the user's language, e.g. `📚 Skill diperbarui: cara jalankan e2e test (.claude/skills/e2e-testing)`.
