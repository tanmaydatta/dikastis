from Dikastis import app
from flask import request, render_template, redirect
import json
import vagrant
from fabric.api import env, execute, task, run
from soldier import soldier
import os
import os.path
import Queue
import threading


base_path = os.path.abspath(os.path.join("", os.pardir)) + "/dikastis"
inq = Queue.Queue()
outq = Queue.Queue()
submit_count = 1

def response_msg(status, msg, **kwargs):
    res = {}
    res['status'] = status
    res['msg'] = msg
    for name, value in kwargs.items():
        res[name] = value
    return json.dumps(res), 200

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


def mytask():
	global submit_count
	run("python /vagrant/checker.py " + str(submit_count) + " A")


@app.route('/up/')
def up():
	v = vagrant.Vagrant(root="vagrant")
	# v.up()
	env.hosts = [v.user_hostname_port()]
	env.key_filename = v.keyfile()
	env.disable_known_hosts = True # useful for when the vagrant box ip changes.
	execute(mytask)
	return 'done'


def start_queue():
	global inq
	while True:
		if not inq.empty():
			print inq.get()

@app.route('/test/')
def test():
	thread = threading.Thread(target=start_queue)
	thread.start()
	return "done"


# @app.route('/push/<num>/')
def push(num):
	global inq
	inq.put(num)
	return num


@app.route('/submit/', methods=['GET', 'POST'])
def submit():
	global submit_count
	if request.method == 'GET':
		return render_template("test.html")

	elif request.method == 'POST':
		v = vagrant.Vagrant(root="vagrant")
		env.hosts = [v.user_hostname_port()]
		env.key_filename = v.keyfile()
		env.disable_known_hosts = True # useful for when the vagrant box ip changes.
		code = request.form['code']
		f = open(base_path + '/submissions/' + str(submit_count) + ".cpp" , 'w')
		f.write(code)
		f.close()
		f = open(base_path + '/vagrant/' + str(submit_count) + ".cpp" , 'w')
		f.write(code)
		f.close()
		execute(mytask)
		# import ipdb; ipdb.set_trace();
		with open(base_path + '/vagrant/log.json') as data_file:
			submit_count  = submit_count + 1
			data = json.load(data_file)
			return json.dumps(data[str(submit_count-1)])
			