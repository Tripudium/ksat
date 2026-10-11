#!/usr/bin/env python3
"""Audit retained k-SAT attempts and plot phase probabilities without censoring bias.

Only the Python standard library is needed to collect and validate results.
Rendering requires the environment's pinned matplotlib and its numpy dependency.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import textwrap


IDENTITY_FIELDS = (
    "id", "n", "k", "m", "alpha_requested", "alpha_actual", "replicate", "seed",
    "chunk_id",
)
RESULT_STATUSES = {
    "SAT-verified", "UNSAT-verified", "UNSAT-unchecked", "unknown", "error",
}
VERIFIED = {"SAT-verified", "UNSAT-verified"}
COUNT_KEYS = {
    "SAT-verified": "sat_verified",
    "UNSAT-verified": "unsat_verified",
    "UNSAT-unchecked": "unsat_unchecked",
    "unknown": "unknown",
    "error": "error",
    "pending": "pending",
}
CELL_FIELDS = (
    "n", "k", "m", "alpha_requested", "alpha_actual", "planned_repetitions",
    "sat_verified", "unsat_verified", "unsat_unchecked", "unknown", "error",
    "pending", "unresolved", "unresolved_fraction", "p_lower", "p_upper",
    "p_estimate", "hoeffding_epsilon_95", "confidence_lower_95",
    "confidence_upper_95", "complete",
)
INSTANCE_FIELDS = IDENTITY_FIELDS + (
    "status", "reason", "selected_attempt_id", "completed_attempt_count",
    "selected_process_wall_seconds", "input_sha256", "diagnostics",
)


class CollectionError(ValueError):
    """The run cannot be summarized under the declared schema."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_integer(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float)) and not isinstance(value, bool)
        and math.isfinite(value)
    )


def _read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON document must be an object")
    return value


def load_manifest(run_dir: Path) -> tuple[dict, str]:
    path = run_dir / "manifest.json"
    try:
        data = path.read_bytes()
        manifest = json.loads(data)
    except (OSError, ValueError) as exc:
        raise CollectionError(f"Cannot read {path}: {exc}") from exc
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise CollectionError("Expected manifest schema_version 1")
    config = manifest.get("config")
    instances = manifest.get("instances")
    if not isinstance(config, dict) or not isinstance(instances, list) or not instances:
        raise CollectionError("Manifest must contain config and nonempty instances")
    if config.get("proof_policy") != "required":
        raise CollectionError("This plotter requires proof_policy='required'")
    n_values = config.get("n_values")
    alpha_values = config.get("alpha_values")
    repetitions = config.get("repetitions")
    k = config.get("k")
    if not _is_integer(k) or k < 2:
        raise CollectionError("Manifest k must be an integer >= 2")
    if (
        not isinstance(n_values, list) or not n_values
        or any(not _is_integer(n) or n < k for n in n_values)
        or len(set(n_values)) != len(n_values)
        or not isinstance(alpha_values, list) or not alpha_values
        or any(not isinstance(a, str) for a in alpha_values)
        or len(set(alpha_values)) != len(alpha_values)
        or not _is_integer(repetitions) or repetitions < 1
    ):
        raise CollectionError("Invalid n_values, alpha_values, or repetitions")
    try:
        alphas = [float(a) for a in alpha_values]
    except ValueError as exc:
        raise CollectionError("alpha_values must be finite decimal strings") from exc
    if any(not math.isfinite(a) or a < 0 for a in alphas):
        raise CollectionError("alpha_values must be finite nonnegative decimals")
    if len(set(alphas)) != len(alphas):
        raise CollectionError("Numerically duplicate alpha_values are ambiguous")
    num_chunks = manifest.get("num_chunks")
    if not _is_integer(num_chunks) or num_chunks < 1:
        raise CollectionError("Invalid num_chunks")
    seen_ids = set()
    planned = {}
    physical_cells = {}
    requested_cells = {}
    for instance in instances:
        if not isinstance(instance, dict) or any(f not in instance for f in IDENTITY_FIELDS):
            raise CollectionError("Each planned instance needs all identity fields")
        identifier = instance["id"]
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", identifier):
            raise CollectionError("Invalid instance id")
        if identifier in seen_ids:
            raise CollectionError(f"Duplicate planned instance id: {identifier}")
        seen_ids.add(identifier)
        if any(not _is_integer(instance[f]) for f in ("n", "k", "m", "replicate", "seed", "chunk_id")):
            raise CollectionError(f"Noninteger instance identity: {identifier}")
        n, m, alpha = instance["n"], instance["m"], instance["alpha_requested"]
        if (
            n not in n_values or instance["k"] != k or m < 0
            or alpha not in alpha_values
            or not 0 <= instance["replicate"] < repetitions
            or not 0 <= instance["chunk_id"] < num_chunks
            or not _finite_number(instance["alpha_actual"])
            or not math.isclose(instance["alpha_actual"], m / n, rel_tol=1e-12, abs_tol=1e-12)
        ):
            raise CollectionError(f"Instance identity disagrees with config: {identifier}")
        planned_key = (n, alpha, instance["replicate"])
        if planned_key in planned:
            raise CollectionError(f"Duplicate planned cell/replicate: {planned_key}")
        planned[planned_key] = identifier
        physical_key = (n, k, m)
        previous_m = requested_cells.setdefault((n, alpha), m)
        if previous_m != m:
            raise CollectionError("One requested-density cell contains different clause counts")
        previous_alpha = physical_cells.setdefault(physical_key, alpha)
        if previous_alpha != alpha:
            raise CollectionError("Requested densities map to the same (n,k,m) cell")
    expected = {
        (n, a, r) for n in n_values for a in alpha_values for r in range(repetitions)
    }
    if set(planned) != expected:
        raise CollectionError("Manifest instances do not cover the complete configured grid")
    return manifest, _sha256(data)


