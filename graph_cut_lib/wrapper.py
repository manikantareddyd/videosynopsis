import numpy as np
import numpy.ctypeslib as npct
import ctypes
from ctypes import *

array_3d_int = npct.ndpointer(dtype=np.int, ndim=3, flags='C_CONTIGUOUS')

lib = npct.load_library("library.so",".")

lib.something.restype = None
lib.something.argtypes = [array_3d_int,c_int,array_3d_int]

ind = np.ones((5,5,3),dtype=np.int)
outd = np.zeros((5,5,3), dtype=np.int)

lib.something(ind,5,outd)

print outd
