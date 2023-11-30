# distutils: language = c++
# distutils: libraries=spdlog

cdef extern from "spdlog/spdlog.h" namespace "spdlog":
    cdef inline void trace[T](const T &msg)

    cdef inline void debug[T](const T &msg)

    cdef inline void info[T](const T &msg)

    cdef inline void warn[T](const T &msg)

    cdef inline void error[T](const T &msg)

    cdef inline void critical[T](const T &msg)

