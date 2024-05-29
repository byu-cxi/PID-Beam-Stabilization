# This code was written to give experience in using callback functions via ctypes (written with testCcode.c)

import numpy as np
from matplotlib import pyplot as plt
import ctypes
import os
import ctypes

file_location = os.path.dirname(os.path.realpath(__file__))
test_so = ctypes.CDLL(f'{file_location}/testccode.so') # CDLL is a c-to-python converter, .dll is a function library

c_int = ctypes.c_int32

class structMirror(ctypes.Structure):
    _fields_ = [('num1', c_int),
                ('num2', c_int),
                ('num3', c_int)]

def callbackFunc(attributes, bytePtr):
    struc = attributes.contents
    print("Callback successful: num =", struc.num1, struc.num2, struc.num3)
    print(np.array(bytePtr[0:4], dtype=ctypes.c_char))
    global num
    num = 12345


callPrototype = ctypes.CFUNCTYPE(None, ctypes.POINTER(structMirror), ctypes.c_char_p)

num = 123
print("num before is",num)
test_so.callbackCaller.argtypes = [c_int, callPrototype]
test_so.callbackCaller(num, callPrototype(callbackFunc))
print("num after is", num)


if False:
    def img_update(x, y):
        plt.scatter(x,y)
        plt.pause(0.000001)

    i=0
    while True:
        img_update(i, 2*i)
        i = i+1


