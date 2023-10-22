from pathlib import Path

def get_asset(file: str) -> Path:
    return Path.cwd() / 'assets' / file