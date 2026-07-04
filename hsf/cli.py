"""hsf CLI: validate | compile | run | goldens | bench  (stdlib argparse; zero extra deps)."""
from __future__ import annotations
import argparse, asyncio, json, sys
from pathlib import Path

def _load(spec_path):
    from hsf.spec import load_spec
    return load_spec(spec_path)

def _goldens_for(spec_id: str) -> list[dict]:
    p = Path("goldens") / spec_id / "cases.jsonl"
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]

def _artifact_path(value: str) -> Path:
    path = Path(value)
    if path.exists():
        return path.resolve()
    matches = sorted(Path().glob(value))
    if len(matches) == 1:
        return matches[0].resolve()
    if not matches:
        raise FileNotFoundError(f"artifact not found: {value}")
    raise ValueError(f"artifact pattern matched multiple files: {value}")

def _schema_of(spec) -> dict:
    out = {}
    for s in spec.steps:
        if s.type == "bounded_invocation" and s.schema_:
            for k, fs in s.schema_.items():
                d = {"type": fs.type}
                if fs.min is not None: d["min"] = fs.min
                if fs.max is not None: d["max"] = fs.max
                out[k] = d
    return out

def cmd_validate(args):
    spec, sha = _load(args.spec)
    print(f"OK {spec.workflow_spec} v{spec.version} sha={sha[:16]}...")

def cmd_compile(args):
    from hsf.foundry.regeneration import compile_with_regeneration
    from hsf.gates.pipeline import run_pipeline, write_receipt
    from hsf.registry import store_artifact
    spec, sha = _load(args.spec)
    goldens = _goldens_for(spec.workflow_spec)
    schema = _schema_of(spec)
    smoke = goldens[:5]
    def gate_runner(src):
        return run_pipeline(src, spec_schema=schema, smoke_cases=smoke,
                            golden_cases=goldens,
                            input_texts=[c["input_text"] for c in goldens[:10]])
    src, meta, chain = compile_with_regeneration(spec, sha, gate_runner, engine=args.engine)
    path, art_sha = store_artifact(src, Path(args.registry), spec.workflow_spec)
    passed, results = gate_runner(src)
    receipt = write_receipt(Path("receipts"), spec_id=spec.workflow_spec, spec_sha=sha,
                            artifact_sha=art_sha, compile_meta=meta, results=results, shipped=passed)
    print(f"COMPILED {path}\nRECEIPT  {receipt}\nshipped={passed} attempts={meta.get('attempts',1)}")

def cmd_run(args):
    from hsf.registry import verify_artifact
    from hsf.runtime import Orchestrator
    from hsf.runtime.extractor import FixtureExtractor
    fields = json.loads(args.extracted) if args.extracted else {}
    orch = Orchestrator(_artifact_path(args.artifact), FixtureExtractor(fields), verify=verify_artifact)
    result = orch.run({"text": args.text})
    print(json.dumps({"status": result.status, "reason": result.reason}))

def cmd_goldens(args):
    from hsf.gates.g4_accuracy import run as g4
    src = _artifact_path(args.artifact).read_text()
    r = g4(src, _goldens_for(args.spec_id))
    print(json.dumps(r.evidence, indent=2))
    sys.exit(0 if r.passed else 1)

def cmd_bench(args):
    from hsf.telemetry import break_even
    print(json.dumps(break_even(args.compile_tokens), indent=2))

def main(argv=None):
    p = argparse.ArgumentParser(prog="hsf", description="Harness Software Factory")
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("validate"); s.add_argument("spec"); s.set_defaults(fn=cmd_validate)
    s = sub.add_parser("compile"); s.add_argument("spec")
    s.add_argument("--engine", default="template", choices=["template", "llm"])
    s.add_argument("--registry", default="registry_store"); s.set_defaults(fn=cmd_compile)
    s = sub.add_parser("run"); s.add_argument("artifact"); s.add_argument("--text", default="")
    s.add_argument("--extracted", default=""); s.set_defaults(fn=cmd_run)
    s = sub.add_parser("goldens"); s.add_argument("artifact"); s.add_argument("spec_id"); s.set_defaults(fn=cmd_goldens)
    s = sub.add_parser("bench"); s.add_argument("--compile-tokens", type=int, default=34000); s.set_defaults(fn=cmd_bench)
    args = p.parse_args(argv)
    args.fn(args)

if __name__ == "__main__":
    main()
