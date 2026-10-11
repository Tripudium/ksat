#!/usr/bin/env python3
"""Local shell integration checks with mocked sbatch/srun; never contacts SLURM."""
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

scripts = Path(__file__).resolve().parent
if sys.version_info[:2] != (3, 12):
    raise SystemExit('Run these checks with the uv project Python 3.12 (uv run --locked python ...).')
for name in ('common.sh', 'setup_environment.sh', 'submit_array.sh', 'run_array.sbatch'):
    subprocess.run(['bash', '-n', str(scripts/name)], check=True)

with tempfile.TemporaryDirectory(prefix='ksat-slurm-check-') as folder:
    temp = Path(folder)
    project = temp/'project with spaces'
    run = project/'run with spaces'
    envdir = project/'test venv'
    mockbin = temp/'mock commands with spaces'
    for directory in (project/'code/vendor/drat-trim', run, envdir/'bin', mockbin):
        directory.mkdir(parents=True)
    target_scripts = project/'experiments/E002_blythe_phase_diagrams/slurm'
    target_scripts.mkdir(parents=True)
    shutil.copy(scripts/'common.sh', target_scripts/'common.sh')
    shutil.copy(scripts/'environment_guard.py', target_scripts/'environment_guard.py')
    shutil.copy(scripts.parents[2]/'code/vendor/drat-trim/drat-trim.c',
                project/'code/vendor/drat-trim/drat-trim.c')
    (project/'pyproject.toml').write_text('[project]\nname="mock-project"\nrequires-python=">=3.12,<3.13"\n')
    (project/'uv.lock').write_text('# mocked lock snapshot; never supplied to uv\n')
    (project/'.python-version').write_text('3.12\n')
    (envdir/'bin/python').symlink_to(sys.executable)
    checker = envdir/'bin/drat-trim'
    checker.write_text('#!/bin/sh\nexit 0\n'); checker.chmod(0o755)
    (run/'manifest.json').write_text(json.dumps({'num_chunks': 3}))
    (project/'code/ksat_experiments.py').write_text('''import json, os, pathlib, sys
with open(os.environ['MOCK_PIPELINE_LOG'], 'a') as log:
    log.write(json.dumps(sys.argv[1:])+'\\n')
if sys.argv[1] == 'preflight':
    pathlib.Path(sys.argv[sys.argv.index('--output')+1]).write_text('{"mock": true}\\n')
''')
    (mockbin/'sbatch.py').write_text('''import json, os, sys
with open(os.environ['MOCK_SBATCH_LOG'], 'a') as log:
    log.write(json.dumps(sys.argv[1:])+'\\n')
print('12345')
''')
    (mockbin/'srun.py').write_text('''import os, sys
args = sys.argv[1:]
while args and args[0].startswith('--'):
    args.pop(0)
os.execv(args[0], args)
''')
    # Kernel shebang parsing cannot quote an interpreter path containing spaces.
    # A /bin/sh launcher can safely quote both the actual interpreter and script.
    # Use the fixture interpreter with spaces so every run exercises this case.
    for command in ('sbatch', 'srun'):
        (mockbin/command).write_text(
            '#!/bin/sh\nexec '+shlex.quote(str(envdir/'bin/python'))+' '+
            shlex.quote(str(mockbin/(command+'.py')))+' "$@"\n')
    (mockbin/'mock-cc').write_text('#!/bin/sh\nprintf "mock compiler (not used to compile anything)\\n"\n')
    for file in mockbin.iterdir(): file.chmod(0o755)
    env = dict(os.environ, PATH=str(mockbin)+os.pathsep+os.environ['PATH'],
               KSAT_PROJECT_DIR=str(project), KSAT_ENV_DIR=str(envdir),
               KSAT_MODULES='', PYTHONNOUSERSITE='1',
               MOCK_SBATCH_LOG=str(temp/'sbatch.jsonl'),
               MOCK_PIPELINE_LOG=str(temp/'pipeline.jsonl'))
    env.pop('KSAT_DRAT_TRIM', None)
    env.pop('KSAT_USE_CURRENT_ENV', None)
    subprocess.run([str(envdir/'bin/python'), str(target_scripts/'environment_guard.py'),
                    'record', '--project', str(project), '--environment', str(envdir),
                    '--checker', str(checker), '--compiler', str(mockbin/'mock-cc'),
                    '--uv-version', 'mocked; uv never executed'], env=env,
                   capture_output=True, text=True, check=True)
    helper = ['bash', str(scripts/'submit_array.sh'), str(run)]
    dry = subprocess.run(helper, env=env, cwd=temp, capture_output=True, text=True)
    assert dry.returncode == 0, (dry.stdout, dry.stderr)
    assert 'Dry run only' in dry.stdout and '--array=0-2%4' in dry.stdout
    assert not (temp/'sbatch.jsonl').exists()
    subprocess.run(helper+['--submit', '--cpus', '4', '--concurrency', '2',
                           '--account', 'test-only-account', '--retry-unknown'],
                   env=env, cwd=temp, capture_output=True, text=True, check=True)
    submitted = json.loads((temp/'sbatch.jsonl').read_text())
    assert '--array=0-2%2' in submitted and '--cpus-per-task=4' in submitted
    assert '--account=test-only-account' in submitted and Path(submitted[-1]).resolve() == run.resolve()
    assert (run/'slurm-logs').is_dir()
    for invalid in (['--cpus','169'], ['--concurrency','0'],
                    ['--mem-per-cpu','4592'], ['--time','48:00:01']):
        result = subprocess.run(helper+invalid, env=env, capture_output=True, text=True)
        assert result.returncode != 0, invalid
    # Simulate SLURM copying the batch script out of its repository location.
    spooled = temp/'spooled-script'
    shutil.copy(scripts/'run_array.sbatch', spooled)
    worker_env = dict(env, SLURM_SUBMIT_DIR='/', SLURM_ARRAY_TASK_ID='2',
                      SLURM_CPUS_PER_TASK='4', SLURM_ARRAY_JOB_ID='12345',
                      KSAT_RETRY_UNKNOWN='1')
    subprocess.run(['bash', str(spooled), str(run)], env=worker_env, cwd=temp,
                   capture_output=True, text=True, check=True)
    calls = [json.loads(line) for line in (temp/'pipeline.jsonl').read_text().splitlines()]
    assert len(calls) == 2 and calls[0][0] == 'preflight' and calls[1][0] == 'run'
    assert calls[1][calls[1].index('--chunk-id')+1] == '2'
    assert calls[1][calls[1].index('--workers')+1] == '4'
    assert '--retry-unknown' in calls[1]
    assert len(list((run/'slurm-logs').glob('preflight-*.json'))) == 1

    # A changed lock is rejected before submission or any solver/preflight call.
    lock = project/'uv.lock'
    original_lock = lock.read_text()
    lock.write_text(original_lock+'# changed after setup\n')
    stale_submit = subprocess.run(helper+['--submit'], env=env, capture_output=True, text=True)
    assert stale_submit.returncode != 0 and 'uv.lock changed' in stale_submit.stderr
    stale_worker = subprocess.run(['bash', str(spooled), str(run)], env=worker_env,
                                  capture_output=True, text=True)
    assert stale_worker.returncode != 0 and 'uv.lock changed' in stale_worker.stderr
    assert len((temp/'sbatch.jsonl').read_text().splitlines()) == 1
    assert len((temp/'pipeline.jsonl').read_text().splitlines()) == 2
    lock.write_text(original_lock)
    prepared = envdir/'ksat-environment.json'
    prepared_text = prepared.read_text()
    prepared.unlink()
    missing = subprocess.run(helper, env=env, capture_output=True, text=True)
    assert missing.returncode != 0 and 'record is missing' in missing.stderr
    prepared.write_text(prepared_text)
    altered = json.loads(prepared_text)
    altered['packages']['mock-unexpected-package'] = '0.0'
    prepared.write_text(json.dumps(altered))
    packages_changed = subprocess.run(helper, env=env, capture_output=True, text=True)
    assert packages_changed.returncode != 0 and 'packages differs' in packages_changed.stderr
    prepared.write_text(prepared_text)
    checker.write_text('#!/bin/sh\n# changed checker binary\nexit 0\n')
    checker_changed = subprocess.run(helper, env=env, capture_output=True, text=True)
    assert checker_changed.returncode != 0 and 'drat_trim_binary_sha256 differs' in checker_changed.stderr

print(json.dumps({'shell_syntax': 'passed', 'mock_submission': 'passed',
                  'default_dry_run': 'passed', 'paths_with_spaces': 'passed',
                  'mock_interpreter_and_command_paths_with_spaces': 'passed',
                  'resource_validation': 'passed', 'optional_module_selection': 'passed',
                  'spooled_worker_preflight_and_chunk': 'passed',
                  'stale_lock_rejected_before_submit_and_run': 'passed',
                  'missing_record_and_changed_packages_rejected': 'passed',
                  'changed_checker_rejected': 'passed',
                  'real_slurm_calls': 0, 'solver_calls': 0,
                  'uv_calls': 0,
                  'limitations': 'No setup sync/download, module-stack execution, or Blythe job was run.'}))
