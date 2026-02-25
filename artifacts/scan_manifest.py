#!/usr/bin/env python3
"""
Scan artifacts directory and generate manifest.json with file listing.
Run this script after adding new files to update the manifest.
"""

import json
import os
from pathlib import Path

def get_file_size(path):
    """Get human-readable file size."""
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_category_from_path(rel_path):
    """Determine category from path."""
    path_str = str(rel_path)
    first_dir = path_str.split('/')[0] if '/' in path_str else path_str
    return first_dir

def main():
    artifacts_dir = Path(__file__).parent

    # Known categories with their extensions
    known_dirs = {
        "docs": ["pdf", "doc", "docx"],
        "slides": ["ppt", "pptx"],
        "markdown": ["md", "mdx"],
        "diagrams": ["mmd", "mermaid"],
        "images": ["png", "jpg", "jpeg", "gif", "webp", "svg"],
        "canvas": ["canvas"],
    }

    # Scan ALL files recursively
    all_files = []
    all_categories = set()

    for file_path in artifacts_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            rel_path = file_path.relative_to(artifacts_dir)
            category = get_category_from_path(rel_path)
            all_categories.add(category)

            ext = file_path.suffix.lstrip('.').lower()
            all_files.append({
                "name": file_path.name,
                "path": str(rel_path),
                "category": category,
                "size": get_file_size(file_path)
            })

    # Sort files by path
    all_files.sort(key=lambda x: x["path"])

    # Build directories list from found categories
    directories = []
    for cat in sorted(all_categories):
        if cat in known_dirs:
            directories.append({
                "id": cat,
                "name": cat.capitalize(),
                "path": f"{cat}/",
                "extensions": known_dirs[cat]
            })
        else:
            # Unknown category - treat as custom
            directories.append({
                "id": cat,
                "name": cat.replace('_', ' ').title(),
                "path": f"{cat}/",
                "extensions": []
            })

    # Create manifest
    manifest = {
        "directories": directories,
        "files": all_files
    }

    # Write manifest
    manifest_path = artifacts_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Generated manifest with {len(all_files)} files in {len(directories)} categories")
    for f in all_files[:20]:
        print(f"  - {f['path']} ({f['category']})")
    if len(all_files) > 20:
        print(f"  ... and {len(all_files) - 20} more files")

if __name__ == "__main__":
    main()
