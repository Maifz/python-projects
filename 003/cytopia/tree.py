#!/usr/bin/env python3
"""Python tree implementation."""

import argparse
import os
import sys


# -------------------------------------------------------------------------------------------------
# COMMAND LINE ARGUMENTS
# -------------------------------------------------------------------------------------------------


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
        "-L", "--level", metavar="lvl", required=False, help="Max display depth of directory tree."
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
    print(args)


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
