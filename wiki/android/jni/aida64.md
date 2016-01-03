### native部分
`libaida_cuda.so`

打开

    /system/vendor/lib/libcuda.so
    /system/vendor/lib/libnvcompute.so
    
调用

    cuDeviceGet()
    cuDeviceGetName()
    cuDeviceTotalMem_v2()
    cuDeviceComputeCapability()
    cuDeviceGetProperties()
    cuDeviceGetAttribute()
    
[接口文档](https://www.cs.cmu.edu/afs/cs/academic/class/15668-s11/www/cuda-doc/html/group__CUDA__DEVICE_gef75aa30df95446a845f2a7b9fffbb7f.html)

`libaida_opencl.so`

打开

    /system/vendor/lib/libOpenCL.so
    /system/lib/libOpenCL.so
    /system/vendor/lib/libPVROCL.so
    /system/vendor/lib/egl/libGLES_mali.so
    /system/vendor/lib/libllvm-a3xx.so
    
调用

    clGetPlatformIDs()
    clGetDeviceIDs()
    clGetDeviceInfo()
    devVenID()
    ...
    
`libaida_cpuid.so`

TBD

#### Sample Code

    #include <cuda.h>
    #include <stdio.h>
    #include <dlfcn.h>

    void * loadCudaLibrary() {
        return dlopen ("libcuda.so", RTLD_NOW);
    }

    void (*getProcAddress(void * lib, const char *name))(void){
        return (void (*)(void)) dlsym(lib,(const char *)name);
    }

    int freeLibrary(void *lib)
    {
        return dlclose(lib);
    }

    typedef CUresult CUDAAPI (*cuInit_pt)(unsigned int Flags);
    typedef CUresult CUDAAPI (*cuDeviceGetCount_pt)(int *count);
    typedef CUresult CUDAAPI (*cuDeviceComputeCapability_pt)(int *major, int *minor, CUdevice dev);

    int main() {
        void * cuLib;
        cuInit_pt my_cuInit = NULL;
        cuDeviceGetCount_pt my_cuDeviceGetCount = NULL;
        cuDeviceComputeCapability_pt my_cuDeviceComputeCapability = NULL;

        if ((cuLib = loadCudaLibrary()) == NULL)
            return 1; // cuda library is not present in the system

        if ((my_cuInit = (cuInit_pt) getProcAddress(cuLib, "cuInit")) == NULL)
            return 1; // sth is wrong with the library
        if ((my_cuDeviceGetCount = (cuDeviceGetCount_pt) getProcAddress(cuLib, "cuDeviceGetCount")) == NULL)
            return 1; // sth is wrong with the library
        if ((my_cuDeviceComputeCapability = (cuDeviceComputeCapability_pt) getProcAddress(cuLib, "cuDeviceComputeCapability")) == NULL)
            return 1; // sth is wrong with the library

        {
            int count, i;
            if (CUDA_SUCCESS != my_cuInit(0))
                return 1; // failed to initialize
            if (CUDA_SUCCESS != my_cuDeviceGetCount(&count))
                return 1; // failed

            for (i = 0; i < count; i++)
            {
                int major, minor;
                if (CUDA_SUCCESS != my_cuDeviceComputeCapability(&major, &minor, i))
                    return 1; // failed

                printf("dev %d CUDA compute capability major %d minor %d\n", i, major, minor);
            }
        }
        freeLibrary(cuLib);
        return 0; 
    }

### java部分
TBD