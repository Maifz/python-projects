import argparse
import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from http.server import HTTPServer, BaseHTTPRequestHandler
from filehandler.file_handler import FileHandler
from argshelper.args_helper import ArgsHelper


class Webserver(BaseHTTPRequestHandler):
    file_handler = FileHandler()

    args_helper = ArgsHelper.getInstance()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', self.args_helper.getContentType())
        self.wfile.write(Webserver.file_handler.readFile(self.args_helper.getIndexFilePath()))


    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        self.send_response(200)
        Webserver.file_handler.appendToFile('test.txt', post_data)
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
    except KeyboardInterrupt as msg:
        print("cancel")
        sys.exit(1)

