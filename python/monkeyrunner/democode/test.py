# python2.7.5
# author : eric zhang
# email  : ericnomail@gmail.com  

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

# We must insatll simplejson instead of json module in Jython, and add the path to Jython.
import sys
if not ('/Library/Python/2.5/site-packages/simplejson-3.6.5' in sys.path):
	sys.path.append('/Library/Python/2.5/site-packages/simplejson-3.6.5')
try:
	import json
except ImportError:
	import simplejson as json

import caseset
import elementset

def autorun(cfg):
	fc = file(cfg)
	dc = json.load(fc)
	runComponent = dc['app']
	devicelist = dc['dev']
	caselist = dc['case']

	fo = file('mi2.json') # TODO: config this in case.json??
	fp = file('path.json')
	do = json.load(fo)
	dp = json.load(fp)

	elementset.load_obj(do)
	elementset.load_path(dp['array'])
	print len(elementset.testobjs)
	print len(elementset.testpath)

	fc.close()
	fo.close()
	fp.close()

	device = MonkeyRunner.waitForConnection(1.0, devicelist[0])
	if device:
		print '...connecting...'
		print '...connected OK.'
		print 'case number: ', len(caselist)
		for case in caselist:
			device.startActivity(component = runComponent)
			getattr(caseset.TCase(), case)(device, case)
			getattr(caseset.TCase(), 'clear')(device)
	else:
		print 'connect failed.'


if len(sys.argv) > 1:
    autorun(sys.argv[1])
else:
    print "Please input the test App, device list and the test case list."
