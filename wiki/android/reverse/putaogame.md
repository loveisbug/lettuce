### 热门游戏排行榜

### 游戏大厅里下载的游戏apk分析

从葡萄游戏大厅里下载深圳梦域科技的“地铁跑酷”v3.0.5.5.11（更新2015-1-13），从安智市场下载标注“官方”的“地铁跑酷”v2.27.0（更新2015-1-16），对比分析。

#### Java部分

* ptsdk（葡萄SDK）
  * 位于`assets/ptsdk`
  * `config`配置文件包含是否支持手柄、玩家人数、手机当手柄等信息。
  * 所有`.p`文件（包括`i`目录、`o`目录、`t`目录下的`.p`文件，`m.z`里解压出来的文件）都是`.png`图片，包括手柄按键指南贴图。
  * `.b`文件未知是什么。
  * `sign`文件里的数字像是CRC校验值，不大像是应用签名的Hash值。尝试了求值`classes.dex`文件的CRC校验，数值对不上。也不是MD5。应该是在应用启动时判断是否被篡改。
  * 一堆图片几个配置文件，这玩意也叫sdk。。。看起来就是一些配置文件了，具体怎么使用要看java代码。
* call native lib
  * `com.unity3d.player.UnityPlayer.java`中`System.loadLibrary("mono");`和 `System.loadLibrary("unity");`
  * `com.yunos.tv.exdeviceservice.client.EXDeviceeManager.java`中`System.loadLibrary("exdeviceservicesdk");`
  * `com.putaolab.ptsdk.i.PTLoader.java`中`System.loadLibrary("plog");`
  * 移除的native库，也要移除相应的Java代码
* 看上去，`com.yunos.tv.exdeviceservice`和`libexdeviceservicesdk.so`一起实现手柄等控制操作。Java部分有以下模块，由client模块负责和C/C++库打交道，处理各外设事件。
  * mouse
  * client
  * exdevice
  * keyboard
  * motion
  * sensor
  * touch
