#!/usr/bin/env python3
"""Python multi-threaded webserver."""

import argparse
import os
import re
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
# LOW-LEVEL COMMUNICATION FUNCTIONS
# -------------------------------------------------------------------------------------------------

def send(s, data, verbose=False):
    """Send data to a connected socket."""
    # Ensure to terminate with desired newline
    if isinstance(data, bytes):
        data = b2str(data)

    lines = data.split("\n")

    for line in lines:
        line += "\n"
        size = len(line)
        line = line.encode()
        send = 0

        # Loop until all bytes have been send
        while send < size:
            try:
                send += s.send(line)
            except (OSError, socket.error) as error:
                print('[Send Error] %s' % (error), file=sys.stderr)
                print(s, file=sys.stderr)
                s.close()
                return


def recv(s, bufsize=1024, verbose=False):
    """Receive data from a connected socket."""
    data = ''
    size = len(data)

    while True:
        try:
            data += b2str(s.recv(bufsize))
        except socket.error as err:
            print(err, file=sys.stderr)
            print(s, file=sys.stderr)
            s.close()
            sys.exit(1)
        if not data:
            if verbose:
                print('[Receive Error] Upstream connection is gone', file=sys.stderr)
            s.close()
            # exit the thread
            return None
        # Newline terminates the read request
        if data.endswith("\n"):
            break
        if data.endswith("\0"):
            break
        # Sometimes a newline is missing at the end
        # If this round has the same data length as previous, we're done
        if size == len(data):
            break
        size = len(data)

    return data


# -------------------------------------------------------------------------------------------------
# HIGH-LEVEL REQUEST/RESPOND FUNCTIONS
# -------------------------------------------------------------------------------------------------

def retrieve_request(s, host, port, bufsize=1024, verbose=False):
    """Get client request."""
    data = recv(s, bufsize=bufsize, verbose=verbose)

    # Client disconnected unexpectedly (without sending anything)
    if data is None:
        return

    lines = data.split("\n")
    if verbose:
        for line in lines:
            print('%s:%i < %s' % (host, port, line), file=sys.stderr)

    # Extract HTTP Request from first line
    regex = re.compile(r'(GET|POST|HEAD|PUT|DELETE|PATCH)\s+(.+)+\s+HTTP\/([1-2]\.[0-1])')
    match = regex.match(lines[0])

    # Check if request is valid
    if match is None or len(match.groups()) != 3:
        send(s, 'HTTP/1.1 400\r\n\r\nBad Request', verbose=verbose)
        return

    verb = match.group(1)
    path = match.group(2)
    vers = match.group(3)

    return verb, path, vers


def respond_get(s, path, vers, verbose=False):
    """Respond to a GET request to the client."""
    if not os.path.isfile(path):
        send(s, 'HTTP/'+vers+' 404\r\n\r\nFile not found', verbose=verbose)
        return

    ext = os.path.splitext(path)[1]

    # Respond with 200
    send(s, 'HTTP/'+vers+' 200 OK', verbose=verbose)

    # Add content-type headers
    if ext in ['.html', '.html']:
        send(s, 'Content-Type: text/html; charset=utf-8\r\n', verbose=verbose)
    elif ext in ['.json']:
        send(s, 'Content-Type: application/json; charset=utf-8\r\n', verbose=verbose)
    else:
        send(s, 'Content-Type: text/plain; charset=utf-8\r\n', verbose=verbose)

    # Serve the content
    with open(path) as content:
        line = content.read()
        print(line)
        send(s, line, verbose=verbose)


# -------------------------------------------------------------------------------------------------
# THREADED REQUEST SERVING
# -------------------------------------------------------------------------------------------------

def serve(s, host, port, docroot, index, bufsize=1024, verbose=False):
    """Threaded function to serve HTTP requests. One call per client."""
    request = retrieve_request(s, host, port, bufsize=bufsize, verbose=verbose)
    if request is None:
        s.close()
        return

    # Split request
    verb, path, vers = request

    # Build filesystem path from document root and request path
    path = '%s/%s' % (docroot, index) if path == '/' else '%s/%s' % (docroot, path)

    if verb == 'GET':
        respond_get(s, path, vers, verbose)
    elif verb == 'HEAD':
        send(s, 'HTTP/'+vers+' 200 OK\r\n', verbose=verbose)
    else:
        # TODO: Other HTTP verbs are not yet implemented
        send(s, 'HTTP/'+vers+' 501\r\n\r\nNot implemented', verbose=verbose)

    s.close()
    return


