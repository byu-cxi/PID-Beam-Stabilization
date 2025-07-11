# This code is used to find constants in the vals.py file
# it moves the motor to find out how many steps of the motor move the beam center by one pixel
# It requires the vals.py and helper.py files
    # (Don't worry, it doesn't use the constants from vals.py that it's trying to find)
# Note: This does not move the motors back to their starting positions.
    # It is a good idea to move, then move again with negative steps to reset the motor location
    # This will also allow you to get 2 estimates for the calibration number.
cam_num = 2 # current setup: 1=upstream, 2=downstream
mot_num = 4 # current setup: 1=Y1, 2=X1, 3=Y2, 4=X2
num_steps = 100  # change this to positive or negative to reverse directions of motor movement

# If getting NaN as center of mass when running this file, maybe the thresholding in the callback function is too high

import time
import ctypes
from ctypes.wintypes import MSG
import numpy as np
from scipy.ndimage import center_of_mass
from matplotlib import pyplot as plt
from helper import * # helper.py in directory
from vals import *   # vals.py in directory
user32 = ctypes.windll.user32



cam_dll = ctypes.cdll.LoadLibrary(dll_path)
c_int = ctypes.c_int

baseline_center = (0,0) # will be set on the first image
baseline_not_set = True 
curr_img_center = (0,0)      # this is used to pass data from the callback function into the main code
images_received_counter = 0
images_processed_counter = 0
mass_center_tracker1 = []
mass_center_tracker2 = []
stored_start_end_imgs = []
save_img = True
scan_time = 35

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

FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*3*(height//binning)*(width//binning)))

def FrameHook(info, data):
    if info.contents.IsFrameBad:
        return
    #print("shape is : ", str(np.array(data.contents).shape))
    img = np.flip(np.array(data.contents)[:,:,0], 0)
    img[img < np.max(img)*.25] = 0 # set everything less than average to 0
    center_mass = center_of_mass(img)

    if False:
        plt.imshow(img)
        plt.title("image from framehook after processing, with max " + str(np.max(img)))
        plt.show()

    if np.isnan(center_mass).any(): # if there isn't any findable center of mass, stop the program
        print("No center of mass found: is the beam on the camera?")
        import os
        os._exit(1)
    global baseline_center
    global baseline_not_set
    global save_img
    global stored_start_end_imgs
    if baseline_not_set:
        baseline_not_set = False
        baseline_center = center_mass
    if save_img:
        save_img = False
        stored_start_end_imgs.append(img)
    
    global images_received_counter
    global curr_img_center
    images_received_counter += 1
    curr_img_center = center_mass
    return


# ---------- Start camera running ----------
if(cam_dll.SSClassicUSB_InitDevice() == 0):
    raise Exception("No cameras found")
if (cam_dll.SSClassicUSB_AddDeviceToWorkingSet(cam_num) == -1):
    raise Exception("Camera didn't connect (might be invalid device number)")
if (cam_dll.SSClassicUSB_StartCameraEngine(None, 8, 2, 0) == -1): # SWITCH for third argument, change based on number of cores (see manual pg. 7)
    raise Exception("Camera not in working set")
if (cam_dll.SSClassicUSB_SetSensorFrequency(cam_num, 24) == -1): # can be 1, 24, 48, 96 (frame rate)
    raise Exception("Frequency setting failed -- cam_num=" + str(cam_num))
res_response = cam_dll.SSClassicUSB_SetCustomizedResolution(cam_num, height, width, bin_choice, 0)
if (res_response != 1):
    raise Exception("Resolution setting didn't work:", res_response)
if (cam_dll.SSClassicUSB_SetExposureTime(cam_num, exposure_choice) == -1): # multiply the number by 50 um to get exposure time, max 15
    raise Exception("Exposure time setting failed")
if (cam_dll.SSClassicUSB_SetGains(cam_num,1,1,gain_choice) != 1): # gain is 2^((num-8)/8) : gain goes .125x -> 8x
    raise Exception("Gain setting failed")              # Despite what documentation says, third value (not first) is controlling one
cbhook = FUNC_PROTOTYPE(FrameHook)
if (cam_dll.SSClassicUSB_InstallFrameHooker(1, cbhook) == -1): # 1 is RAW, 2 is BMP
    raise Exception("Frame hooker start failed")
if (cam_dll.SSClassicUSB_StartFrameGrab(cam_num) == -1):
    raise Exception("Frame grabbing failed")



print("Starting initial measurement")

# ---------- Collect the locations for the initial location ----------

msg = MSG() # These three functions are neccessary to get data out of the callback function
GM = user32.GetMessageA
TM = user32.TranslateMessage
DM = user32.DispatchMessageA

t_end = time.time() + scan_time
while time.time() < t_end:
    GM(ctypes.pointer(msg), 0, 0, 0)
    TM(ctypes.pointer(msg))
    DM(ctypes.pointer(msg))

    if curr_img_center == (0,0): # (0,0) means that a new image hasn't been processed yet
        time.sleep(.01)
        continue

    mass_center_tracker1.append(list(curr_img_center))
    curr_img_center = (0,0)
    images_processed_counter += 1


temp = np.copy(stored_start_end_imgs)

# ---------- Get ready to get info from second location ----------
#average_x_y_initial = np.array(mass_center_tracker1).mean(axis=0) # This is without winsoring
average_x_y_initial = find_winsored_average(mass_center_tracker1)
print("initial location =", average_x_y_initial)

from pylablib.devices import Newport
with Newport.Picomotor8742() as nwpt:
    nwpt.move_by(mot_num, num_steps)
    nwpt.wait_move(axis=mot_num)
curr_img_center = (0,0)
time.sleep(1)

delay_var = True
# ---------- Find new average center -----------t_end = time.time() + 3
t_end = time.time() + scan_time
while time.time() < t_end:
    # These three functions are neccessary to get data out of the callback function
    GM(ctypes.pointer(msg), 0, 0, 0)
    TM(ctypes.pointer(msg))
    DM(ctypes.pointer(msg))

    if curr_img_center == (0,0): # (0,0) means that a new image hasn't been processed yet
        time.sleep(.01)
        continue

    mass_center_tracker2.append(list(curr_img_center))
    curr_img_center = (0,0)
    images_processed_counter += 1

    if delay_var:
        save_img = True
        delay_var = False

# ---------- Shut Down Camera ----------
cam_dll.SSClassicUSB_StopFrameGrab(cam_num)
cam_dll.SSClassicUSB_StopCameraEngine() # cannot access information in data_ptr after this command
cam_dll.SSClassicUSB_UnInitDevice()

# ---------- print required information ----------
#average_x_y_final = np.array(mass_center_tracker2).mean(axis=0) # this is without winsorizing
average_x_y_final = find_winsored_average(mass_center_tracker2)
print("average final =", average_x_y_final)

difference = average_x_y_final - average_x_y_initial
print("Cam_num is", cam_num)
print("Mot_num is", mot_num)
print("If X-axis shift, the calibration number is", (num_steps/difference[1]))
print("If Y-axis shift, the calibration number is", (num_steps/difference[0]))
print("Note: This number will likely be in the thousands if the motor did not move in that axis")
print("Put these numbers into the vals.py file")


if True:
    x_vals, y_vals = np.array(mass_center_tracker1).transpose()
    plt.plot(x_vals, y_vals, '-or')
    x_vals, y_vals = np.array(mass_center_tracker2).transpose()
    plt.plot(x_vals, y_vals, '-og')
    plt.title("Center of mass (Red=pre-move, Green=Post-move)")

if (len(stored_start_end_imgs) != 2):
    breakpoint()
    raise Exception("stored_start_end_imgs has " + str(len(stored_start_end_imgs)) + " elements instead of 2")
fig = plt.figure()

fig.add_subplot(1,2,1)
plt.imshow(np.log(np.log(stored_start_end_imgs[0]+1)+1))
plt.title("initial location")

fig.add_subplot(1,2,2)
plt.imshow(np.log(np.log(stored_start_end_imgs[1]+1)+1))
plt.title("final location")

plt.suptitle("Image before and after mirror move")
plt.show()