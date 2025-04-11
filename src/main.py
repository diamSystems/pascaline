#!/usr/bin/env python3.12
"""
Pascaline Transpiler 1.1.0
(c) 2025 diam Systems Ltd. All rights reserved.
A robust transpiler for converting Pascaline (.pasc) code to Python 3.12,
compiling it to bytecode (.pyc) and running it, along with a reverse
transpilation mode that outputs .pasc files alongside Python source files.
"""

import os
import sys
import re
import shutil
import subprocess
import argparse
import logging
import py_compile

# Configure logging.
logging.basicConfig(
    level=logging.INFO,
    format="[Pascaline] %(message)s"
)
logger = logging.getLogger(__name__)

VERSION = "1.1.0"
PY_VERSION = "3.12"
COPYRIGHT = "© 2025 diam Systems Ltd. All rights reserved."

# ----------------------------------------------------------------------
# Transpilation Functions
# ----------------------------------------------------------------------
def transpile_code(source: str) -> str:
    """
    Converts Pascaline source into valid Python code.
    
    The following mappings are applied on code (outside of string literals):
      - 'fun' at start of a line -> 'def'
      - 'use' at start of a line -> 'import'
      - 'echo(' -> 'print('
      - '=>' -> 'return'
      
    Comments are left completely untouched.
    """
    try:
        # Protect multiline strings (docstrings and triple-quoted strings)
        triple_quote_pattern = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', re.DOTALL)
        placeholders = []
        def holdout(match):
            placeholders.append(match.group(0))
            return f"__PSTRING__{len(placeholders)-1}__"
        protected_source = triple_quote_pattern.sub(holdout, source)

        # Process line by line so that we do not affect inline comments.
        processed_lines = []
        for line in protected_source.splitlines():
            # Split the line at the first occurrence of a comment marker (# or //)
            # We do not change the comment part.
            # First try to look for a '#' marker.
            code_part = line
            comment_part = ""
            # Check for '#' outside quotes by a simple split; if not reliable, we assume
            # that code and comment are separated by the first occurrence.
            if '#' in line:
                parts = line.split('#', 1)
                code_part, comment_part = parts[0], '#' + parts[1]
            elif '//' in line:
                parts = line.split('//', 1)
                code_part, comment_part = parts[0], '//' + parts[1]
            # Now, transform only the code part.
            indent_match = re.match(r'^(\s*)', code_part)
            indent = indent_match.group(1) if indent_match else ""
            transformed = code_part

            # Transform keywords at line start.
            if re.match(r'^\s*fun\b', transformed):
                transformed = re.sub(r'^\s*fun\b', f'{indent}def', transformed)
            elif re.match(r'^\s*use\b', transformed):
                transformed = re.sub(r'^\s*use\b', f'{indent}import', transformed)
            # Other substitutions: within the code part only.
            transformed = re.sub(r'\becho\(', 'print(', transformed)
            transformed = re.sub(r'=>', 'return', transformed)

            # Rejoin the transformed code and the original comment part.
            new_line = transformed + ((" " + comment_part) if comment_part else "")
            processed_lines.append(new_line)

        processed_code = "\n".join(processed_lines)

        # Restore multiline strings from placeholders.
        def restore_placeholder(match):
            index = int(match.group(1))
            return placeholders[index]
        final_code = re.sub(r'__PSTRING__(\d+)__', restore_placeholder, processed_code)

        return final_code
    except Exception as e:
        logger.error(f"Error during transpiling: {e}")
        sys.exit(1)

