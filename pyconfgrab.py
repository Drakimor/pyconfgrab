#!/usr/bin/env python

import os,sys,re
import pexpect
from optparse import OptionParser

class config:
	"This will handle processing the rancid config file."
	
	def __init__(self):
		self.hosts = []
		self.users = {}
		self.passwds = {}
		self.methods = {}
		self.epass = {}
		cfg_file = open(os.path.join(os.path.expanduser('~'), '.cloginrc'),'r')
		for line in cfg_file:
			if line.strip() == '':
				continue
			entry = line.split()
			if not entry[2] in self.hosts:
				self.hosts.append(entry[2])
			if entry[1] == 'user':
				self.users[entry[2]] = entry[3]
			elif entry[1] ==  'password':
				self.passwds[entry[2]] = entry[3]
				if len(entry) == 5:
					self.epass[entry[2]] = entry[4]
			elif entry[1] == 'method':
				self.methods[entry[2]] = entry[3]

	def get_by_name(self, target, list):
		for host in self.hosts:
			if re.compile('^' + host).findall(target):
				return list[host]
		return ''
	
	def get_user(self, target):
		return self.get_by_name(target, self.users)
	def get_passwd(self, target):
		return self.get_by_name(target, self.passwds)

class ssh_conn:
	"Creates an ssh session to run commands and read output."

	def __init__(self,host,user,passwd,verbose=0):
		self.user = user
		self.host = host
		self.verbose = verbose
		self.passwd = passwd
		self.connected = False
		self.prompt = '.*[\>|#|\$]'

	def __del__(self):
		self.conn.sendline("exit")

	def __timeout(self):
		print 'ERROR: SSH could not login. Here is what SSH said:'
		print self.conn.before, self.conn.after
		return False

	def __login(self, prompt=False):
		ssh_newkey = 'Are you sure you want to continue connecting'
		i = self.conn.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword: '])
		if i == 0: # Timeout
			return self.__timeout()
		elif i == 1: # SSH does not have the public key. Just accept it.
			self.conn.sendline ('yes')
			i = self.conn.expect([pexpect.TIMEOUT, '[P|p]assword: '])
			if i == 0: # Timeout
				return self.__timeout()
		self.conn.sendline(self.passwd)
		i = self.conn.expect([pexpect.TIMEOUT, pexpect.EOF ,'[P|p]assword: ', self.prompt])
		if i == 0:
			return self.__timeout()
		if i == 1:
			return True
		elif i == 2:
			print "Error: Password not accepted."
			return False
		elif i == 3 and prompt == True:
			prompt = self.conn.after.split('\n')
			self.prompt = prompt[len(prompt)-1]
			self.connected=True
			return True

	def login(self):
		if self.connected:
			print "Error: Already connected to %s"% self.host
			return False
		self.conn = pexpect.spawn('ssh -l %s %s'%(self.user, self.host))
		return self.__login(prompt=True)

	def run(self, command, filter=[]):
		if not self.connected:
			print "Error: not connected to %s, log in first"% self.host
			return False
		filter.append(command)
		self.conn.sendline(command)
		i = self.conn.expect([pexpect.TIMEOUT, self.prompt])
		if i == 0:
			print "Error: timeout sending - %s"% command
		raw_data = self.conn.before
		raw_data = re.compile('[\r|\n]+').split(raw_data)
		filter = [re.compile(expr) for expr in filter]
		good_data = ''
		for line in raw_data:
			for regex in filter:
				if regex.findall(line):
					break
			else:
				good_data += line + os.linesep
		return good_data
	
	def scp_file(self, rfile, lfile):
		self.conn = pexpect.spawn('scp -q %s@%s:%s %s'%(self.user, self.host, rfile, lfile))
		if self.__login():
			return True
		return False

def get_opts():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", help="write report to FILE", metavar="FILE")

	return parser.parse_args()