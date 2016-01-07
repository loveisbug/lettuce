**问题：Jython里不能`import json`**

* 报错`import error`。
* `MonkeyRunner`用的是Jython 2.5.3，可能是基于Python 2.5，
* 而Python在2.7版本后才有`json`模块，
* 一个解决方法是在Python 2.5版本下安装`simplejson`模块，以Mac OS X举例，
  * Android SDk目录下可以看到，

        android-sdks/tools/lib/jython-standalone-2.5.3.jar

  * 下载[`simplejson`](https://pypi.python.org/pypi/simplejson)，拷贝到Python目录`/Library/Python/2.5/site-packages/`，解压，安装，
  
        tar -xzf simplejson-3.6.5.tar.gz
        python setup.py install
        
  * 在`MonkeyRunner`下`import simplejson`还是报错`import error`，
  * 查看Jython path，没有`simplejson`的路径，
  
        import sys
        sys.path
        
  * 添加`simplejson`路径`sys.path.append('/Library/Python/2.5/site-packages/simplejson-3.6.5')`，然后`import`成功，
  * 但是退出后失效，解决方法1是用`PYTHONPATH`，解决方法2是在Python脚本里动态添加，添加还需要判断重复，最好还能将[路径标准化](http://blog.csdn.net/shanliangliuxing/article/details/8823461)，对Windows系统做些处理，
  * 目前先采用代码里动态添加的方法，先不管Windows系统了。
  
        import sys
        if not ('/Library/Python/2.5/site-packages/simplejson-3.6.5' in sys.path):
            sys.path.append('/Library/Python/2.5/site-packages/simplejson-3.6.5')
        try:
            import json
        except ImportError:
            import simplejson as json
