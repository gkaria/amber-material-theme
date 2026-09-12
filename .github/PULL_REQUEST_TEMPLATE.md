## What changed

<!-- One or two sentences. Screenshots for anything visual (dark and light if both are affected). -->

## Checklist

- [ ] I edited a source (`scripts/variants.py`, a generator in `scripts/`, or `scripts/base-palenight-italic.json`), not a generated file in `themes/`, `ghostty/`, `codex/`, `claude-code/`, `opencode/`, `windows-terminal/`, `powershell/`, `starship/`, `grok/`, `icon-themes/`, or `icons/amber-material/`.
- [ ] I re-ran the build chain in order (see `CONTRIBUTING.md`) and committed the regenerated outputs.
- [ ] `python3 scripts/check_generated.py` reports in sync.
- [ ] `python3 scripts/test_check_generated.py` passes.
- [ ] `README.md` palette tables are updated if a documented hex changed.
