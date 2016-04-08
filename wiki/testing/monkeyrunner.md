### MonkeyRunner能做什么

[MonkeyRunner](http://developer.android.com/tools/help/monkeyrunner_concepts.html) interacts with the device or emulator below the level of the framework APIs.

* installs an Android application or test package,
* runs it,
* sends keystrokes to it,
* takes screenshots of its user interface,
* stores screenshots on the workstation,
* record/playback test case.

### 需求分析

* 支持不同设备（分辨率不同，还有什么不同？）
* 目前看下来，可能只能用坐标值来定位控件了。没法用Android Hierarchy Viewer来定位界面元素。
  * 量产设备无法使用Hierarchy Viewer，报错`Unable to debug device. Could not connect to the view server.`，也不能使用easy package里的`By`和`EasyMonkeyDevice`这两个类。
  * 找到一个开源项目[`ViewServer`](https://github.com/romainguy/ViewServer)据说可以支持Hierarchy Viewer，尚未仔细考察。
  * 需确认root后是否可以使用Hierarchy Viewer，OK后再确认`EasyMonkeyDevice`和`By`是否可以用。
  * 可以用`MonkeyRecorder`来录制测试用例（主要是用来记录点击操作的坐标值）。如下，

```python
    from com.android.monkeyrunner.recorder import MonkeyRecorder as recorder  
    recorder.start(dev_conn)
```
  * 除了Hierarchy Viewer不可用之外，我们的应用布局方法没有给每个位置的控件一个唯一的id。可以用`MonkeyRecorder`来辅助建立控件位置库，也可以用Android Tools `monitor`来分析每一个view里的控件坐标范围。尝试下来，`monitor`比较好用。
    * 不同分辨率盒子的不同坐标用配置文件，`json` or `xml`？

```python    
    displayX = (x - minX) * displayWidth / (maxX - minX + 1)
    displayY = (y - minY) * displayHeight / (maxY - minY + 1)
```
    * Python脚本读取不同配置文件，给控件对象初始化坐标值，建立每个控件的安全可TOUCH坐标点，
    * 针对每个测试用例，建立从`startActivity`之后的抵达路径，
    * 每个测试用例执行完成后，怎么回到一个初始状态以便于下一个用例的开始执行（抵达路径合理）？
    * `MonkeyImage`可以对比两张截图，返回布尔值，可以调整允许的差异（百分比0.0~1.0），
    * 问题：很多界面（列表、矩阵）中的元素没有ID；可TOUCH坐标点的计算依赖于该控件在view中的位置，
    * `json`格式的坐标配置文件，每个子项目由`name`、`lt`、`rb`、`touchpoint`、`sub`组成，`touchpoint`是自动计算还是建库时填入？
      * [控件](https://github.com/loveisbug/lettuce/blob/master/python/monkeyrunner/democode/mi2.json)
      * [路径](https://github.com/loveisbug/lettuce/blob/master/python/monkeyrunner/democode/path.json)
      * Python解析`json`

```python      
    import json
    f = file('test.json')
    s = json.load(f)
    # 's' is 'dict', s['sub'] is 'list'.
    f.close()
```
      * 解析控件json文件建立控件列表，解析路径json文件建立测试用例路径列表。
      * 选择需要执行的测试用例，从用例路径列表中得到其控件列表，再从控件列表中获取每个控件的坐标。
    * 有[`ViewClient`](https://github.com/dtmilano/AndroidViewClient)插件可以用来获取控件文本，可以尝试，
    
* 管理测试用例库。
  * 便于根据测试需求选取合适的用例组合。
  * 独立用例执行完应用状态的重置。
* 输出测试结果，定制报告格式。
* ...
* TODO
  * 搭建调试环境
  * 检查版本更新测试用例
  * 页面展示测试用例
  * 应用下载测试用例
  * 应用更新测试用例
  * ...
  
### 框架

* 针对每一次自动测试，编辑测试配置文件`case.json`
* 文件内包含
  * App包名+主界面`Activity`
  * 待测试设备名（`serialNumber`）
  * case集，字符串`casen`列表
* 自动测试脚本读取设备`serialNumber`，连接设备；运行待测App，开始执行case集中的case
* TODO
  * 每一个case执行后如何判断pass/fail
  * 每一个case执行后如何统一返回一个初始状态便于下一个case的执行

**参考**

[https://github.com/yeetrack/monkeyrunner](https://github.com/yeetrack/monkeyrunner)

#### 坑

* [无法`import json`](https://github.com/loveisbug/lettuce/blob/master/wiki/testing/mr_json.md)
* [截图比较](https://github.com/loveisbug/lettuce/blob/master/wiki/testing/mr_image.md)