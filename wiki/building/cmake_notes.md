### Makefile

`Android.mk`

* `LOCAL_LDFLAGS`和`LOCAL_LDLIBS`的主要区别
  * `LOCAL_LDFLAGS` appear *before* the list of object files and libraries on the final linker command-line, this is where you want to put actual "flags" that affect linker behaviour.
  * `LOCAL_LDLIBS` appear *after* the list of object files and libraries on the final linked command-line, this is where you want to put actual system library dependencies.
  * The distinction exists because of the way static linking works on Unix, i.e. the order of object files, static libraries and shared libraries is very important to determine the final result, and sometimes you really to ensure that something appears before / after the other.
  * In the end, I recommend following the documentation, i.e.:
    * Put real linker flags into `LOCAL_LDFLAGS`
    * Put system library dependencies into `LOCAL_LDLIBS`
    * Only use `LOCAL_LDLIBS` for system library dependencies. If you want to point to another library, it's much better to list them in either `LOCAL_STATIC_LIBRARIES` and `LOCAL_SHARED_LIBRARIES` (even if this means defining a PREBUILT_XXX module for them), because this lets the build system work out dependencies and ordering automatically for you.

### CMake Tips

* Project
  * 顶层的`CMakeLists.txt`必须包含`project()`命令。仅通过`include()`调用是不够的。如果没有，CMake会隐式增加一个并默认支持语言C和CXX。

* macro
  * macro名字中不能有`-`字符。否则会报错Parse error.  Expected a command name, got unquoted argument with text ""。
  * 如何在`CMakeLists.txt`文件里增加link and compile flags
    * 假设有这些flag需要添加
    
          set(GCC_COMMON_CFLAGS "-O0 -g -DFOO")
    * 方法1，仅对compile flags有效
    
          add_definitions(${GCC_COMMON_CFLAGS})
    * 方法2，对已有cmake变量追加
    
          set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${GCC_COMMON_CFLAGS}")
          set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GCC_COMMON_CFLAGS}")
    * 方法3，使用target属性，参考[cmake compile flag target property](http://www.cmake.org/cmake/help/v2.8.8/cmake.html#prop_tgt%3aCOMPILE_FLAGS)，需要知道target name
    
          get_target_property(TEMP ${THE_TARGET} COMPILE_FLAGS)
          if(TEMP STREQUAL "TEMP-NOTFOUND")
            SET(TEMP "") # set to empty string
          else()
            SET(TEMP "${TEMP} ") # a space to cleanly separate from existing content
          endif()
          # append our values
          SET(TEMP "${TEMP}${GCC_COMMON_CFLAGS}" )
          set_target_properties(${THE_TARGET} PROPERTIES COMPILE_FLAGS ${TEMP} )