### 框架：设备驱动程序模型

`/proc`文件系统，首次被设计成允许用户态应用程序访问内核内部数据结构的文件系统。

`/sysfs`文件系统本质上与`/proc`目的相同，还提供关于内核数据结构的附加信息，组织结构更合理。  
目标：展现组件间的层次关系。  
核心数据结构`kobject`，与`sysfs`文件系统绑定，每个`kobject`对应`sysfs`文件系统中的一个目录。  
组件用容器来描述，`kobject`嵌入容器中。容器典型例子有总线、设备、驱动程序的描述符。  
`kobject`有引用计数器，也可作为其容器的引用计数器，等于0则释放`kobject`使用的资源，执行`kobj_type`对象的`release`方法释放容器本身。`kset`数据结构把`kobjects`组织成层次树。  
一个`subsystem`可以包括不同类型的`kset`。

### 组件

**设备**由`device`对象描述，`device`对象全部收集在`devices_subsys`子系统中，该子系统对应目录`/sys/devices`。  
`/sys/devices`下的目录结构与硬件设备的物理组织是匹配的。  
`device_register()`函数的功能是往设备驱动程序模型中插入一个新的`device`对象，并自动在`/sys/devices`目录下为其创建一个新的目录。  
**驱动程序**由`device_driver`对象描述。**总线**由`bus_type`对象描述。其中`bus_subsys`子系统与目录`/sys/bus`对应，嵌入在`bus_type`对象中的所有子系统集合在一起，譬如`/sys/bus/pci`目录与PCI总线类型相对应。  
每种总线的子系统包含两个`kset`，`drivers`和`devices`，分别对应于`bus_type`对象中的`drivers`和`devices`字段。  
而`drivers`这个`kset`包含描述符`device_driver`，描述与该总线类型相关的所有设备驱动程序；`devices`这个`kset`包含描述符`device`，描述给定总线类型上连接的所有设备。  
**类**由`class`对象描述。所有类对象属于与`/sys/class`目录对应的`class_subsys`子系统。例如有一个`/sys/class/input`目录，它就与设备驱动程序模型的`input`类相对应。

### 设备文件

* 索引节点包含设备标识符，而不是指向磁盘上数据块的指针。
* 设备标识符由设备文件类型（字符或块）和主设备号（相同的由同一个设备驱动程序处理）次设备号组成。