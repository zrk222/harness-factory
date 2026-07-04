# Release And Public Review Checklist

Use this when publishing HSF as a public credibility artifact.

## Before Creating A Release

Run the evidence loop:

```bash
python -m pip install -e ".[dev]"
pytest -q
hsf validate specs/glp1_review.yaml
hsf compile specs/glp1_review.yaml
hsf goldens registry_store/glp1_review-*.py glp1_review
python -c "import json,glob; r=json.load(open(glob.glob('receipts/*.json')[0])); print({'shipped': r['shipped'], 'accuracy': r['gates'][3]['evidence']['accuracy'], 'n': r['gates'][3]['evidence']['n'], 'correct': r['gates'][3]['evidence']['correct']})"
```

Expected evidence:

```text
38 passed
shipped: true
accuracy: 1.0
n: 40
correct: 40
```

## Suggested GitHub Topics

Add these topics to help discovery:

```text
code-factory
ltap
compiled-ai
deterministic-ai
ai-agents
workflow-engine
python
audit-log
prompt-injection
golden-tests
compliance
github-actions
```

## Suggested Repository Description

```text
Compile YAML workflows into signed, gate-tested Python artifacts with LTAP receipts.
```

## Suggested First Release

Use `v1.0.0` if the goal is public review and Release Radar-style visibility.
Use `v0.1.0` if you want to label it as an early preview.

Suggested release title:

```text
HSF: Code factory for signed, gate-tested workflow artifacts
```

Suggested release notes:

```markdown
## What is included

- YAML workflow specs compiled into deterministic Python artifacts
- four-gate validation pipeline: security, syntax, execution, accuracy
- LTAP-style receipts with spec hash, artifact hash, doctrine hash, gate evidence, and shipped verdict
- adversarial prompt-injection goldens proving the decision is unchanged while the audit log flags the input
- Python 3.11 and 3.12 GitHub Actions CI
- public README visual and Claude Code/Codex usage guide

## Why it matters

HSF moves expensive model reasoning out of the live request path. Teams can pay
the compile and validation cost once, then run signed deterministic artifacts
for every transaction. That means lower runtime spend, faster decisions, fewer
manual review loops, and better audit evidence.

## Evidence

- `pytest -q`: 38 passed
- `hsf goldens registry_store/glp1_review-*.py glp1_review`: accuracy 1.0, n 40, correct 40
- receipt integrity: shipped true

## Scope notes

- signing is local HMAC-SHA256; ed25519 is the documented production upgrade
- security gate is a built-in AST scanner; bandit and presidio are optional extras
- Temporal backend is an import-guarded adapter stub
- clinical examples are synthetic test data, not a healthcare product
```

## Places To Ask For Review

- GitHub repository issues: open a `Request for review` issue with the evidence above.
- GitHub Community Discussions: ask for feedback on the repo, README, and safety claims.
- GitHub Release Radar: submit if the current submission path is open and this is a major release.
- DEV Community: publish a short post showing the code-factory diagram, the 4-gate pipeline, and the receipt evidence.
- LinkedIn/X/Hacker News: lead with the concrete claim, not hype: "YAML workflow in, signed gate-tested Python artifact out."

## Review Request Template

```markdown
I am looking for technical review of HSF, a small code-factory prototype that
compiles YAML workflow specs into signed Python artifacts and blocks shipment
unless security, syntax, execution, and golden-answer gates pass.

Repo: <repo url>
Release: <release url>

Evidence:
- pytest: 38 passed
- goldens: accuracy 1.0, n 40, correct 40
- receipt: shipped true
- CI: Python 3.11 + 3.12

I would especially value review of:
- the gate model
- the prompt-injection fixture and audit behavior
- the HMAC signing boundary and ed25519 upgrade path
- whether the README explains the scope honestly
```
