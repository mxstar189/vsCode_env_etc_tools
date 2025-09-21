"""env_load_util

Small helper to locate and load the repository root .env and expose helper functions
so other scripts can import a single source of truth for environment loading.

Usage:
    from scripts.env_load_util import env
    env.load()
    db_url = env.get_database_url()
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Dict

try:
    # prefer python-dotenv if available
    from dotenv import load_dotenv, dotenv_values
except Exception:
    load_dotenv = None
    dotenv_values = None


class EnvLoader:
    def __init__(self, root: Optional[Path] = None, env_name: str = ".env"):
        self.root = Path(root) if root else Path(__file__).resolve().parents[1]
        self.env_name = env_name
        self.env_path = self.find_env()
        self._loaded = False

    def find_env(self) -> Optional[Path]:
        # walk upward to find .env in repo root
        cur = Path(__file__).resolve().parent
        for p in [cur] + list(cur.parents):
            candidate = p / self.env_name
            if candidate.exists():
                return candidate
        return None

    def load(self, override: bool = False) -> bool:
        """Load variables into os.environ. Returns True if loaded."""
        if not self.env_path:
            return False
        if load_dotenv:
            # use python-dotenv if installed
            load_dotenv(dotenv_path=str(self.env_path), override=override)
            self._loaded = True
            return True
        # fallback: parse ourselves
        vals = dotenv_values(str(self.env_path)) if dotenv_values else None
        if vals is None:
            # manual parse
            with open(self.env_path, "r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"')
                    if override or k not in os.environ:
                        os.environ[k] = v
            self._loaded = True
            return True
        # if dotenv_values produced dict
        for k, v in vals.items():
            if v is None:
                continue
            if override or k not in os.environ:
                os.environ[k] = v
        self._loaded = True
        return True

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.environ.get(key, default)

    def as_dict(self) -> Dict[str, str]:
        # return subset of envs found in .env file
        if not self.env_path:
            return {}
        out: Dict[str, str] = {}
        with open(self.env_path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"')
        return out

    def get_database_url(self) -> Optional[str]:
        # Try common patterns for Postgres
        user = self.get("POSTGRES_USER")
        pw = self.get("POSTGRES_PASSWORD")
        host = self.get("POSTGRES_HOST")
        port = self.get("POSTGRES_PORT")
        db = self.get("POSTGRES_DB")
        if user and pw and host and db:
            port_part = f":{port}" if port else ""
            return f"postgresql://{user}:{pw}@{host}{port_part}/{db}"
        # fallback to single URL env var
        return self.get("DATABASE_URL")


# singleton
env = EnvLoader()

if __name__ == "__main__":
    print("env_path:", env.env_path)
    print("loaded:", env._loaded)
    print("as_dict keys:", list(env.as_dict().keys()))
