#!/usr/bin/env python

import os,sys,pyrancid

(options, args) = pyrancid.get_opts()

hostn = args[0]

conf = pyrancid.config()
conn = pyrancid.ssh_conn(hostn, conf.get_user(hostn), conf.get_passwd(hostn))

conn.scp_file('/mnt/flash/config.tgz',hostn)