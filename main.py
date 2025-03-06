# This is the main file that will be run to stabilize the beam
# You will need 2 other files for this code: vals.py and helper.property
    # Make sure you use the auto-calibration code to enter the correct values into vals.py
# In addition, you will need 2 .dll files for the Mightex Camera: SSClassic_USBCamera_SDK.dll and SSUsbLib.dll
# I arranged my files like this (dll_folder is in the same directory as this code)
    # dll_folder/
    # └── Mightex/
    #     ├── SSClassic_USBCamera_SDK.dll
    #     └── SSUsbLib.dll

# When moving to new system, what to do to get it set up:
    # Change thresholding in FrameHook to properly get rid of background noise
    # Update functions in CameraContext
    # Run auto-calibration to get vals.py variables updated
    # Determine whether the PID variables need to be updated?

import time
import ctypes
from ctypes.wintypes import MSG
import numpy as np
from scipy.ndimage import center_of_mass
from helper import * # helper.py in directory
from vals import *   # vals.py in directory
from pylablib.devices import Newport
from matplotlib import pyplot as plt
user32 = ctypes.windll.user32


cam_dll = ctypes.cdll.LoadLibrary(dll_path)
c_int = ctypes.c_int

baseline_center_1 = (0,0)     # will be set on the first image. This is the location the program tries to move toward
baseline_center_2 = (0,0)
baseline_not_set_1 = True
baseline_not_set_2 = True
curr_img_center_1 = (0,0)   # this is the current location of the center-of-mass of the most recent image
curr_img_center_2 = (0,0)   # It is used to pass data from the callback function into the main code

n = 20                      # int > 1 - used to control how many time steps back the Integral can see in the PID controller

images_received_counter = 0   # These are for program tracking only, not for program functionality
images_processed_counter = 0
images_failed_counter = 0  # number of frames that admitted that they were bad
images_dark_counter = 0

error_tracker_1 = [[0.,0.]]*n     # used to keep track of error over time. Initialized with extra zeros for PID reasons
error_tracker_2 = [[0.,0.]]*n

which_camera_to_take_image_from_next = 1 # This allows us to alternate cameras


    

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

