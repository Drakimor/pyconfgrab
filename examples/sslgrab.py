#!/usr/bin/env python

import os,sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()

if options.filename:
	host = options.filename
elif args[0]:
	host = args[0]

srch_dir = "/home/upload/sslvpn"
files = os.listdir(srch_dir)
new_file = ''
for file in files:
	if file.startswith('.'):
		continue
	if new_file == '': new_file = file
	if os.stat(os.path.join(srch_dir, file)).st_mtime > os.stat(os.path.join(srch_dir, new_file)).st_mtime:
		new_file = file

for file in files:
	if file != new_file:
		os.remove(os.path.join(srch_dir, file))

conf_file=open(os.path.join(srch_dir, new_file))
out_file=open(host,'w')
for line in conf_file:
	out_file.write(line)
conf_file.close()
out_file.close()
