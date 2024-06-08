# This is the main file that will be run to stabilize the beam
# You will need 2 other files for this code: vals.py and helper.property
    # Make sure you use the auto-calibration code to enter the correct values into vals.py
# In addition, you will need 2 .dll files for the Mightex Camera: SSClassic_USBCamera_SDK.dll and SSUsbLib.dll
# I arranged my files like this (dll_folder is in the same directory as this code)
    # dll_folder/
    # └── Mightex/
    #     ├── SSClassic_USBCamera_SDK.dll
    #     └── SSUsbLib.dll


import time
import ctypes
from ctypes.wintypes import MSG
import numpy as np
from scipy.ndimage import center_of_mass
from helper import * # helper.py in directory
from vals import *   # vals.py in directory
from pylablib.devices import Newport
user32 = ctypes.windll.user32


cam_dll = ctypes.cdll.LoadLibrary(dll_path)
cam_num = 1 # one-indexed, references camera from the initDevice function
c_int = ctypes.c_int

baseline_center = (0,0)     # will be set on the first image. This is the location the program tries to move toward
baseline_not_set = True 
curr_img_center = (0,0)     # this is the current location of the center-of-mass of the most recent image
                                # It is used to pass data from the callback function into the main code
n = 20                      # int > 1 - used to control how far back the Integral can see in the PID controller
images_received_counter = 0   # These 3 are for program tracking only, not for program functionality
images_processed_counter = 0
error_tracker = [[0.,0.]]*n


    

# -----------------Callback function & related-----------------------

