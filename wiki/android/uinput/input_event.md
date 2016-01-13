### 目标
#### 目的

拦截用户手柄输入，模拟input event发送给系统。

#### 参考对象

* 飞智
  * 安装飞智市场后，提示安装飞智手柄助手和飞智手柄助手驱动。
  * 手柄助手驱动应用请求大量权限。
    * 详细看一下手柄助手驱动请求的所有权限。
    * [飞智手柄助手分析]()
  * 游戏包本身没有改动。
  * 支持多款手柄。
  * 限制1：启动游戏厅安装手柄助手和驱动的时候一定不要勾选小米增强版独有的“安装应用到sd卡”功能。
  * 限制2：一定要先启动飞智游戏厅，从游戏厅启动游戏。不要没启动游戏厅，直接从系统桌面启动游戏，这样可能导致飞智手柄助手没有正常工作。

### 尝试的可能性
#### `uinput`（需突破root权限）

* 使用`uinput`，可以从用户态向内核发送input event。
* 状况：测试代码能跑通。
* 问题：App如果需要访问`dev/uinput`，必须先执行`chmod 666 dev/uinput`，需要root设备。
* 尝试方向。
  * **系统签名**
    * 获取系统签名可以在App中访问`dev/uinput`。
    * 局限：获取了特定的系统签名，只能在特定系统中运行。不同厂家的系统签名不同，只有运行此源码编译的系统的设备才能识别该签名。
    * 需要使用公钥/私钥文件`platform.x509.pem`和`platform.pk8`。是否有可能选择合适的系统，覆盖相对多电视盒/智能电视。
      * 确认飞智是否获取了小米ROM的系统签名，排除飞智是使用系统签名这个方法的可能性。
        * 查看签名指纹信息 `keytool -printcert -file prj/META-INF/CERT.RSA`
        * `feizhiyouxidatin.3987.com.apk`的签名信息如下。
        
                Owner: EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US
                Issuer: EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US
                Serial number: b3998086d056cffa
                Valid from: Wed Apr 16 06:40:50 CST 2008 until: Sun Sep 02 06:40:50 CST 2035
                Certificate fingerprints:
                         MD5:  8D:DB:34:2F:2D:A5:40:84:02:D7:56:8A:F2:1E:29:F9
                         SHA1: 27:19:6E:38:6B:87:5E:76:AD:F7:00:E7:EA:84:E4:C6:EE:E3:3D:FA
                         SHA256: C8:A2:E9:BC:CF:59:7C:2F:B6:DC:66:BE:E2:93:FC:13:F2:FC:47:EC:77:BC:6B:2B:0D:52:C1:1F:51:19:2A:B8
                         Signature algorithm name: MD5withRSA
                         Version: 3

                Extensions: 

                #1: ObjectId: 2.5.29.35 Criticality=false
                AuthorityKeyIdentifier [
                KeyIdentifier [
                0000: 4F E4 A0 B3 DD 9C BA 29   F7 1D 72 87 C4 E7 C3 8F  O......)..r.....
                0010: 20 86 C2 99                                         ...
                ]
                [EMAILADDRESS=android@android.com, CN=Android, OU=Android, O=Android, L=Mountain View, ST=California, C=US]
                SerialNumber: [    b3998086 d056cffa]
                ]

                #2: ObjectId: 2.5.29.19 Criticality=false
                BasicConstraints:[
                  CA:true
                  PathLen:2147483647
                ]

                #3: ObjectId: 2.5.29.14 Criticality=false
                SubjectKeyIdentifier [
                KeyIdentifier [
                0000: 4F E4 A0 B3 DD 9C BA 29   F7 1D 72 87 C4 E7 C3 8F  O......)..r.....
                0010: 20 86 C2 99                                         ...
                ]
                ]

        * `com.android.motionelfdriver_mi.apk`的签名信息如下。
        
                Owner: L=Mountain, ST=California, C=US
                Issuer: L=Mountain, ST=California, C=US
                Serial number: a07a328482f70d2a
                Valid from: Mon Apr 01 11:08:12 CST 2013 until: Fri Aug 17 11:08:12 CST 2040
                Certificate fingerprints:
                         MD5:  49:5A:6B:E8:6A:31:A3:F5:68:79:3E:A3:D9:88:3D:90
                         SHA1: 08:32:F8:EB:8B:B2:28:12:1A:6E:A9:0C:AD:D8:9D:58:2C:B1:9C:7D
                         SHA256: A7:A0:E1:0A:61:A5:AF:93:62:43:76:DF:60:E9:DE:F9:43:63:58:F5:0A:A6:17:4E:54:23:63:3B:85:6E:2B:E1
                         Signature algorithm name: SHA1withRSA
                         Version: 3

                Extensions: 

                #1: ObjectId: 2.5.29.35 Criticality=false
                AuthorityKeyIdentifier [
                KeyIdentifier [
                0000: 47 20 36 84 E5 62 38 5A   DA 79 10 8C 4C 94 C5 05  G 6..b8Z.y..L...
                0010: 50 37 59 2F                                        P7Y/
                ]
                ]

                #2: ObjectId: 2.5.29.19 Criticality=false
                BasicConstraints:[
                  CA:true
                  PathLen:2147483647
                ]

                #3: ObjectId: 2.5.29.14 Criticality=false
                SubjectKeyIdentifier [
                KeyIdentifier [
                0000: 47 20 36 84 E5 62 38 5A   DA 79 10 8C 4C 94 C5 05  G 6..b8Z.y..L...
                0010: 50 37 59 2F                                        P7Y/
                ]
                ]

        * 小米系统应用的签名如下，可以看到，**飞智的手柄助手驱动用了小米系统签名**。
        
                Owner: L=Mountain, ST=California, C=US
                Issuer: L=Mountain, ST=California, C=US
                Serial number: a07a328482f70d2a
                Valid from: Mon Apr 01 11:08:12 CST 2013 until: Fri Aug 17 11:08:12 CST 2040
                Certificate fingerprints:
                         MD5:  49:5A:6B:E8:6A:31:A3:F5:68:79:3E:A3:D9:88:3D:90
                         SHA1: 08:32:F8:EB:8B:B2:28:12:1A:6E:A9:0C:AD:D8:9D:58:2C:B1:9C:7D
                         SHA256: A7:A0:E1:0A:61:A5:AF:93:62:43:76:DF:60:E9:DE:F9:43:63:58:F5:0A:A6:17:4E:54:23:63:3B:85:6E:2B:E1
                         Signature algorithm name: SHA1withRSA
                         Version: 3

                Extensions: 

                #1: ObjectId: 2.5.29.35 Criticality=false
                AuthorityKeyIdentifier [
                KeyIdentifier [
                0000: 47 20 36 84 E5 62 38 5A   DA 79 10 8C 4C 94 C5 05  G 6..b8Z.y..L...
                0010: 50 37 59 2F                                        P7Y/
                ]
                ]

                #2: ObjectId: 2.5.29.19 Criticality=false
                BasicConstraints:[
                  CA:true
                  PathLen:2147483647
                ]

                #3: ObjectId: 2.5.29.14 Criticality=false
                SubjectKeyIdentifier [
                KeyIdentifier [
                0000: 47 20 36 84 E5 62 38 5A   DA 79 10 8C 4C 94 C5 05  G 6..b8Z.y..L...
                0010: 50 37 59 2F                                        P7Y/
                ]
                ]

  * Linux上运行Native C程序。
    * 把Native C的代码编译成`so`库供Android App使用，由此遇到App权限不足的问题。
    * **是否有可能**把Native C的实现做成可执行程序，在Linux上运行。

#### 虚拟设备驱动

* 问题
  * 安装驱动需要root权限？
  * 需要对应平台的内核源代码？

#### `Instrumentation`（排除）

* `Instrumentation`可以监听系统和应用程序之间的通讯。可以利用它给应用程序发送鼠标键盘消息。
* 局限：如果要向其他App发送消息，还是需要系统签名。