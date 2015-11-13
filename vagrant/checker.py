import sys
from soldier import soldier
import json

verdict = {'TLE': 'TLE', 'RE': 'RE', 'CE': 'CE', 'WA': 'WA', 'AC': 'AC'}

def response_msg(status, msg, **kwargs):
    res = {}
    res['status'] = status
    res['msg'] = msg
    for name, value in kwargs.items():
        res[name] = value
    return res

# compilation
a = soldier.run("g++ /vagrant/" + str(sys.argv[1]) + ".cpp")
if a.status_code != 0:
	data = {}
	with open('/vagrant/log.json') as data_file:
		data = json.load(data_file)
	data[str(sys.argv[1])] = response_msg('OK', verdict['CE'])
	f = open('/vagrant/log.json', 'w')
	f.write(json.dumps(data))
	f.close()
	sys.exit(0)

else:
	# print "timeout 1s ./a.out < problems/" + str(sys.argv[2]) + ".in > " + str(sys.argv[1]) + ".out"
	f = open("/vagrant/problems/" + str(sys.argv[2]) + ".in", 'r')
	# f.write(str(a.output))
	a = soldier.run("timeout 1s ./a.out", stdin=str(f.read()))
	f.close()
	f = open(str(sys.argv[1]) + '.out', 'w')
	f.write(str(a.output))
	f.close()
	# time limit check
	if a.status_code == 124:
		data = {}
		with open('/vagrant/log.json') as data_file:
			data = json.load(data_file)
			data[str(sys.argv[1])] = response_msg('OK', verdict['TLE'])
			f = open('/vagrant/log.json', 'w')
			f.write(json.dumps(data))
			f.close()
			# sys.exit(0)

	# runtime error
	elif a.status_code != 0:
		data = {}
		with open('/vagrant/log.json') as data_file:
			data = json.load(data_file)
			data[str(sys.argv[1])] = response_msg('OK', verdict['RE'])
			f = open('/vagrant/log.json', 'w')
			f.write(json.dumps(data))
			f.close()
			# sys.exit(0)
	# wa check
	else:
		# print "diff problems/" + str(sys.argv[2]) + ".in " + str(sys.argv[1]) + ".out"
		a = soldier.run("diff /vagrant/problems/" + str(sys.argv[2]) + ".out " + str(sys.argv[1]) + ".out")
		# print a.output
		if a.output:
			data = {}
			with open('/vagrant/log.json') as data_file:
				data = json.load(data_file)
				data[str(sys.argv[1])] = response_msg('OK', verdict['WA'])
				f = open('/vagrant/log.json', 'w')
				f.write(json.dumps(data))
				f.close()
				# sys.exit(0)

		else:
			data = {}
			with open('/vagrant/log.json') as data_file:
				data = json.load(data_file)
				data[str(sys.argv[1])] = response_msg('OK', verdict['AC'])
				f = open('/vagrant/log.json', 'w')
				f.write(json.dumps(data))
				f.close()
				# sys.exit(0)