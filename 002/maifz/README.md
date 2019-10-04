## Simple Webserver
![Language](https://img.shields.io/badge/Python-3-red.svg)
[![License](https://img.shields.io/badge/license-MIT-%233DA639.svg)](https://opensource.org/licenses/MIT)
##### Usage
```bash
./web-server.py -h

usage: web-server.py [-h] [-l LISTEN] [-p PORT] [-t TYPE] [-fp FILE_PATH]
                     [-ip INDEX_FILE_PATH]

Simple Webserver

optional arguments:
  -h, --help            show this help message and exit
  -l LISTEN, --listen LISTEN
                        IP-address on which your server should listen -
                        default= 127.0.0.1
  -p PORT, --port PORT  Port on which your server should listen - default=
                        8000
  -t TYPE, --type TYPE  Content Type, accepts text or text/plain
  -fp FILE_PATH, --file-path FILE_PATH
                        file-path to write text of POST
  -ip INDEX_FILE_PATH, --index-path INDEX_FILE_PATH
                        file-path to your index.html
```

##### Examples

listen to another port
```bash
./web-server.py -p 8080
``` 

listen to another ip
```bash
./web-server.py -l "192.168.199.199"
``` 

change the index.html
```bash
./web-server.py -ip "path/to/your.html"
```

change the content type header
```bash
./web-server.py -t "text/html"
```

change the file where the post should write into
```bash
./web-server.py -fp "path/to/your.txt"
```

