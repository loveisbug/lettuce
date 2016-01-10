### uinput

* [Getting Start](http://thiemonge.org/getting-started-with-uinput)
* 打开设备是否需要non-blocking mode？

        fd = open("/dev/input/uinput", O_WRONLY | O_NONBLOCK);

### Android touch device

* virtual key map file
* input device configuration file(default for typical general-purpose touch peripherals such as external USB or Bluetooth HID touch screens or touch pads)
* then system will classify the input device
  * touch screen
  * touch pad
  * pointer device
* As of Android Ice Cream Sandwich 4.0, touch screen drivers may need to be changed to comply with the Linux input protocol specification.The following changes may be required:
  * When a tool becomes inactive (finger goes "up"), it should stop appearing in subsequent multi-touch sync reports. When all tools become inactive (all fingers go "up"), the driver should send an empty sync report packet, such as `SYN_MT_REPORT` followed by `SYN_REPORT`.
    * Previous versions of Android expected "up" events to be reported by sending a pressure value of 0.
  * Physical pressure or signal strength information should be reported using `ABS_MT_PRESSURE`.
    * Previous versions of Android retrieved pressure information from `ABS_MT_TOUCH_MAJOR`.
  * Touch size information should be reported using `ABS_MT_TOUCH_MAJOR`.
    * Previous versions of Android retrieved size information from `ABS_MT_TOOL_MAJOR`.

#### Android .idc文件

[https://source.android.com/devices/input/touch-devices.html](https://source.android.com/devices/input/touch-devices.html)

[https://source.android.com/devices/input/input-device-configuration-files.html](https://source.android.com/devices/input/input-device-configuration-files.html)

**example**

    # Basic Parameters
    # The virtual device should be a touch screen.
    touch.deviceType = touchScreen
    # It seems that we don't need it to be orientation aware.
    touch.orientationAware = 0

    # Size
    # The size is assumed to be proportional to the diameter (width) of the touch or tool.
    touch.size.calibration = diameter
    # A constant scale factor used in the calibration. The default value is 1.0.
    touch.size.scale = 10  
    touch.size.bias = 0
    # If the value is 1, the reported size will be divided by the number of contacts.
    touch.size.isSummed = 0
    # internal or external touch screens??
    device.internal = 1

    # Pressure  
    # Driver reports signal strength as pressure.  
    #  
    # A normal thumb touch typically registers about 200 signal strength  
    # units although we don't expect these values to be accurate.
    # For physical or amplitude, output.pressure = raw.pressure * touch.pressure.scale
    touch.pressure.calibration = amplitude  
    touch.pressure.scale = 0.005  
  
    # Orientation
    # If the value is none, output.orientation = 0
    touch.orientation.calibration = none

### Linux multi-touch protocol

* [Linux multi-touch protocol](https://www.kernel.org/doc/Documentation/input/multi-touch-protocol.txt)
* 根据硬件设备能力，协议分为Type A和Type B两种类型。
  * Type A，触摸点不能被区分和追踪，上报raw data
    * 上报某个触摸点信息的最后，通过调用`input_mt_sync()`隔开不同触摸点的信息，会产生一个`SYN_MT_REPORT`消息。这个消息触发接受者获取到一个触摸点信息，并准备接收下一个触摸点信息。
    * 驱动程序需要一次性上报当前触摸屏上的所有触摸点的全部信息。上报顺序不重要，消息的过滤和触摸点的跟踪在用户空间处理。
  * Type B，硬件设备可以区分和追踪触摸点，通过slot更新一个触摸点的信息
    * 需要给已经识别的触摸点分配一个slot，用这个slot上报这个触摸点的变化信息。通过修改slot的`ABS_MT_TRACKING_ID`可以实现新增、替换，去除触摸点。
      * 非负ID是触摸点，未使用的slot ID是-1。
      * 一个以前不存在的ID出现表示一个新触摸点，一个ID不存在了表示删除了。
      * 只有变化的信息被上报，因此每一个触摸点的完整信息必须放在接收端进行维护。
    * 开始上报某个触摸点信息时，调用`input_mt_slot()`区分触摸点，传递slot作为参数，会产生一个`ABS_MT_SLOT`消息，告诉接收者正在针对哪个slot更新信息。
    * 驱动程序调用`input_sync()`标识多点触摸信息传输结束，触发接收者处理上次`EV_SYN/SYN_REPORT`之后的事件，并准备下一次接收。
  * Type B相比Type A，可以减少发送给用户空间的数据。使用slot区分触摸点，需要使用`ABS_MT_TRACKING_ID`。
* 问题
  * If the driver reports one of `BTN_TOUCH` or `ABS_PRESSURE` in addition to the `ABS_MT` events, the last `SYN_MT_REPORT` event may be omitted. Otherwise, the last `SYN_REPORT` will be dropped by the input core, resulting in no zero-contact event reaching userland.

### Linux设备驱动

* [笔记](https://github.com/loveisbug/lettuce/blob/master/wiki/android/uinput/linux_device_driver.md)