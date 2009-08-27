#!/usr/bin/env python

# APC PDU config grab

import os,sys,socket
from optparse import OptionParser
import pyconfgrab

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

(options, args) = parser.parse_args()

if args[0]:
	hostn = args[0]
elif options.filename:
	hostn = options.filename

host_tmp = hostn + '.new'

config = pyconfgrab.config()
user = config.get_by_name(hostn, config.users)
passwd = config.get_by_name(hostn, config.passwds)

conn = pyconfgrab.ssh_conn(hostn, user, passwd)
conn.scp_file("config.ini",host_tmp)
