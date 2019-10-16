#!/usr/bin/env python3
"""Python tree implementation."""

import argparse
import os
import sys
import locale

# -------------------------------------------------------------------------------------------------
# GLOBALS
# -------------------------------------------------------------------------------------------------

# Keep track of num of dirs and files
CNT_DIRS = 0
CNT_FILES = 0


# -------------------------------------------------------------------------------------------------
# Tree Functions
# -------------------------------------------------------------------------------------------------


def get_size(path, do_print=False):
    """Get size of dir/file in a formatted way."""
    if not do_print:
        return ""
    # size in bytes
    size = int(os.path.getsize(path))
    # sizes in unites
    kilo = 1024
    mega = kilo * 1024
    giga = mega * 1024
    tera = giga * 1024
    peta = tera * 1024
    exa = peta * 1024
    zetta = exa * 1024
    yotta = zetta * 1024

    if size >= yotta:
        result = size / yotta
        unit = "Y"
    if size >= zetta:
        result = size / zetta
        unit = "Z"
    elif size >= exa:
        result = size / exa
        unit = "E"
    elif size >= peta:
        result = size / peta
        unit = "P"
    elif size >= tera:
        result = size / tera
        unit = "T"
    elif size >= giga:
        result = size / giga
        unit = "G"
    elif size >= mega:
        result = size / mega
        unit = "M"
    elif size >= kilo:
        result = size / kilo
        unit = "K"
    # size < 1024:
    else:
        result = size
        unit = None

    if unit is not None:
        if result >= 10:
            output = "{:.0f}{}".format(result, unit)
        else:
            output = "{:.1f}{}".format(result, unit)
    else:
        output = "{}".format(result)

    return "[{:>4}]  ".format(output)


def retrieve_files(path, hidden=False, dir_only=False):
    """Retrieve files/dirs from a path based on criteria."""
    # Get files
    files = os.listdir(path=path)
    # Remove hidden files/dirs (anything that starts with dot)
    if not hidden:
        files = list(filter(lambda x: True if not x.startswith(".") else False, files))
    # Remove files and only keep directories
    if dir_only:
        files = list(filter(lambda x, path=path: os.path.isdir(os.path.join(path, x)), files))
    # Sort files
    collate = os.environ["LC_ALL"] if "LC_ALL" in os.environ else "C"
    locale.setlocale(locale.LC_COLLATE, collate)
    files.sort(key=locale.strxfrm)

    return files


def print_tree(path, hidden=False, dir_only=False, human=False, level=None, curr_level=1, prevs=[]):
    """Get files recursively."""
    global CNT_DIRS
    global CNT_FILES

    # Get files and sort alphabetically
    files = retrieve_files(path, hidden=hidden, dir_only=dir_only)
    total = len(files)
    last = total - 1  # last index

    for idx, f in enumerate(files):
        abs_path = os.path.join(path, f)

        if os.path.isdir(abs_path):
            CNT_DIRS += 1
        else:
            CNT_FILES += 1

        # Print previous recursion round delimiter
        for delim in prevs:
            print(delim, end="")

        # If it is the last element on the current level, then
        # print the sign that shows the last element
        if idx == last:
            print("%s" % ("└── "), end="")
        # If more elements are to come, then we print the sign,
        # that has continuation
        else:
            print("%s" % ("├── "), end="")
        print("%s%s" % (get_size(abs_path, human), f))

        if level is None or level > curr_level:
            if os.path.isdir(abs_path):
                # Build delimiter for next recursion round
                tmp = prevs.copy()

                # If it is not the last element on this level, (there is an element after it)
                # we need to print the dashes until the element is reached
                if idx < last:
                    tmp.append("│   ")
                # If it is the last element on this level, we do not print
                # the continuation line, but just empty spaces.
                else:
                    tmp.append("    ")

                # Recurse for directories
                print_tree(abs_path, hidden, dir_only, human, level, curr_level + 1, tmp)


# -------------------------------------------------------------------------------------------------
# ARG CHECKERS
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


# -------------------------------------------------------------------------------------------------
# COMMAND LINE ARGUMENTS
# -------------------------------------------------------------------------------------------------


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
        help="Max display depth of directory tree.",
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
    print_tree(args.path, args.all, args.dir, args.human, args.level)

    if args.dir:
        print("\n%i %s" % (CNT_DIRS, "directory" if CNT_DIRS == 1 else "directories"))
    else:
        print(
            "\n%i %s, %i %s"
            % (
                CNT_DIRS,
                "directory" if CNT_DIRS == 1 else "directories",
                CNT_FILES,
                "file" if CNT_FILES == 1 else "files",
            )
        )


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
