#!/usr/bin/env python3
"""
build_llms_with_gitingest.py – Generate llms.txt and llms-full.txt using GitIngest

This script uses GitIngest to create two files for AI coding assistants:
- llms.txt: A concise version with filtered content
- llms-full.txt: Complete documentation and code content

Usage:
  python scripts/build_llms_with_gitingest.py
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def count_tokens(text: str) -> int:
    """Estimate token count using tiktoken or word count."""
    try:
        import tiktoken
        return len(tiktoken.get_encoding("cl100k_base").encode(text))
    except Exception:
        return len(text.split())


def run_gitingest(
    source_path: str,
    include_patterns: List[str] = None,
    exclude_patterns: List[str] = None,
    max_size: int = None
) -> str:
    """Run GitIngest with specified filters and return the output."""
    cmd = ["gitingest", source_path, "-o", "-"]
    
    if include_patterns:
        for pattern in include_patterns:
            cmd.extend(["-i", pattern])
    
    if exclude_patterns:
        for pattern in exclude_patterns:
            cmd.extend(["-e", pattern])
    
    if max_size:
        cmd.extend(["-s", str(max_size)])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running GitIngest: {e}")
        print(f"Stderr: {e.stderr}")
        return ""


def build_llms_txt(project_root: Path) -> str:
    """Build the concise llms.txt with documentation focus."""
    # Focus on documentation and key files only
    include_patterns = [
        "README.md",      # Main README
        "CHANGELOG.md",   # Changelog
        "LICENSE",        # License
        "docs/*.md",      # Main docs
        "*/README.md",    # Language-specific READMEs
        "pyproject.toml", # Python config
        "package.json",   # TypeScript config
        "go.mod",         # Go config
    ]
    
    exclude_patterns = [
        "node_modules/*",
        "*.lock",
        "dist/*", 
        "build/*",
        "__pycache__/*",
        ".pytest_cache/*",
        "venv/*",
        "test_env/*",
        "agentbay_example_env/*",
        ".github/*",
        ".aoneci/*",
        "cookbook/*",
        "assets/*",
        "scripts/*",
        "python/scripts/*",
        "golang/scripts/*",
        "typescript/scripts/*",
        # Exclude Aliyun SDK slices only
        "python/agentbay/api/*",
        "typescript/src/api/*",
        "golang/api/*",
        "*.min.js",
        "*.log",
        "tmp/*",
        "downloads/*",
        "logs/*",
        ".git/*",
        "*.pyc",
        "coverage.xml",
        ".coverage",
        "*.png",
        "*.jpg", 
        "*.jpeg",
        "*.gif",
        "*.svg",
        "*.ico",
        "tests/*",        # Exclude test files for concise version
        "test/*",
        "*test*",
    ]
    
    # Limit file size to 20KB for concise version
    return run_gitingest(
        str(project_root),
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        max_size=15000  # tighter concise cap (15KB)
    )


def build_llms_full_txt(project_root: Path) -> str:
    """Build the comprehensive llms-full.txt."""
    # Include more file types but still exclude binaries and deps
    include_patterns = [
        "*.md",
        "*.txt",
        "*.py",
        "*.ts",
        "*.tsx",
        "*.js",
        "*.jsx",
        "*.go",
        # Config whitelist only (avoid large data JSON/YAML)
        "package.json",
        "tsconfig.json",
        "go.mod",
        "pyproject.toml",
        "*.toml",
        "*.cfg",
        "*.ini",
        "*.sh",
        "*.bash",
    ]

    exclude_patterns = [
        "node_modules/*",
        "*.lock",
        "dist/*",
        "build/*",
        "__pycache__/*",
        ".pytest_cache/*",
        "venv/*",
        "test_env/*",
        "agentbay_example_env/*",
        ".github/*",
        ".aoneci/*",
        "cookbook/*",
        "assets/*",
        "scripts/*",
        "python/scripts/*",
        "golang/scripts/*",
        "typescript/scripts/*",
        # Exclude Aliyun SDK slices only
        "python/agentbay/api/*",
        "typescript/src/api/*",
        "golang/api/*",
        "*.min.js",
        "*.log",
        "tmp/*",
        "downloads/*",
        "logs/*",
        ".git/*",
        "*.pyc",
        "coverage.xml",
        ".coverage",
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.gif",
        "*.svg",
        "*.ico",
        "*.whl",
        "*.tar.gz",
        "*.zip",
        "tests/*",
        "test/*",
        "*test*",
        # API docs are generated from code; keep code instead
        "docs/api/*",
        "python/docs/api/*",
        "typescript/docs/api/*",
        "golang/docs/api/*",
    ]

    # Allow larger files for full version
    return run_gitingest(
        str(project_root),
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        max_size=120000  # tighter full cap (120KB)
    )


def main() -> None:
    """Main entry point for the script."""
    ap = argparse.ArgumentParser(
        description="Generate llms.txt and llms-full.txt using GitIngest",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Project root directory (default: parent of scripts/)"
    )
    ap.add_argument(
        "--out-root", 
        type=Path,
        default=None,
        help="Output directory (default: project root)"
    )
    ap.add_argument(
        "--index-limit",
        type=int,
        default=100_000,
        help="Maximum tokens for llms.txt (default: 100,000)"
    )
    ap.add_argument(
        "--full-limit",
        type=int, 
        default=1_000_000,
        help="Maximum tokens for llms-full.txt (default: 1,000,000)"
    )
    args = ap.parse_args()

    project_root = args.project_root.resolve()
    out_root = args.out_root.resolve() if args.out_root else project_root

    print(f"Project root: {project_root}")
    print(f"Output directory: {out_root}")
    print("")

    # Check if GitIngest is available
    try:
        subprocess.run(["gitingest", "--help"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: GitIngest not found. Please install it first:")
        print("  pip install gitingest")
        sys.exit(1)

    # Build concise version
    print("Building llms.txt (concise version with GitIngest)...")
    llms_content = build_llms_txt(project_root)
    
    if not llms_content:
        print("Error: Failed to generate llms.txt content")
        sys.exit(1)

    # Build full version  
    print("\nBuilding llms-full.txt (comprehensive version with GitIngest)...")
    llms_full_content = build_llms_full_txt(project_root)

    # Check token limits
    llms_tokens = count_tokens(llms_content)
    llms_full_tokens = count_tokens(llms_full_content)

    print(f"\nToken counts:")
    print(f"  llms.txt: {llms_tokens:,} tokens")
    print(f"  llms-full.txt: {llms_full_tokens:,} tokens")

    if llms_tokens > args.index_limit:
        print(f"\n⚠️  Warning: llms.txt exceeds limit ({llms_tokens:,} > {args.index_limit:,})")

    if llms_full_tokens > args.full_limit:
        print(f"\n⚠️  Warning: llms-full.txt exceeds limit ({llms_full_tokens:,} > {args.full_limit:,})")

    # Write output files
    (out_root / "llms.txt").write_text(llms_content, encoding="utf-8")
    (out_root / "llms-full.txt").write_text(llms_full_content, encoding="utf-8")

    print("\n✅ Generated llms.txt and llms-full.txt successfully using GitIngest")
    print(f"   Output location: {out_root}")


if __name__ == "__main__":
    main()