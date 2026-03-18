import subprocess
import sys


def run_migrations() -> None:
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Alembic migration failed.")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        raise