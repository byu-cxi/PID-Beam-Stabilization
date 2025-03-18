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
# 1 is upstream, 2 is downstream. motorX where X is the port number
y_cam1_pix_to_motor1_steps = -8    # y motor on mirror 1
y_cam1_pix_to_motor3_steps = 1     # 
y_cam2_pix_to_motor1_steps = 1     # 
y_cam2_pix_to_motor3_steps = -55   # y motor on mirror 2

x_cam1_pix_to_motor2_steps = 7     # x motor on mirror 1
x_cam1_pix_to_motor4_steps = 1     # 
x_cam2_pix_to_motor2_steps = 1     # 
x_cam2_pix_to_motor4_steps = 85    # x motor on mirror 2


# Look at "matrix notes.nb" for the math behind these matrices
    # columns are motor numbers, rows are camera numbers
# The motivation for this is that this is a MIMO system, not a SISO (multiple/single input, m/s output)
    # I found that treating this as a pair of SISO systems (two linked pairs of one mirror to one camera)
    # leads there to be two competing PI controllers, which does bad things to stability.
    # Making these matrices should hopefully treat it as a MIMO system
    #
    # Another way of looking at it is that these matrices change from the measurement vector basis into a more
    # natural eigenbasis, whose vectors are a linear combination of the measurement basis
    
Y_matrix = [[y_cam2_pix_to_motor3_steps, -y_cam1_pix_to_motor3_steps],
            [-y_cam2_pix_to_motor1_steps, y_cam1_pix_to_motor1_steps]]
#noninverted_y_matrix = [[y_cam1_pix_to_motor1_steps, y_cam1_pix_to_motor3_steps],
#                        [y_cam2_pix_to_motor1_steps, y_cam2_pix_to_motor3_steps]]

X_matrix = [[x_cam2_pix_to_motor4_steps, -x_cam1_pix_to_motor4_steps],
            [-x_cam2_pix_to_motor2_steps, x_cam1_pix_to_motor2_steps]]
#noninverted_x_matrix = [[x_cam1_pix_to_motor2_steps, x_cam1_pix_to_motor4_steps],
#                        [x_cam2_pix_to_motor2_steps, x_cam2_pix_to_motor4_steps]]

if __name__ == "__main__":
    print("Wrong file: This file stores setup values for other files to use")