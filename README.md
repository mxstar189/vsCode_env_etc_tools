Small personal toolbox for inspecting and working with environment files, VS Code settings, and simple DB inspection.

IMPORTANT: this repository is public. Do NOT commit secrets (API keys, DB passwords, private keys) into the repo. Keep secrets in a local `.env` that is excluded from version control.

Quick links

- `scripts/README.md` — instructions for the included scripts (env loader, checks, DB inspector)

Getting started (Windows PowerShell)

1. Create and activate virtualenv, then install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run the env check (shows mismatches between `.env` file and the current process environment):

```powershell
python .\scripts\check_env.py
```

3. Inspect database (if POSTGRES_* or DATABASE_URL are set in `.env`):

```powershell
python .\scripts\db_inspect.py --sample 5
```

Security guidance

- Ensure `.env` is listed in `.gitignore` so secrets never get committed.
- If a secret is accidentally committed, rotate credentials immediately and remove the secret from git history (use `git filter-repo` or similar).
- Consider adding a pre-commit hook to block commits containing `API_KEY`, `SECRET`, `PASSWORD`, or other likely secret names.

If you'd like, I can add a pre-commit configuration that checks for common secrets before commit.
