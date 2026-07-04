# Launch Playbook

This is the practical launch plan for HSF. The audience is engineers who have
been burned by unreliable agents in production and want a deterministic path
from policy to code.

## Before Posting

Finish these first:

- PyPI package works: `pip install harness-factory`
- README demo GIF is visible above the fold
- release is green on GitHub Actions
- `Share your spec` issue is pinned
- repo topics are set for discovery

PyPI is handled through GitHub Trusted Publishing. Configure a PyPI trusted
publisher for:

- owner: `zrk222`
- repository: `harness-factory`
- workflow: `publish-pypi.yaml`
- environment: `pypi`

After that, publishing a GitHub release can publish to PyPI without a long-lived
token. This follows PyPI's Trusted Publishing flow with GitHub OIDC.

## Tier 1: Launch Moment

### Hacker News

Best title:

```text
Show HN: A factory that compiles LLM workflows into deterministic, gated Python
```

Posting discipline:

- Tuesday through Thursday, around 8-9am ET.
- Stay in the comments all day.
- Lead with working code, not vision language.
- Concede limits clearly.
- Use the thesis line: "Prompt injection cannot reach code that has no prompt."

### Lobste.rs

Smaller and higher-signal. Worth posting if you can get an invite. Use the same
technical framing, with less launch-copy energy.

## Tier 2: Reddit

Stagger posts over a week. Do not post all subreddits on one day.

- `r/Python`: pure-AST gate, subprocess sandbox, package ergonomics.
- `r/LLMDevs`: agent reliability and prompt-injection boundary.
- `r/AI_Agents`: deterministic production path for agent-designed workflows.
- `r/MachineLearning`: `[P]` project angle, H=0 determinism, replay test.
- `r/LocalLLaMA`: template engine works offline; no API required.
- `r/programming`: compilation as an old idea applied to AI workflows.

Reddit line that should travel:

```text
You cannot socially engineer an if-statement.
```

## Tier 3: Compounding Surfaces

- PR relevant awesome-lists: `awesome-llm`, `awesome-ai-agents`,
  `awesome-python`.
- Cross-post the launch article to DEV and Hashnode.
- Submit to TLDR AI, Python Weekly, Pointer, and Changelog News.
- Share in MLOps Community Slack and Latent Space Discord show-and-tell
  channels.
- Link the HITL reference page when talking to compliance-minded teams:
  `docs/human-in-the-loop.md`.

## Tier 4: Durable Authority

- Publish an architecture writeup with a Zenodo DOI.
- Pitch PyCon and AI Engineer World's Fair.
- Pitch Practical AI, The Changelog, and Talk Python.

Pitch the pattern, not just the repo:

```text
Compile the workflow once, gate it, sign it, and run static code in production.
```

## Short Launch Copy

```text
Prompt injection cannot reach code that has no prompt.

HSF compiles YAML workflows into signed, gate-tested Python artifacts. The demo
feeds a live injection attempt to the runtime; the decision stays DENIED and the
audit log flags the input.

Repo: https://github.com/zrk222/harness-factory
```

## Evidence To Include

- `pytest -q`: 49 passed
- CI: Python 3.11 and 3.12 green
- GLP-1 goldens: accuracy 1.0, n 40, correct 40
- receipt: shipped true
- `hsf demo`: decision unchanged, injection flagged
- `hsf init`: generated workflow compiles and passes immediately
- `hsf serve`: signed artifact becomes REST endpoint
