import subprocess, time, os, sys
cmd = [sys.executable, 'keylogger.py']

p = subprocess.Popen(cmd,
  stdout=subprocess.PIPE,
  stderr=subprocess.STDOUT)

#for line in p.stdout:
#    print line,
for line in iter(p.stdout.readline, b''):
  return str((line.rstrip() )
