"""
clean_migrations.py

Deletes all Django migration files (except __init__.py), .pyc files, and __pycache__
directories in your project—without touching virtual-env folders.
"""

import os
import shutil
import sys

# Names of virtual-env (or any) directories to skip completely
VENV_DIRS = {'venv', '.venv', 'env', 'ENV'}

def should_skip_dir(dirname: str) -> bool:
    """Return True if this directory should be skipped (e.g. a virtualenv)."""
    return dirname in VENV_DIRS

def main(root: str = '.'):
    removed_py = 0
    removed_pyc = 0
    removed_cache = 0

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Prune venv dirs (won’t recurse into them)
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]

        # If this is a migrations folder, remove all .py except __init__.py
        if os.path.basename(dirpath) == 'migrations':
            for fname in filenames:
                full = os.path.join(dirpath, fname)
                if fname.endswith('.py') and fname != '__init__.py':
                    os.remove(full)
                    removed_py += 1
                    print(f"Deleted: {full}")
                elif fname.endswith('.pyc'):
                    os.remove(full)
                    removed_pyc += 1
                    print(f"Deleted: {full}")

        # In any folder, if there’s a __pycache__ subdir, delete it wholesale
        if '__pycache__' in dirnames:
            cache_dir = os.path.join(dirpath, '__pycache__')
            shutil.rmtree(cache_dir)
            removed_cache += 1
            print(f"Removed directory: {cache_dir}")
            # Also remove it from dirnames so os.walk won't re-enter it
            dirnames.remove('__pycache__')

    print("\n✅  Done!")
    print(f" • Python migrations deleted: {removed_py}")
    print(f" • Compiled .pyc deleted:       {removed_pyc}")
    print(f" • __pycache__ dirs removed:    {removed_cache}")

if __name__ == '__main__':
    # Allow passing a custom root directory, e.g. python clean_migrations.py path/to/project
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(target)
