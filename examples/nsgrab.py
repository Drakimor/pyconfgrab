#!/usr/bin/env python

import os,sys,pyrancid

(options, args) = pyrancid.get_opts()

hostn = args[0]

filter = ['^# Last modified by']

conf = pyrancid.config()
conn = pyrancid.ssh_conn(hostn, conf.get_user(hostn), conf.get_passwd(hostn))
conn.login()

out_file=open(hostn,'w')
out_file.write(conn.run('show runningConfig', filter))
out_file.close()