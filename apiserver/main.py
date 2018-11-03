from BaseHTTPServer import HTTPServer
import sys
# sys.path.append('config/')
# sys.path.append('db/')
# sys.path.append('restHandler/')
# sys.path.append('twitterStreaming/')
# sys.path.append('twitterStreaming/')

from restHandler.simplerequesthandler import SimpleRequestHandler
from db.dbconnect import DBConnect


def run(server_class=HTTPServer,
    handler_class=SimpleRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


def main():
	con = DBConnect().getDB()
	run()

if __name__ == '__main__':
	main()




# import cgi
# import json

# TODOS = [
#     {'id': 1, 'title': 'learn python'},
#     {'id': 2, 'title': 'get paid'},
# ]


# httpd = HTTPServer(('0.0.0.0', 8000), RestHTTPRequestHandler)
# while True:
#     httpd.handle_request()