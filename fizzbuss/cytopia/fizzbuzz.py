#!/usr/bin/env python3
"""Fizzbuzz."""

import sys


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------


def main():
    """Start the program."""
    for i in range(1, 101):
        print("%d: " % (i), end="")
        if i % 3 == 0:
            print("%s" % ("fizz"), end="")
        if i % 5 == 0:
            print("%s" % ("buzz"), end="")
        print()


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
