import time
import os
import argparse
import shlex
import subprocess
import glob
import logging

parser = argparse.ArgumentParser(description='Node resource statistics generator')
parser.add_argument('--refresh',  help="refresh interval (secs)",   default=86400, type=int)
parser.add_argument('--average',  help="averaging interval (secs)", default=10,	  type=int)
parser.add_argument('--maxfiles', help="maximum number of log files", default=1000,  type=int)
parser.add_argument('--password', help="server password", default="foobar", type=str, required=False)
pars = vars(parser.parse_args())

os.chdir('/root')

cmd = 'venv/bin/python3 dstat_server/dstat_pub_server.py --password {PASSWORD}'
cmd = cmd.format(PASSWORD=pars['password'])
print(cmd)
proc = subprocess.Popen(shlex.split(cmd))

# the dstat command line
cmd_temp = 'nohup /usr/bin/dstat -Ta --noupdate --noheader --vmstat --output {outfilename} {avesec} > /dev/null &'

logdir = '/root/dstat_logs/'

c = 0
while True:
	c += 1
	_now = str(int(time.time()))
	basename = 'dstat-'+_now+'.log'
	filename = logdir + os.sep + basename

	logging.info('cycle %d starts. Logging to %s' % (c, filename))
	cmd = cmd_temp.format(
		outfilename = filename,
		avesec      = pars['average']
	)
	p = subprocess.Popen(cmd, shell=True)
	time.sleep(pars['refresh'])
	p.terminate()

	# keep number of files to a limit
	logfiles = glob.glob(logdir+'/dstat-*.log')
	logfiles.sort()
	logfiles.reverse()
	for i in range(pars['maxfiles'], len(logfiles)):
		os.remove(logfiles[i])
	# end for
# end while