def _attempt_time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("missing started_utc")
    stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("started_utc must contain a timezone")
    return stamp.astimezone(timezone.utc)


def _validate_artifacts(run_dir: Path, result: dict) -> None:
    required = set()
    if result["status"] in VERIFIED:
        required = {"input", "witness" if result["status"] == "SAT-verified" else "proof"}
    root = run_dir.resolve()
    for artifact in ("input", "witness", "proof"):
        hash_field = artifact + "_sha256"
        present = artifact in result or hash_field in result
        if not present and artifact not in required:
            continue
        relative = result.get(artifact)
        expected = result.get(hash_field)
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise ValueError(f"missing or invalid {artifact} artifact path")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise ValueError(f"missing or invalid {hash_field}")
        path = (root / relative).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f"{artifact} artifact escapes run directory")
        if not path.is_file():
            raise ValueError(f"missing {artifact} artifact: {relative}")
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for block in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(block)
        if digest.hexdigest() != expected:
            raise ValueError(f"{hash_field} artifact mismatch")


def select_instance_result(run_dir: Path, instance: dict, manifest_hash: str) -> dict:
    """Choose one outcome per planned instance, failing closed on suspect data."""
    paths = sorted((run_dir / "attempts" / instance["id"]).glob("*/result.json"))
    record = {field: instance[field] for field in IDENTITY_FIELDS}
    record.update(
        status="pending", reason="No completed result.json", selected_attempt_id=None,
        completed_attempt_count=len(paths), selected_process_wall_seconds=None,
        input_sha256=None, diagnostics=[],
    )
    attempts = []
    for path in paths:
        try:
            result = _read_json(path)
            for field in IDENTITY_FIELDS:
                if (
                    field not in result or result[field] != instance[field]
                    or (_is_integer(instance[field]) and not _is_integer(result[field]))
                ):
                    raise ValueError(f"identity mismatch: {field}")
            if result.get("manifest_sha256") != manifest_hash:
                raise ValueError("manifest_sha256 mismatch")
            if result.get("attempt_id") != path.parent.name:
                raise ValueError("attempt_id differs from its directory")
            status = result.get("status")
            if status not in RESULT_STATUSES:
                raise ValueError(f"invalid final status: {status!r}")
            started = _attempt_time(result.get("started_utc"))
            input_hash = result.get("input_sha256")
            if input_hash is not None and not (
                isinstance(input_hash, str) and re.fullmatch(r"[0-9a-f]{64}", input_hash)
            ):
                raise ValueError("invalid input_sha256")
            if status in VERIFIED and input_hash is None:
                raise ValueError("verified outcome lacks input_sha256")
            _validate_artifacts(run_dir, result)
            wall = result.get("process_wall_seconds")
            if wall is not None and (not _finite_number(wall) or wall < 0):
                raise ValueError("invalid process_wall_seconds")
            attempts.append((started, result["attempt_id"], result))
        except (OSError, ValueError, TypeError) as exc:
            record["diagnostics"].append(f"{path.relative_to(run_dir)}: {exc}")
    if record["diagnostics"]:
        record.update(status="error", reason="Invalid retained attempt; outcome not trusted")
        return record
    if not attempts:
        return record
    attempts.sort(key=lambda item: (item[0], item[1]))
    input_hashes = {a[2].get("input_sha256") for a in attempts} - {None}
    if len(input_hashes) > 1:
        record.update(status="error", reason="Retained attempts have different input hashes")
        record["diagnostics"].append("Same planned instance has inconsistent input_sha256 values")
        return record
    verified = [a for a in attempts if a[2]["status"] in VERIFIED]
    if len({a[2]["status"] for a in verified}) > 1:
        record.update(status="error", reason="Conflicting verified SAT and UNSAT outcomes")
        record["diagnostics"].append("Conflicting certificates require investigation; neither outcome counted")
        return record
    selected = (verified[0] if verified else attempts[-1])[2]
    record.update(
        status=selected["status"], reason=selected.get("reason", ""),
        selected_attempt_id=selected["attempt_id"],
        selected_process_wall_seconds=selected.get("process_wall_seconds"),
        input_sha256=selected.get("input_sha256"),
    )
    return record


