# PSEUDOCODE
    # while true:
        # If callback function has gotten new center?
            # should update as fast as it can
        # find center of mass error
            # find current center
            # subtract that from the baseline
        # find how much to move center of image
            # PID controller
        # move motor to new location
            # convert pixels to needed mirror movement (should be constant)
        # store relevant data for improvement

from pylablib.devices import Newport
from scipy.ndimage import center_of_mass
from matplotlib import pyplot as plt
import ctypes
import numpy as np
import time
import os

from helper import *

# ---------- important constants ----------

motor_port = 1
height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)
cam_num = 1 # one-indexed, references camera from the initDevice function
c_short = ctypes.c_uint16
c_int = ctypes.c_int
threshold = 100
temp_center = (0,0)
error_log = [(0.,0.),(0.,0.),(0.,0.),(0.,0.),(0.,0.)]

dll_path = "C:\\Users\\hct10\\Documents\\Classes\\CURRENT\\Sandberg Research\\Code\\Senior Project\\dll_folder\Mightex\\SSClassic_USBCamera_SDK.dll"
cam_dll = ctypes.cdll.LoadLibrary(dll_path)

# ---------- Essential functions ----------

def TakeImage(): # returns numpy array
    data_ptr = (c_short * img_size)()
    data_ptr = cam_dll.SSClassicUSB_GetCurrentFrame(0, 1, data_ptr)
    if (data_ptr == 0):
        raise Exception("Frame collecting failed")
   
    img = np.array(data_ptr[metadata_size:img_size//4], dtype=c_int) # breaking here?
    img = np.trim_zeros(img) # remove zeros from end
    img = np.pad(img, (0,(width//2)*(height//2)-img.shape[0]), 'median') # in case the last few numbers from the camera were 0
    img = img.reshape((width//2, height//2))
    return np.flip(img,0)

def FindCurrentCenterMass(img):
    img[img<threshold] = 0
    return center_of_mass(img)

def CalculateHowMuchToMove(current_error):
    P = .7
    # I = 
    # D = 
    print("TODO implement PID")
    return tuple(x*P for x in current_error)

def CalculateMirrorMovement(beam_shift):
    print("TODO calculate constant")
    return tuple(x/1000 for x in beam_shift)





# ---------- Camera Setup ----------

class attributeMirror(ctypes.Structure): # this class is needed in order to get the info from the TProcessedDataProperty struct
    _fields_ = [( "CameraID", c_int ),
                ( "WorkMode", c_int),
                ( "SensorClock", c_int),
                ( "Row", c_int ),
                ( "Column", c_int ),
                ( "Bin", c_int ),
                ( "BinMode", c_int),
                ( "CameraBit", c_int),
                ( "XStart", c_int ),
                ( "YStart", c_int ),
                ( "ExposureTime", c_int ),
                ( "RedGain", c_int ),
                ( "GreenGain", c_int ),
                ( "BlueGain", c_int ),
                ( "TimeStamp", c_int ),
                ( "SensorMode", c_int),
                ( "TriggerOccurred", c_int ),
                ( "TriggerEventCount", c_int ),
                ( "FrameSequenceNo", c_int ),
                ( "IsFrameBad", c_int ),
                ( "FrameProcessType", c_int ),
                ( "FilterAcceptForFile", c_int ) ]
def FrameHook(info, data):
    arr = np.array(data.contents)
    plt.imshow(arr)
    plt.show()
    print(arr.shape)
    global temp_center
    temp_center = FindCurrentCenterMass(arr)
FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*1280*960))#(height*width//4)))
cbhook = FUNC_PROTOTYPE(FrameHook)

if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")
if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")
if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")
if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")
if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Frame grabbing failed")

# print("waiting to get baseline")
# while temp_center == (0,0):
#     time.sleep(.01)
# baseline_center = temp_center # wherever the beam is when the program turns on is the official center
# temp_center = (0,0)
# print("image center baseline is at", baseline_center)

# ---------- run loop ----------
#with Newport.Picomotor8742() as nwpt:
    #while true:
time.sleep(1)
t_end = time.time() + 2
while time.time() < t_end:
#    img = TakeImage()

    if (temp_center == (0,0)):
        time.sleep(.01)
        continue
    if True:
        AddCrossHairs(img,baseline_center)
        plt.imshow(img)
        plt.show()
    error = TupleSubtract(baseline_center, temp_center)
    beam_shift = CalculateHowMuchToMove(error)
    mirror_shift = CalculateMirrorMovement(beam_shift)
    error_log.append(error)




if False: # show plot of errors over the course of the loop
    x_val, y_val = np.array(error_log).transpose()
    plt.plot(x_val, y_val, '-o')
    plt.show()

print("Program finished")
print("center is ", temp_center)