* [反编译学习](https://github.com/loveisbug/lettuce/blob/master/wiki/android/reverse/decompile_android_notes.md)

#### C/C++/C#部分

##### `.so`

* 看起来，葡萄大厅把游戏的支付部分都去掉了。

原生|大厅|备注
----|----|----
`libdserv.so`|N/A|integrate various payment SDKs, AnyStore SDK
`libegamepay.so`|N/A|integrate various payment SDKs, AnyStore SDK
`libhfswpay.so`|N/A|
`libmain.so`|N/A|
`libmono.so`(3.9MB)|`libmono.so`(85KB) 从中再调用`assets/libs/armeabi-v7a/libmono.so`(3.8MB)??|Unity3D lib
`libsmsiap.so`|N/A|移动MM提供的，和支付有关
`libunity.so`(11MB)|`libunity.so`(44KB) 从中再调用`assets/libs/armeabi-v7a/libunity.so`(6.8MB)??|Unity3D lib
N/A|`libexdeviceservicesdk.so`|`yunos.tv.exdeviceservice/client`不知道是不是yun os提供的库
N/A|`libplog.so`|葡萄SDK ptsdk lib

* apk包的`lib`目录下Unity3D lib文件很小，`assets`里放了两个看上去正常一些的lib文件。
* `libmono.so`是一个跨平台的.NET框架工具，
  * 其中的`mono_image_open_from_data_full()`接口调用`assets/bin/Data/Managed`目录下一系列`Assembly-CSharp.dll`和`UnityEngine.dll`等。
* 比较原生的和大厅放到`assets`目录里的`libunity.so`，
  * 大厅版多出了很多类似这样名字里包含"money"的函数（撇开头尾中间的混淆）：`_ZNSt10moneypunctIwLb0EE4intlE`，`_ZNKSt17moneypunct_bynameIcLb0EE16do_negative_signEv`。
* 分析`libexdeviceservicesdk.so`
  * 依赖`libstdc++.so`, `libm.so`, `libc.so`, `libdl.so`, liblog.so
  * 指令集ARMv5TE, Little endian
  * C++代码实现这几个类
    * `AppInfo` -- 获取应用信息、系统信息、video size等。
    * `ExDevice` -- 获取各类型外设输入数据，调用`Communicator`对象的方法发送事件消息。
    * `EXDeviceManager` -- 对Java层有提供JNI接口。像是实现了一个server，Java层实现一个client。
    * `Communicator` -- 发送、处理事件消息。
    * `RemoteConn`
    * `RemoteThread` -- 线程间通讯。
    * `BackWriter`
  * C代码实现
    * `cJSON` -- 外设的输入数据封装成JSON格式。
    * `ev` -- `libev`事件库？看上去用的是`libev`4.15版本。
    * `event` -- `libevent`？像是对`libev`的封装。
    * `block` --
* 分析`libplog.so`
  * 依赖`libstdc++.so`, `libm.so`, `libc.so`, `libdl.so`
  * 指令集 ARMv5TE, Little endian
* [IDA Pro使用笔记](https://github.com/loveisbug/lettuce/blob/master/wiki/vulnerability/reverse/idaq_notes.md)

##### `.dll`

* 对比原生版本和葡萄版本的dll差异

文件|原生|大厅|备注
----|----|----|----
`Assembly-CSharp-firstpass.dll`|127KB|84KB|
`Assembly-CSharp.dll`|2MB|712KB|
`mscorlib.dll`|1.6MB|1.5MB|
`P31RestKit.dll`|10KB|15KB|
`System.Core.dll`|34KB|32KB|
`System.dll`|79KB|79KB|
`UnityEngine.dll`|266KB|220KB|

* decompile dlls
  * `Assembly-CSharp-firstpass.dll`
    * 大厅版去掉了1个类Json，属于如下命名空间
    
    namespace|
    ----|
    MiniJSON|
    
  * `Assembly-CSharp.dll`
    * 大厅版去掉了大量类定义，分别属于以下命名空间
    
    namespace|
    ----|
    Chall.Interface|
    Chall.Internal|
    com.kiloo.awards|
    JetBrains.Annotations|
    Kiloo.Common|
    TopRun.Internal|
    UnityEngine|
    
  * `UnityEngine.dll`
  
  原生|大厅
  ----|----
  `UnityEngine`|
  `UnityEngine.Internal`|No
  `UnityEngine.SocialPlatforms`|
  `UnityEngine.SocialPlatforms.GameCenter`|
  `UnityEngine.SocialPlatforms.Impl`|
  `UnityEngineInternal`|
  
  * `P31RestKit.dll`
* 通过dll的封装实现热更新？参考[unity3d代码热更新](http://jingpin.jikexueyuan.com/article/30278.html)，和[Unity3D热更新](http://www.cnblogs.com/crazylights/p/3897742.html)。

#### 猜想

* Java部分增加`com.yunos.tv.exdeviceservice`，包括对各种输入事件的监听和一个client。
* native部分增加`libexdeviceservicesdk.so`，实现一个server。
* native部分用假的`libmono.so`, `libunity.so`替换，用来加载所需的so库和dll库。
* 这样，看上去似乎可以不修改dll，我们需要知道native部分怎么调用Unity3D接口把事件传递过去。

![](https://github.com/loveisbug/lettuce/blob/master/wiki/pic/UnityEngine_App.png)

#### Step-By-Step修改原始地铁跑酷apk

* 获取apk，apktool+dex2jar+JD-GUI得到`AndroidManifest.xml`、资源文件、`jar`文件，`src`目录下的java文件。
* 清空`src`目录，工程中引入`jar`文件。
* 编译。
  * 报错。`AndroidManifest.xml`中`String types not allowed (at 'screenOrientation' with value 'sensorPortait')`。
  * 参照葡萄游戏大厅的改动，把`sensorPortait`换成`landscape`，通过。
  * stackoverflow上有人提到一个[targetApi相关的typo error](http://stackoverflow.com/a/23514685/1361234)，说是在API 16修复，我们工程里是API 19。
* 添加我们的手柄SDK。编译。
  * `.so`
    * 现在的`.so`库只有`armeabi`（ARMv5）版本的，最好做`armeabi-v7a`（ARMv7）。
  * `.jar`
* 修改smali文件，增加代码调用SDK API。
  * 譬如，只调用`IInputInterceptor.setMode(int mode)`。
  * 主包`com.kiloo.subwaysurf.RRAndroidPluginActivity`做了反编译保护，只能看smali文件。
  * 通过apktool反编译、再编译出apk，签名。
    * 想通过·apktool b -c·来[“Copies original AndroidManifest.xml and META-INF folder into built apk.”](https://code.google.com/p/android-apktool/wiki/ApktoolOptions)，还是躲不掉重新签名。
  * 在`com.putaolab.ptsdk.activity.PTMainActivity.smali`中增加如下代码，build、签名后运行。

        # interfaces
        .implements Lcom/blablaname/tv/controller/sdk/interceptor/IInputEventListener;

        # instance fields
        .field private mInputInterceptor:Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;

        ...

        .method protected onCreate(Landroid/os/Bundle;)V
            .locals 3
            .param p1, "savedInstanceState"    # Landroid/os/Bundle;

            .prologue
            invoke-super {p0, p1}, Landroid/app/Activity;->onCreate(Landroid/os/Bundle;)V

            const-string v1, "ERICTAG"
            const-string v2, "In PTMainActivity, onCreate(), Test Begin*****"
            invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

            new-instance v0, Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;

            invoke-direct {v0, p0, p0}, Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;-><init>(Landroid/content/Context;Lcom/blablaname/tv/controller/sdk/interceptor/IInputEventListener;)V

            iput-object v0, p0, Lcom/putaolab/ptsdk/activity/PTMainActivity;->mInputInterceptor:Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;

            const/4 v1, 0x0
            invoke-virtual {p0, v1}, Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;->setMode(I)V    

            const-string v1, "ERICTAG"
            const-string v2, "In PTMainActivity, onCreate(), Test End*******"
            invoke-static {v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;)I

            return-void
        .end method

        .method public onSdkGenericMotionEvent(Landroid/view/MotionEvent;)Z
            .locals 1
            .param p1, "event"    # Landroid/view/MotionEvent;
            return v0
        .end method

        .method public onSdkKeyEvent(Landroid/view/KeyEvent;)Z
            .locals 1
            .param p1, "event"    # Landroid/view/KeyEvent;
            return v0
        .end method

        .method public onSdkTouchEvent(Landroid/view/MotionEvent;)Z
            .locals 1
            .param p1, "event"    # Landroid/view/MotionEvent;
            return v0
        .end method

  * 报错如下，
  
        W/dalvikvm(4700): VFY: 'this' arg 'Lcom/putaolab/ptsdk/activity/PTMainActivity;' not instance of 'Lcom/blablaname/tv/controller/sdk/interceptor/InputInterceptor;'

### 启动大厅时抓包分析

### 手机当手柄apk分析