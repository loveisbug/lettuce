* 截图比较时，尽量用`MonkeyImage.getSubImage()`缩小需比较的范围，尽量用`percent = 1.0`作为参数来比较。
  * 两次截图rect完全一致，
  * 第一次截图，存为预留文件
  
        imagefile = dev.takeSnapshot().getSubImage((514, 233, 644, 85))
        imagefile.writeToFile('up-to-date.png', 'png')
        
  * 第二次截图，对比
  
        imageTrue = MonkeyRunner.loadImageFromFile('up-to-date.png')
        passed = imageTrue.sameAs(dev.takeSnapshot().getSubImage((514, 233, 644, 85)), 1.0)
        
  * 截图               