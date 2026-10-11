# POSIX checker compilation follow-up

On 11 October 2026 the user reported successful setup on Blythe's login02,
with an implicit-declaration warning for `getc_unlocked`. The output ended
with matching environment provenance and both environment/checker ready.
This establishes user-reported login-node setup, not compute-node execution
or certificate preflight on Blythe.

The updated setup adds `-D_POSIX_C_SOURCE=200809L` to strict C99 compilation,
and the environment record now records that exact flag. The vendored C source
and its pinned hash are unchanged. glibc exposes these POSIX declarations via
feature-test macros: [GNU libc documentation](https://sourceware.org/glibc/manual/latest/html_node/Feature-Test-Macros.html),
[Linux man-pages requirements](https://man7.org/linux/man-pages/man3/unlocked_stdio.3.html).

[checks.json](checks.json) retains commands, return codes and hashes. On the
local macOS host, compilation with implicit declarations treated as errors,
the actual offline setup, mocked SLURM checks, and positive/negative certificate
preflight all passed. The compiler log is empty. No Linux rebuild or scheduler
call was performed by the assistant. The earlier helper versions are preserved
under `../../slurm/archive/uv-before-posix-2026-10-11/`.

After transferring the updated sources to an idle Blythe checkout, rerun:

```sh
bash experiments/E002_blythe_phase_diagrams/slurm/setup_environment.sh
```

This recompiles the checker and writes a fresh provenance record. The previous
successful setup did not require an emergency repair; this change makes the
function declaration explicit and avoids the reported compiler warning.
