from cython cimport numeric


cpdef numeric func(numeric a, int b=0):
    return a + b
