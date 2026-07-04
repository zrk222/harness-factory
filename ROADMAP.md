# Roadmap

## v0.2 (shipped)
- `hsf init` scaffold
- `hsf demo`
- `hsf serve` (FastAPI)
- `hsf badge`
- Spec gallery: 5 domains, zero-code-change generality test

## v0.3 (help wanted)
- [ ] `hsf draft "<policy in English>"` - LLM drafts the spec YAML, which then
      walks the normal loader + gates (generation-plane only; good first issue
      for the prompt, the pipeline already exists)
- [ ] ed25519 signing via `cryptography` (interface is ready in `hsf/registry`)
- [ ] GitHub Action: run someone's specs through the four gates in their CI
- [ ] Temporal backend beyond the adapter stub
- [ ] TypeScript artifact target
- [ ] Nested/multi-branch workflow specs (sequential branches, sub-workflows)

## Principles that won't change
One model call per workflow type. H = 0 at runtime. No artifact ships ungated.
Claims trace to receipts, never prose.
