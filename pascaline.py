# pascaline.py (located in the 'runtime' folder)
import os
import re
import json
import logging
import time
import threading
from functools import partial, reduce

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

def find(lst, condition):
    """Finds the first item in a list that matches the condition."""
    for item in lst:
        if condition(item):
            return item
    return None

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

def find(lst, condition):
    """Finds the first item that matches the condition."""
    for item in lst:
        if condition(item):
            return item
    return None

def filter_list(lst, condition):
    """Filters a list based on a condition."""
    return [item for item in lst if condition(item)]

def map_list(lst, func):
    """Applies a function to each item in a list and returns the results."""
    return [func(item) for item in lst]

def reduce_list(lst, func, initial=None):
    """Reduces a list to a single value by applying a function."""
    return reduce(func, lst, initial)

# Dictionary utilities
def get_dict_value(d, key, default=None):
    """Safely gets a value from a dictionary."""
    return d.get(key, default)

def merge_dicts(dict1, dict2):
    """Merges two dictionaries."""
    merged = dict1.copy()  # Create a copy to avoid modifying the original
    merged.update(dict2)
    return merged

def dict_keys(d):
    """Returns the keys of a dictionary."""
    return list(d.keys())

def dict_values(d):
    """Returns the values of a dictionary."""
    return list(d.values())

def dict_items(d):
    """Returns the items (key-value pairs) of a dictionary."""
    return list(d.items())

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
def get_current_time():
    """Returns the current time as a formatted string."""
    return time.strftime("%Y-%m-%d %H:%M:%S")

# Regular expression utilities
def regex_match(pattern, string):
    """Returns True if the pattern matches the string."""
    return bool(re.match(pattern, string))

def regex_find(pattern, string):
    """Finds all matches of the pattern in the string."""
    return re.findall(pattern, string)

def regex_replace(pattern, replacement, string):
    """Replaces occurrences of the pattern in the string with the replacement."""
    return re.sub(pattern, replacement, string)

# Functional programming utilities
def compose(*functions):
    """Returns a function that is the composition of the given functions."""
    def composed(x):
        for func in reversed(functions):
            x = func(x)
        return x
    return composed

def partial_func(func, *args, **kwargs):
    """Returns a partially applied function."""
    return partial(func, *args, **kwargs)

def memoize(func):
    """Memoizes a function by caching its results."""
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    return wrapper

# Concurrency utilities
def run_in_thread(func, *args):
    """Runs a function in a separate thread."""
    thread = threading.Thread(target=func, args=args)
    thread.start()
    return thread

# JSON utilities
def to_json(obj):
    """Converts an object to a JSON string."""
    return json.dumps(obj)

def from_json(json_string):
    """Converts a JSON string to a Python object."""
    return json.loads(json_string)

# Logging utilities
def setup_logger(name='pascaline'):
    """Sets up a logger with INFO level and stream handler."""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
