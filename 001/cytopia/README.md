# netcat.py

Python netcat implementations

| Name                     | Description             |
|--------------------------|-------------------------|
| [netcat.py](01-tcp-only) | Netcat TCP-only version |
| [netcat.py](02-tcp-udp)  | Netcat TCP/UDP version  |

## Usage (TCP-only)
```bash
$ 01-tcp-only/netcat.py -h

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

## Usage (TCP/UDP)
```bash
$ 02-tcp-udp/netcat.py -h

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
