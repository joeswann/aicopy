# File-to-Clipboard Script

This Python script allows you to copy the contents of multiple files or entire directories to your clipboard. It's particularly useful for developers who need to quickly share code snippets or project structures.

## Features

- Copy contents of individual files to clipboard
- Recursively copy contents of entire directories
- Support for glob patterns to select multiple files or directories
- Respect `.gitignore` rules
- Exclude specific files or directories using patterns
- Automatically skip binary files and common lock files (e.g., `package-lock.json`, `yarn.lock`)
- Formatted output with file paths and content delimiters

## Requirements

- Python 3.x
- `pyperclip` library

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Install the required `pyperclip` library:

   ```
   pip install pyperclip
   ```

3. Download the script and save it as `aicopy.py` (or any name you prefer).

## Usage

```
python aicopy.py [-h] [-e EXCLUDE] PATH [PATH ...]
```

### Arguments

- `PATH`: One or more paths or glob patterns of files or folders to copy.
- `-e EXCLUDE`, `--exclude EXCLUDE`: Exclude files or folders matching the given pattern (can be used multiple times).
- `-h`, `--help`: Show the help message and exit.

### Examples

1. Copy a single file:

   ```
   python aicopy.py path/to/file.py
   ```

2. Copy multiple files using glob patterns:

   ```
   python aicopy.py *.py *.js
   ```

3. Copy an entire directory:

   ```
   python aicopy.py path/to/directory
   ```

4. Copy files while excluding specific patterns:
   ```
   python aicopy.py . -e *.log -e temp/*
   ```

## How It Works

1. The script processes the provided paths and glob patterns.
2. It respects `.gitignore` rules by reading `.gitignore` files in the current and parent directories.
3. Files and directories are processed recursively, skipping those that match exclude patterns or `.gitignore` rules.
4. Binary files are automatically detected and skipped.
5. The content of each valid file is read and formatted with the file path and delimiters.
6. All processed content is combined and copied to the clipboard.

## Notes

- The script automatically ignores the `.git` directory and its contents.
- Common lock files like `package-lock.json` and `yarn.lock` are automatically ignored.
- If no valid files are found or processed, the script will exit with a status code of 1.

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or encounter any bugs.

## License

This project is licensed under the MIT License
