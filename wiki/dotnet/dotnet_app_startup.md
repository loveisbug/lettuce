### Order of Events in Windows Forms

#### Application Startup and Shutdown Events

The Form and Control classes expose a set of events related to application startup and shutdown. When a Windows Forms application starts, the startup events of the main form are raised in the following order:

* Control.HandleCreated
* Control.BindingContextChanged
* Form.Load
* Control.VisibleChanged
* Form.Activated
* Form.Shown

When an application closes, the shutdown events of the main form are raised in the following order:

* Form.Closing
* Form.FormClosing
* Form.Closed
* Form.FormClosed
* Form.Deactivate

#### Startup Events
* [https://msdn.microsoft.com/en-us/library/t4zch4d2(v=vs.90).aspx](https://msdn.microsoft.com/en-us/library/t4zch4d2(v=vs.90).aspx)

### WebBrowser DocumentCompleted事件
* [判断WebBrowser加载完毕](http://blog.csdn.net/cometnet/article/details/5261192，http://bbs.csdn.net/topics/360016295)
* Open the Application page of the project properties. Click the View Application Events button and then use the drop-downs at the top of the code window to create a handler for the Startup event. The 'e' parameter of that event handler provides direct access to the commandline parameters. If you want to exit without creating the startup form, just set e.Cancel to True.