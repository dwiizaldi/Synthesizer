#!/usr/bin/python
#
#

import sys
import SocketServer
import threading
import argparse
import re
import cgi
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import time
import json
import ast
import subprocess
import os.path
from os import path


# 
CMD_DESCRIPTIONS = '\
   - support restful-api calls\n\
	- add key/value pair to store\n\
		- retrieve key/value from store\n\
   - recordID : key, data : value\n\
\n'


#
class LocalData(object):
  records = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):


  def do_POST(self,need_reinit=False):
    global attr, delay_post_f, delay_post_b, delay_get_f, delay_get_b, time
 

#====================FOR ADDING RECORD AND SET DELAY==========================

    if None != re.search('/api/v1/addrecord/*', self.path):
      print "something for addrecord"
      # delay
      time.sleep(float(delay_post_f))

      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        recordID = self.path.split('/')[-1]
        LocalData.records[recordID] = data
        print "record added successfully - key: %s, value: %s" % (recordID, data)
      else:
        data = {}

      # delay
      time.sleep(float(delay_post_b))

      self.send_response(200)
      self.end_headers()


    elif None != re.search('/api/v1/setdelay/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
	dtype = self.path.split('/')[-1]
	LocalData.records[dtype] = data
	for kkey in data:
	  pass
	print "new delay inputted - type: %s, value: %s" % (dtype, kkey)
	if dtype == 'delay_post_f':
	  delay_post_f = kkey
	elif dtype == 'delay_post_b':
	  delay_post_b = kkey
	elif dtype == 'delay_get_f':
	  delay_get_f = kkey
	elif dtype == 'delay_get_b':
	  delay_get_b = kkey	
        print "current delay values are: %s, %s, %s, %s" % (delay_post_f, delay_post_b, delay_get_f, delay_get_b)
      else:
        data = {}

      self.send_response(200)
      self.end_headers()


    elif None != re.search('/api/v1/setstress/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        stype = self.path.split('/')[-1]
        LocalData.records[stype] = data
        for num in data:
          value,time = num.split(",")

        if stype == 'cpu':
          print "start stressing CPU with load %s%% within %ss" % (value,time)           
          subprocess.call("stress-ng --cpu '%s' --timeout '%s'" % (value,time), shell=True)

        if stype == 'mem':
          print "start stressing memory with value %s bytes within %ss" % (value,time)
          subprocess.call("stress-ng --vm 2 --vm-bytes '%s' --timeout '%s'" % (value,time), shell=True)

        if stype == 'io':
          print "start stressing disk with value %s within %ss" % (value,time)
          subprocess.call("stress-ng --io %s --timeout '%s'" % (value,time), shell=True)
     
      else:
        data = {}

      self.send_response(200)
      self.end_headers()
    

    elif None != re.search('/api/v1/stressnet/*', self.path):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'application/json':
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        ntype = self.path.split('/')[-1]
        LocalData.records[ntype] = data
        for net in data:
         pass
        if ntype == 'bandwidth':
          print "start limiting the bandwidth: %s" % (net)
      else:
        data = {}

      self.send_response(200)
      self.end_headers()

    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return


#-------------------------------------------------------

  def do_GET(self):
    global attr, delay_post_f, delay_post_b, delay_get_f, delay_get_b

    if None != re.search('/api/v1/getrecord/*', self.path):

      # delay
      time.sleep(float(delay_get_f))

      recordID = self.path.split('/')[-1]

      # delay
      time.sleep(float(delay_get_b))

      if LocalData.records.has_key(recordID):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(LocalData.records[recordID])
      else:
        self.send_response(400, 'Bad Request: record not exists')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return
 
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
  allow_reuse_address = True
 
  def shutdown(self):
    self.socket.close()
    HTTPServer.shutdown(self)
 
class SimpleHttpServer():
  def __init__(self, ip, port):
    self.server = ThreadedHTTPServer((ip,port), HTTPRequestHandler)
 
  def start(self):
    self.server_thread = threading.Thread(target=self.server.serve_forever)
    self.server_thread.daemon = True
    self.server_thread.start()
 
  def waitForThread(self):
    self.server_thread.join()
 
  def addRecord(self, recordID, jsonEncodedRecord):
    LocalData.records[recordID] = jsonEncodedRecord
 
  def stop(self):
    self.server.shutdown()
    self.waitForThread()

#
#
# ARGUMENTS FOR NEW VALUE DELAY INPUT
# delay = x,x,x,x
#
#

attr = '0,0,0,0'
delay_post_f = 0
delay_post_b = 0
delay_get_f = 0
delay_get_b = 0


#
# -- main --
#
if __name__=='__main__':
#  parser = argparse.ArgumentParser(description='HTTP Server')
#  parser.add_argument('ip', help='HTTP Server IP')
#  parser.add_argument('port', type=int, help='Listening port for HTTP Server')
#  args = parser.parse_args()

  # check arguments
  for arg in sys.argv:
#	print (arg)
	if arg == '-?' or arg == '-h' or arg == '--help':
		helper(sys.argv[0])
		sys.exit()


  # ip
  try: 
	_ip = sys.argv[1]
  except IndexError:
	_ip = "127.0.0.1"

  # port
  try: 
	_port = int(sys.argv[2])
  except IndexError:
	_port = 8011
  print "=> web+db ip: %s, port: %d" % (_ip, _port)


  print '=> delay: %s,%s,%s,%s' % (delay_post_f, delay_post_b, delay_get_f, delay_get_b)



  print 'HTTP Server Running (ip: %s, port: %d)...' % (_ip, _port)


  handler = HTTPRequestHandler
  httpd = SocketServer.TCPServer(("", _port), handler)
  httpd.serve_forever()


