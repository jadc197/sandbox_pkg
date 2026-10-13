from __future__ import annotations

import os
import sys
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Attempts to use tiktoken for exact GPT-4o token counts.

    Falls back to a safe character-ratio rule of thumb for source code if not installed.
    """
    try:
        import tiktoken

        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except ImportError:
        # Code typically has shorter words, symbols, and indentation.
        # 3.5 characters per token is a highly reliable estimate for source code.
        return int(len(text) / 3.5)


def generate_xml_context(
    root_dir: str | Path | None = None,
    output_file: str | Path | None = None,
) -> None:
    # Resolve script location and default repo root (one level above scripts/)
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    default_root = script_dir.parent if script_dir.name == "scripts" else script_dir

    target_root = default_root if root_dir is None else Path(root_dir).resolve()
    out_path = (
        target_root / "repo_context.xml"
        if output_file is None
        else Path(output_file).resolve()
    )

    if not target_root.is_dir():
        print(f"❌ Error: The directory '{target_root}' does not exist.")
        sys.exit(1)

    ignore_dirs = {
        ".git",
        ".github",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".idea",
        ".vscode",
        "build",
        "dist",
    }
    ignore_files = {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "repo_context.xml",
        ".DS_Store",
        script_path.name,
        "repo2prompt.py",
        "repo_to_prompt.py",
        #        "AGENTS.md",
    }
    allowed_extensions = {
        ".py",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".html",
        ".css",
        ".json",
        ".md",
        ".yml",
        ".yaml",
        ".toml",
        ".ini",
        ".sh",
        ".txt",
    }

    print(f"Scanning target directory: {target_root}")

    xml_output = []
    xml_output.append("<repository>")

    # 1. Output the Directory Map
    xml_output.append("  <structure>")
    for root, dirs, files in os.walk(target_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
        for file in files:
            if file in ignore_files or file.startswith("."):
                continue
            file_path = os.path.relpath(os.path.join(root, file), target_root)
            xml_output.append(f"    <file_path>{file_path}</file_path>")
    xml_output.append("  </structure>")

    # 2. Append Content Blocks
    xml_output.append("  <source_files>")
    for root, dirs, files in os.walk(target_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith(".")]
        for file in files:
            if file in ignore_files or file.startswith("."):
                continue

            _, ext = os.path.splitext(file)
            if ext.lower() in allowed_extensions:
                file_path = os.path.relpath(os.path.join(root, file), target_root)
                full_path = os.path.join(root, file)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    xml_output.append(f'    <file path="{file_path}">')
                    xml_output.append(content)
                    xml_output.append("    </file>")
                except OSError as e:
                    print(f"Skipping {file_path} due to error: {e}")

    xml_output.append("  </source_files>")
    xml_output.append("</repository>")

    final_payload = "\n".join(xml_output)

    # Write output to repo root
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(final_payload)

    size_mb = os.path.getsize(out_path) / (1024 * 1024)
    token_count = estimate_tokens(final_payload)

    print("\n" + "=" * 40)
    print("📋 REPOSITORY COMPILE COMPLETE")
    print("=" * 40)
    print(f"📁 Output File: {out_path.resolve()}")
    print(f"💾 File Size:  {size_mb:.2f} MB")
    print(f"🤖 Est. Tokens: {token_count:,}")
    print("=" * 40)

    if token_count > 100000:
        print("⚠️ Warning: Context is large (>100k tokens).")
        print("  • GPT-4o Limit: ~128k tokens.")
        print("  • Claude 3.5 Limit: ~200k tokens.")
        print("  Consider pruning non-essential files if the AI loses attention.\n")
    else:
        print("✅ Safe size! Fits comfortably within all major AI context windows.\n")


if __name__ == "__main__":
    # first generate the repo_tree.md:
    os.system("tree .. > ../repo_tree.md")

    # target_path = sys.argv[1] if len(sys.argv) > 1 else None
    target_path = None
    generate_xml_context(target_path)
