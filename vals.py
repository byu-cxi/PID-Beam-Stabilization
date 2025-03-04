# useful values that are good to have all over the place

height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)


import os
dll_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/dll_folder/Mightex/SSClassic_USBCamera_SDK.dll'

bin_choice = 0 # ranges from 0 (no binning) to 2 (bin by 4)
binning = 2**bin_choice

# Get these values from auto-calibration.py code
# Assumption made that movement of the X motor doen't change the Y location (and vice versa)
    # Code doesn't break if this isn't true, but it becomes a bit less efficient
# Intuitively (Picomotor steps / pixel change)
# 1 is upstream, 2 is downstream, not the port number on the controller
y_cam1_pix_to_motor1_conversion = -7
y_cam1_pix_to_motor2_conversion = -11
y_cam2_pix_to_motor1_conversion = -33
y_cam2_pix_to_motor2_conversion = -35

x_cam1_pix_to_motor1_conversion = 6
x_cam1_pix_to_motor2_conversion = 7
x_cam2_pix_to_motor1_conversion = 40
x_cam2_pix_to_motor2_conversion = 30

Mx = [[1,1],[1,1]]
My = [[1,1],[1,1]]


if __name__ == "__main__":
    print("Wrong file: This file stores setup values for other files to use")