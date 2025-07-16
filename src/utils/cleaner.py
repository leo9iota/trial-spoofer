#!/usr/bin/env python3
"""
Cache cleaning utilities for VS Code, Cursor, and Augment Code.
"""

from __future__ import annotations

import shutil
from collections.abc import Iterator
from pathlib import Path

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
        for glob_pattern in purge_globs:
            cache_paths: Iterator[Path] = home.glob(glob_pattern)
            for cache_path in cache_paths:
                if cache_path.exists():
                    log_message: str = f"Removing {cache_path}"
                    log(log_message)
                    shutil.rmtree(cache_path, ignore_errors=True)
                    cleaned_any = True

        if not cleaned_any:
            no_cache_message: str = "No VS Code caches found to clean"
            log(no_cache_message)

        return True
    except Exception as e:
        error_msg: str = str(e)
        log(f"Failed to clean VS Code caches: {error_msg}")
        return False
