# This is the main file that will be run to stabilize the beam

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

baseline_center = (0,0)     # will be set on the first image
baseline_not_set = True 
curr_img_center = (0,0)     # this is used to pass data from the callback function into the main code
images_received_counter = 0
images_processed_counter = 0
n = 20                      # int > 1 - used to control how far back the Integral can see in the PID controller
error_tracker = [[0.,0.]]*n

    

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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*(height//binning)*(width//binning)))

def FrameHook(info, data):
    # To whoever is trying to improve this code:
    # I'm sorry
    # (Unless that person is me - if so, you deserve this)
    img = np.flip(np.array(data.contents).reshape((width//binning, height//binning)), 0)
    img[img < (np.max(np.max(img))/10)] = 0 # set everything less than 10% max to 0
    center_mass = center_of_mass(img)
    global baseline_center
    global baseline_not_set
    if baseline_not_set:
        baseline_center = center_mass
        baseline_not_set = False
    
    global images_received_counter
    global curr_img_center
    images_received_counter += 1
    curr_img_center = center_mass


def PID(axis, error_tracker):
    global n
    final_elements = np.array(error_tracker).transpose()[axis, -n:] # array of n elements

    P = .65         # adjust this until you see oscillations after move, then divide by 2
    I = .3 / n      # adjust this to reduce oscillations, and change n to somewhat large value
    D = 0           # Not going to include D because A) papers said that it wasn't necessary, and
                                                #    B) Don't have a reliable way to track timing

    P_contribution = - P * final_elements[n-1]
    I_contribution = - I * np.sum(final_elements)
    D_contribution = - D * (final_elements[n-1] - final_elements[n-2])

    return P_contribution + I_contribution + D_contribution

# print info about image collection efficiency
def PrintStats():
    global images_received_counter
    global images_processed_counter
    print("Total images received -", images_received_counter)
    print("Total images processed -", images_processed_counter)
    print("Responded to", int(100*images_processed_counter/images_received_counter), "% of collected images")


# ---------- Handle Ctrl-C events ----------
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
if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")

if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")

if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")

if (cam_dll.SSClassicUSB_SetCustomizedResolution(cam_num, height, width, bin_choice, 0) != 1):
    raise Exception("Resolution setting didn't work:", res_response)

cbhook = FUNC_PROTOTYPE(FrameHook)
if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")

if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Frame grabbing failed")



# ---------- run loop! ----------
msg = MSG()
GM = user32.GetMessageA
TM = user32.TranslateMessage
DM = user32.DispatchMessageA

i = 0
time_steps = []
print("Starting stabilization loop now")
continue_loop = True # will be set to false on ctrl-c
with Newport.Picomotor8742() as nwpt:
    while continue_loop:
        i += 1
        # These three functions are neccessary to get data out of the callback function
        GM(ctypes.pointer(msg), 0, 0, 0)
        TM(ctypes.pointer(msg))
        DM(ctypes.pointer(msg))

        if curr_img_center == (0,0): # (0,0) means that a new image hasn't been processed yet
            time.sleep(.01)
            continue
        elif (np.isnan(curr_img_center[0]) or np.isnan(curr_img_center[1])): # center of mass gives NaN when given array of 0's
            raise Exception("No signal detected: is the beam on the camera?")

        y_err, x_err = TupleSubtract(curr_img_center, baseline_center)
        curr_img_center = (0,0)
        images_processed_counter += 1
        error_tracker.append([y_err, x_err])

        y_pixel_shift = PID(0, error_tracker) # 0 for Y, 1 for X
        x_pixel_shift = PID(1, error_tracker)

        y_step_num = int(y_pixel_shift * y_pixel_to_motorstep_conversion)
        x_step_num = int(x_pixel_shift * x_pixel_to_motorstep_conversion)

        # Note: I guess in the docs, "device" refers to the controller board, not the motor
        if abs(y_step_num) > 1:
            nwpt.move_by(1, y_step_num) # 1 for Y, 2 for X
            while (nwpt.is_moving(axis=1)): # yes I could use the nwpt.wait_move() function
                time.sleep(.001)            # but in the pylablib source code it does exactly this
        if abs(x_step_num) > 1:             # sequence, except sleeps for .01 instead of .001 seconds
            nwpt.move_by(2, x_step_num)     # and the higher precision can't hurt
            while (nwpt.is_moving(axis=2)):
                time.sleep(.001)

        time_steps.append(time.time())



# ----------------- Shut down ---------------------

cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
cam_dll.SSClassicUSB_StopCameraEngine() # cannot access information in data_ptr after this command
cam_dll.SSClassicUSB_UnInitDevice()


PrintStats()

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