def reverse_transpile_code(source: str) -> str:
    """
    Converts Python source code into Pascaline syntax.
    
    The following mappings are applied on code (outside of string literals):
      - 'def' at start of a line -> 'fun'
      - 'import' at start of a line -> 'use'
      - 'print(' -> 'echo('
      - 'return' -> '=>'
      
    Comments are left completely untouched.
    """
    try:
        # Protect multiline strings.
        triple_quote_pattern = re.compile(r'(""".*?"""|\'\'\'.*?\'\'\')', re.DOTALL)
        placeholders = []
        def holdout(match):
            placeholders.append(match.group(0))
            return f"__PSTRING__{len(placeholders)-1}__"
        protected_source = triple_quote_pattern.sub(holdout, source)

        # Process line by line.
        processed_lines = []
        for line in protected_source.splitlines():
            # Split out comment if present.
            code_part = line
            comment_part = ""
            if '#' in line:
                parts = line.split('#', 1)
                code_part, comment_part = parts[0], '#' + parts[1]
            # Transform the code part:
            indent_match = re.match(r'^(\s*)', code_part)
            indent = indent_match.group(1) if indent_match else ""
            transformed = code_part

            if re.match(r'^\s*def\b', transformed):
                transformed = re.sub(r'^\s*def\b', f'{indent}fun', transformed)
            elif re.match(r'^\s*import\b', transformed):
                transformed = re.sub(r'^\s*import\b', f'{indent}use', transformed)
            transformed = re.sub(r'\bprint\(', 'echo(', transformed)
            transformed = re.sub(r'\breturn\b', '=>', transformed)

            new_line = transformed + ((" " + comment_part) if comment_part else "")
            processed_lines.append(new_line)
        processed_code = "\n".join(processed_lines)

        # Restore multiline strings.
        def restore_placeholder(match):
            index = int(match.group(1))
            return placeholders[index]
        final_code = re.sub(r'__PSTRING__(\d+)__', restore_placeholder, processed_code)
        return final_code
    except Exception as e:
        logger.error(f"Error during reverse transpiling: {e}")
        sys.exit(1)

def process_file(input_path: str, output_path: str, reverse: bool = False) -> None:
    """
    Reads a source file, processes it (either transpile or reverse transpile),
    and writes the result to the output file.
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            source = infile.read()
    except UnicodeDecodeError:
        try:
            with open(input_path, 'r', encoding='latin-1') as infile:
                source = infile.read()
        except Exception as e:
            logger.error(f"Error reading file {input_path}: {e}")
            sys.exit(1)

    processed = reverse_transpile_code(source) if reverse else transpile_code(source)
    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            outfile.write(processed)
        logger.info(f"Processed: {input_path} -> {output_path}")
    except Exception as e:
        logger.error(f"Error writing to file {output_path}: {e}")
        sys.exit(1)

# ----------------------------------------------------------------------
# Project Build Logic
# ----------------------------------------------------------------------
def build_project(source_root: str, build_root: str, reverse: bool = False) -> None:
    """
    Processes each source file in the project.
    
    For normal transpilation (reverse==False):
      - Transpile .pasc files into .py
      - Copy .py files as-is
      - Output is placed in a temporary build directory that mimics the source structure.
    
    For reverse transpilation (reverse==True):
      - Reverse transpile .py files into .pasc
      - Output is stored alongside the originals (in-place).
    """
    abs_build_root = os.path.abspath(build_root) if build_root else None

    for dirpath, _, filenames in os.walk(source_root):
        if abs_build_root and os.path.abspath(dirpath) == abs_build_root:
            continue

        if reverse:
            target_dir = dirpath
        else:
            rel_path = os.path.relpath(dirpath, source_root)
            target_dir = os.path.join(build_root, rel_path)
            os.makedirs(target_dir, exist_ok=True)

        for filename in filenames:
            src_file = os.path.join(dirpath, filename)
            if not reverse and filename.endswith('.pasc'):
                base = os.path.splitext(filename)[0]
                target_file = os.path.join(target_dir, base + '.py')
                process_file(src_file, target_file, reverse=False)
            elif not reverse and filename.endswith('.py'):
                target_file = os.path.join(target_dir, filename)
                shutil.copy2(src_file, target_file)
                logger.info(f"Copied: {src_file} -> {target_file}")
            elif reverse and filename.endswith('.py'):
                base = os.path.splitext(filename)[0]
                target_file = os.path.join(target_dir, base + '.pasc')
                process_file(src_file, target_file, reverse=True)
            # Other files are ignored.

# ----------------------------------------------------------------------
# Compile and Execute Logic
# ----------------------------------------------------------------------
def compile_and_run(build_root: str, main_relative_path: str, extra_args: list = None) -> None:
    """
    Compiles the transpiled Python code into bytecode and executes it.
    """
    main_py_path = os.path.join(build_root, main_relative_path)
    logger.info(f"Compiling {main_py_path} to bytecode...")
    try:
        compiled_path = py_compile.compile(main_py_path, cfile=main_py_path + "c", doraise=True)
    except py_compile.PyCompileError as e:
        logger.error(f"Compilation error: {e}")
        sys.exit(1)

    command = ['python3.12', compiled_path]
    if extra_args:
        command.extend(extra_args)

    logger.info(f"Running compiled bytecode: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Execution error: {e}")
        sys.exit(1)

# ----------------------------------------------------------------------
# CLI Interface
# ----------------------------------------------------------------------
def print_info() -> None:
    """
    Prints information about the transpiler.
    """
    print(f"""
