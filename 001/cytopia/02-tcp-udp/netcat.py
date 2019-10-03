#!/usr/bin/env python3

import argparse
import socket
import sys
import threading


# -------------------------------------------------------------------------------------------------
# GLOBALS
# -------------------------------------------------------------------------------------------------

# In case the server is running in UDP mode
# it must wait for the client to connect in order
# to retrieve its addr and port in order to be able
# to send data back to it.
UDP_CLIENT_ADDR = None
UDP_CLIENT_PORT = None


# -------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------------------------------

def b2str(data):
    '''Convert bytes into string type'''
    try:
        return data.decode('utf-8')
    except:
        pass
    try:
        return data.decode('utf-8-sig')
    except:
        pass
    try:
        return data.decode('ascii')
    except:
        return data.decode('latin-1')


# -------------------------------------------------------------------------------------------------
# CLIENT/SERVER COMMUNICATOIN FUNCTIONS
# -------------------------------------------------------------------------------------------------

def send(s, udp=False, crlf=False, verbose=False):
    '''Send one newline terminated line to a connected socket'''

    # In case of sending data back to an udp client we need to wait
    # until the client has first connected and told us its addr/port
    if udp and UDP_CLIENT_ADDR == None and UDP_CLIENT_PORT == None:
        while UDP_CLIENT_ADDR == None and UDP_CLIENT_PORT == None:
            pass
        if verbose:
            print('Client:     %s:%i' % (UDP_CLIENT_ADDR, UDP_CLIENT_PORT), file=sys.stderr)

    # Loop for the thread
    while True:
        # Read user input
        data = input()

        # Ensure to terminate with desired newline
        if isinstance(data, bytes):
            data = b2str(data)
        if crlf:
            data += "\r\n"
        else:
            data += "\n"

        size = len(data)
        data = data.encode()
        send = 0

        # Loop until all bytes have been send
        while send < size:
            try:
                if udp:
                    send += s.sendto(data, (UDP_CLIENT_ADDR, UDP_CLIENT_PORT))
                else:
                    send += s.send(data)
            except (OSError, socket.error) as error:
                print('[Send Error] %s' % (error), file=sys.stderr)
                print(s, file=sys.stderr)
                s.close()
                # exit the thread
                return

    # Close connection when thread stops
    s.close()


def receive(s, udp=False, bufsize=1024, verbose=False):
    '''Read one newline terminated line from a connected socket'''

    global UDP_CLIENT_ADDR
    global UDP_CLIENT_PORT

    if verbose:
        print('Receiving:  bufsize=%i' % (bufsize), file=sys.stderr)

    # Loop for the thread
    while True:
        data = ''
        size = len(data)

        while True:
            try:
                (byte, addr) = s.recvfrom(bufsize)
                data += b2str(byte)

                # If we're receiving data from a UDP client
                # we can finally set its addr/port in order
                # to send data back to it (see send() function)
                if udp:
                    UDP_CLIENT_ADDR, UDP_CLIENT_PORT = addr

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
# CLIENT/SERVER INITIALIZATION FUNCTIONS
# -------------------------------------------------------------------------------------------------

###
### Server/Client (TCP+UDP)
###
def create_socket(udp=False, verbose=False):
    '''Create TCP or UDP socket'''
    try:
        if udp:
            if verbose:
                print('Socket:     UDP', file=sys.stderr)
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            if verbose:
                print('Socket:     TCP', file=sys.stderr)
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as error:
        print('[Socker Error] %s', (error), file=sys.stderr)
        sys.exit(1)


