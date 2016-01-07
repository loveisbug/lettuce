# python2.7.5
# author : eric zhang
# email  : ericnomail@gmail.com

class SFObj(object):
	"""docstring for SFObj"""
	def __init__(self, name, lt, rb, touch, sub):
		super(SFObj, self).__init__()
		self.name = name
		self.lt = lt
		self.rb = rb
		self.touch = touch
		if len(lt) >= 2 and len(rb) >= 2:
			self.touch[1] = lt[0] + (rb[0] - lt[0]) / 2
			self.touch[2] = lt[1] + 20
		else:
			self.touch[1] = 0
			self.touch[2] = 0
		self.sub = sub

class SFTestPath(object):
	"""docstring for SFTestPath"""
	def __init__(self, name, alias, path):
		super(SFTestPath, self).__init__()
		self.name = name
		self.alias = alias
		self.path = path

idx = 0 # used for load_obj() only.
testobjs = []
testpath = []

def load_obj(d):
	global idx
	testobjs.append(SFObj(d['name'], d['lt'], d['rb'], d['touch'], d['sub']))
	print "The " + str(idx) + " obj is " + testobjs[idx].name + ", it has " + str(len(testobjs[idx].sub)) + " sub objs"
	print "    It's action is: " + testobjs[idx].touch[0] + " [" + str(testobjs[idx].touch[1]) + ", " + str(testobjs[idx].touch[2]) + "]"
	idx += 1
	for tmpobj in d['sub']:
		load_obj(tmpobj)

def load_path(d):
	i = 0
	for tmppath in d:
		testpath.append(SFTestPath(tmppath['name'], tmppath['alias'], tmppath['path']))
		print "The path of " + testpath[i].name + ", " + testpath[i].alias + ":"
		print testpath[i].path
		i += 1

def getPath(path, name):
	for p in path:
		if p.name.find(name) >= 0:
			return p.path

def getObjPos(objs, name):
	for o in objs:
		if o.name == name:
			return o.touch
