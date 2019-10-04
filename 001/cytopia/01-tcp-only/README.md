# netcat.py

Python netcat implementation with TCP-only support. (see [netcat.py](../02-tcp-udp) for TCP and UDP support).


## Usage
```bash
$ netcat.py -h
usage: netcat.py [-h] [-l] [-C] [-v] hostname port

Netcat implementation in Python.

positional arguments:
  hostname       address to listen or connect to
  port           port to listen on or connect to

optional arguments:
  -h, --help     show this help message and exit
  -l, --listen   listen mode, for inbound connects
  -C, --crlf     send CRLF as line-endings (default: LF)
  -v, --verbose  be verbose and print info to stderr
```
