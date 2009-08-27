#!/usr/bin/env python

import os,sys
import time, datetime
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()

today = datetime.date.today()

if options.filename:
	host = options.filename
elif args[0]:
	host = args[0]

srch_dir = "/home/upload/sslvpn"
files = os.listdir(srch_dir)
newest_file = ''
for file in files:
	if file.startswith('.'):
		continue
	if newest_file == '': newest_file = file
	check_f = os.path.join(srch_dir, file)
	check_f_time = os.stat(check_f).st_mtime
	if check_f_time > os.stat(os.path.join(srch_dir, newest_file)).st_mtime:
		newest_file = file
		
	file_date = time.localtime(check_f_time)
	file_date = datetime.date(int(file_date[0]), int(file_date[1]), int(file_date[2]))
	if (today - file_date).days > 7:
		os.remove(check_f)

conf_file=open(os.path.join(srch_dir, newest_file))
out_file=open(host,'w')
for line in conf_file:
	out_file.write(line)
conf_file.close()
out_file.close()