def summarize_cells(instances: list[dict]) -> list[dict]:
    grouped = {}
    for item in instances:
        grouped.setdefault((item["n"], item["k"], item["m"]), []).append(item)
    cells = []
    for (n, k, m), records in sorted(grouped.items()):
        counts = dict.fromkeys(COUNT_KEYS.values(), 0)
        for record in records:
            counts[COUNT_KEYS[record["status"]]] += 1
        repetitions = len(records)
        lower = counts["sat_verified"] / repetitions
        upper = 1 - counts["unsat_verified"] / repetitions
        unresolved = repetitions - counts["sat_verified"] - counts["unsat_verified"]
        epsilon = math.sqrt(math.log(40) / (2 * repetitions))
        cells.append({
            "n": n, "k": k, "m": m,
            "alpha_requested": records[0]["alpha_requested"],
            "alpha_actual": m / n, "planned_repetitions": repetitions,
            **counts, "unresolved": unresolved,
            "unresolved_fraction": unresolved / repetitions,
            "p_lower": lower, "p_upper": upper,
            "p_estimate": lower if unresolved == 0 else None,
            "hoeffding_epsilon_95": epsilon,
            "confidence_lower_95": max(0.0, lower - epsilon),
            "confidence_upper_95": min(1.0, upper + epsilon),
            "complete": unresolved == 0,
        })
    return cells


