#!/usr/local/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import time
import pprint
from slackclient import SlackClient
import json

#Create a config file for these variables later
hostname = ""
hostport = 61000
pp = pprint.PrettyPrinter(indent=4)

class HookReceiver(BaseHTTPRequestHandler):
		def do_GET(self):
                    self.send_response(400)
                    self.send_header("Content-type", "text/json")
                    self.end_headers()
                    return

		def _deliver(self, contents):
                    token = "test123"
                    sc = SlackClient(token)
                    return sc.api_call("chat.postMessage", channel="#general", text=contents, username="webdog-bot")

		def do_POST(self):
                    length = int(self.headers['Content-Length'])
                    #The header below descibes the type of message this is.
                    action = self.headers['X-GitHub-Event']
                    #Decode the binary message and move it into a JSON object
                    post_data = json.loads(self.rfile.read(length).decode("utf-8"))
                    if "create" in action:
                        contents = (action, post_data['ref'])
                        #self._deliver(contents)
                    elif "pull_request" in action:
                        url = post_data['pull_request']['url']
                        title = post_data['pull_request']['title']
                        
                        contents = "Pull Request %s(%s) was %s\n%s" %(post_data['number'], title, post_data['action'], url) 
                        self._deliver(contents)
                    elif "status" in action:
                        url = post_data["commit"]["html_url"]
                        state = post_data["state"]
                        branch = post_data["branches"][0]["name"]
                        
                        contents = "Build Triggered on Branch %s with status update: %s\n%s" % (branch, state, url)
                        self._deliver(contents)
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
