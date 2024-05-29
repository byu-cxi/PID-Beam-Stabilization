from ctypes import *
from time import sleep
from ctypes.wintypes import MSG
import cv2
import imutils
import time

#Numpy module is needed to acquire frame data
#Install module by typing in command prompt: py -m pip install numpy
import numpy as np
n = 1

libw = windll.user32
GetMessage = libw.GetMessageA
TranslateMessage = libw.TranslateMessage
DispatchMessage = libw.DispatchMessageA

libc = cdll.msvcrt
kbhit = libc._kbhit # keyboard hit

class INFO(Structure):
    _fields_ = [ ( "CameraID", c_int ),
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

#For c_ubyte, multiply by max resolution of camera (eg. 752*480 BCE-CG04-U)
FRAMECALLBACK = CFUNCTYPE(None, POINTER(INFO), POINTER(c_ubyte*1280*960) )
#Create frame callback function
def FrameCallback( info, data ):
    #Print camera information to command prompt (ID, Resolution, Exposure Time)
    global n
    global start
    # print(info.contents.CameraID, info.contents.Row, info.contents.Column, info.contents.ExposureTime)
    x = data.contents
    arr = np.array(x)
    arr = imutils.resize(arr, width=500)
    cv2.imshow('Show Image', arr)
    # arr.astype('int16').tofile('image%s.raw' % n)  #Save frame data in raw format

    if n == 1:
        start = time.time()
        n += 1
    elif n == 100:
        end = time.time()
        n = 1
        fps = 100/(end - start)
        print("FPS: ", fps)
    else:
        n += 1
    # print(arr)  #Print array data to command prompt

#Load SDK - Python file must be in same folder as SDK DLL
# lib = cdll.SSClassic_USBCamera_SDK
lib = cdll.LoadLibrary("C:\\Users\\hct10\\Documents\\Classes\\CURRENT\\Sandberg Research\\Code\\Senior Project\\dll_folder\Mightex\\SSClassic_USBCamera_SDK.dll")

print("InitDevice =", lib.SSClassicUSB_InitDevice())  #Initialize device
moduleno = create_string_buffer(16)
serialno = create_string_buffer(16)
print("GetModuleNoSerialNo = ", lib.SSClassicUSB_GetModuleNoSerialNo(1,moduleno,serialno))
print("ModuleNo =", repr(moduleno.raw))  #Show model number
print("SerialNo =", repr(serialno.raw))  #Show serial number
print("AddDeviceToWorkingSet =", lib.SSClassicUSB_AddDeviceToWorkingSet(1))
print("StartCameraEngine =", lib.SSClassicUSB_StartCameraEngine(None, 8, 2, 0))

framecb = FRAMECALLBACK(FrameCallback)  #Create callback function
print("InstallFrameHooker =", lib.SSClassicUSB_InstallFrameHooker(1, framecb))
lib.SSClassicUSB_SetExposureTime(1, 100) #Set exposure time to 10ms

while(True):
    print("")
    print("Select an option: ")
    print("1 - Grab frames")
    print("2 - Live View")
    print("3 - Quit application")
    inp = input("Enter an option: ")

    if(inp == "1"):
        frame = int(input("Enter number of frames to grab: "))
        print("StartFrameGrab =", lib.SSClassicUSB_StartFrameGrab(1, frame))

        msg = MSG()
        while True:
            if(kbhit()):
                break
            GetMessage(pointer(msg), 0, 0, 0)
            TranslateMessage(pointer(msg))
            DispatchMessage(pointer(msg))
            sleep(0.01)

    if(inp == "2"):
        print("StartFrameGrab =", lib.SSClassicUSB_StartFrameGrab(1))
        msg = MSG()
        while True:
            if(kbhit()):
                cv2.destroyAllWindows()
                break
            GetMessage(pointer(msg), 0, 0, 0)
            TranslateMessage(pointer(msg))
            DispatchMessage(pointer(msg))
            sleep(0.01)
    if(inp == "3"):
        break
    else:
        continue


print("StopFrameGrab =", lib.SSClassicUSB_StopFrameGrab(1))
print("StopCameraEngine =", lib.SSClassicUSB_StopCameraEngine())
print("UnInitDevice =", lib.SSClassicUSB_UnInitDevice())
