# HTTPD server


## Usage
```bash
$ ./httpd.py -h
usage: httpd.py [-h] [-v] -d DIR [-i INDEX] hostname port

Python httpd server.

positional arguments:
  hostname              address to listen on
  port                  port to listen on

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         be verbose and print info to stderr
  -d DIR, --docroot DIR
                        path from where to serve documents
  -i INDEX, --index INDEX
                        defines the file that will be served as index
                        (default: index.html)
```

## Example
```bash
$ ./httpd.py -v -d docroot -i index.html 0.0.0.0 8080

Socket:     TCP
Binding:    0.0.0.0:8080
Listening:  backlog=1
Docroot:    docroot
Index:      index.html
```