# -------------------------------------------------------------------------------------------------
# SERVER INITIALIZATION FUNCTIONS
# -------------------------------------------------------------------------------------------------

def create_socket(verbose=False):
    """Create TCP socket."""
    try:
        if verbose:
            print('Socket:     TCP', file=sys.stderr)
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print('[Socker Error] %s', (error), file=sys.stderr)
        sys.exit(1)


def bind(s, host, port, verbose=False):
    """Bind TCP or UDP socket to host/port."""
    if verbose:
        print('Binding:    %s:%i' % (host, port), file=sys.stderr)
    try:
        s.bind((host, port))
    except (OverflowError, OSError, socket.error) as error:
        print('[Bind Error] %s' % (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)


def listen(s, backlog=1, verbose=False):
    """Make TCP socket listen."""
    try:
        if verbose:
            print('Listening:  backlog=%i' % (backlog), file=sys.stderr)
        s.listen(backlog)
    except socket.error as error:
        print('[Listen Error] %s', (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)


def accept(s, verbose=False):
    """Accept connections on TCP socket."""
    try:
        c, addr = s.accept()
    except (socket.gaierror, socket.error) as error:
        print('[Accept Error] %s', (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)

    host, port = addr
    if verbose:
        print('Client:     %s:%i' % (host, port), file=sys.stderr)

    return c, host, port


# -------------------------------------------------------------------------------------------------
# SERVER
# -------------------------------------------------------------------------------------------------

def run_server(host, port, docroot, index, backlog=1, bufsize=1024, verbose=False):
    """Start TCP/UDP server on host/port and wait endlessly to sent/receive data."""
    s = create_socket(verbose=verbose)

    bind(s, host, port, verbose=verbose)
    listen(s, backlog=backlog, verbose=verbose)

    if verbose:
        print('Receiving:  bufsize=%i' % (bufsize), file=sys.stderr)
        print('Docroot:    %s' % docroot, file=sys.stderr)
        print('Index:      %s' % index, file=sys.stderr)

    # Accept clients
    while True:
        # Blocking call until a new client connects
        c, h, p = accept(s, verbose=verbose)
        t = threading.Thread(target=serve, args=(c, ), kwargs={
            'host': h,
            'port': p,
            'docroot': docroot,
            'index': index,
            'bufsize': bufsize,
            'verbose': verbose
        })
        # if the main thread kills, this thread will be killed too.
        t.daemon = True
        t.start()


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


def _args_check_docroot(value):
    """Check arguments for invalid port number."""
    strvalue = str(value)

    if not os.path.exists(strvalue):
        raise argparse.ArgumentTypeError("%s path does not exist." % value)
    if not os.path.isdir(strvalue):
        raise argparse.ArgumentTypeError("%s is not a directory." % value)

    return strvalue


def get_args():
    """Retrieve command line arguments."""
    parser = argparse.ArgumentParser(description='Python httpd server.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='be verbose and print info to stderr')
    parser.add_argument('-r', '--root', metavar='DIR', required=True,
                        type=_args_check_docroot, help='path from where to serve documents')
    parser.add_argument('-i', '--index', metavar='FILE', default='index.html', required=False,
                        help='defines the file that will be served as index (default: index.html)')
    parser.add_argument('hostname', type=str, help='address to listen on')
    parser.add_argument('port', type=_args_check_port, help='port to listen on')
    return parser.parse_args()


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------

def main():
    """Start the program."""
    args = get_args()

    listen_backlog = 1
    receive_buffer = 1024

    run_server(
        args.hostname,
        args.port,
        args.root,
        args.index,
        backlog=listen_backlog,
        bufsize=receive_buffer,
        verbose=args.verbose
    )


if __name__ == "__main__":
    # Catch Ctrl+c and exit without error message
    try:
        main()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
