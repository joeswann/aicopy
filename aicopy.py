#!/usr/bin/env python3

import os
import sys
import glob
import fnmatch
import pyperclip
import argparse

def should_exclude(path, exclude_patterns, gitignore_entries):
    if '.git' in path.split(os.path.sep):
        return True
    if any(pattern in path for pattern in exclude_patterns):
        return True
    for entry in gitignore_entries:
        if entry.startswith('/'):
            if fnmatch.fnmatch(path, entry[1:]):
                return True
        elif fnmatch.fnmatch(path, '*/' + entry):
            return True
        elif fnmatch.fnmatch(path, entry):
            return True
    return False

def find_gitignore(path):
    gitignore_entries = []
    while True:
        gitignore_path = os.path.join(path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as file:
                entries = [line.strip() for line in file if line.strip() and not line.startswith('#')]
                gitignore_entries.extend(entries)
        parent_dir = os.path.dirname(path)
        if parent_dir == path:
            break
        path = parent_dir
    return gitignore_entries

def process_file(path, exclude_patterns, gitignore_entries):
    if should_exclude(path, exclude_patterns, gitignore_entries):
        print(f"Ignoring file '{path}'.")
        return None
    try:
        with open(path, 'r') as file:
            content = file.read()
        print(f"Added file '{path}' to clipboard buffer.")
        return f"File: {path}\n----\n```{content}```\n----\n\n"
    except UnicodeDecodeError:
        print(f"Skipping binary file '{path}'.")
        return None

def process_directory(path, exclude_patterns, gitignore_entries):
    all_content = []
    if should_exclude(path, exclude_patterns, gitignore_entries):
        print(f"Ignoring directory '{path}'.")
        return all_content
    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d != '.git' and not should_exclude(os.path.join(root, d), exclude_patterns, gitignore_entries)]
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if filename in ['package-lock.json', 'yarn.lock']:
                print(f"Ignoring lock file '{file_path}'.")
                continue
            content = process_file(file_path, exclude_patterns, gitignore_entries)
            if content:
                all_content.append(content)
    return all_content

def copy_to_clipboard(paths, exclude_patterns):
    all_content = []
    for path in paths:
        gitignore_entries = find_gitignore(path)
        if os.path.isfile(path):
            content = process_file(path, exclude_patterns, gitignore_entries)
            if content:
                all_content.append(content)
        elif os.path.isdir(path):
            all_content.extend(process_directory(path, exclude_patterns, gitignore_entries))
        else:
            print(f"Path '{path}' does not exist.")

    if all_content:
        pyperclip.copy("\n".join(all_content))
        print("Copied all valid files to clipboard.")
        return True
    else:
        print("No valid files found.")
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Copy files or folders to clipboard.')
    parser.add_argument('paths', metavar='PATH', type=str, nargs='+',
                        help='path or glob pattern of files or folders to copy')
    parser.add_argument('-e', '--exclude', action='append', type=str,
                        help='exclude files or folders matching the given pattern (can be used multiple times)')
    args = parser.parse_args()

    all_paths = []
    for path_or_glob in args.paths:
        paths = glob.glob(path_or_glob)
        if not paths:
            print(f"No files or folders found matching '{path_or_glob}'.")
        else:
            all_paths.extend(paths)

    if not all_paths:
        sys.exit(1)

    exclude_patterns = args.exclude or []

    copied = copy_to_clipboard(all_paths, exclude_patterns)

    if not copied:
        sys.exit(1)
