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

## 管理工具
[PECL](https://pecl.php.net/)

[brew](http://brew.sh/index_zh-cn.html)

```
sudo su
curl -L http://github.com/mxcl/homebrew/tarball/master | tar xz --strip 1 -C /usr/local
```