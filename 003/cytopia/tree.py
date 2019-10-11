#!/usr/bin/env python3
"""Python multi-threaded webserver."""

import argparse
import sys


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
        "-d",
        "--dir",
        action="store_true",
        required=False,
        help="List directories only.",
    )
    parser.add_argument(
        "-L",
        "--level",
        metavar="lvl",
        required=False,
        help="Max display depth of directory tree.",
    )
    parser.add_argument(
        "-H",
        "--human",
        action="store_true",
        required=False,
        help="Print the size of each file but in a more human readable way.",
    )
    return parser.parse_args()


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------


def main():
    """Start the program."""
    args = get_args()


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
