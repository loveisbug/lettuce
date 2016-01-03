###CHAPTER 3 Basic Types, Strings, and Arrays

* Do not forget to check the return value of `GetStringUTFChars`.
* Do not forget to call `ReleaseStringChars` when you no longer need access to the string elements returned from `GetStringChars`.

###CHAPTER 4 Fields and Methods

* At the Java programming language level, you can invoke a static method f in class Cls using two alternative syntaxes: either Cls.f or obj.f where obj is an instance of Cls. (The latter is the recommended programming style, however.)
* In the JNI, you must always specify the class reference when issuing static method calls from native code.
* Given that we can implement equivalent functionality using other JNI functions, why does the JNI provide built-in functions such as `NewString`?
* The reason is that the built-in string functions are far more efficient than calling the `java.lang.String` API from native code. String is the most frequently used type of objects.
* The native code should not invoke a constructor on the same object multiple times.
* Obtaining field and method IDs requires symbolic lookups based on the name and descriptor of the field or method. Symbolic lookups are relatively expensive.
* where feasible, it is preferable to cache field and method IDs in the static initializer of their defining classes.
* Java/native calls are potentially slower than Java/Java calls for the following reasons:
  * Native methods most likely follow a defferent calling convention than that used by Java/Java calls inside the Java virtual machine implementation. As a result, the virtual machine must perform additional operations to build arguments and set up the stack frame before jumping to a native method entry point.
  * It is common for the virtual machine to inline method calls. Inlining Java/native calls is a lot harder than inlining Java/Java calls.
* The performance characteristics of a native/Java callback is technically similar to Java/native call.
  * In theory, the overhead of native/Java callbacks could also be within two to three times of Java/Java calls. In practice, however, native/Java callbacks are relatively infrequent. Virtual machine implementations do not usually optimize the performance of callbacks.
  * At the time of this writing many production virtual machine implementations are such that the overhead of a native/Java callback can be as much as ten times higher than a Java/Java call.
* The overhead of field access using the JNI lies in the cost of calling through the JNIEnv. Rather than directly dereferencing objects, the native code has to perform a C function call which in turn dereferences the object.
* The JNI field access overhead is typically negligible because a function call takes only a few cycles.
###CHAPTER 5 Local and Global References

* Local references are also only valid in the thread that creates them. A local reference that is created in one thread cannot be used in another thread. It is a programming error for a native method to store a local reference in a global variable and expect another thread to use the local reference.
* Each JNI reference consumes a certain amount of memory by itself, in addition to the memory taken by the referred object.
* As a JNI programmer, you should be aware of the number of references that your program will use at a given time.
* should explicitly free local references in order to avoid excessive memory usage.
  * You need to create a large number of local references in a single native method invocation.
  * You want to write a utility function that is called from unknown contexts.
  * Your native method does not return at all.
  * Your native method accesses a large object, thereby creating a local reference to the object. The native method then performs additional computation before returning to the caller. The local reference to the large object will prevent the object from being garbage collected until the native method returns, even if the object is no longer used in the remainder of the native method.
* The JNI specification dictates that the virtual machine automatically ensures that each native method can create at least 16 local references.