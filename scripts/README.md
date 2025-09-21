## Scripts for environment checks and DB inspection

## Files

- `env_load_util.py`: reusable loader that finds repository `.env` and loads values into process env. Import `env` and call `env.load()`.
- `check_env.py` / `check_env.ps1`: compare `.env` values with the current process environment and show `.vscode/settings.json` if present.
- `db_inspect.py`: connect to Postgres using `POSTGRES_*` variables from `.env` (or `DATABASE_URL`) and list tables, row counts, and sample rows.

## Quick start (Windows PowerShell)

1. Create a virtualenv and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```

2. Run the checks:

```powershell
python .\scripts\check_env.py
./scripts/check_env.ps1
```

3. Inspect the database (after activating virtualenv):

```powershell
python .\scripts\db_inspect.py --sample 5
```

## Notes

- The loader searches upward from `scripts/` to find the first `.env` file. If you move scripts, update `env_load_util.EnvLoader` root or pass a path.
- `db_inspect.py` uses SQLAlchemy and needs a DB driver installed (`psycopg2-binary` for Postgres).
