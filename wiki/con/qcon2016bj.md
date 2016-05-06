###移动开发
####“百度移动开发平台最佳实践” - 百度
* 解耦、复用，线上bug修复
* 动态修复
  * oc code -改写-> 动态Lua脚本 -下载-> 脚本解析器 --> 生成iOS函数 -不需编译-> 动态替换添加
  * java code -编译-> plugin.apk -下载-> apk解析器 --> 生成dex -不需编译-> 动态替换添加

###前端
####“打造HTML5游戏引擎开发工具之路” - 青瓷引擎
* 2D/3D引擎
  * [pixi.js](http://www.pixijs.com/)，超快、开源HTML5、JavaScript 2D渲染引擎，使用带有Canvas回调功能的WebGL。
  * [babylon.js](http://www.babylonjs.com/)，基于WebGL、HTML5和JavaScript的开源3D游戏引擎。
* WebGL
  * 2013，Android默认的WebView核与Android Chrome不一样，独立的Chrome 28的核开启不了WebGL。
  * Mobile Browsers: HTML5 Compatibility
    * iOS issues...
      * Backgrounding host crashes WebGL rendering
      * Web Audio and Audio Tag both need to be unlocked on touch event (Use ‘touchend' for iOS 9, ‘touchstart' for previous versions)
      * FPS drops after application re-activated from background on iOS 9, fixed in iOS 9.3
      * Use ```shrink-to-fit``` meta-tag or ```documentElement.clientHeight/Width``` to workaround ```window.innerHeight/Width``` iOS issue on iOS 9
    * Android Audio and Sound FX issues...
      * Stalled audio does not report errors consistently and has binary use of stopped or error report. Need monitor both
      * Sometime Audio Tag showing wrong duration. Save the duration value in meta file when editing as alternative
      * Web Audio is still not well supported
      * Concurrent audio is very limited and problematic
    * Third-Party Browsers issues...
      * UC browser has no gradient fill for text, requires workaround: gradient rect on text - globalCompositeOperation as ‘source-in’
      * Tencent's X5 hardware acceleration only on first 5 canvases; ensure game’s rendering is within these
      * UC browser returns incorrect height value after keyboard disappears
      * If ES6 features used, Emscripten transcompiles are incompatible with any browser not ES6 compliant. eg: ```Math.fround(x) & Math.imul(x, y)```
  * Optimising Mobile Browser Performance
    * Use AppCache for speed and offline browsing
    * Use DOM and dirty rectangles to reduce power consumption
    * Keep your JS/HTML/CSS payload under 2MB
    * Reduce resolution/Canvas size to reduce memory usage
    * Avoid using ‘Stencil’ for some browsers in Android
    * Sample and cache computation for skeleton animation
    * Avoid using ```LINE_LOOP``` and ```TRIANGLE_FAN```
    * Limit batch size, and balance mobile and desktop
    * Getters and setters call overhead is still significant on mobile
    * Is WebGL rendering always faster then Canvas?
    * 性能标准[asm.js](http://asmjs.org/)

####“ReactMix HTML+CSS+JS写React Native” - 携程
* [ReactMix](https://github.com/xueduany/react-mix)在React Native和ReactJs的基础上，全新架构一层Framework和自动化翻译工具，通过相应的翻译机制和扩展模式，将现有的浏览器中可执行的HTML页面、JS代码和CSS样式，同步翻译成为React Native可以执行的代码。

###架构
####“前后端分离中API接口与数据Mock的思考与应用” - 美团大众
* 前端都需要mock
  * iOS：[Nocilla](https://github.com/luisobo/Nocilla)
  * 网页：[mock.js](http://mockjs.com/)

###Testing
####“移动测试体系” - 华为
* 使用[Appium](http://appium.io/)的经验
  * 开源，多种用例语言，跨移动平台，Native/Hybrid/Web
* 在线兼容性测试
  * [阿里MQC](http://mqc.aliyun.com/)，[云测](http://www.testin.cn/)，[百度MTC](http://mtc.baidu.com/)

