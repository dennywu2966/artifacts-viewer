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

    # Root-level meta files to skip (not artifacts)
    skip_root_files = {'index.html', 'manifest.json', 'scan_manifest.py', 'SAVED_FROM.txt'}

    # Scan ALL files recursively, skipping root-level meta files
    all_files = []
    all_categories = {}  # cat_id -> set of extensions

    for file_path in artifacts_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith('.'):
            rel_path = file_path.relative_to(artifacts_dir)
            parts = rel_path.parts

            # Skip root-level meta files
            if len(parts) == 1 and parts[0] in skip_root_files:
                continue

            # Skip files directly in artifacts root that aren't in subdirs
            if len(parts) == 1:
                continue

            category = parts[0]  # First directory component
            ext = file_path.suffix.lstrip('.').lower()

            if category not in all_categories:
                all_categories[category] = set()
            if ext:
                all_categories[category].add(ext)

            all_files.append({
                "name": file_path.name,
                "path": str(rel_path).replace("\\", "/"),
                "category": category,
                "size": get_file_size(file_path)
            })

    # Sort files by path
    all_files.sort(key=lambda x: x["path"])

    # Build directories list from found categories
    directories = []
    for cat in sorted(all_categories.keys()):
        if cat in known_dirs:
            directories.append({
                "id": cat,
                "name": cat.capitalize(),
                "path": f"{cat}/",
                "extensions": known_dirs[cat]
            })
        else:
            # Dynamic directory - detect extensions from actual files
            detected_exts = sorted(all_categories[cat])
            directories.append({
                "id": cat,
                "name": cat.replace('_', '-').replace('-', ' ').title(),
                "path": f"{cat}/",
                "extensions": detected_exts
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