def collect_run(run_dir: Path, *, allow_partial: bool = False) -> dict:
    run_dir = Path(run_dir).resolve()
    manifest, manifest_hash = load_manifest(run_dir)
    identifiers = {item["id"] for item in manifest["instances"]}
    attempts_root = run_dir / "attempts"
    if attempts_root.exists():
        for directory in attempts_root.iterdir():
            if directory.is_dir() and directory.name not in identifiers and any(directory.glob("*/result.json")):
                raise CollectionError(f"Completed result for unplanned instance: {directory.name}")
    records = [select_instance_result(run_dir, item, manifest_hash) for item in manifest["instances"]]
    pending = sum(record["status"] == "pending" for record in records)
    if pending and not allow_partial:
        raise CollectionError(
            f"{pending}/{len(records)} planned instances have no completed result; "
            "use --allow-partial to retain them as unresolved pending outcomes"
        )
    counts = dict.fromkeys(COUNT_KEYS.values(), 0)
    for record in records:
        counts[COUNT_KEYS[record["status"]]] += 1
    return {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir), "manifest_sha256": manifest_hash,
        "config": manifest["config"], "planned_instances": len(records),
        "synthetic_fixture": manifest.get("synthetic_fixture") is True,
        "allow_partial": allow_partial, "counts": counts,
        "cells": summarize_cells(records), "instances": records,
        "uncertainty": {
            "sample_interval": "[SAT-verified/R, 1-UNSAT-verified/R]; R is planned repetitions",
            "confidence": "95% pointwise Hoeffding envelope, epsilon=sqrt(log(40)/(2R))",
            "assumption": "Independent formula replicates from the stated uniform clause ensemble",
            "multiplicity": "Pointwise intervals are not simultaneous confidence bands over the grid",
            "timeouts": "Unchecked, unknown, error and pending outcomes remain unresolved",
            "verification": "Status is audited from runner records; this plotter does not rerun proof checkers",
        },
    }


def _write_csv(path: Path, records: list[dict], fields: tuple[str, ...]) -> None:
    with path.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            row = dict(record)
            if "diagnostics" in row:
                row["diagnostics"] = json.dumps(row["diagnostics"], ensure_ascii=False)
            writer.writerow(row)


