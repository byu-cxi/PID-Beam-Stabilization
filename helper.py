# file for functions that are important,
    # but not the main focus of the program

def TupleSubtract(tup1, tup2):
    return tuple(map(lambda i,j : i-j, tup1, tup2))

def TupleAdd(tup1, tup2):
    return tuple(map(lambda i,j : i+j, tup1, tup2))


import numpy as np

# modifies image to make it easy to see where the image center (or any other point) is
def AddCrossHairs(img, point):
    val = int(np.max(np.max(img)) / 4)
    img[int(point[0]),:] = val
    img[:,int(point[1])] = val
    return img


# This takes the error tracking information, and uses PI algorithm to determine where the beam should be shifted to
def PID(axis, error_tracker, n, scaler=1):
    final_elements = np.array(error_tracker).transpose()[axis, -n:] # array of n elements

    # look up Ziegler-Nichols method if these need to be changed  (https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=9013)
    P = scaler * .65        # adjust this until you see oscillations after move, then divide by 2
    I = scaler * .3 / n      # adjust this to reduce oscillations, and change n to somewhat large value
    D = scaler * 0           # Not going to include D because papers said that it wasn't necessary. Can be added in if you want
                                        # Just be careful of timing: changing the frame rate will require changing D
                                        # This makes sense: the motors stop when they are done moving, so the D shouldn't matter?

    P_contribution = - P * final_elements[n-1]
    I_contribution = - I * np.sum(final_elements)
    D_contribution = - D * (final_elements[n-1] - final_elements[n-2])

    return P_contribution + I_contribution + D_contribution




# print info about image collection efficiency
# It is possible that two images can be collected before the loop finishes, meaning one image center is overwritten
    # (Especially when the motor is moving large distances, or the frame rate is high)
# This function tells how often that happens
# images_received is the number of times the callback function got an image
# images_processed is the number of times the main loop was able to respond to one of those images
def PrintStats(images_received, images_processed, images_failed, images_dark, time_elapsed):
    print("Total images received -", images_received)
    print("Images where beam was blocked -", images_dark)
    print("Total images processed -", images_processed)
    if (images_received-images_dark != 0):
        print("Responded to", int(100*images_processed/(images_received-images_dark)), "% of collected (non-dark) images")
    print("Number of bad images -", images_failed)
    print("Stabilized beam for", time_elapsed, "seconds")
    print("On average,", images_processed/time_elapsed, "images processed / second")


import contextlib
import ctypes
import ctypes.wintypes
winmm = ctypes.windll.winmm

# used in SleepModifier context manager
class TIMECAPS(ctypes.Structure):
    _fields_ = (('wPeriodMin', ctypes.wintypes.UINT),
                ('wPeriodMax', ctypes.wintypes.UINT))

# This manager reduces the time that windows sleeps from around 15 ms to min_sleep seconds
# This allows us to waste less time sleeping in the loop, at the cost of higher computer power/cpu usage
@contextlib.contextmanager
def SleepModifier(min_sleep):
    caps = TIMECAPS()
    winmm.timeGetDevCaps(ctypes.byref(caps), ctypes.sizeof(caps))
    min_sleep = min(max(min_sleep, caps.wPeriodMin), caps.wPeriodMax)
    winmm.timeBeginPeriod(min_sleep)
    yield
    winmm.timeEndPeriod(min_sleep)

from scipy.stats.mstats import winsorize
def find_winsored_average(mass_center_tracker):
    mass_center_tracker = np.array(mass_center_tracker)
    average0 = np.array(winsorize(mass_center_tracker[:,0],limits=[.1,.1])).mean()
    average1 = np.array(winsorize(mass_center_tracker[:,1],limits=[.1,.1])).mean()
    average_x_y = np.array([average0, average1])

    return average_x_y



if __name__ == "__main__":
    print("Wrong file: this file stores functions that are useful in multiple programs")