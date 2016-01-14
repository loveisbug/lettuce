### 使用和限制

* 安装飞智市场后，提示安装飞智手柄助手和飞智手柄助手驱动。
* 限制1：启动游戏厅安装手柄助手和驱动的时候一定不要勾选小米增强版独有的“安装应用到sd卡”功能。
* 限制2：一定要先启动飞智游戏厅，从游戏厅启动游戏。不要没启动游戏厅，直接从系统桌面启动游戏，这样可能导致飞智手柄助手没有正常工作。
  * 以上两个限制来源：飞智社区：小米盒子增强版大厅安装与使用说明
  * 在小米盒子上实测了出现过，退出飞智游戏大厅，清理内存，进入西游游戏，无法使用莱仕达手柄；进入飞智游戏大厅，拔插该手柄，弹出框要求允许应用“飞智手柄助手”访问该USB设备，之后可以使用。
  * 沙发管家清理内存清除手柄助手驱动，仍在后台运行。
* 看了一下一个M3淘宝页面（飞智北京总代）介绍，提及已确认支持的盒子和不支持的盒子。
  * “只有开放了权限的盒子才能用体感精灵M3手柄玩游戏”。小米官网说体感游戏需要ROOT。
  * 未列出支持的，自行安装体感精灵APK验证，虽然这里说的是体感精灵，不是手柄助手驱动，是否可以猜测，这里有提权动作？
* 目前不支持的盒子（电视）
  * 大麦盒子
  * 天猫魔盒
    * 1S增强和2 暂不支持
    * 1S 即将支持
  * 乐视盒子、乐视电视 部分游戏
  * 华为秘盒 部分游戏
* 支持的手柄
* 安装方法

### apk
#### Java部分分析
#### C/C++部分分析

### 权限

* 手柄助手驱动应用请求大量权限。
  * USB外设访问权限。
  * 在其他应用之上显示内容。
  * receive tvbox start and stop
  * tvbox start and stop
  * `com.xiaomi.permission.AUTH_SERVICE`
    * 这里请求了xiaomi的自定义权限，这可能会在Android L里遇到问题，Android L里不允许安装请求相同权限但是签名不同的App。
  * 查阅敏感日志数据
  * 更改系统显示设置
  * 修改安全系统设置
* 3层apk的包名和所请求的权限如下。
  * 飞智游戏大厅`feizhiyouxidatin.3987.com.apk`，包名`com.game.motionelf`
  
        uses-permission: android.permission.ACCESS_DOWNLOAD_MANAGER
        uses-permission: android.permission.INTERNET
        uses-permission: android.permission.ACCESS_NETWORK_STATE
        uses-permission: android.permission.ACCESS_WIFI_STATE
        uses-permission: android.permission.ACCESS_COARSE_LOCATION
        uses-permission: android.permission.WAKE_LOCK
        uses-permission: android.permission.WRITE_EXTERNAL_STORAGE
        uses-permission: android.permission.MOUNT_UNMOUNT_FILESYSTEMS
        uses-permission: android.permission.READ_EXTERNAL_STORAGE
        uses-permission: android.permission.RESTART_PACKAGES
        uses-permission: android.permission.GET_TASKS
        uses-permission: android.permission.DELETE_PACKAGES
        uses-permission: android.permission.WRITE_SETTINGS
        uses-permission: android.permission.ACCESS_WIFI_STATE
        uses-permission: android.permission.INSTALL_PACKAGES
        
  * 飞智手柄助手`com.android.motionelf.apk`，包名`com.android.motionelf`
  
        uses-permission: android.permission.ACCESS_DOWNLOAD_MANAGER
        uses-permission: android.permission.INTERNET
        uses-permission: android.permission.ACCESS_NETWORK_STATE
        uses-permission: android.permission.ACCESS_WIFI_STATE
        uses-permission: android.permission.ACCESS_COARSE_LOCATION
        uses-permission: android.permission.WAKE_LOCK
        uses-permission: android.permission.WRITE_EXTERNAL_STORAGE
        uses-permission: android.permission.RESTART_PACKAGES
        uses-permission: android.permission.SYSTEM_ALERT_WINDOW
        uses-permission: android.permission.INJECT_EVENTS
        uses-permission: android.permission.GET_TASKS
        uses-permission: android.permission.READ_FRAME_BUFFER
        uses-permission: android.permission.DELETE_PACKAGES
        uses-permission: android.permission.WRITE_SETTINGS
        uses-permission: android.permission.WRITE_SECURE_SETTINGS
        uses-permission: android.permission.RECEIVE_BOOT_COMPLETED
        uses-permission: android.hardware.usb.host
        uses-permission: android.permission.INSTALL_PACKAGES
        
  * 飞智手柄助手驱动`com.android.motionelfdriver_mi.apk`，driver系列apk们的包名都是`com.android.motionelfdriver`
  
        uses-permission: android.permission.ACCESS_DOWNLOAD_MANAGER
        uses-permission: android.permission.INTERNET
        uses-permission: android.permission.ACCESS_NETWORK_STATE
        uses-permission: android.permission.ACCESS_WIFI_STATE
        uses-permission: android.permission.ACCESS_COARSE_LOCATION
        uses-permission: android.permission.WAKE_LOCK
        uses-permission: android.permission.WRITE_EXTERNAL_STORAGE
        uses-permission: android.permission.RESTART_PACKAGES
        uses-permission: android.permission.SYSTEM_ALERT_WINDOW
        uses-permission: android.permission.GET_TASKS
        uses-permission: android.permission.WRITE_SETTINGS
        uses-permission: android.permission.RECEIVE_BOOT_COMPLETED
        uses-permission: android.hardware.usb.host

### 线程

`top -t`看，进程`com.android.motionelf`的`UID`是`u0_a85`，进程`com.android.motionelfdriver`的`UID`是`system`。

![](https://github.com/loveisbug/lettuce/blob/master/wiki/pic/feizhidriverthread.png)