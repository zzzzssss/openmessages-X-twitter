from BaseHTTPServer import HTTPServer
import sys


from restHandler.simplerequesthandler import SimpleRequestHandler
from db.dbconnect import DBConnect


def run(server_class=HTTPServer,
    handler_class=SimpleRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
	run()

if __name__ == '__main__':
	main()

