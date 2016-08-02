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

安装apc自带管理工具，浏览器访问```http://YOUR_HOST/apc.php```。

## [XCache](http://xcache.lighthttpd.net)
安装

```
sudo apt-get install php5-xcache
```
```
yum install xcache
```

## [eAsccelerator](www.eaccelerator.net)
安装

```
sudo apt-get install php5-eaccelerator
```
```
yum install php-eacceleartor
```
下载安装

```
wget http://bart.eaccelerator.net/source/0.9.6.1/eacceleartor-0.9.6.1.tar.bz2
tar xvjf eaccelerator-0.9.6.1.tar.bz2
```
```
phpize
./configure
make
sudo make install
```

缓存文件夹

```eA```默认缓存目录是```/tmp/eaccelerator```，建议更改此位置并从```/tmp```中删除，因为该目录会在每次系统重新启动时被清空。推荐在```/var/```中创建目录，完整的目录位置可以是```/var/cache/eaccelerator```。

修改```php.ini```文件

```
extension="eaccelerator.so"
eaccelerator.shm_size="16"
eaccelerator.cache_dir="/var/cache/eaccelerator"
eaccelerator.enable="1"
eaccelerator.optimizer="1"
eaccelerator.check_mtime="1"
eaccelerator.debug="0"
eaccelerator.filter=""
eaccelerator.shm_max="0"
eaccelerator.shm_ttl="0"
eaccelerator.shm_prune_period="0"
eaccelerator.shm_only="0"
eaccelerator.compress="1"
eaccelerator.compress_level="9"
```
## 工具
[PECL](https://pecl.php.net/)

[brew](http://brew.sh/index_zh-cn.html)

```
sudo su
curl -L http://github.com/mxcl/homebrew/tarball/master | tar xz --strip 1 -C /usr/local
```