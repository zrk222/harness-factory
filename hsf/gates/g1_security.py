"""Gate 1 - Security. Pure-AST scanner (no external tools required).

Checks: closed-world imports (hsf.runtime + stdlib whitelist), forbidden
builtins/calls (eval/exec/os.system/subprocess/socket), nondeterminism
sources (random, time in logic, os.environ reads), file writes, canary leak,
and injection-pattern scan over spec/context inputs. bandit/semgrep can be
layered on via the [guards] extra; this gate is self-sufficient without them.
"""
from __future__ import annotations
import ast, re
from .base import GateResult, Finding

ALLOWED_IMPORT_ROOTS = {"hsf", "dataclasses", "typing", "__future__", "enum", "math", "decimal"}
FORBIDDEN_CALLS = {"eval", "exec", "compile", "__import__", "open"}
FORBIDDEN_MODULES = {"os", "subprocess", "socket", "random", "sys", "shutil", "pathlib",
                     "urllib", "requests", "http", "pickle", "time"}
INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions", r"disregard .{0,20}system prompt",
    r"you are now", r"reveal .{0,20}(prompt|instructions|canary)", r"exfiltrate",
]

def scan_inputs_for_injection(text: str) -> list[Finding]:
    out = []
    for pat in INJECTION_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            out.append(Finding("HSF-INJ-001", "high", f"injection pattern {pat!r} at char {m.start()}", "<input>"))
    return out

def run(source: str, canary: str | None = None, input_texts: list[str] | None = None) -> GateResult:
    findings: list[Finding] = []
    if canary and canary in source:
        findings.append(Finding("HSF-CANARY-001", "critical", "compile canary leaked into artifact"))
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return GateResult("security", False, [Finding("HSF-SYN-000", "critical", f"unparseable: {e}", line=e.lineno or 0)])
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mods = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""]
            for mod in mods:
                root = mod.split(".")[0]
                if root in FORBIDDEN_MODULES:
                    findings.append(Finding("HSF-IMP-002", "critical", f"forbidden import {mod!r} (CWE-94 surface)", line=node.lineno))
                elif root not in ALLOWED_IMPORT_ROOTS:
                    findings.append(Finding("HSF-IMP-001", "critical", f"import {mod!r} outside closed world", line=node.lineno))
        if isinstance(node, ast.Call):
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else (fn.attr if isinstance(fn, ast.Attribute) else "")
            if name in FORBIDDEN_CALLS:
                findings.append(Finding("HSF-CALL-001", "critical", f"forbidden call {name}() (CWE-94)", line=node.lineno))
            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
                dotted = f"{fn.value.id}.{fn.attr}"
                if dotted in {"os.system", "os.popen", "subprocess.run", "subprocess.Popen"}:
                    findings.append(Finding("HSF-CALL-002", "critical", f"forbidden call {dotted} (CWE-78)", line=node.lineno))
    for pat_text in input_texts or []:
        findings.extend(scan_inputs_for_injection(pat_text))
    inj_only = all(f.code == "HSF-INJ-001" for f in findings) if findings else False
    passed = not findings or inj_only  # input injection is flagged evidence, not an artifact defect
    return GateResult("security", passed, findings, {"scanner": "hsf-ast-v1"})
