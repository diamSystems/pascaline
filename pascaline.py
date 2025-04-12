# pascaline.py (located in the 'runtime' folder)
import os

# Looping utilities
def for_each(collection, func):
    """Applies a function to each item in a collection."""
    for item in collection:
        func(item)

# String utilities
def starts_with(s, prefix):
    """Returns True if the string s starts with the prefix."""
    return s.startswith(prefix)

def ends_with(s, suffix):
    """Returns True if the string s ends with the suffix."""
    return s.endswith(suffix)

def split(s, delimiter):
    """Splits the string s by the given delimiter."""
    return s.split(delimiter)

def format_string(template, **kwargs):
    """Formats a string using a template and keyword arguments."""
    return template.format(**kwargs)

# List utilities
def append(lst, item):
    """Appends an item to a list."""
    lst.append(item)

def remove(lst, item):
    """Removes an item from a list."""
    lst.remove(item)

# File I/O utilities
def read_file(path):
    """Reads the content of a file."""
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return None

def write_file(path, content):
    """Writes content to a file."""
    try:
        with open(path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file {path}: {e}")

# Type checking utilities
def is_int(value):
    """Checks if the value is an integer."""
    return isinstance(value, int)

def is_str(value):
    """Checks if the value is a string."""
    return isinstance(value, str)

# Error handling
def try_except(func, default_value=None):
    """Runs a function and returns a default value if an error occurs."""
    try:
        return func()
    except Exception as e:
        print(f"Error: {e}")
        return default_value

# Date and time utilities
import time

def get_current_time():
    """Returns the current time as a formatted string."""
    return time.strftime("%Y-%m-%d %H:%M:%S")

