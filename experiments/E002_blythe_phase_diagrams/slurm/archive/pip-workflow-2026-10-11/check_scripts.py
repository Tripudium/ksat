#!/usr/bin/env python3
"""Local shell integration checks with mocked sbatch/srun; never contacts SLURM."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

scripts = Path(__file__).resolve().parent
for name in ('common.sh', 'setup_environment.sh', 'submit_array.sh', 'run_array.sbatch'):
    subprocess.run(['bash', '-n', str(scripts/name)], check=True)

with tempfile.TemporaryDirectory(prefix='ksat-slurm-check-') as folder:
    temp = Path(folder)
    project = temp/'project with spaces'
    run = project/'run with spaces'
    envdir = project/'test venv'
    mockbin = temp/'mockbin'
    for directory in (project/'code', run, envdir/'bin', mockbin):
        directory.mkdir(parents=True)
    target_scripts = project/'experiments/E002_blythe_phase_diagrams/slurm'
    target_scripts.mkdir(parents=True)
    shutil.copy(scripts/'common.sh', target_scripts/'common.sh')
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
    (mockbin/'sbatch').write_text(f'#!{sys.executable}\n'+'''import json, os, sys
with open(os.environ['MOCK_SBATCH_LOG'], 'a') as log:
    log.write(json.dumps(sys.argv[1:])+'\\n')
print('12345')
''')
    (mockbin/'srun').write_text(f'#!{sys.executable}\n'+'''import os, sys
args = sys.argv[1:]
while args and args[0].startswith('--'):
    args.pop(0)
os.execv(args[0], args)
''')
    for file in mockbin.iterdir(): file.chmod(0o755)
    env = dict(os.environ, PATH=str(mockbin)+os.pathsep+os.environ['PATH'],
               KSAT_PROJECT_DIR=str(project), KSAT_ENV_DIR=str(envdir),
               KSAT_USE_CURRENT_ENV='1', KSAT_MODULES='',
               MOCK_SBATCH_LOG=str(temp/'sbatch.jsonl'),
               MOCK_PIPELINE_LOG=str(temp/'pipeline.jsonl'))
    env.pop('KSAT_DRAT_TRIM', None)
    helper = ['bash', str(scripts/'submit_array.sh'), str(run)]
    dry = subprocess.run(helper, env=env, cwd=temp, capture_output=True, text=True, check=True)
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
    no_modules = dict(env, KSAT_USE_CURRENT_ENV='0')
    missing = subprocess.run(helper, env=no_modules, capture_output=True, text=True)
    assert missing.returncode != 0 and 'Set KSAT_MODULES' in missing.stderr

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

print(json.dumps({'shell_syntax': 'passed', 'mock_submission': 'passed',
                  'default_dry_run': 'passed', 'paths_with_spaces': 'passed',
                  'resource_validation': 'passed', 'module_selection_guard': 'passed',
                  'spooled_worker_preflight_and_chunk': 'passed',
                  'real_slurm_calls': 0, 'solver_calls': 0,
                  'limitations': 'No setup installation, module-stack execution, or Blythe job was run.'}))
