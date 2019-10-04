# netcat.py

Python netcat implementation with TCP and UDP support. (see [netcat.py](../01-tcp-only) for a TCP-only version).


## Usage
```bash
$ netcat.py -h

Netcat implementation in Python.

positional arguments:
  hostname       address to listen or connect to
  port           port to listen on or connect to

optional arguments:
  -h, --help     show this help message and exit
  -l, --listen   listen mode, for inbound connects
  -C, --crlf     send CRLF as line-endings (default: LF)
  -u, --udp      UDP mode
  -v, --verbose  be verbose and print info to stderr
```
