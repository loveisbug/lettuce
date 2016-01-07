# python2.7.5
# author : eric zhang
# email  : ericnomail@gmail.com  

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage
import elementset

class TCase():
	def runCase1(self, dev, case):
		# update check, only in Simple Chinese.
		tpath = elementset.getPath(elementset.testpath, case)
		print '/***** testing case:', case, tpath, '*****/'
		for node in tpath:
			nodepos = elementset.getObjPos(elementset.testobjs, node)
			print '  * touch [' + str(nodepos[1]) + ', ' + str(nodepos[2]) + ']'
			dev.touch(nodepos[1], nodepos[2], 'DOWN_AND_UP')
			MonkeyRunner.sleep(1)
		imageTrue = MonkeyRunner.loadImageFromFile('up-to-date.png')
		passed = imageTrue.sameAs(dev.takeSnapshot().getSubImage((514, 233, 644, 85)), 1.0) # magic number for the 'up-to-date.png'
		print '  *', case, 'passed.' if passed else 'failed.'		

	def runCase2(self, dev, case):
		# update hint,
		tpath = elementset.getPath(elementset.testpath, case)
		print '/***** testing case:', case, tpath, '*****/'

	def runCase3(self, dev, case):
		# login,
		tpath = elementset.getPath(elementset.testpath, case)
		print '/***** testing case:', case, tpath, '*****/'
		for node in tpath:
			nodepos = elementset.getObjPos(elementset.testobjs, node)
			print '  * ' + nodepos[0] + ' [' + str(nodepos[1]) + ', ' + str(nodepos[2]) + ']'
			if nodepos[0] == 'touch':
				dev.touch(nodepos[1], nodepos[2], 'DOWN_AND_UP')
			elif nodepos[0] == 'type':
				dev.touch(nodepos[1], nodepos[2], 'DOWN_AND_UP')
				MonkeyRunner.sleep(2)
				dev.type('8888')
				MonkeyRunner.sleep(2)
			elif nodepos[0] == 'press':
				pass
			MonkeyRunner.sleep(1)


	def clear(self, dev):
		dev.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
		MonkeyRunner.sleep(2)