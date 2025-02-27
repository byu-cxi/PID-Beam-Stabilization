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
bin_choice = 0
bin = 2**bin_choice
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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*(height//bin)*(width//bin)))

import numpy as np
from scipy.ndimage import center_of_mass
import threading
first = True
img_caught = False
num_imgs_tot = 0
testing = []
def FrameHook(info, data):
    print("shape is : ", str(np.array(data.contents).shape))
    x = center_of_mass(np.array(data.contents))
    t = threading.active_count()
    print("center mass at", x, "(Num threads:", t, ")")
    #print("shape is ", str(np.array(data.contents).shape))
    #time.sleep(1)
    global first
    global num_imgs_tot
    global img_caught
    num_imgs_tot += 1
    img_caught = True
    if first:
        first = False
        from matplotlib import pyplot as plt
        img = np.flip(np.array(data.contents), 0)
        plt.imshow(img)
        plt.show()


# ---------- Start camera running ----------

import contextlib

@contextlib.contextmanager
def CameraContext(cam_num, cam_dll):
    if(cam_dll.SSClassicUSB_InitDevice() == 0):
        raise Exception("No cameras found")
    if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
        raise Exception("Camera didn't connect (might be invalid device number)")
    if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
        raise Exception("Camera not in working set")
    if (cam_dll.SSClassicUSB_SetSensorFrequency(cam_num, 24) == -1):
        raise Exception("Frequency setting failed")
    res_response = cam_dll.SSClassicUSB_SetCustomizedResolution(cam_num, height, width, bin_choice, 0)
    if (res_response != 1):
        raise Exception("Resolution setting didn't work:", res_response)
    if (cam_dll.SSClassicUSB_SetExposureTime(cam_num, 4) == -1): # multiply the number by 50 um to get exposure time
        raise Exception("Exposure time setting failed")

    global FUNC_PROTOTYPE
    cbhook = FUNC_PROTOTYPE(FrameHook)

    if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
        raise Exception("Frame hooker start failed")
    if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
        raise Exception("Frame grabbing failed")

    yield # This is where the loop is run: when the loop is ended, the rest of the function is run

    cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
    cam_dll.SSClassicUSB_StopCameraEngine()
    cam_dll.SSClassicUSB_UnInitDevice()

import time

# ---------- run loop! ----------
def main():
    msg = MSG()
    GM = user32.GetMessageA
    TM = user32.TranslateMessage
    DM = user32.DispatchMessageA
    imgs_caught_counter = 0
    time_delay = 1
    with CameraContext(cam_num, cam_dll):
        t = time.time() + time_delay
        while time.time() < t:
            #print("num threads:", threading.active_count())
            GM(ctypes.pointer(msg), 0, 0, 0)
            TM(ctypes.pointer(msg))
            DM(ctypes.pointer(msg))
            print("here")
            global img_caught
            if img_caught:
                imgs_caught_counter += 1
                img_caught = False
            time.sleep(.01)


    print("total imgs =", num_imgs_tot)
    print("caught imgs =", imgs_caught_counter)
    print("imgs/sec", num_imgs_tot / time_delay)
    # ----------------- Shut down ---------------------
    cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
    cam_dll.SSClassicUSB_StopCameraEngine() # cannot access information in data_ptr after this command
    cam_dll.SSClassicUSB_UnInitDevice()



#from line_profiler import LineProfiler # LineProfiler helps find where the program is spending its time

if __name__ == "__main__":
    main()
    # lp = LineProfiler()
    # lp.add_function(FrameHook)
    # lp_wrapper = lp(main)
    # lp_wrapper()
    # lp.print_stats()