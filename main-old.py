import sys
import os
import inspect
import clr
import numpy as np
import ctypes
from matplotlib import pyplot as plt



strCurrFile = os.path.abspath (inspect.stack()[0][1])
strPathDllFolder = os.path.join(os.path.dirname(strCurrFile), "dll_folder\\Newport")

from pylablib.devices import Newport
print("num devices =", Newport.get_usb_devices_number_picomotor())
nwpt = Newport.Picomotor8742()
print("available axes =", nwpt.get_all_axes())

# Add the DLL folder path to the system search path (before adding references)
sys.path.append (strPathDllFolder)

# Add a reference to .NET assembly required (in dll folder)
clr.AddReference ("UsbDllWrap")
# Import a class from a namespace
from Newport.USBComm import *
from System.Text import StringBuilder
from System.Collections import Hashtable
from System.Collections import IDictionaryEnumerator


# Call the class constructor to create an object
oUSB = USB (True)

# Discover all connected devices
bStatus = oUSB.OpenDevices (0, True)


#"""
height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)

libs = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/dll_folder'
cam_dll = ctypes.CDLL(f'{libs}/Mightex/SSClassic_USBCamera_SDK.dll') # CDLL is a c-to-python converter, .dll is a function library

cam_num = 1 # one-indexed, references camera from the initDevice function

c_short = ctypes.c_uint16
c_int = ctypes.c_int

if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")

if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")

if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 4, 1) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")

if (cam_dll.SSClassicUSB_SetUSBConnectMonitor(cam_num, 1) < 0): # makes sure camera doesn't turn off
    raise Exception("USB Watchdog function failed")

if (cam_dll.SSClassicUSB_SetCameraWorkMode(cam_num, 1) == -1): # TODO choose normal vs trigger # 0 is normal (continuous stream of images), 1 is trigger mode
    raise Exception("Setting work mode failed")

if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num, 0x8888) == -1): # second argument should be 0x8888 for infinite frames
    raise Exception("Frame grabbing failed")




# c_int = ctypes.c_int
# cam_dll is SSClassic_USBCamera_SDK.dll


class attributeMirror(ctypes.Structure): # this class is needed in order to get the info from the TProcessedDataProperty struct
    _fields_ = [('CameraID', c_int),
                ('WorkMode', c_int),
                ('SensorClock', c_int),
                ('Row', c_int),
                ('Column', c_int),
                ('Bin', c_int),
                ('BinMode', c_int),
                ('CameraBit', c_int),
                ('XStart', c_int),
                ('YStart', c_int),
                ('ExposureTime', c_int),
                ('RedGain', c_int),
                ('GreenGain', c_int),
                ('BlueGain', c_int),
                ('TimeStamp', c_int),
                ('SensorMode', c_int),
                ('TriggerOccurred', c_int),
                ('TriggerEventCount', c_int),
                ('FrameSequenceNo', c_int),
                ('IsFrameBad', c_int),
                ('FrameProcessType', c_int),
                ('FilterAcceptForFile', c_int)]
# contains list of c_ints like CameraID, WorkMode, that are neccessary information

def FrameHook(attributes, img_pointer):   
    print("TODO get img -- Callback succeeded!")

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*(height*width)))

cam_dll.SSClassicUSB_InstallFrameHooker.argtypes = [c_int, FUNC_PROTOTYPE]
if (cam_dll.SSClassicUSB_InstallFrameHooker(0, FUNC_PROTOTYPE(FrameHook)) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")





if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Camera trigger failed")
# if (cam_dll.SSClassicUSB_SoftTrigger(cam_num) == -1):
#     raise Exception("Camera trigger failed")


if False:
    cam_dll.SSClassicUSB_GetCurrentFrame16bit.argtypes = [c_int, c_int, ctypes.POINTER(c_short)] # set arg types
    cam_dll.SSClassicUSB_GetCurrentFrame16bit.restype = ctypes.POINTER(c_short)
    data_ptr = (c_short * img_size)()
    data_ptr = cam_dll.SSClassicUSB_GetCurrentFrame16bit(0, 1, data_ptr)

    # "_type_ must have storage info" means that I'm trying to get a pointer to a python object, when it should be to a ctypes object

    if (data_ptr == None):
        raise Exception("Frame collecting failed")

    temp = np.array(data_ptr[metadata_size:img_size], dtype=ctypes.c_uint16) # breaking here?
    temp = np.trim_zeros(temp) # remove zeros from end
    temp = np.pad(temp, (0,(width//2)*(height//2)-temp.shape[0]), 'median') # in case the last few numbers from the camera were 0

    #print("data has length", temp.shape) # TODO this is 1/4 the total length expected: is it binning? something else?

    # add .contents after data_ptr? 
    #data = np.array(data_ptr[metadata_size:img_size]).reshape((width, height)) # remove metadata, and reshape # TODO replace
    data = temp.reshape((width//2, height//2))
    print("max value is", str(np.max(np.max(data)))+",", "min is", np.min(np.min(data)))
    plt.imshow(data)
    if np.max(np.max(np.abs(data))) != 0:
        plt.show()


#with Newport.Picomotor8742() as motor:
#    motor.move_by(100)


cam_dll.SSClassicUSB_SetUSBConnectMonitor(cam_num, 0)
cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
cam_dll.SSClassicUSB_StopCameraEngine() # cannot access information in data_ptr after this command
cam_dll.SSClassicUSB_UnInitDevice()


#"""
# Shut down all communication
oUSB.CloseDevices ()
print ("Devices Closed.\n")
