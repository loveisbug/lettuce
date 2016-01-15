### 使用和限制

* 安装飞智市场后，提示安装飞智手柄助手和飞智手柄助手驱动。
* 限制1：启动游戏厅安装手柄助手和驱动的时候一定不要勾选小米增强版独有的“安装应用到sd卡”功能。
* 限制2：一定要先启动飞智游戏厅，从游戏厅启动游戏。不要没启动游戏厅，直接从系统桌面启动游戏，这样可能导致飞智手柄助手没有正常工作。
  * 以上两个限制来源：[飞智社区：小米盒子增强版大厅安装与使用说明](http://www.flydigi.com/faq/?post=19)
  * 在小米盒子上实测了出现过，退出飞智游戏大厅，清理内存，进入西游游戏，无法使用莱仕达手柄；进入飞智游戏大厅，拔插该手柄，弹出框要求允许应用“飞智手柄助手”访问该USB设备，之后可以使用。
  * 沙发管家清理内存清除手柄助手驱动，仍在后台运行。
* 看了一下一个[M3淘宝页面（飞智北京总代）](http://item.taobao.com/item.htm?id=36446104727)介绍，提及已确认支持的盒子和不支持的盒子。
  * “只有开放了权限的盒子才能用体感精灵M3手柄玩游戏”。小米官网说体感游戏需要ROOT。
  * 未列出支持的，自行安装体感精灵APK验证，虽然这里说的是体感精灵，不是手柄助手驱动，是否可以猜测，这里有提权动作？
* 目前[不支持的盒子（电视）](http://www.flydigi.com/?do=support)
  * 大麦盒子
  * 天猫魔盒
    * 1S增强和2 暂不支持
    * 1S 即将支持
  * 乐视盒子、乐视电视 部分游戏
  * 华为秘盒 部分游戏
* [支持的手柄](http://www.flydigi.com/?do=shoubing)
* [安装方法](http://www.flydigi.com/faq/?post=2)

### apk

* 飞智游戏大厅apk结构如下，
  * 大厅应用（Android原生系统签名）
    * `feizhiyouxidatin.3987.com`
  * 手柄助手应用（都是Android原生系统签名）
    * `com.android.motionelf.apk`
    * `com.android.motionelf_tm.apk`
  * 手柄助手驱动应用（各平台系统签名）
    * `com.android.motionelfdriver_himedia.apk`
    * `com.android.motionelfdriver_hisense.apk`
    * `com.android.motionelfdriver_konka.apk`
    * `com.android.motionelfdriver_mi.apk`
    * `com.android.motionelfdriver_yunos.apk`
    * `com.android.motionelfdriver.apk`
* 各driver应用apk签名的MD5。

driver|MD5|info
----|----|----
himedia|70:51:55:CB:59:1D:66:61:F9:66:3E:04:67:8D:95:BA|Owner: EMAILADDRESS=jame.luo@himedia.cn, CN=jame, OU=himedia, O=himedia, L=Shenzhen, ST=Guangdong, C=CN
hisense|E6:00:D3:9F:9E:A8:3E:20:9C:9F:12:51:2F:20:30:03|Owner: EMAILADDRESS=chenyijun@hisense.com, CN=yijun.chen, OU=DTV, O=Hisense.inc, L=QingDao, ST=ShanDong, C=CN
konka|64:88:49:92:77:BF:23:56:79:5A:AC:B3:C6:D7:74:D7|Owner: EMAILADDRESS=TVRDC@konka.com, CN=RDC, OU=TV, O=KONKA, L=ShenZhen, ST=GuangDong, C=CN
mi|49:5A:6B:E8:6A:31:A3:F5:68:79:3E:A3:D9:88:3D:90|Owner: L=Mountain, ST=California, C=US
yunos|E5:DA:1D:1B:54:A9:F8:FD:17:85:58:2C:15:FB:46:E3|Owner: EMAILADDRESS=tangrong.lx@alibaba-inc.com, CN=tangrong, OU=YUNOSTV, O=Alibaba, L=Hangzhou, ST=ZheJiang, C=CN
(android)|8D:DB:34:2F:2D:A5:40:84:02:D7:56:8A:F2:1E:29:F9|Owner: EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US

* 大厅apk的`assets`目录下还有以下文件，
  * `com.xiaoyt.red.cfg`
  * `install-recovery.sh`
  
        /system/bin/motionelf_server&
  * `test_b.sh`
  
        mount -o remount rw /system;/data/local/tmp/busybox cp /data/local/tmp/su /system/bin/.sux;chmod 6755 /system/bin/.sux;
  * libevent.so
  * libevent2.so
  * libevent3.so
  * sensors.default.so
  * ...
* 手柄助手apk里没有.so库，assets目录里有大量的.cfg文件。

#### Java部分分析
#### C/C++部分分析

* 以`com.android.motionelfdriver_mi.apk`为例，其`lib`目录下的`.so`文件`libgamepad_zhushou.so`，从这个`.so`中[dump](https://github.com/loveisbug/lettuce/blob/master/wiki/vulnerability/reverse/badmemory.md#objdump)出函数列表如下，从中大致猜测：
  * JNI接口
    * `Java_com_android_motionelfdriver_MotionElfService_zhushouInit`
    * `Java_com_android_motionelfdriver_MotionElfService_zhushouCfgStatus`
    * `Java_com_android_motionelfdriver_MotionElfService_zhushouStop`
  * 使用`dev/uinput`。
  * `Java_com_android_motionelfdriver_MotionElfService_zhushouInit`中起线程调用`uinput_create`，然后依次`uinput_create_keyboard`，`uinput_create_Mouse`，`uinput_create_sensor`，然后`uinput_init`。
  
        00001e44 <usleep@plt-0x14>
        00001e58 <usleep@plt>
        00001e64 <pthread_mutex_lock@plt>
        00001e70 <write@plt>
        00001e7c <__errno@plt>
        00001e88 <strerror@plt>
        00001e94 <__android_log_print@plt>
        00001ea0 <pthread_mutex_unlock@plt>
        00001eac <socket_local_server@plt>
        00001eb8 <bsd_signal@plt>
        00001ec4 <pthread_create@plt>
        00001ed0 <accept@plt>
        00001edc <read@plt>
        00001ee8 <close@plt>
        00001ef4 <sqrt@plt>
        00001f00 <__aeabi_idiv@plt>
        00001f0c <free@plt>
        00001f18 <memset@plt>
        00001f24 <gettimeofday@plt>
        00001f30 <calloc@plt>
        00001f3c <open@plt>
        00001f48 <strncpy@plt>
        00001f54 <ioctl@plt>
        00001f60 <perror@plt>
        00001f6c <__stack_chk_fail@plt>
        00001f78 <sprintf@plt>
        00001f84 <usb_device_connect_kernel_driver@plt>
        00001f90 <usb_device_claim_interface@plt>
        00001f9c <__cxa_finalize@plt>
        00001fa8 <Java_com_android_motionelfdriver_MotionElfService_zhushouCfgStatus-0x10>
        00001fb8 <Java_com_android_motionelfdriver_MotionElfService_zhushouCfgStatus>
        00001fc8 <Java_com_android_motionelfdriver_MotionElfService_zhushouStop>
        00001fd8 <convertData_2G>
        00002014 <accelConvertData_32mG>
        0000203c <accelFilter>
        00002090 <iir_filter>
        000020d4 <fdfz_des>
        00002128 <socket_client_write>
        00002268 <socket_write>
        000022bc <update_button_data>
        000022ec <update_simulate_mouse_data>
        00002328 <De_data_process>
        000024dc <X9_data_process>
        00002848 <M3_data_process>
        00002ba0 <Java_com_android_motionelfdriver_MotionElfService_zhushouInit>
        00002ff4 <fd_keystick_keycheck>
        00003014 <fd_js_phase_process>
        0000307c <fd_js_phase_check>
        0000311c <fd_set_keytable>
        00003180 <enable_JS0_event>
        00003198 <disable_JS0_event>
        000031a8 <enable_JS1_event>
        000031c0 <disable_JS1_event>
        000031d0 <enable_KS0_event>
        00003200 <disable_KS0_event>
        00003210 <enable_KS1_event>
        00003240 <disable_KS1_event>
        00003250 <joystick_dongle_reshape>
        00003338 <uinput_destroy>
        000033bc <uinput_report_touch_move_event>
        00003420 <uinput_report_touch_release_event>
        00003468 <uinput_report_touch_press_event>
        00003544 <uinput_report_move_event>
        00003570 <uinput_report_right_js_release_event>
        000035b4 <uinput_report_right_js_move_event>
        00003610 <uinput_report_right_js_event>
        00003698 <uinput_report_left_js_release_event>
        000036dc <uinput_report_left_js_move_event>
        00003734 <uinput_report_left_js_event>
        000037f8 <uinput_report_moveRel_event>
        00003868 <uinput_report_key_press_event>
        00003908 <fd_insert_keyevent>
        000039ec <fd_press_keyevent>
        00003a18 <uinput_report_key_release_event>
        00003a84 <fd_period_keyevent>
        000044ec <fd_release_keyevent>
        00004570 <fd_key_maintain>
        00004e80 <uinput_report_all_release_event>
        00004f2c <fd_destroy_keytable>
        00004f7c <fd_default_keytable>
        00005008 <fd_socket_parsing>
        000051bc <uinput_init>
        000051dc <uinput_input_report_gyro>
        00005280 <sensor_write_gyro>
        00005298 <uinput_input_report_acc>
        00005320 <sensor_write_acc>
        00005338 <uinput_create_Mouse>
        0000546c <uinput_create>
        0000559c <uinput_create_keyboard>
        00005718 <uinput_create_sensor>
        00005858 <find_hidraw_Mi>
        00005bbc <find_hidraw_X9>
        00005cb4 <find_hidraw_M3>
        00005dd0 <find_hidraw_Device>
        00005f50 <write_hidraw_X9>
        000060b4 <write_hidraw_M3>
        00006208 <is_connect_M3>
        00006230 <is_connect_X9>
        00006258 <is_connect_Mi>
        00006270 <is_connect_GP>
        00006298 <hid_write>
        00006364 <usb_device_init_X9>
        000063b4 <usb_device_init_M3>
        00006434 <thread_usbhost>
        00006448 <usb_device_change>
        000064d4 <usb_device_reconnect_X9>
        00006514 <usb_device_reconnect_M3>

    * 在`uinput_create`中，打开`/dev/uinput`，

            0000546c <uinput_create>:
                546c:       b5f0            push    {r4, r5, r6, r7, lr} //参数压栈
                546e:       4605            mov     r5, r0
                5470:       4845            ldr     r0, [pc, #276]  ; (5588 <uinput_create+0x11c>)
                5472:       f5ad 6d8c       sub.w   sp, sp, #1120   ; 0x460
                5476:       b081            sub     sp, #4
                5478:       460f            mov     r7, r1
                547a:       4478            add     r0, pc  //__stack_chk_guard_ptr
                547c:       6800            ldr     r0, [r0, #0]  //__stack_chk_guard
                547e:       4616            mov     r6, r2
                5480:       2100            movs    r1, #0  //memset的参数c
                5482:       f240 425c       movw    r2, #1116       ; 0x45c  //memset的参数n
                5486:       6803            ldr     r3, [r0, #0]
                5488:       4668            mov     r0, sp  //memset的参数s
                548a:       f8cd 345c       str.w   r3, [sp, #1116] ; 0x45c
                548e:       f7fc ed44       blx     1f18 <memset@plt>  //调用memset(void *s, int c, size_t n)
                5492:       b90d            cbnz    r5, 5498 <uinput_create+0x2c>
                5494:       4d3d            ldr     r5, [pc, #244]  ; (558c <uinput_create+0x120>)
                5496:       447d            add     r5, pc  //"/dev/uinput"
                5498:       2001            movs    r0, #1  //calloc的参数nmemb
                549a:       2104            movs    r1, #4  //calloc的参数size
                549c:       f7fc ed48       blx     1f30 <calloc@plt>  //调用calloc(int nmenb, int size)
                54a0:       4604            mov     r4, r0
                54a2:       2800            cmp     r0, #0
                54a4:       d05d            beq.n   5562 <uinput_create+0xf6>
                54a6:       4628            mov     r0, r5  //open的参数file，就是"/dev/uinput"
                54a8:       f640 0101       movw    r1, #2049       ; 0x801  //open的参数oflag，从0x801看，似乎是O_WRONLY|O_TRUNC
                54ac:       f7fc ed46       blx     1f3c <open@plt>  //调用open("/dev/uinput", O_WRONLY|O_TRUNC)
                54b0:       2800            cmp     r0, #0
                54b2:       6020            str     r0, [r4, #0]
                54b4:       dc04            bgt.n   54c0 <uinput_create+0x54>
                54b6:       4620            mov     r0, r4
                54b8:       2400            movs    r4, #0
                54ba:       f7fc ed28       blx     1f0c <free@plt>
                54be:       e050            b.n     5562 <uinput_create+0xf6>
    
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