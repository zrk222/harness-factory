# Human-In-The-Loop Links

HSF does not replace human review. It makes review cheaper and more useful by
turning workflow behavior into static code, receipts, audit logs, and golden
cases that reviewers can inspect.

Use human-in-the-loop review when a workflow has legal, clinical, financial,
employment, moderation, or brand-risk impact. The recommended pattern is:

1. Compile and gate the workflow with HSF.
2. Route low-confidence, high-impact, or policy-edge cases to a reviewer queue.
3. Store reviewer outcomes as new private goldens.
4. Recompile and rerun the gates before shipping the next artifact.

## Tools And References

- [Label Studio](https://labelstud.io/) - open-source data labeling, AI
  evaluation, and human-in-the-loop workflow platform.
- [Label Studio active learning guide](https://docs.humansignal.com/guide/active_learning)
  - routes uncertain examples to annotators and feeds review outcomes back into
  the model or evaluation loop.
- [Humanloop](https://humanloop.com/home) - enterprise LLM evals, prompt
  management, observability, and human-review context. Note: Humanloop's docs
  reported a 2025 platform sunset, so check the current Anthropic/Humanloop
  status before depending on it.
- [Humanloop docs](https://humanloop.com/docs/getting-started/overview) -
  archived/current documentation for eval-driven and collaborative LLM
  development practices.

## How HSF Fits HITL

HSF should sit before and after the human queue:

```text
facts -> signed HSF artifact -> deterministic decision -> audit log
                         |-> review queue for edge cases
review outcome -> private golden -> compile -> gates -> signed artifact
```

The human reviewer is not asked to trust a prompt. They review the extracted
facts, the static rule path, the audit log, and the receipt. That keeps human
judgment focused on the hard cases instead of spending reviewer time on cases
the policy already handles deterministically.
