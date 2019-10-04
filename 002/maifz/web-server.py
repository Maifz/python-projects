#!/usr/bin/env python3
import argparse
import sys
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from filehandler.filehandler import FileHandler
from argshelper.argshelper import ArgsHelper


class Webserver(BaseHTTPRequestHandler):
    file_handler = FileHandler()

    args_helper = ArgsHelper.getInstance()

    def do_GET(self):
        try:
            self.wfile.write(Webserver.file_handler.readFile(self.args_helper.getIndexFilePath()))
        except FileNotFoundError:
            self.send_response(404)
            return

        self.send_response(200)
        self.send_header('Content-Type', self.args_helper.getContentType())
        self.end_headers()

    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
        except TypeError:
            self.send_response(411)
            return

        response = Webserver.file_handler.appendToFile(self.args_helper.getWriteFilePath(), post_data)

        if not response:
            self.send_response(404)
            return

        self.send_response(200)
        print(post_data)


PORT = 8000
SERVER_ADDRESS = '127.0.0.1'
CONTENT_TYPE = "text/plain"
DEFAULT_FILE = "test.txt"
DEFAULT_INDEX_FILE = "index.html"


def run_server(server_address, port):
    server = HTTPServer((server_address, port), Webserver)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description='Simple Webserver')
    parser.add_argument(
        "-l",
        "--listen",
        default=SERVER_ADDRESS,
        help="IP-address on which your server should listen - default= " + str(SERVER_ADDRESS)
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=PORT,
        help="Port on which your server should listen - default= " + str(PORT)
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default=CONTENT_TYPE,
        help="Content Type, accepts text or text/plain"
    )
    parser.add_argument(
        "-fp",
        "--file-path",
        type=str,
        default=DEFAULT_FILE,
        help="file-path to write text of POST",
        dest="file_path"
    )
    parser.add_argument(
        "-ip",
        "--index-path",
        type=str,
        default=DEFAULT_INDEX_FILE,
        help="file-path to your index.html",
        dest="index_file_path"
    )
    args = parser.parse_args()
    args_helper = ArgsHelper.getInstance()
    args_helper.initializeArguments(args.type, args.file_path, args.index_file_path)

    run_server(args.listen, args.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\ncancel\n")
        sys.exit(1)
