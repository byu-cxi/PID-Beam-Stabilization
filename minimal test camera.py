# This is the minimal amount of code to take an image in a Mightex camera using callback functions

import os
import time
import ctypes
from ctypes.wintypes import MSG
user32 = ctypes.windll.user32

libs = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
cam_dll = ctypes.CDLL(f'{libs}/dll_folder/Mightex/SSClassic_USBCamera_SDK.dll') # CDLL is a c-to-python converter, .dll is a function library


cam_num = 1 # one-indexed, references camera from the initDevice function
c_int = ctypes.c_int
height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)

# -----------------Callback things-----------------------

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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*1280*960))#(height*width//4)))

import numpy as np
from scipy.ndimage import center_of_mass
def FrameHook(info, data):
    print("center mass at", center_of_mass(np.array(data.contents)))


# ---------- Start camera running ----------
if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")

if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")

if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")

cbhook = FUNC_PROTOTYPE(FrameHook)
if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")

# if (cam_dll.SSClassicUSB_SetCameraWorkMode(cam_num, 0) == -1): # TODO choose normal vs trigger # 0 is normal (continuous stream of images), 1 is trigger mode
#     raise Exception("Setting work mode failed")

if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Frame grabbing failed")

import time
time.sleep(3)

# ---------- run loop! ----------
msg = MSG()
GM = user32.GetMessageA
TM = user32.TranslateMessage
DM = user32.DispatchMessageA
for i in range(3):
    GM(ctypes.pointer(msg), 0, 0, 0)
    TM(ctypes.pointer(msg))
    DM(ctypes.pointer(msg))
    time.sleep(.01)
    if i%50 == 0:
        print(i)

# ----------------- Shut down ---------------------
cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
cam_dll.SSClassicUSB_StopCameraEngine() # cannot access information in data_ptr after this command
cam_dll.SSClassicUSB_UnInitDevice()
