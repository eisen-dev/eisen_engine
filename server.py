#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def add(self, a, b):
      """Test method"""
      return a + b


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()