def render_plots(summary: dict, output_dir: Path) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    import numpy as np

    config = summary["config"]
    n_values = sorted(config["n_values"])
    alpha_values = sorted(config["alpha_values"], key=float)
    lookup = {(c["n"], c["alpha_requested"]): c for c in summary["cells"]}
    k = config["k"]
    run_label = "Run: " + " ".join(str(config.get("name", "unnamed run")).split())
    unresolved = sum(summary["counts"][key] for key in ("unsat_unchecked", "unknown", "error", "pending"))
    ensemble = f"Random {k}-SAT | uniform proper clauses, sampled with replacement"
    subtitle = (
        f"{summary['planned_instances']:,} planned instances; {unresolved:,} unresolved "
        "(including timeouts, unchecked results, errors and pending jobs)"
    )
    fixture_prefix = "SYNTHETIC FIXTURE | " if summary.get("synthetic_fixture") else ""
    if fixture_prefix:
        ensemble = fixture_prefix + ensemble
        subtitle = "Software test only; not empirical threshold data. " + subtitle
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titleweight": "semibold", "savefig.dpi": 180,
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    outputs = []

    def save(fig, stem):
        for suffix in ("png", "pdf"):
            name = f"{stem}.{suffix}"
            fig.savefig(output_dir / name, bbox_inches="tight", facecolor="white")
            outputs.append(name)
        plt.close(fig)

    def footer(fig, paragraphs, width, minimum_reserve=0.20):
        text = "\n".join(textwrap.fill(paragraph, width=width) for paragraph in [run_label, *paragraphs])
        fig.text(0.5, 0.02, text, ha="center", va="bottom", fontsize=9)
        # Reserve physical space for every wrapped line, separately from axes
        # ticks and labels. Negative figure coordinates plus bbox_inches='tight'
        # do not reserve this space and can overlap labels on small grids.
        return max(minimum_reserve, 0.055 + 0.18 * len(text.splitlines()) / fig.get_figheight())

    def matrix(field):
        return np.array([
            [np.nan if lookup[n, a][field] is None else lookup[n, a][field] for a in alpha_values]
            for n in n_values
        ], dtype=float)

    def decorate(ax):
        tick_step = max(1, math.ceil(len(alpha_values) / 10))
        x_ticks = list(range(0, len(alpha_values), tick_step))
        if x_ticks[-1] != len(alpha_values) - 1:
            x_ticks.append(len(alpha_values) - 1)
        ax.set_xticks(x_ticks, [alpha_values[i] for i in x_ticks], rotation=35, ha="right")
        y_step = max(1, math.ceil(len(n_values) / 15))
        y_ticks = list(range(0, len(n_values), y_step))
        if y_ticks[-1] != len(n_values) - 1:
            y_ticks.append(len(n_values) - 1)
        ax.set_yticks(y_ticks, [str(n_values[i]) for i in y_ticks])
        ax.set_xlabel(r"Requested clause density $\alpha$")
        ax.set_ylabel("Variables n")

    fig, axes = plt.subplots(1, 3, figsize=(15, max(4.8, min(8, 0.3 * len(n_values) + 3))), sharey=True)
    specifications = [
        ("p_lower", "SAT fraction: lower bound", "viridis"),
        ("p_upper", "SAT fraction: upper bound", "viridis"),
        ("unresolved_fraction", "Unresolved fraction", "magma"),
    ]
    for ax, (field, title, cmap) in zip(axes, specifications):
        im = ax.imshow(matrix(field), origin="lower", aspect="auto", vmin=0, vmax=1, cmap=cmap, interpolation="nearest")
        ax.set_title(title, pad=12)
        decorate(ax)
        fig.colorbar(im, ax=ax, fraction=0.045, pad=0.025, label="Fraction of all planned replicates")
    fig.suptitle(ensemble, fontsize=15, y=0.99)
    bottom = footer(fig, [subtitle, "Bounds show sample censoring, not sampling confidence."], 165)
    fig.tight_layout(rect=(0, bottom, 1, 0.94), w_pad=2)
    save(fig, "phase_bounds")

    estimate = matrix("p_estimate")
    if np.any(np.isfinite(estimate)):
        fig, ax = plt.subplots(figsize=(8, max(4.8, min(8, 0.3 * len(n_values) + 3))))
        cmap = plt.get_cmap("viridis").copy()
        cmap.set_bad("#e5e7eb")
        im = ax.imshow(np.ma.masked_invalid(estimate), origin="lower", aspect="auto", vmin=0, vmax=1, cmap=cmap, interpolation="nearest")
        decorate(ax)
        fig.colorbar(im, ax=ax, label="Verified SAT / planned replicates")
        ax.set_title(f"{fixture_prefix}Random {k}-SAT: estimates in fully resolved cells", pad=14)
        valid = estimate[np.isfinite(estimate)]
        levels = [value for value in (0.05, 0.5, 0.95) if valid.min() < value < valid.max()]
        if levels and min(estimate.shape) >= 2:
            # corner_mask=False excludes a whole grid square if any corner is unresolved.
            contours = ax.contour(np.ma.masked_invalid(estimate), levels=levels, colors="white", linewidths=1.1, corner_mask=False)
            if any(len(segment) for segments in contours.allsegs for segment in segments):
                ax.clabel(contours, inline=True, fmt={v: f"{100*v:g}%" for v in levels}, fontsize=8)
        bottom = footer(fig, ["Gray = unresolved cell. Contours use only complete grid squares; no monotonic fit or smoothing.", "Empirical contours are not confidence contours or asymptotic threshold claims."], 110)
        fig.tight_layout(rect=(0, bottom, 1, 0.98))
        save(fig, "phase_complete_estimates")

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = plt.get_cmap("tab10")
    n_handles = []
    for index, n in enumerate(n_values):
        cells = sorted((c for c in summary["cells"] if c["n"] == n), key=lambda c: c["alpha_actual"])
        x = np.array([c["alpha_actual"] for c in cells])
        lower = np.array([c["p_lower"] for c in cells])
        upper = np.array([c["p_upper"] for c in cells])
        confidence_lower = np.array([c["confidence_lower_95"] for c in cells])
        confidence_upper = np.array([c["confidence_upper_95"] for c in cells])
        point = np.array([np.nan if c["p_estimate"] is None else c["p_estimate"] for c in cells])
        color = colors(index % 10)
        ax.fill_between(x, confidence_lower, confidence_upper, color=color, alpha=0.075)
        ax.fill_between(x, lower, upper, color=color, alpha=0.2)
        ax.plot(x, lower, color=color, linestyle="--", linewidth=0.9)
        ax.plot(x, upper, color=color, linestyle="--", linewidth=0.9)
        ax.plot(x, point, color=color, marker="o", markersize=3.5, linewidth=1.4)
        # Vertical segments make uncertainty visible even for a one-density grid.
        ax.vlines(x, confidence_lower, confidence_upper, color=color, alpha=0.25, linewidth=0.8)
        ax.vlines(x, lower, upper, color=color, alpha=0.75, linewidth=1.5)
        n_handles.append(Line2D([0], [0], color=color, linewidth=2, label=f"n = {n}"))
    ax.set(xlabel=r"Actual clause density $m/n$", ylabel="Satisfiability probability / sample bounds", ylim=(-0.02, 1.02))
    ax.set_title(f"{fixture_prefix}Random {k}-SAT: finite-size curves and uncertainty", pad=14)
    ax.grid(axis="y", color="#d1d5db", linewidth=0.5)
    ax.legend(handles=n_handles, loc="upper right", ncol=max(1, math.ceil(len(n_values) / 8)), fontsize=9)
    bottom = footer(fig, ["Solid markers: fully resolved estimates. Dashed bounds/darker fill: unresolved-sample interval.", "Pale envelope: 95% pointwise Hoeffding uncertainty, including unresolved outcomes; not simultaneous over the grid.", "Lines join measured density points without a fitted scaling law. " + subtitle], 125, minimum_reserve=0.27)
    fig.tight_layout(rect=(0, bottom, 1, 0.98))
    save(fig, "finite_size_curves")
    summary["plotting"] = {
        "matplotlib_version": matplotlib.__version__,
        "python_version": sys.version,
        "script_sha256": _sha256(Path(__file__).read_bytes()),
        "files": outputs,
        "heatmap_axes": "Requested alpha and n are discrete grid cells; spacing is categorical",
        "curve_axes": "Actual alpha=m/n is numerical; n labels identify each curve",
    }
    return outputs


