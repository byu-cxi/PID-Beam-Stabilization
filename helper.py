# file for functions that are important,
    # but not the main focus of the program
import numpy as np

def TupleSubtract(tup1, tup2):
    return tuple(map(lambda i,j : i-j, tup1, tup2))

def TupleAdd(tup1, tup2):
    return tuple(map(lambda i,j : i+j, tup1, tup2))

def AddCrossHairs(img, point):
    val = int(np.max(np.max(img)) / 4)
    img[int(point[0]),:] = val
    img[:,int(point[1])] = val

if __name__ == "__main__":
    print("Wrong file")