# This has 3x the size of monochrome, but I only need the red array. Need to get all three though or nothing comes through
FUNC_PROTOTYPE = ctypes.CFUNCTYPE(None, ctypes.POINTER(attributeMirror), ctypes.POINTER(ctypes.c_ubyte*3*(height//binning)*(width//binning)))










# This is the callback function for the camera (look up callback functions if you don't know what that means)
# It takes the data properties as info (in the shape of attributeMirror), and the image data as arguments
# It finds the center of mass of the image, and updates global variables with it
    # (Note: this is called from a different thread each time, so returning normally isn't possible as far as I know)
        # return will only stop the thread. To get data out of this function, I'm using global variables
def FrameHook(info, data):
        # Variables that should be different depending on what camera it's coming from
            # baseline_center
            # curr_img_center
            # baseline_not_set
    cam_num = info.contents.CameraID # This is 1 or 2

    global images_received_counter
    images_received_counter += 1

    if info.contents.IsFrameBad:
        global images_failed_counter
        images_failed_counter += 1
        print("Received bad image")
        #plt.imshow(np.flip(np.array(data.contents)[:,:,0], 0))
        #plt.show()
        return #This is where I filter out the half-image problem, or other failed images

    img = np.flip(np.array(data.contents)[:,:,0], 0)
    #del data # delete data to free space
    #max = np.max(np.max(img))
    img[img < np.average(img)*1.0] = 0 # set everything less than 100% average to 0
    center_mass = center_of_mass(img)

    if np.isnan(center_mass).any(): # If so, then the entire image is below 50% max (aka it's all zeros, or something else weird)
        print("No center of mass found: is something wrong with the camera?")
        if False: # debugging code - saves image to file
            from PIL import Image
            im = Image.fromarray(img)
            im.save("image that failed to find center.jpeg")
            print("Saved bad image to image file in home directory")
        return

    rad = 25 # radius to look around center of mass at in pixels
             # (For very small beams, may need to reduce this, at cost of greater chance of error)
    beam_region = img[int(center_mass[0])-rad:int(center_mass[0])+rad, int(center_mass[1])-rad:int(center_mass[1])+rad]
    if False: # For debugging
        plt.imshow(AddCrossHairs(img, (rad,rad)))
        plt.show()
    bitmap = np.where(beam_region > 0, 1, 0) # 1 for pixels not thresholded, 0 for pixels that were

    if np.average(np.average(bitmap)) < .7: # if less than 70% the pixels in region are not thresholded, no beam on image
        print("dark frame")
        global images_dark_counter
        images_dark_counter += 1
        return # This means that the center of mass isn't surrounded by bright pixels
                # which probably means the shutter is on. If so, shouldn't do anything for now
    
    # ----- From here on, we assume that the image is a good one (has beam, no errors) -----

    # These will save the center of mass if this is the first image taken in 
    global baseline_center_1
    global baseline_center_2
    global baseline_not_set_1
    global baseline_not_set_2
    if baseline_not_set_1 and (cam_num == 1):
        baseline_center_1 = center_mass
        baseline_not_set_1 = False
    if baseline_not_set_2 and (cam_num == 2):
        baseline_center_2 = center_mass
        baseline_not_set_2 = False
    
    if (cam_num == 1):
        global curr_img_center_1
        curr_img_center_1 = center_mass
    if (cam_num == 2):
        global curr_img_center_2
        curr_img_center_2 = center_mass











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

import contextlib
@contextlib.contextmanager
def CameraContext(cam_dll): # if adding more than 2 cams, need to add code to allow cam_num not only be 1 or 2
    num_device_connected = cam_dll.SSClassicUSB_InitDevice()
    if (num_device_connected == 0): # only done once
        raise Exception("No cameras found")
    if (num_device_connected != 2):
        raise Exception("Cannot find two cameras! Are both connected?")

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




if __name__ == "__main__":
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
    time_elapsed = 0
    time_steps_1 = []
    time_steps_2 = []
    print("Starting stabilization loop now (Ctrl-C to stop)")
    continue_loop = True # will be set to false on ctrl-c
    sleep_time = .010 # can shrink this down to .001 seconds, but this should be plenty: The smaller this is, the more energy the computer uses
    with SleepModifier(sleep_time), CameraContext(cam_dll), Newport.Picomotor8742() as nwpt: # TODO replace
        t_start = time.time()
        while continue_loop: # ctrl+c will make this false
            i += 1
            # These three functions are neccessary to get data out of the callback function
            GM(ctypes.pointer(msg), 0, 0, 0)
            TM(ctypes.pointer(msg))
            DM(ctypes.pointer(msg))

            if (np.isnan(curr_img_center_1[0]) or np.isnan(curr_img_center_1[1]) 
                or np.isnan(curr_img_center_2[0]) or np.isnan(curr_img_center_2[1])): # center of mass gives NaN when given array of 0's
                raise Exception("No signal detected: is the beam on the camera?")


            y_step_num1 = 0
            x_step_num1 = 0
            y_step_num2 = 0
            x_step_num2 = 0

            if (which_camera_to_take_image_from_next == 1) and (curr_img_center_1 != (0,0)):        # image taken from camera 1
                y_err, x_err = TupleSubtract(curr_img_center_1, baseline_center_1) # caluclate error in pixels
                images_processed_counter += 1
                error_tracker_1.append([y_err, x_err])
                time_steps_1.append(time.time())

                y_pixel_shift_1 = PID(0, error_tracker_1, n) # 0 for Y, 1 for X     # PID function in helper.py
                x_pixel_shift_1 = PID(1, error_tracker_1, n) # tells how many pixels to shift by

                # calculate how many motor steps will move the beam by that amount of pixels
                y_step_num1 = int(y_pixel_shift_1 * y_cam1_pix_to_motor1_conversion) # y move on mirror 1
                x_step_num1 = int(x_pixel_shift_1 * x_cam1_pix_to_motor2_conversion)

                which_camera_to_take_image_from_next = 2 # flip flop

            elif (which_camera_to_take_image_from_next == 2) and (curr_img_center_2 != (0,0)):      # image taken from camera 2
                y_err, x_err = TupleSubtract(curr_img_center_2, baseline_center_2) # caluclate error in pixels
                images_processed_counter += 1
                error_tracker_2.append([y_err, x_err])
                time_steps_2.append(time.time())

                y_pixel_shift_2 = PID(0, error_tracker_2, n, scaler=.3) # 0 for Y, 1 for X     # PID function in helper.py
                x_pixel_shift_2 = PID(1, error_tracker_2, n, scaler=.3) # tells how many pixels to shift by

                # calculate how many motor steps will move the beam by that amount of pixels
                y_step_num2 = int(y_pixel_shift_2 * y_cam2_pix_to_motor3_conversion) # etc.
                x_step_num2 = int(x_pixel_shift_2 * x_cam2_pix_to_motor4_conversion)

                which_camera_to_take_image_from_next = 1 # flip flop
            
            else:
                time.sleep(sleep_time)
                continue


            # Note: in the docs, "device" refers to the controller board, not the motor
            # 1 is upstream, 2 is downstream
            min_move = 2

            y1_axis = 1
            x1_axis = 2
            y2_axis = 3
            x2_axis = 4

            if abs(y_step_num1) >= min_move:
                nwpt.move_by(y1_axis, y_step_num1) # 1 for Y, 2 for X
                while (nwpt.is_moving(axis=y1_axis)):     # yes I could use the nwpt.wait_move() function
                    time.sleep(sleep_time)              # but in the pylablib source code it does exactly this 
            if abs(x_step_num1) >= min_move:             # sequence, except sleeps for .01 instead of .001 seconds
                nwpt.move_by(x1_axis, x_step_num1)             # and the higher precision can't hurt
                while (nwpt.is_moving(axis=x1_axis)):
                    time.sleep(sleep_time)
            if abs(y_step_num2) >= min_move:
                nwpt.move_by(y2_axis, y_step_num2)
                while (nwpt.is_moving(axis=y2_axis)):
                    time.sleep(sleep_time)
            if abs(x_step_num2) >= min_move:
                nwpt.move_by(x2_axis, x_step_num2)
                while (nwpt.is_moving(axis=x2_axis)):
                    time.sleep(sleep_time)
        
        time_elapsed = time.time() - t_start
        curr_img_center_1 = (0,0) # now that we've moved the motor, we should retake any images stored
        curr_img_center_2 = (0,0)


    # ----------------- Shut down camera ---------------------


    PrintStats(images_received_counter, images_processed_counter, images_failed_counter, images_dark_counter, time_elapsed)

    # plot error over time for camera 1: x, y, and total
    if False:
        from math import sqrt
        error_tracker = error_tracker_1 # Looking at camera 1
        time_steps = time_steps_1
        y_vals, x_vals = np.array(error_tracker)[n:].transpose() # TODO save this data so I can look at it later
        tot_err = [sqrt(x**2 + y**2) for x,y in error_tracker[n:]]
        plt.plot(time_steps, y_vals, '-.b')
        plt.plot(time_steps, x_vals, '-.r')
        plt.plot(time_steps, tot_err, '-*', color="black")

        plt.title("cam1 -- Error over time (x is blue, y is red, total is black)")
        plt.show()

    # plot total error for both cameras, and save all error data to csv
    if True:
        from math import sqrt
        import csv 
        import datetime
        import os

        if (len(error_tracker_1) > len(error_tracker_2)): # camera 1 goes before camera 2, so sometimes it has one more image than 2
            error_tracker_2.append(error_tracker_2[-1])
            try:
                time_steps_2.append(time_steps_2[-1])
            except:
                print("length of cam 2 images is " + str(len(time_steps_2)))
                print("length of cam 1 images is " + str(len(time_steps_1)))
                raise Exception("camera two never took images")

        y_vals1, x_vals1 = np.array(error_tracker_1)[n:].transpose()
        y_vals2, x_vals2 = np.array(error_tracker_2)[n:].transpose()
        tot_err1 = [sqrt(x**2 + y**2) for x,y in error_tracker_1[n:]] # first n are initialized with zeros
        tot_err2 = [sqrt(x**2 + y**2) for x,y in error_tracker_2[n:]]

        # --- Save the error data! I want to make figures from this later! ---
        csv_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' 2_cam_stabilization.csv'
        with open(os.path.join(os.getcwd(),'CSV',csv_name), 'w', newline="") as f:
            writer = csv.writer(f)
            names = [["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]]

            writer.writerows(names)
            writer.writerows(np.transpose([time_steps_1,y_vals1,x_vals1,tot_err1, time_steps_2,y_vals2,x_vals2,tot_err2]))

        plt.plot(time_steps_1, tot_err1, '-.b', label="Camera 1 net error")
        plt.plot(time_steps_2, tot_err2, '-.r', label="Camera 2 net error")

        plt.title("Total error for cameras 1,2 over time={:.2f}".format(time_elapsed))
        plt.show()