def write_outputs(summary: dict, output_dir: Path) -> None:
    """Create a fresh output directory; never overwrite an earlier collection."""
    output_dir = Path(output_dir)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(exist_ok=False)
    _write_csv(output_dir / "summary.csv", summary["cells"], CELL_FIELDS)
    _write_csv(output_dir / "instances.csv", summary["instances"], INSTANCE_FIELDS)
    render_plots(summary, output_dir)
    with (output_dir / "summary.json").open("x", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, allow_nan=False)
        handle.write("\n")
    with (output_dir / "README.txt").open("x", encoding="utf-8") as handle:
        handle.write(
            "Random k-SAT phase diagrams\n"
            f"Manifest SHA-256: {summary['manifest_sha256']}\n"
            "summary.csv: one row per planned (n,k,m) cell.\n"
            "instances.csv: selected outcomes and retained-attempt audit diagnostics.\n"
            "summary.json: machine-readable summaries, assumptions and plotting provenance.\n"
            "An empty p_estimate CSV field / JSON null means unresolved replicates remain.\n"
            "Every planned replicate remains in the denominator, including timeouts.\n"
            "Sample-censoring bounds differ from the wider 95% pointwise Hoeffding envelope.\n"
            "Retained attempts are observations of the same instance, not extra samples.\n"
            "The plotter audits statuses and hashes; it does not independently recheck certificates.\n"
            "The PNG/PDF diagrams are empirical finite-size results, not threshold proofs.\n"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="New directory; must not already exist")
    parser.add_argument("--allow-partial", action="store_true", help="Keep missing results as pending/unknown, in every denominator")
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error(f"Output already exists; choose a new directory: {args.output}")
    try:
        summary = collect_run(args.run_dir, allow_partial=args.allow_partial)
        write_outputs(summary, args.output)
    except (CollectionError, OSError, ImportError) as exc:
        parser.exit(2, f"Collection failed: {exc}\n")
    print(f"Wrote {len(summary['cells'])} cells from {summary['planned_instances']} planned instances to {args.output}")
    if summary["counts"]["error"]:
        print(f"Warning: {summary['counts']['error']} instance(s) remain errors; see instances.csv", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