Pascaline Transpiler {VERSION}
Built on Python {PY_VERSION}
A robust transpiler for converting Pascaline (.pasc) code to Python 3.12 bytecode.
{COPYRIGHT}
Visit: https://diamsystems.odoo.com/pascaline
""")

def main() -> None:
    """
    Main entry point for the command-line interface.
    """
    parser = argparse.ArgumentParser(
        description="Pascaline Transpiler - Convert Pascaline code to Python 3.12 bytecode.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--version", action="version", version=f"Pascaline Transpiler {VERSION}")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    run_parser = subparsers.add_parser("run", help="Transpile .pasc files, compile and run using Python 3.12")
    run_parser.add_argument("mainfile", help="Path to the main .pasc file")
    run_parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="Additional arguments for the transpiled program")

    reverse_parser = subparsers.add_parser("reverse", help="Reverse transpile .py files to .pasc (in-place)")
    reverse_parser.add_argument("mainfile", help="Path to a main .py file to reverse transpile")

    info_parser = subparsers.add_parser("info", help="Display transpiler info")

    args = parser.parse_args()

    if args.command == "info":
        print_info()
        sys.exit(0)

    if args.command == "reverse":
        mainfile = os.path.abspath(args.mainfile)
        if not mainfile.endswith('.py'):
            logger.error("Error: Must provide a '.py' file for reverse transpilation.")
            sys.exit(1)
        source_root = os.path.dirname(mainfile)
        logger.info("Starting reverse transpilation...")
        build_project(source_root, build_root="", reverse=True)
        logger.info("Reverse transpilation complete.")
        sys.exit(0)

    if args.command == "run":
        mainfile = os.path.abspath(args.mainfile)
        if not mainfile.endswith('.pasc'):
            logger.error("Error: Must provide a '.pasc' file for run mode.")
            sys.exit(1)
        source_root = os.path.dirname(mainfile)
        rel_main = os.path.relpath(mainfile, source_root).replace('.pasc', '.py')
        build_root = os.path.join(source_root, ".pasc_build")
        if os.path.exists(build_root):
            shutil.rmtree(build_root)
        os.makedirs(build_root, exist_ok=True)

        logger.info("Transpiling project files into build directory...")
        build_project(source_root, build_root, reverse=False)
        logger.info("Transpilation complete.")

        compile_and_run(build_root, rel_main, args.extra_args)

        logger.info("Execution finished. Cleaning up build directory...")
        shutil.rmtree(build_root)
        sys.exit(0)

    parser.print_help()
    sys.exit(1)

if __name__ == '__main__':
    main()
