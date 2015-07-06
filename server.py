#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc


class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def add(self, a, b):
      """Test method"""
      return a+b

  @pyjsonrpc.rpcmethod
  def get_all_packages(overlay_path):
        import portage
        from gentoolkit.package import Package
        """Returns all packages from a given overlay path.
        """
        packages = {}
        porttree = portage.db[portage.root]['porttree']
        vartree = portage.db[portage.root]['vartree']
        ins_pkg = []
        for cp in porttree.dbapi.cp_all():
            ins_pkg.append(cp)
        return ins_pkg

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()