# One of the two arguments to the callback function is in this shape
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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*(height//binning)*(width//binning)))

# This is the callback function for the camera (look up callback functions if you don't know what that means)
# It takes the data properties as info (in the shape of attributeMirror), and the image data as arguments
# It finds the center of mass of the image, and updates global variables with it
    # (Note: this is called from a different thread each time, so returning normally isn't possible as far as I know)
def FrameHook(info, data):
    img = np.flip(np.array(data.contents).reshape((width//binning, height//binning)), 0)
    img[img < (np.max(np.max(img))/10)] = 0 # set everything less than 10% max to 0
    center_mass = center_of_mass(img)
    if np.isnan(center_mass).any():
        print("No center of mass found: is the beam on the camera?")
        import os
        os._exit(1)
        
    global baseline_center
    global baseline_not_set
    if baseline_not_set:
        baseline_center = center_mass
        baseline_not_set = False
    
    global images_received_counter
    global curr_img_center
    images_received_counter += 1
    curr_img_center = center_mass


# ---------- Handle Ctrl-C events ----------

# Without this Ctrl-C handler, most of the time that you hit Ctrl-C, it will be while a function from
    # a .dll file is running. They were written in fortran, which has its own Ctrl-C handler, and it
    # throws some extremely uncatchable errors, meaning that it's impossible to run code after hitting Ctrl-C
    # (cleanup or plotting error) without using this chunk of code

CTRL_C_EVENT = 0
# CTRL_BREAK_EVENT = 1
# CTRL_CLOSE_EVENT = 2
# CTRL_LOGOFF_EVENT = 5
# CTRL_SHUTDOWN_EVENT = 6
def Ctrl_C_Handler(err_type):
    if err_type is CTRL_C_EVENT:
        print("Ctrl-C event detected")
        global continue_loop
        continue_loop = False
        return True

_HandlerRoutine = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.DWORD)
_ctrl_c_handler = _HandlerRoutine(Ctrl_C_Handler)

if not ctypes.windll.kernel32.SetConsoleCtrlHandler(_ctrl_c_handler):
    raise ctypes.WinError(ctypes.get_last_error())




# ---------- Start camera running ----------

# To find the documentation for these functions go to:
    # https://www.mightexsystems.com/product/usb3-0-monochrome-or-color-5mp-cmos-camera-8-or-12-bit/
# Download the .zip file from the Downloads section toward the bottom
# Go to SDK/Documents, and there's a pdf with information on all of this
    # It's named:   Mightex Super Speed USB Camera (SM-Series) SDK Manual

if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")

if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")

if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")

if (cam_dll.SSClassicUSB_SetSensorFrequency(cam_num, 24) == -1):
    raise Exception("Frequency setting failed")

if (cam_dll.SSClassicUSB_SetCustomizedResolution(cam_num, height, width, bin_choice, 0) != 1):
    raise Exception("Resolution setting didn't work:", res_response)

cbhook = FUNC_PROTOTYPE(FrameHook)
if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")

if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Frame grabbing failed")



# ---------- run loop! ----------

# Starts the context managers for the motors and the sleep modifier
# Then runs loop checking to see if the camera has sent an image back yet
    # If so, it moves the motors (if the move is big enough)

# These three functions are neccessary to get data out of the callback function
msg = MSG()
GM = user32.GetMessageA
TM = user32.TranslateMessage
DM = user32.DispatchMessageA

i = 0
time_steps = []
print("Starting stabilization loop now (Ctrl-C to stop)")
continue_loop = True # will be set to false on ctrl-c
sleep_time = .005
with Newport.Picomotor8742() as nwpt, SleepModifier(sleep_time):
    while continue_loop:
        i += 1
        # These three functions are neccessary to get data out of the callback function
        GM(ctypes.pointer(msg), 0, 0, 0)
        TM(ctypes.pointer(msg))
        DM(ctypes.pointer(msg))

        if curr_img_center == (0,0): # (0,0) means that a new image hasn't been processed yet
            time.sleep(sleep_time)
            continue
        elif (np.isnan(curr_img_center[0]) or np.isnan(curr_img_center[1])): # center of mass gives NaN when given array of 0's
            raise Exception("No signal detected: is the beam on the camera?")

        y_err, x_err = TupleSubtract(curr_img_center, baseline_center) # caluclate error in pixels
        curr_img_center = (0,0)
        images_processed_counter += 1
        error_tracker.append([y_err, x_err])

        y_pixel_shift = PID(0, error_tracker, n) # 0 for Y, 1 for X
        x_pixel_shift = PID(1, error_tracker, n)

        y_step_num = int(y_pixel_shift * y_pixel_to_motorstep_conversion) # calculate how many motor steps will
        x_step_num = int(x_pixel_shift * x_pixel_to_motorstep_conversion) # move the beam by that amount of pixels

        # Note: in the docs, "device" refers to the controller board, not the motor
        min_move = 2
        if abs(y_step_num) >= min_move:
            nwpt.move_by(1, y_step_num) # 1 for Y, 2 for X
            while (nwpt.is_moving(axis=1)):     # yes I could use the nwpt.wait_move() function
                time.sleep(sleep_time)              # but in the pylablib source code it does exactly this 
        if abs(x_step_num) >= min_move:             # sequence, except sleeps for .01 instead of .001 seconds
            nwpt.move_by(2, x_step_num)             # and the higher precision can't hurt
            while (nwpt.is_moving(axis=2)):
                time.sleep(sleep_time)

        time_steps.append(time.time())



# ----------------- Shut down camera ---------------------

cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
cam_dll.SSClassicUSB_StopCameraEngine()
cam_dll.SSClassicUSB_UnInitDevice()


PrintStats(images_received_counter, images_processed_counter)

# plot error over time
if True:
    from matplotlib import pyplot as plt
    from math import sqrt
    x_vals, y_vals = np.array(error_tracker)[n:].transpose()
    tot_err = [sqrt(x**2 + y**2) for x,y in error_tracker[n:]]
    plt.plot(time_steps, y_vals, '-.b')
    plt.plot(time_steps, x_vals, '-.r')
    plt.plot(time_steps, tot_err, '-*', color="black")

    plt.title("Error over time (x is blue, y is red, total is black)")
    plt.show()

