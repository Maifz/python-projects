#!/usr/bin/env python3
"""Python netcat implementation for TCP."""

import argparse
import socket
import sys
import threading


# -------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------------------------------

def b2str(data):
    """Convert bytes into string type."""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        pass
    try:
        return data.decode('utf-8-sig')
    except UnicodeDecodeError:
        pass
    try:
        return data.decode('ascii')
    except UnicodeDecodeError:
        return data.decode('latin-1')


# -------------------------------------------------------------------------------------------------
# CLIENT/SERVER FUNCTIONS
# -------------------------------------------------------------------------------------------------

def send(s, crlf=False, verbose=False):
    """Send one newline terminated line to a connected socket."""
    # Loop for the thread
    while True:
        # Read user input
        data = input()

        # Ensure to append newline
        if isinstance(data, bytes):
            data = b2str(data)
        if crlf:
            data += "\r\n"
        else:
            data += "\n"

        # Convert back to bytes and send
        try:
            s.sendall(data.encode())
        except socket.error:
            if verbose:
                print('Upstream connection is gone while sending', file=sys.stderr)
            s.close()
            # exit the thread
            return

    # Close connection when thread stops
    s.close()


def receive(s, bufsize=1024, verbose=False):
    """Read one newline terminated line from a connected socket."""
    # Loop for the thread
    while True:
        data = ''
        size = len(data)

        while True:
            try:
                data += b2str(s.recv(bufsize))
            except socket.error as err:
                print(err, file=sys.stderr)
                s.close()
                sys.exit(1)
            if not data:
                if verbose:
                    print('upstream connection is gone while receiving', file=sys.stderr)
                s.close()
                # exit the thread
                return
            # Newline terminates the read request
            if data.endswith("\n"):
                break
            # Sometimes a newline is missing at the end
            # If this round has the same data length as previous, we're done
            if size == len(data):
                break
            size = len(data)
        # Remove trailing newlines
        data = data.rstrip("\r\n")
        data = data.rstrip("\n")
        if verbose:
            print('< ', end='', flush=True, file=sys.stderr)
        print(data)

    # Close connection when thread stops
    s.close()


# -------------------------------------------------------------------------------------------------
# CLIENT FUNCTIONS
# -------------------------------------------------------------------------------------------------

def connect(host, port, bufsize=1024, crlf=False, verbose=False):
    """Connect to host:port and send data."""
    # Create socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        s.close()
        print(msg, file=sys.stderr)
        sys.exit(1)

    # Get remote IP
    if verbose:
        print('Resolving:  ', host, file=sys.stderr)
    try:
        addr = socket.gethostbyname(host)
    except socket.gaierror as msg:
        s.close()
        print(msg, file=sys.stderr)
        sys.exit(1)

    # Bind socket
    if verbose:
        print('Connecting: ', addr + ':' + str(port), file=sys.stderr)
    try:
        s.connect((addr, port))
    except socket.error as msg:
        s.close()
        print(msg, file=sys.stderr)
        sys.exit(1)

    # Start sending and receiving threads
    tr = threading.Thread(target=receive, args=(s, ), kwargs={
        'bufsize': bufsize,
        'verbose': verbose
    })
    ts = threading.Thread(target=send, args=(s, ), kwargs={
        'crlf': crlf,
        'verbose': verbose
    })
    # If the main thread kills, this thread will be killed too.
    tr.daemon = True
    ts.daemon = True
    # Start threads
    tr.start()
    ts.start()

    # Do cleanup on the main program
    while True:
        if not tr.is_alive():
            s.close()
            sys.exit(0)
        if not ts.is_alive():
            s.close()
            sys.exit(0)


# -------------------------------------------------------------------------------------------------
# SERVER FUNCTIONS
# -------------------------------------------------------------------------------------------------

def listen(host, port, backlog=1, bufsize=1024, crlf=False, verbose=False):
    """Listen on host:port and wait endlessly for client to send data."""
    try:
        # Create server socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind socket
        if verbose:
            print('Binding:   ', host + ':' + str(port), file=sys.stderr)
        s.bind((host, port))

        # Listen on socket
        if verbose:
            print('Listening:', ' backlog=' + str(backlog), file=sys.stderr)
        s.listen(backlog)

    except (OverflowError, socket.error) as msg:
        s.close()
        print(msg, file=sys.stderr)
        sys.exit(1)

    # Accept connection and get client socket and address tuple
    c, addr = s.accept()
    host, port = addr
    if verbose:
        print('Connected: ', str(host) + ':' + str(port), file=sys.stderr)
        print('Receiving: ', 'bufsize=' + str(bufsize), file=sys.stderr)

    # Start sending and receiving threads
    tr = threading.Thread(target=receive, args=(c, ), kwargs={
        'bufsize': bufsize,
        'verbose': verbose
    })
    ts = threading.Thread(target=send, args=(c, ), kwargs={
        'crlf': crlf,
        'verbose': verbose
    })
    # If the main thread kills, this thread will be killed too.
    tr.daemon = True
    ts.daemon = True
    # Start threads
    tr.start()
    ts.start()

    # Do cleanup on the main program
    while True:
        if not tr.is_alive():
            c.close()
            s.close()
            sys.exit(0)
        if not ts.is_alive():
            c.close()
            s.close()
            sys.exit(0)


# -------------------------------------------------------------------------------------------------
# COMMAND LINE ARGUMENTS
# -------------------------------------------------------------------------------------------------

def _args_check_port(value):
    """Check arguments for invalid port number."""
    min_port = 1
    max_port = 65535
    intvalue = int(value)

    if intvalue < min_port or intvalue > max_port:
        raise argparse.ArgumentTypeError("%s is an invalid port number." % value)
    return intvalue


def get_args():
    """Retrieve command line arguments."""
    parser = argparse.ArgumentParser(description='Netcat implementation in Python.')
    parser.add_argument('-l', '--listen', action='store_true', required=False,
                        help='listen mode, for inbound connects')
    parser.add_argument('-C', '--crlf', action='store_true', required=False,
                        help='send CRLF as line-endings (default: LF)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='be verbose and print info to stderr')
    parser.add_argument('hostname', type=str, help='address to listen or connect to')
    parser.add_argument('port', type=_args_check_port, help='port to listen on or connect to')
    return parser.parse_args()


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------

def main():
    """Start the program."""
    args = get_args()

    listen_backlog = 1
    receive_buffer = 1024

    if args.listen:
        listen(
            args.hostname,
            args.port,
            backlog=listen_backlog,
            bufsize=receive_buffer,
            crlf=args.crlf,
            verbose=args.verbose
        )

    else:
        connect(
            args.hostname,
            args.port,
            bufsize=receive_buffer,
            crlf=args.crlf,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
