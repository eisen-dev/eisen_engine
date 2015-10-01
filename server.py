#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import portage
from gentoolkit.package import Package
from _emerge import main
import hashlib
import subprocess
import threading
import time
import Queue

class RequestHandler(pyjsonrpc.HttpRequestHandler):

  def emerge(self,package):
        bashCommand = "emerge -v "+package+" 2>&1 \n"
        print bashCommand
        UND = subprocess.Popen(bashCommand, stdout=subprocess.PIPE, shell=True)
        for line in UND.stdout:
            return line.strip('\n')

  @pyjsonrpc.rpcmethod
  def install_package(self,package):
        """install package.
        """
        q = Queue.Queue()
        print package
        t = threading.Thread(target=self.emerge, args=[package])
        t.daemon = True
        t.start()
        s = q.get()
        return s
  

  @pyjsonrpc.rpcmethod
  def get_all_packages_sha1(overlay_path):
        """Returns all packages sha1.
        """
        packages = {}
        porttree = portage.db[portage.root]['porttree']
        vartree = portage.db[portage.root]['vartree']
        ins_pkg = []
        for cp in porttree.dbapi.cp_all():
            for i in porttree.dbapi.cp_list(cp):
                ins_pkg.append(portage.catpkgsplit(i))
        sha1= hashlib.sha1(str(ins_pkg)).hexdigest()
        return sha1

  @pyjsonrpc.rpcmethod
  def get_all_packages(overlay_path):
        """Returns all packages from a given overlay path.
        """
        packages = {}
        porttree = portage.db[portage.root]['porttree']
        vartree = portage.db[portage.root]['vartree']
        ins_pkg = []
        for cp in porttree.dbapi.cp_all():
            for i in porttree.dbapi.cp_list(cp):
                ins_pkg.append(portage.catpkgsplit(i))
        return ins_pkg

  @pyjsonrpc.rpcmethod
  def get_installed_packages(overlay_path):
        """Returns installed packages from a given overlay path.
        """
        packages = {}
        porttree = portage.db[portage.root]['porttree']
        vartree = portage.db[portage.root]['vartree']
        ins_pkg = []
        for cp in porttree.dbapi.cp_all():
            for i in vartree.dbapi.cp_list(cp):
                ins_pkg.append(portage.catpkgsplit(i))
        return ins_pkg

  @pyjsonrpc.rpcmethod
  def get_installed_packages_sha1(overlay_path):
        """Returns installed packages sha1.
        """
        packages = {}
        porttree = portage.db[portage.root]['porttree']
        vartree = portage.db[portage.root]['vartree']
        ins_pkg = []
        for cp in porttree.dbapi.cp_all():
            for i in vartree.dbapi.cp_list(cp):
                ins_pkg.append(portage.catpkgsplit(i))
        sha1= hashlib.sha1(str(ins_pkg)).hexdigest()
        return sha1

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()
