# HTTPD server

![Language](https://img.shields.io/badge/Python-3-red.svg)
[![License](https://img.shields.io/badge/license-MIT-%233DA639.svg)](https://opensource.org/licenses/MIT)

A socket based web server written in Python 3 without any external dependencies.

## Usage
```bash
$ ./httpd.py -h
usage: httpd.py [-h] [-v] -r DIR [-i FILE] hostname port

Python httpd server.

positional arguments:
  hostname              address to listen on
  port                  port to listen on

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be verbose and print info to stderr
  -r DIR, --root DIR    path from where to serve documents
  -i FILE, --index FILE
                        defines the file that will be served as index
                        (default: index.html)
```

## Example
```bash
$ ./httpd.py -v -r docroot -i index.html 0.0.0.0 8080

Socket:     TCP
Binding:    0.0.0.0:8080
Listening:  backlog=1
Docroot:    docroot
Index:      index.html
```
In another terminal, you can access the files served by the webserver
```bash
curl localhost:8080
curl localhost:8080/index.html
curl localhost:8080/index.json
```
