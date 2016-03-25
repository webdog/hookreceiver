#!/usr/local/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
#import urlparse
import urllib
import time
import pprint

#Create a config file for these variables later
hostname = ""
hostport = 61000
pp = pprint.PrettyPrinter(indent=4)

class HookReceiver(BaseHTTPRequestHandler):
        def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()
                return

        def do_POST(self):
                length = int(self.headers['Content-Length'])
                post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
                print("INCOMING POST CONTENTS TO SCREEN")
                pp.pprint(post_data)
                self.send_response(200)
                self.send_header("Content-type", "text/json")
                self.end_headers()


if __name__ == '__main__':
        httpd = HTTPServer((hostname, hostport), HookReceiver)
        print(time.asctime(), "Server Starts - %s:%s" % (hostname, hostport))
        try:
                httpd.serve_forever()
        except KeyboardInterrupt:
                pass
        httpd.server_close()
        print(time.asctime(), "Server Stops - %s:%s" % (hostname, hostport))
