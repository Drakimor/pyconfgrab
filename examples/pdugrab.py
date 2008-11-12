#!/usr/bin/env python

import os,sys,socket
from optparse import OptionParser
from ftplib import FTP

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()

if args[0]:
	hostn = args[0]
elif options.filename:
	hostn = options.filename

host_tmp = hostn + '.new'

try:
	ftp = FTP(host=hostn, user='root', passwd='zaKrysHka')
	ftp.retrbinary('RETR config.ini', open(host_tmp, 'wb').write)
	ftp.quit()
except socket.error, e:
	print "Error connecting to " + hostn + ": %s"% e[1]
	if os.path.exists(host_tmp):
		os.remove(host_tmp)
	sys.exit(1)
	
conf_file=open(host_tmp)
out_file=open(hostn,'w')
for line in conf_file:
	if line.count('Configuration file, generated on') > 0:
		continue
	out_file.write(line)
conf_file.close()
out_file.close()

if os.path.exists(host_tmp):
	os.remove(host_tmp)