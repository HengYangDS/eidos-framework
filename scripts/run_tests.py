import sys
import unittest
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    # Ensure local src/ is importable first
    sys.path.insert(0, str(repo_root / "src"))

    tests_dir = repo_root / "tests"
    if not tests_dir.exists():
        print("No tests directory found.")
        return 0

    loader = unittest.defaultTestLoader
    suite = loader.discover(start_dir=str(tests_dir), pattern="test_*.py", top_level_dir=str(repo_root))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
