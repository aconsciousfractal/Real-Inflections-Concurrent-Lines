"""Build the article with a preinstalled TeX distribution.

Generated files remain under build/ and output/.
Run from any directory: python -X utf8 path/to/build_manuscript.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "build"
OUTPUT = ROOT / "output" / "pdf"
STEM = "real_inflections_concurrent_lines"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    start = time.perf_counter()
    started = datetime.now(timezone.utc).isoformat()
    BUILD.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    executables = {name: shutil.which(name) for name in ("pdflatex", "bibtex")}
    missing = [name for name, path in executables.items() if path is None]
    if missing:
        raise RuntimeError("Missing local TeX executables: " + ", ".join(missing))

    # BibTeX resolves these local copies without platform-dependent BIBINPUTS.
    for filename in (STEM + ".tex", "references.bib"):
        shutil.copyfile(ROOT / filename, BUILD / filename)
    version = subprocess.run(
        [executables["pdflatex"], "--version"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=20, check=True,
    ).stdout
    installer_flags = ["--disable-installer"] if "miktex" in version.lower() else []
    latex = [
        executables["pdflatex"], *installer_flags,
        "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
        STEM + ".tex",
    ]
    commands = [
        latex,
        [executables["bibtex"], *installer_flags, STEM],
        latex,
        latex,
    ]
    runs = []
    for index, command in enumerate(commands, 1):
        tick = time.perf_counter()
        result = subprocess.run(
            command, cwd=BUILD, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=120,
        )
        log = BUILD / f"build_step_{index}.txt"
        log.write_text(result.stdout + result.stderr, encoding="utf-8")
        runs.append({
            "command": [Path(command[0]).name, *command[1:]],
            "exit_code": result.returncode,
            "elapsed_seconds": round(time.perf_counter() - tick, 6),
            "log": log.relative_to(ROOT).as_posix(),
        })
        if result.returncode:
            print(result.stdout[-7000:] + result.stderr[-2000:])
            raise RuntimeError(f"TeX build failed at step {index}; see {log}")

    final_log = (BUILD / (STEM + ".log")).read_text(
        encoding="utf-8", errors="replace"
    )
    warnings = [
        line.strip() for line in final_log.splitlines()
        if "Warning:" in line or "Overfull" in line or "Underfull" in line
    ]
    blockers = [
        line for line in warnings
        if "undefined" in line.lower() or "Rerun" in line or "Overfull" in line
    ]
    if blockers:
        raise RuntimeError("Unresolved final TeX diagnostics: " + repr(blockers))
    target = OUTPUT / (STEM + ".pdf")
    shutil.copyfile(BUILD / (STEM + ".pdf"), target)
    page_match = re.search(r"Output written on .+ \((\d+) pages?", final_log)
    receipt = {
        "schema": "manuscript-build-v1",
        "started_utc": started,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "verdict": "BUILD_PASS_VISUAL_REVIEW_PENDING",
        "scope": "Typesetting only; no independent mathematical review.",
        "sources": {
            filename: sha256(ROOT / filename)
            for filename in (STEM + ".tex", "references.bib", "build_manuscript.py")
        },
        "output": target.relative_to(ROOT).as_posix(),
        "output_sha256": sha256(target),
        "pages": int(page_match.group(1)) if page_match else None,
        "commands": runs,
        "warnings": warnings,
        "visual_review": "pending",
    }
    (BUILD / "build_receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "verdict": receipt["verdict"], "pages": receipt["pages"],
        "output": str(target), "sha256": receipt["output_sha256"],
        "warnings": warnings,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

