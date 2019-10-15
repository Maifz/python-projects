#!/usr/bin/env python3
"""Python tree implementation."""

import argparse
import os
import re
import sys
from functools import cmp_to_key


# -------------------------------------------------------------------------------------------------
# GLOBALS
# -------------------------------------------------------------------------------------------------

# Compiled regex to check for alphanumerics
IS_ALPHANUM = re.compile(r'[a-zA-Z0-9]')

# Keep track of num of dirs and files
CNT_FILES = 0
CNT_DIRS = 0


# -------------------------------------------------------------------------------------------------
# SORT FUNCTIONS
# -------------------------------------------------------------------------------------------------


def sort_default(a, b):
    """
    Sort dirs/files by default tree sorting.

    returns 0 if elements are equal
    returns -1 if a is smaller than b
    returns 1 if a is greater than b
    """
    # Both characters are alphanumeric
    if IS_ALPHANUM.match(a[0]) and IS_ALPHANUM.match(b[0]):
        if a[0].lower() < b[0].lower():
            return -1
        elif a[0].lower() > b[0].lower():
            return 1
    # Only a is alphanumeric
    elif IS_ALPHANUM.match(a[0]) and IS_ALPHANUM.match(b[0]) is None:
        if len(b) > 1:
            return sort_default(a, b[1:])
        return 1
    # Only b is alphanumeric
    elif IS_ALPHANUM.match(a[0]) is None and IS_ALPHANUM.match(b[0]):
        if len(a) > 1:
            return sort_default(a[1:], b)
        return -1

    # Nothing matches, compare the next character if it has it
    if len(a) == 1 and len(b) == 1:
        return -1 if ord(a[0]) <= ord(b[0]) else 0
    elif len(a) == 1 and len(b) > 1:
        return -1
    elif len(a) > 1 and len(b) == 1:
        return 1
    else:
        # Remove first from both strings char and recurse
        return sort_default(a[1:], b[1:])


# -------------------------------------------------------------------------------------------------
# Tree Functions
# -------------------------------------------------------------------------------------------------


def retrieve_files(path, hidden=False, dir_only=False):
    """Retrieve files/dirs from a path based on criteria."""
    # Get files
    files = os.listdir(path=path)

    # Remove hidden files/dirs (anything that starts with dot)
    if not hidden:
        files = list(filter(lambda x: True if not x.startswith('.') else False, files))
    # Remove files and only keep directories
    if dir_only:
        files = list(filter(lambda x, path=path: os.path.isdir(os.path.join(path, x)), files))
    # Sort files
    files = sorted(files, key=cmp_to_key(sort_default))

    return files


def print_tree(path, hidden=False, dir_only=False, level=None, curr_level=1, prevs=[]):
    """Get files recursively."""
    global CNT_DIRS
    global CNT_FILES
    # Get files and sort alphabetically
    files = retrieve_files(path, hidden=hidden, dir_only=dir_only)
    total = len(files)
    last = total - 1  # last index

    for idx, f in enumerate(files):
        abs_path = os.path.join(path, f)

        # Print previous recursion round delimiter
        for delim in prevs:
            print(delim, end='')

        # If it is the last element on the current level, then
        # print the sign that shows the last element
        if idx == last:
            print('%s' % ('└── '), end='')
        # If more elements are to come, then we print the sign,
        # that has continuation
        else:
            print('%s' % ('├── '), end='')
        print('%s' % f)

        if level is None or level > curr_level:
            if os.path.isdir(abs_path):
                CNT_DIRS += 1
                # Build delimiter for next recursion round
                tmp = prevs.copy()

                # If it is not the last element on this level, (there is an element after it)
                # we need to print the dashes until the element is reached
                if idx < last:
                    tmp.append('│   ')
                # If it is the last element on this level, we do not print
                # the continuation line, but just empty spaces.
                else:
                    tmp.append('    ')

                print_tree(abs_path, hidden, dir_only, level, curr_level+1, tmp)
            else:
                CNT_FILES += 1


# -------------------------------------------------------------------------------------------------
# COMMAND LINE ARGUMENTS
# -------------------------------------------------------------------------------------------------


def _args_check_level(value):
    """Check if level is correct."""
    try:
        intval = int(value)
    except Exception:
        raise argparse.ArgumentTypeError("%s must be an integer." % value)

    if intval < 1:
        raise argparse.ArgumentTypeError("%s must be greater than 0." % value)

    return int(value)


def _args_check_path(value):
    """Check if path exists."""
    if not os.path.isdir(value):
        raise argparse.ArgumentTypeError("%s directory does not exist." % value)

    return value


def get_args():
    """Retrieve command line arguments."""
    parser = argparse.ArgumentParser(description="Python tree implementation.")
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        required=False,
        help="All files are printed. By default tree does not print hidden files.",
    )
    parser.add_argument(
        "-d", "--dir", action="store_true", required=False, help="List directories only."
    )
    parser.add_argument(
        "-L",
        "--level",
        metavar="lvl",
        type=_args_check_level,
        required=False,
        help="Max display depth of directory tree."
    )
    parser.add_argument(
        "-H",
        "--human",
        action="store_true",
        required=False,
        help="Print the size of each file but in a more human readable way.",
    )
    parser.add_argument(
        "path",
        type=_args_check_path,
        nargs="?",
        default=".",
        help="address to listen or connect to",
    )
    return parser.parse_args()


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------


def main():
    """Start the program."""
    args = get_args()

    print(args.path)
    print_tree(args.path, args.all, args.dir, args.level)

    if args.dir:
        print("\n%i %s" % (CNT_DIRS, 'directory' if CNT_DIRS == 1 else 'directories'))
    else:
        print("\n%i %s, %i %s" % (
            CNT_DIRS,
            'directory' if CNT_DIRS == 1 else 'directories',
            CNT_FILES,
            'file' if CNT_FILES == 1 else 'files',
        ))


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
