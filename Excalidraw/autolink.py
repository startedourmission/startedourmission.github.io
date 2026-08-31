#!/usr/bin/env python3
"""
Auto-link: scan blog posts and insert [[wiki links]] for known targets.

Usage:
  python3 autolink.py                    # dry-run (show what would change)
  python3 autolink.py --apply            # actually modify files
  python3 autolink.py --apply --file X   # single file only

Rules:
  - Only link first occurrence per target per file
  - Skip frontmatter (between --- lines)
  - Skip code blocks (``` ... ```)
  - Skip existing [[links]]
  - Skip headings (# lines)
  - Skip image embeds (![[...]])
  - Minimum target length: 3 chars
  - Case-sensitive matching
"""

import os, re, sys, yaml

BLOG_DIR = "/Users/chajinwoo/Vaults/AutoVault/markdown-blog"

# Too generic or short — skip these as link targets
SKIP_TARGETS = {
    "Python", "CLAUDE", "ART", "ReLU", "LSTM", "LLM", "RNN", "CNN",
    "index", "links", "Transformer", "Posts",
    # file stems that are chapters (don't link "1장" everywhere)
}

def collect_targets():
    """Collect all linkable targets: filename → [aliases]"""
    targets = {}  # display_name → filename (without .md)

    for root, dirs, files in os.walk(BLOG_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            name = f[:-3]  # remove .md
            filepath = os.path.join(root, f)

            # filename itself is a target
            if len(name) >= 3 and name not in SKIP_TARGETS:
                targets[name] = name

            # extract aliases from frontmatter
            try:
                with open(filepath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
                if fm_match:
                    fm_text = fm_match.group(1)
                    # simple alias extraction
                    in_aliases = False
                    for line in fm_text.split('\n'):
                        if line.strip().startswith('aliases:'):
                            in_aliases = True
                            continue
                        if in_aliases:
                            if line.strip().startswith('- '):
                                alias = line.strip()[2:].strip().strip('"').strip("'")
                                # skip [[]] wrapped aliases
                                if alias.startswith('[['):
                                    continue
                                if len(alias) >= 3 and alias not in SKIP_TARGETS:
                                    targets[alias] = name
                            elif not line.startswith(' ') and not line.startswith('\t'):
                                in_aliases = False
            except:
                pass

    return targets

def should_skip_line(line):
    """Check if line should be skipped."""
    stripped = line.strip()
    if stripped.startswith('#'):  # heading
        return True
    if stripped.startswith('![['):  # image embed
        return True
    if stripped.startswith('```'):  # code fence
        return True
    if stripped.startswith('|'):  # table
        return True
    if stripped.startswith('>'):  # blockquote — allow linking inside
        return False
    return False

def autolink_file(filepath, targets, apply=False):
    """Process a single file. Returns list of changes made."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and body
    fm_match = re.match(r'^(---\s*\n.*?\n---\s*\n)(.*)', content, re.DOTALL)
    if not fm_match:
        return []

    frontmatter = fm_match.group(1)
    body = fm_match.group(2)

    # Get this file's own name to avoid self-linking
    own_name = os.path.splitext(os.path.basename(filepath))[0]

    # Track which targets we've already linked in this file
    linked = set()
    changes = []

    # Find existing [[links]] to avoid double-linking
    existing_links = set(re.findall(r'\[\[([^\]|]+)', body))

    # Sort targets by length (longest first) to avoid partial matches
    sorted_targets = sorted(targets.items(), key=lambda x: -len(x[0]))

    # Process line by line, tracking code blocks
    lines = body.split('\n')
    in_code_block = False
    new_lines = []

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block or should_skip_line(line):
            new_lines.append(line)
            continue

        for display, filename in sorted_targets:
            if display in linked:
                continue
            if filename == own_name:
                continue
            if filename in existing_links or display in existing_links:
                continue

            # Check if display text exists in this line (not inside existing [[]])
            # Use word boundary-ish matching
            pattern = re.escape(display)
            match = re.search(r'(?<!\[\[)(?<!\|)' + pattern + r'(?!\]\])', line)

            if match:
                # Replace first occurrence only
                if display == filename:
                    replacement = f'[[{display}]]'
                else:
                    replacement = f'[[{filename}|{display}]]'

                line = line[:match.start()] + replacement + line[match.end():]
                linked.add(display)
                changes.append(f"  {display} → {replacement}")

        new_lines.append(line)

    new_body = '\n'.join(new_lines)
    new_content = frontmatter + new_body

    if changes and apply:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return changes

def main():
    apply = '--apply' in sys.argv
    single_file = None
    if '--file' in sys.argv:
        idx = sys.argv.index('--file')
        if idx + 1 < len(sys.argv):
            single_file = sys.argv[idx + 1]

    print("Collecting link targets...")
    targets = collect_targets()
    print(f"Found {len(targets)} linkable targets\n")

    total_changes = 0
    total_files = 0

    for root, dirs, files in os.walk(BLOG_DIR):
        for f in files:
            if not f.endswith(".md"):
                continue
            if single_file and single_file not in f:
                continue

            filepath = os.path.join(root, f)
            changes = autolink_file(filepath, targets, apply=apply)

            if changes:
                relpath = os.path.relpath(filepath, BLOG_DIR)
                print(f"{'✏️' if apply else '📋'} {relpath}")
                for c in changes:
                    print(c)
                print()
                total_changes += len(changes)
                total_files += 1

    mode = "Applied" if apply else "Would apply"
    print(f"\n{mode} {total_changes} links across {total_files} files")
    if not apply:
        print("Run with --apply to make changes")

if __name__ == "__main__":
    main()
