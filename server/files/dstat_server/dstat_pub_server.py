# simple server to print out the statistics of cpu and memory of the machine
import glob
import argparse
import psutil
import datetime
import flask
from flask import Flask
import copy
import json
import os
# parse inputs
parser = argparse.ArgumentParser(description='Node resource statistics generator')
parser.add_argument('--password' , help="password to access the server", required=False, default="foobar")
pars = vars(parser.parse_args())
password = pars['password']


# initiate the app
app = Flask(__name__)

@app.route('/heartbeat', methods=['POST'])
def gen_heartbeat(n=600):
	# read input parameter
	content = flask.request.get_json() # silent=True

	# authentication
	try:
		if password != content["password"]:
			heartbeat = {'authentication' : "failed"}
			return flask.jsonify(heartbeat)
	except Exception as e:
		heartbeat = {'error' : repr(e)}
		return flask.jsonify(heartbeat)
	# end try

	heartbeat = {
			'hostname'     : os.system('hostname'),
			'timestamp'    : datetime.datetime.utcnow().isoformat(),
			'cpu_pct'      : psutil.cpu_percent(),
			'memory_pct'   : psutil.virtual_memory().percent,
			'authentication' : "success"
		}
	return flask.jsonify(heartbeat)
# end def

@app.route('/dstat', methods=['POST'])
#@login_required
def pub_dstat(n=600):

	keys = [('epoch', 'epoch'), ('total cpu usage', 'usr'), ('total cpu usage', 'sys'), ('total cpu usage', 'idl'), ('total cpu usage', 'wai'), ('total cpu usage', 'hiq'), ('total cpu usage', 'siq'), ('dsk/total', 'read'), ('dsk/total', 'writ'), ('net/total', 'recv'), ('net/total', 'send'), ('paging', 'in'), ('paging', 'out'), ('system', 'int'), ('system', 'csw'), ('procs', 'run'), ('procs', 'blk'), ('procs', 'new'), ('memory usage', 'used'), ('memory usage', 'buff'), ('memory usage', 'cach'), ('memory usage', 'free'), ('paging', 'in'), ('paging', 'out'), ('dsk/total', 'read'), ('dsk/total', 'writ'), ('system', 'int'), ('system', 'csw'), ('total cpu usage', 'usr'), ('total cpu usage', 'sys'), ('total cpu usage', 'idl'), ('total cpu usage', 'wai'), ('total cpu usage', 'hiq'), ('total cpu usage', 'siq')]

	_dat = {'epoch': {'epoch': None}, 'total cpu usage': {'usr': None, 'sys': None, 'idl': None, 'wai': None, 'hiq': None, 'siq': None}, 'dsk/total': {'read': None, 'writ': None}, 'net/total': {'recv': None, 'send': None}, 'paging': {'in': None, 'out': None}, 'system': {'int': None, 'csw': None}, 'procs': {'run': None, 'blk': None, 'new': None}, 'memory usage': {'used': None, 'buff': None, 'cach': None, 'free': None}}

	# read input parameter
	content = flask.request.get_json() # silent=True
	n = content.setdefault('n', n)

	# authentication
	try:
		if password != content["password"]:
			heartbeat = {'authentication' : "failed"}
			return flask.jsonify(heartbeat)
	except Exception as e:
		heartbeat = {'error' : repr(e)}
		return flask.jsonify(heartbeat)
	# end try

	# if the authentication is success
	# list all log files
	logfiles = glob.glob('/root/dstat_logs/dstat-*.log')
	logfiles.sort()
	logfiles.reverse()

	# read and parse from files
	output = []
	for logfile in logfiles:
		out = parse_to_json(logfile, n)
		output.extend(out)
		if len(output) >= n:
			output = output[:n]
			output.reverse()
			break
		# end if
	# end for


	response = {
		'hostname'  : os.system('hostname'),
		'timestamp' : datetime.datetime.utcnow().isoformat(),
		'data': output,
		'authentication' : "success"
	}

	return flask.jsonify(response)
# end def


def parse_to_json(filename, nlines=None):
	with open(filename) as fin:
		lines = fin.read().strip().splitlines()
	# end with

	content = []
	for line in lines:
		cols = line.replace('"', '').split(',')
		try:
			cols = list(map(float, cols))
			content.append(cols)
		except ValueError:
			continue
		# end try
	# end for
	if nlines is not None:
		content = content[-nlines:]

	output = []
	for rows in content:
		dat = copy.deepcopy(_dat)
		for i in range(len(rows)):
		    p, q = keys[i]
		    dat[p][q] = rows[i]
		# end for
		output.append(dat)
	# end for

	output = list(reversed(output))
	return output
# end def

app.run(host='0.0.0.0', port=80)

