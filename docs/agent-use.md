# Using HSF With Claude Code Or Codex

This repo is agent-friendly because every meaningful claim can be checked with
commands. A coding agent should not need to guess whether a change is good; it
should run the suite, compile the demo workflow, inspect the golden result, and
report the receipt evidence.

## One-Time Setup

Clone and install the repo:

```bash
git clone https://github.com/zrk222/harness-factory.git
cd harness-factory
python -m pip install -e ".[dev]"
pytest -q
```

Expected result:

```text
49 passed
```

## Claude Code Prompt

Paste this into Claude Code after opening the repo:

```text
You are working in the harness-factory repository.

Task: <describe the change you want>

Preserve these project rules:
- No hand-copied metrics. Any number in docs must trace to a test, golden run,
  or receipt.
- No tuning on public-claim fixture sets.
- A new workflow type should usually be specs + goldens only. If compiler or
  runtime code must change, explain why.
- Keep generated receipts, registry artifacts, caches, and egg-info out of git.

Before finishing, run:
- python -m pip install -e ".[dev]"
- pytest -q
- hsf validate specs/glp1_review.yaml
- hsf compile specs/glp1_review.yaml
- hsf goldens registry_store/glp1_review-*.py glp1_review

Report exact evidence:
- test result
- golden accuracy, n, and correct count
- receipt shipped value
- files changed
- any limitations or skipped checks
```

## Codex Prompt

Paste this into Codex after opening the repo:

```text
Work in this repo only. Make the requested change and verify it end to end.

Requested change:
<describe the change>

Project contract:
- Keep the public README easy to read.
- Do not hand-copy metrics; use test, golden, or receipt output.
- Do not tune on public-claim fixture sets.
- New workflow types should be added through specs and goldens unless there is
  a clear factory bug.
- Do not commit generated registry_store/, receipts/, __pycache__, .pytest_cache,
  or egg-info files.

Verification commands:
python -m pip install -e ".[dev]"
pytest -q
hsf validate specs/glp1_review.yaml
hsf compile specs/glp1_review.yaml
hsf goldens registry_store/glp1_review-*.py glp1_review

Closeout:
Summarize exact evidence, including test count, golden accuracy, receipt
shipped status, changed files, and any skipped checks.
```

## Adding A New Workflow With An Agent

Give the agent the workflow policy in plain English, then ask it to create:

- `specs/<workflow_id>.yaml`
- `goldens/<workflow_id>/cases.jsonl`
- tests that prove the new workflow compiles and passes goldens

Useful prompt:

```text
Add a new HSF workflow called <workflow_id>.

The desired policy is:
<describe the approval, denial, human-review, or routing policy>

Implement this as specs + goldens first. Do not change compiler or runtime code
unless the existing factory cannot express the workflow. If code changes are
needed, explain the factory gap and add a focused regression test.

Run pytest and the HSF validate/compile/goldens loop before finishing.
```

## Reviewing Agent Output

Check these before accepting an agent change:

- `pytest -q` passes.
- `hsf goldens ...` reports `accuracy: 1.0`.
- the compile receipt says `shipped: true`.
- README metrics match command output.
- public-claim fixture sets were not silently edited to make a failure pass.
- generated folders remain ignored and uncommitted.

## Evidence Commands

Use these commands when you want the agent to prove the current demo is healthy:

```bash
pytest -q
hsf validate specs/glp1_review.yaml
hsf compile specs/glp1_review.yaml
hsf goldens registry_store/glp1_review-*.py glp1_review
python -c "import json,glob; r=json.load(open(glob.glob('receipts/*.json')[0])); print({'shipped': r['shipped'], 'accuracy': r['gates'][3]['evidence']['accuracy'], 'n': r['gates'][3]['evidence']['n'], 'correct': r['gates'][3]['evidence']['correct']})"
```

Expected evidence for the included demo:

```text
49 passed
accuracy: 1.0
n: 40
correct: 40
shipped: true
```
