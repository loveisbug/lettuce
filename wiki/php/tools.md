## VLD
用```pecl install channel://pecl.php.net/vld-0.10.1```来安装。

## strace

Mac上可以用```dtruss```替代。```ps auxw |grep www-data```找到进程```pid```，然后```dtruss -p processID```。

## Xdebug
用```PECL```安装，或者下载[源码](http://xdebug.org/download.php)安装。

```
tar -xzf  xdebug-2.4.0.tgz
cd xdebug-2.4.0
phpize
```
报错没安装```autoconf```，用```brew install autoconf```来安装。

```
brew install autoconf
phpize
./configure --enable-xdebug
make
```
然后```make test```测试一下。

```
make install
```

报错

```
Installing shared extensions:     /usr/lib/php/extensions/no-debug-non-zts-20121212/
cp: /usr/lib/php/extensions/no-debug-non-zts-20121212/#INST@98930#: Operation not permitted
```
[解决方案](http://www.cnblogs.com/yoainet/p/5088171.html)

修改```php.ini```文件，

```
[PHP_Xdebug]
zend_extension_ts="FULL PATH TO php_xdebug file"
```

```
xdebug.profiler_enable = 1
xdebug.profiler_enable_trigger = 1
xdebug.profiler_output_dir="ABSOLUTE PATH TO XDEBUG LOGS DIRECTORY"
xdebug.profiler_append=On
xdebug.profiler_output_name = "cachegrind"
```

### GUI工具

- [WinCacheGrind](http://sourceforge.net/projects/wincachegrind)
- [KDECacheGrind](http://kcachegrind.sourceforge.net/html/Download.html)

  ```
 ./configure
 make
 make install
  ```

## Alternative PHP Cache(APC)

用```PECL```来安装。

```
sudo pecl install apc
```
如果遇到如下报错，可以按照bata版，或者从源代码生成。

```
'/tmp/pear/temp/APC/php_apc.c:959: error: duplicate 'static'
make: *** [php_apc.lo] Error 1
ERROR: `make' failed'
```
```
sudo pecl install apc-beta
```

修改```php.ini```

```
extension=apc.so
apc.enabled=1
apc.stat=1
```

## XCache
## eAsccelerator

## 工具
[PECL](https://pecl.php.net/)

[brew](http://brew.sh/index_zh-cn.html)

```
sudo su
curl -L http://github.com/mxcl/homebrew/tarball/master | tar xz --strip 1 -C /usr/local
```