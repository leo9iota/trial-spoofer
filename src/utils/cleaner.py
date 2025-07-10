#!/usr/bin/env python3
"""
Cache cleaning utilities for VS Code, Cursor, and Augment Code.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterator

from .helper import log


def clean_vscode_caches(home: Path) -> bool:
    """Purge VS Code / Cursor / Augment caches under $HOME."""
    try:
        purge_globs: list[str] = [
            ".config/Code*",
            ".vscode*",
            ".config/cursor",
            ".cursor",
            ".cache/augment*",
        ]

        cleaned_any: bool = False
        for g in purge_globs:
            cache_paths: Iterator[Path] = home.glob(g)
            for p in cache_paths:
                if p.exists():
                    log(f"Removing {p}")
                    shutil.rmtree(p, ignore_errors=True)
                    cleaned_any = True

        if not cleaned_any:
            log("No VS Code caches found to clean")

        return True
    except Exception as e:
        log(f"Failed to clean VS Code caches: {e}")
        return False
