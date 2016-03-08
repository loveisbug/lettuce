### Decompile

* `apktool`处理`AndroidManifest.xml`、资源文件和[`smali`](https://github.com/loveisbug/lettuce/blob/master/wiki/android/reverse/smali_spec.md)文件。
* [`dex2jar` + `JD-GUI`](https://github.com/loveisbug/lettuce/blob/master/wiki/vulnerability/reverse/badmemory.md#dex2jar--jd-gui)获得`jar`。

### Recompile
#### Trial

* 从[decompileandroid.com](http://www.decompileandroid.com/)获得反编译出来的java源代码文件，recompile不通过。
  * 报错：
    1. 可能是由循环等跳转逻辑产生的类似`_L1`，`_L7`这样的标签`"cannot be resolved to a variable"`。
    1. 混淆过的方法名无法处理。
    1. 一些`import`的自定义类在代码里报错。
* 在前一步的基础上（工程目录）删除所有`src`目录下的`java`文件，给工程加入`dex2jar`得到的`jar`文件，可以recompile。但是无法在Android模拟器（Genymotion）上运行。
  * 报错：
  
            D/AndroidRuntime( 1220): >>>>>> AndroidRuntime START com.android.internal.os.RuntimeInit <<<<<<
            D/AndroidRuntime( 1220): CheckJNI is OFF
            D/AndroidRuntime( 1220): Calling main entry com.android.commands.am.Am
            D/AndroidRuntime( 1220): Shutting down VM
            D/AndroidRuntime( 1249): Shutting down VM
            E/AndroidRuntime( 1249): FATAL EXCEPTION: main
            E/AndroidRuntime( 1249): Process: com.minicliphr.subwaysurfing, PID: 1249
            E/AndroidRuntime( 1249): java.lang.RuntimeException: Unable to instantiate activity ComponentInfo{com.minicliphr.subwaysurfing/com.putaolab.ptsdk.activity.PTMainActivity}: java.lang.ClassNotFoundException: Didn't find class "com.putaolab.ptsdk.activity.PTMainActivity" on path: DexPathList[[zip file "/data/app/com.minicliphr.subwaysurfing-1.apk"],nativeLibraryDirectories=[/data/app-lib/com.minicliphr.subwaysurfing-1, /system/lib]]
  * 原App也未能再成功运行，原因未知，可能和JNI代码及Android模拟器有关。于是，尝试把recompile的App安装到电视盒子上。
    * [参考1](http://stackoverflow.com/questions/26839947/runtimeexception-didnt-find-class-on-path-dexpathlist-that-makes-mad)
    * [参考2](http://stackoverflow.com/questions/23074381/didnt-find-class-on-path-dexpathlist)
  * App安装到盒子上还是不能运行。报错：
  
            02-11 11:44:53.383 D/AndroidRuntime( 3672): Shutting down VM
            02-11 11:44:53.383 E/AndroidRuntime( 3672): FATAL EXCEPTION: main
            02-11 11:44:53.383 E/AndroidRuntime( 3672): Process: com.minicliphr.subwaysurfing, PID: 3672
            02-11 11:44:53.383 E/AndroidRuntime( 3672): java.lang.RuntimeException: Unable to instantiate activity ComponentInfo{com.minicliphr.subwaysurfing/com.putaolab.ptsdk.activity.PTMainActivity}: java.lang.ClassNotFoundException: Didn't find class "com.putaolab.ptsdk.activity.PTMainActivity" on path: DexPathList[[zip file "/data/app/com.minicliphr.subwaysurfing-1.apk"],nativeLibraryDirectories=[/data/app-lib/com.minicliphr.subwaysurfing-1, /vendor/lib, /system/lib]]  
    * 原因是昏头犯了一个低级错误，decompileandroid上反编译出来的源代码zip包里`library`目录是`lib`，需要改成`libs`。否则recompile的apk里丢失了`libs`里的`.so`库文件。

#### 小结

* 反编译到Java这一层，跳转逻辑和对象名变化较大，很可能无法再次编译。
* `classes.dex`转成`jar`是可以再次编译的。自己新增的模块`jar`应该可以一样地导入工程里。
* `smali`这一层，不清楚做过`ProGuard`混淆后会有怎样的影响。还不清楚怎么把自己新增的模块代码加进去。
* 如果除了新增，还需要修改代码，是不是只能改`smali`代码。