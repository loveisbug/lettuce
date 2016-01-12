### Dalvik字节码
#### 类型

Dalvik字节码有两种类型，原始类型和引用类型。对象和数组是引用类型，其它都是原始类型。

    V       void，只能用于返回值类型
    Z       boolean
    B       byte
    S       short
    C       char
    I       int
    J       long (64bit)
    F       float
    D       double (64bit)
    
对象以`Lpackage/name/ObjectName;`的形式表示。  
前面的`L`表示这是一个对象类型，`package/name/`是该对象所在的包，`ObjectName`是对象的名字，`;`表示对象名称的结束。相当于java中的`package.name.ObjectName`。  
例如：`Ljava/lang/String;`相当于`java.lang.String`。

#### 数组

* `[I`表示1个整型一维数组，相当于java中的`int[]`。
* 对于多维数组，只要增加`[`就行了。`[[I`相当于`int[][]`，`[[[I`相当于`int[][][]`。注意每一维的最多`255`个。
* 对象数组的表示：`[Ljava/lang/String;`表示一个`String`对象数组。

#### 方法

表示形式：

    Lpackage/name/ObjectName;->MethodName(III)Z

* `Lpackage/name/ObjectName;`表示类型，`MethodName`是方法名。`III`为参数（在此是3个整型参数），`Z`是返回类型（`bool`型）。
* 方法的参数是一个接一个的，中间没有隔开。

一个更复杂的例子：

    method(I[[IILjava/lang/String;[Ljava/lang/Object;)Ljava/lang/String;
    
在java中则为：

    String method(int, int[][], int, String, Object[])
    
#### 字段

表示形式：

    Lpackage/name/ObjectName;->FieldName:Ljava/lang/String;
    
即包名，字段名和各字段类型。

#### 寄存器

在Dalvik字节码中，寄存器都是32位的，能够支持任何类型。64位类型（`Long`和`Double`型）用2个寄存器表示。  
有两种方式指定一个方法中有多少寄存器是可用的。

  * `.registers`指令指定了方法中寄存器的总数。
  * `.locals`指令表明了方法中非参寄存器的数量。

#### 方法的传参

* 当一个方法被调用的时候，方法的参数被置于最后N个寄存器中。如果一个方法有2个参数，5个寄存器（`v0`-`v4`），那么参数将置于最后2个寄存器——`v3`和`v4`。
* 非静态方法中的第一个参数总是调用该方法的对象。

例如，非静态方法`LMyObject;->callMe(II)V`有2个整型参数，另外还有一个隐含的`LMyObject;`参数，所以总共有3个参数。假如在该方法中指定了5个寄存器（`v0`-`v4`），以`.registers`方式指定5个或以`.locals`方式指定2个（即2个`local`寄存器+3个参数寄存器）。当该方法被调用的时候，调用该方法的对象（即`this`引用）存放在`v2`中，第一个整型参数存放在`v3`中，第二个整型参数存放在`v4`中。  
对于静态方法除了没有隐含的`this`参数外其它都一样。

#### 寄存器的命名方式

有两种方式——V命名方式和P命名方式。P命名方式中的第一个寄存器就是方法中的第一个参数寄存器。在下表中我们用这两种命名方式来表示上一个例子中有5个寄存器和3个参数的方法。

    v0      第一个local register
    v1      第二个local register
    v2      p0      第一个parameter register
    v3      p1      第二个parameter register
    v4      p2      第三个parameter register

你可以用任何一种方式来引用参数寄存器——他们没有任何差别。

注意：

* `baksmali`默认对参数寄存器使用P命名方式。如果想使用V命名方式，可以使用`-pl—no-parameter-registers`选项。
* 使用P命名方式是为了防止以后如果要在方法中增加寄存器，需要对参数寄存器重新进行编号的缺点。

#### `long/double`值

`long`和`double`类型是64位的，需要2个寄存器（切记切记）。 例如，对于非静态方法`LMyObject;->MyMethod(IJZ)V`，参数分别是`LMyObject;`, `int`, `long`, `bool`。故该方法需要5个寄存器来存储参数。

    p0      this
    p1      I
    p2,p3   J
    p4      Z

#### Dalvik opcodes

[Dalvik opcodes查表](http://pallergabor.uw.hu/androidblog/dalvik_opcodes.html)

### smali specification
#### 修改`smali`文件

    const-string v0, "MyTag"
    const-string v1, "Something to print"
    # assuming you have an exception in v2...
    invoke-static {v0, v1, v2}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable)I