#!/usr/bin/env python3
"""Record/check a prepared uv environment without syncing or contacting a network."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

PROJECT_FILES = ('pyproject.toml', 'uv.lock', '.python-version')
SOURCE_RELATIVE = 'code/vendor/drat-trim/drat-trim.c'
SOURCE_SHA256 = 'd834b649f437e091597f5347f259b9f681087f89ca0844d0cee250a1a1a0c2ee'
UPSTREAM_COMMIT = '2e3b2dc0ecf938addbd779d42877b6ed69d9a985'


def fail(message: str) -> None:
    raise SystemExit('Environment check failed: '+message+
                     '\nRun slurm/setup_environment.sh again in this checkout before submitting or running jobs.')


def digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as error:
        fail(f'cannot read {path}: {error}')


def packages() -> dict[str, str]:
    names = {re.sub(r'[-_.]+', '-', dist.metadata['Name']).lower()
             for dist in importlib.metadata.distributions() if dist.metadata['Name']}
    return {name: importlib.metadata.version(name) for name in sorted(names)}


def state(project: Path, checker: Path) -> dict:
    if sys.version_info[:2] != (3, 12):
        fail('the project requires Python 3.12; active interpreter is '+platform.python_version())
    if not checker.is_file() or not os.access(checker, os.X_OK):
        fail(f'proof checker is missing or not executable: {checker}')
    source_hash = digest(project/SOURCE_RELATIVE)
    if source_hash != SOURCE_SHA256:
        fail('vendored proof-checker source differs from the pinned source revision')
    return {
        'project_sha256': {name: digest(project/name) for name in PROJECT_FILES},
        'python_version': platform.python_version(),
        'python_executable': sys.executable,
        'packages': packages(),
        'module_selection': os.environ.get('KSAT_MODULES', ''),
        'loaded_modules': os.environ.get('LOADEDMODULES', ''),
        'drat_trim_source_sha256': source_hash,
        'drat_trim_binary_sha256': digest(checker),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('record', 'check'))
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--environment', type=Path, required=True)
    parser.add_argument('--checker', type=Path, required=True)
    parser.add_argument('--compiler', default='cc')
    parser.add_argument('--uv-version', default='not supplied')
    args = parser.parse_args()
    current = state(args.project, args.checker)
    destination = args.environment/'ksat-environment.json'
    if args.action == 'record':
        now = datetime.now(timezone.utc)
        current.update(
            schema_version=1, created_utc=now.isoformat(),
            project_directory=str(args.project.resolve()),
            environment_directory=str(args.environment.resolve()),
            platform=platform.platform(), uv_version=args.uv_version,
            setup_command='uv sync --locked',
            drat_trim_upstream_commit=UPSTREAM_COMMIT,
            compiler=args.compiler, compiler_flags=['-std=c99', '-O2'],
            compiler_version=subprocess.run([args.compiler, '--version'], text=True,
                                             capture_output=True, check=False).stdout,
            proof_checker_preflight='Deferred to preflight inside the allocation.',
        )
        content = json.dumps(current, indent=2, sort_keys=True)+'\n'
        history = args.environment/f'ksat-setup-{now:%Y%m%dT%H%M%S.%fZ}-{os.getpid()}.json'
        with history.open('x') as stream:
            stream.write(content)
        temporary = destination.with_name(destination.name+f'.{os.getpid()}.tmp')
        with temporary.open('x') as stream:
            stream.write(content)
        os.replace(temporary, destination)
        print(f'Environment provenance: {history}')
    else:
        try:
            recorded = json.loads(destination.read_text())
        except (OSError, ValueError) as error:
            fail(f'prepared-environment record is missing or invalid: {destination}: {error}')
        if recorded.get('schema_version') != 1:
            fail('prepared-environment record has an unsupported schema')
        for name, expected in current['project_sha256'].items():
            if recorded.get('project_sha256', {}).get(name) != expected:
                fail(f'{name} changed since environment setup (for example after git pull)')
        for name in ('python_version', 'packages', 'module_selection', 'loaded_modules',
                     'drat_trim_source_sha256', 'drat_trim_binary_sha256'):
            if recorded.get(name) != current[name]:
                fail(f'{name} differs from the prepared environment')
        print('Prepared environment matches project lock, Python, packages, modules and checker.')


if __name__ == '__main__':
    main()
