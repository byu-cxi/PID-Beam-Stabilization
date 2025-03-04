# Are cameras always numbered in the same order? If not, how?
# Maybe I should use the serial number instead?
# This file exists to help me answer these questions

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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*3*(height//bin)*(width//bin)))

import numpy as np
from scipy.ndimage import center_of_mass
import threading
first = True
img_caught = False
num_imgs_tot = 0
testing = []
def FrameHook(info, data):
    x = center_of_mass(np.array(data.contents))
    #print("shape is ", str(np.array(data.contents).shape))
    global first
    global num_imgs_tot
    global img_caught
    num_imgs_tot += 1
    img_caught = True
    if first:
        if (info.contents.CameraID == 1):
            return
        first = False
        from matplotlib import pyplot as plt
        from matplotlib.colors import Normalize
        img = np.flip(np.array(data.contents), 0)
        img = (img / np.max(np.max(img)))*255
        plt.imshow(img, norm=Normalize(vmin=0,vmax=255,clip=False))
        plt.title("cam_num = " + str(info.contents.CameraID))
        plt.show()


# ---------- Start camera running ----------

import contextlib

@contextlib.contextmanager
def CameraContext(cam_dll): # if adding more than 2 cams, need to add code to allow cam_num not only be 1 or 2
    num_device_connected = cam_dll.SSClassicUSB_InitDevice()
    if (num_device_connected == 0): # only done once
        raise Exception("No cameras found")

    for cam_num in range(1, num_device_connected+1):
        if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
            raise Exception("Camera didn't connect (might be invalid device number) -- cam_num=" + str(cam_num))

    if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
        raise Exception("Camera not in working set")

    global FUNC_PROTOTYPE
    cbhook = FUNC_PROTOTYPE(FrameHook)
    for cam_num in range(1, num_device_connected+1):
        if (cam_dll.SSClassicUSB_SetSensorFrequency(cam_num, 24) == -1): # can be 1, 24, 48, 96 (frame rate)
            raise Exception("Frequency setting failed -- cam_num=" + str(cam_num))
        # if (cam_dll.SSClassicUSB_SetCameraWorkMode(cam_num, 1) == -1): # 1 is trigger, 0 is normal
        #     raise Exception("Could not set work mode")
        res_response = cam_dll.SSClassicUSB_SetCustomizedResolution(cam_num, height, width, bin_choice, 0)
        if (res_response != 1):
            raise Exception("Resolution setting didn't work:", res_response)
        if (cam_dll.SSClassicUSB_SetExposureTime(cam_num, 4) == -1): # multiply the number by 50 um to get exposure time
            raise Exception("Exposure time setting failed")

    if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
        raise Exception("Frame hooker start failed")

    for cam_num in range(1, num_device_connected+1):
        if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
            raise Exception("Frame grabbing failed -- cam_num=" + str(cam_num))

    yield # This is where the loop is run: when the loop is ended, the rest of the function is run

    for cam_num in range(1, num_device_connected+1):
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
    time_delay = 2
    with CameraContext(cam_dll):
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