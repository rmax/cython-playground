
ctypedef fused num_t:
    int
    float


cdef num_t _func(num_t a, num_t b) nogil:
    return a + b


def func(num_t a, num_t b):
    cdef num_t r
    with nogil:
        r = _func(a, b)
    return r
