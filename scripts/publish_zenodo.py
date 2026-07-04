from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path


def api_json(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Zenodo API {exc.code}: {body}") from exc


def upload_file(bucket_url: str, token: str, path: Path) -> dict:
    request = urllib.request.Request(
        f"{bucket_url.rstrip('/')}/{path.name}",
        data=path.read_bytes(),
        method="PUT",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Zenodo upload {exc.code}: {body}") from exc


def git_archive(repo: Path, output: Path) -> None:
    subprocess.run(
        ["git", "archive", "--format=zip", f"--output={output}", "HEAD"],
        cwd=repo,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish the current HSF release archive to Zenodo.")
    parser.add_argument("--api-base", default="https://zenodo.org/api")
    parser.add_argument("--token-env", default="ZENODO_ACCESS_TOKEN")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--publish", action="store_true", help="Publish the deposit after upload.")
    parser.add_argument("--receipt", type=Path, default=Path("docs/zenodo-publication-receipt.json"))
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    token = os.environ.get(args.token_env, "").strip()
    if not token:
        raise SystemExit(f"Missing {args.token_env}; set it in the shell, not in the repo.")

    metadata = json.loads((repo / ".zenodo.json").read_text(encoding="utf-8"))
    archive = args.archive
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    if archive is None:
        temp_dir = tempfile.TemporaryDirectory()
        archive = Path(temp_dir.name) / f"harness-factory-v{metadata['version']}.zip"
        git_archive(repo, archive)

    api_base = args.api_base.rstrip("/")
    deposition = api_json("POST", f"{api_base}/deposit/depositions", token, {})
    upload = upload_file(deposition["links"]["bucket"], token, archive)
    deposition = api_json(
        "PUT",
        f"{api_base}/deposit/depositions/{deposition['id']}",
        token,
        {"metadata": metadata},
    )
    if args.publish:
        deposition = api_json(
            "POST",
            f"{api_base}/deposit/depositions/{deposition['id']}/actions/publish",
            token,
        )

    receipt = {
        "published": bool(args.publish),
        "deposition_id": deposition.get("id"),
        "record_id": deposition.get("record_id") or deposition.get("id"),
        "doi": deposition.get("doi"),
        "doi_url": deposition.get("doi_url"),
        "record_url": deposition.get("record_url") or deposition.get("links", {}).get("html"),
        "archive": str(archive),
        "uploaded_file": upload.get("key") or upload.get("filename") or archive.name,
    }
    receipt_path = repo / args.receipt
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))

    if temp_dir is not None:
        temp_dir.cleanup()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