###
### Server (TCP+UDP)
###
def bind(s, host, port, verbose=False):
    '''Bind TCP or UDP socket to host/port'''
    if verbose:
        print('Binding:    %s:%i' % (host, port), file=sys.stderr)
    try:
        s.bind((host, port))
    except (OverflowError, OSError, socket.error) as error:
        print('[Bind Error] %s' % (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)


###
### Server (TCP only)
###
def listen(s, backlog=1, verbose=False):
    '''Make TCP socket listen'''
    try:
        if verbose:
            print('Listening:  backlog=%i' % (backlog), file=sys.stderr)
        s.listen(backlog)
    except socket.error as error:
        print('[Listen Error] %s', (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)


###
### Server (TCP only)
###
def accept(s, verbose=False):
    '''Accept connections on TCP socket'''
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

    return c


###
### Client (TCP+UDP)
###
def resolve(hostname, verbose=False):
    '''Resolve hostname to IP addr or return False in case of error'''
    if verbose:
        print('Resolving:  %s' % (hostname), file=sys.stderr)
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror as error:
        print('[Resolve Error] %s' % (error), file=sys.stderr)
        return False


###
### Client (TCP+UDP)
###
def connect(s, addr, port, verbose=False):
    '''Connect to a server via IP addr/port'''
    if verbose:
        print('Connecting: %s:%i' % (addr, port), file=sys.stderr)
    try:
        s.connect((addr, port))
    except socket.error as error:
        print('[Connect Error] %s' % (error), file=sys.stderr)
        print(s, file=sys.stderr)
        s.close()
        sys.exit(1)


# -------------------------------------------------------------------------------------------------
# CLIENT
# -------------------------------------------------------------------------------------------------

def run_client(host, port, udp=False, bufsize=1024, crlf=False, verbose=False):
    '''Connect to host:port and send data'''

    global UDP_CLIENT_ADDR
    global UDP_CLIENT_PORT

    s = create_socket(udp=udp, verbose=verbose)

    addr = resolve(host, verbose=verbose)
    if not addr:
        s.close()
        sys.exit(1)

    if udp:
        UDP_CLIENT_ADDR = addr
        UDP_CLIENT_PORT = port
    else:
        connect(s, addr, port, verbose=verbose)

    # Start sending and receiving threads
    tr = threading.Thread(target=receive, args=(s, ), kwargs={'udp': udp, 'bufsize': bufsize, 'verbose': verbose})
    ts = threading.Thread(target=send, args=(s, ), kwargs={'udp': udp, 'crlf': crlf, 'verbose': verbose})
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
# SERVER
# -------------------------------------------------------------------------------------------------

def run_server(host, port, udp=False, backlog=1, bufsize=1024, crlf=False, verbose=False):
    '''Start TCP/UDP server on host/port and wait endlessly to sent/receive data'''

    s = create_socket(udp=udp, verbose=verbose)

    bind(s, host, port, verbose=verbose)

    if not udp:
        listen(s, backlog=backlog, verbose=verbose)
        c = accept(s, verbose=verbose)
    else:
        c = s

    # start sending and receiving threads
    tr = threading.Thread(target=receive, args=(c, ), kwargs={'udp': udp, 'bufsize': bufsize, 'verbose': verbose})
    ts = threading.Thread(target=send, args=(c, ), kwargs={'udp': udp, 'crlf': crlf, 'verbose': verbose})
    # if the main thread kills, this thread will be killed too.
    tr.daemon = True
    ts.daemon = True
    # start threads
    tr.start()
    ts.start()

    # do cleanup on the main program
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
    '''check arguments for invalid port number'''
    min_port = 1
    max_port = 65535
    intvalue = int(value)

    if intvalue < min_port or intvalue > max_port:
        raise argparse.ArgumentTypeError("%s is an invalid port number." % value)
    return intvalue


def get_args():
    '''Retrieve command line arguments'''
    parser = argparse.ArgumentParser(description='Netcat implementation in Python.')
    parser.add_argument('-l', '--listen', action='store_true', required=False,
                        help='listen mode, for inbound connects')
    parser.add_argument('-C', '--crlf', action='store_true', required=False,
                        help='send CRLF as line-endings (default: LF)')
    parser.add_argument('-u', '--udp', action='store_true', required=False,
                        help='UDP mode')
    parser.add_argument('-v', '--verbose', action='store_true', required=False,
                        help='be verbose and print info to stderr')
    parser.add_argument('hostname', type=str, help='address to listen or connect to')
    parser.add_argument('port', type=_args_check_port, help='port to listen on or connect to')
    return parser.parse_args()


# -------------------------------------------------------------------------------------------------
# MAIN ENTRYPOINT
# -------------------------------------------------------------------------------------------------

def main():
    '''main entrypoint'''

    args = get_args()

    listen_backlog = 1
    #receive_buffer = 4096
    receive_buffer = 1024

    if args.listen:
        run_server(
            args.hostname,
            args.port,
            args.udp,
            backlog=listen_backlog,
            bufsize=receive_buffer,
            crlf=args.crlf,
            verbose=args.verbose
        )
    else:
        run_client(
            args.hostname,
            args.port,
            args.udp,
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
