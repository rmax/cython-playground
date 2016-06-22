from cython cimport numeric


cpdef numeric func(numeric a, int b):
    return a + b
