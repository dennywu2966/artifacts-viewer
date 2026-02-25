#!/usr/bin/env python3
"""
Save artifact to ~/projects/artifacts-viewer with optional category organization.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path


def get_category_from_extension(filename: str) -> str:
    """Determine category based on file extension."""
    ext = Path(filename).suffix.lower()
    categories = {
        '.pdf': 'docs',
        '.doc': 'docs',
        '.docx': 'docs',
        '.ppt': 'slides',
        '.pptx': 'slides',
        '.md': 'markdown',
        '.mdx': 'markdown',
        '.png': 'images',
        '.jpg': 'images',
        '.jpeg': 'images',
        '.gif': 'images',
        '.svg': 'diagrams',
    }
    return categories.get(ext, 'other')


def save_artifact(source_path: str, custom_name: str = None, category: str = None) -> str:
    """Save artifact to artifacts-viewer."""
    source = Path(source_path).resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    # Determine target directory - always use artifacts subdirectory
    artifacts_dir = Path.home() / "projects" / "artifacts-viewer" / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Determine category
    if category is None:
        category = get_category_from_extension(source.name)

    # Create category subdirectory
    category_dir = artifacts_dir / category
    category_dir.mkdir(exist_ok=True)

    # Determine target filename
    if custom_name:
        # Preserve extension from source
        ext = source.suffix
        if not custom_name.endswith(ext):
            custom_name = custom_name + ext
        target_name = custom_name
    else:
        target_name = source.name

    target_path = category_dir / target_name

    # Handle duplicate names
    if target_path.exists():
        base = target_path.stem
        ext = target_path.suffix
        counter = 1
        while target_path.exists():
            target_path = category_dir / f"{base}_{counter}{ext}"
            counter += 1

    # Copy file
    shutil.copy2(source, target_path)

    return str(target_path)


def main():
    parser = argparse.ArgumentParser(description="Save artifact to artifacts-viewer")
    parser.add_argument("source", help="Source file path")
    parser.add_argument("--name", "-n", help="Custom name for the artifact")
    parser.add_argument(
        "--category", "-c",
        choices=["docs", "slides", "markdown", "images", "diagrams", "other"],
        help="Category (auto-detected if not specified)"
    )

    args = parser.parse_args()

    try:
        target = save_artifact(args.source, args.name, args.category)
        print(f"Artifact saved to: {target}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
