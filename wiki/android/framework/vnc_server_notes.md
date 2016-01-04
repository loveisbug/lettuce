![](https://github.com/loveisbug/lettuce/blob/master/wiki/pic/droid_vnc_server_01.png)

### Framebuffer

### GRALLOC

Android各子系统通过HAL层操作底层帧缓冲区，Gralloc就是干这个活的。

* 由`FramebufferNativeWindow`在构造函数中加载。
* `gralloc.default.so`小结

![](https://github.com/loveisbug/lettuce/blob/master/wiki/pic/droid_vnc_server_02.png)

### Native Window

### Flinger