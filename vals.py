# useful values that are good to have all over the place
import os
import numpy as np


height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)


dll_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/dll_folder/Mightex/SSClassic_USBCamera_SDK.dll'

bin_choice = 0 # ranges from 0 (no binning) to 2 (bin by 4)
binning = 2**bin_choice

# Get these values from auto-calibration.py code
# Assumption made that movement of the X motor doen't change the Y location (and vice versa)
    # Code doesn't break if this isn't true, but it becomes a bit less efficient
# Intuitively (Picomotor steps / pixel change)
# 1 is upstream, 2 is downstream. motorX where X is the port number
y_cam1_pix_to_motor1_steps = -8    # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -15   # etc.
y_cam2_pix_to_motor1_steps = -67
y_cam2_pix_to_motor3_steps = -55

x_cam1_pix_to_motor2_steps = 7     # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 8     # etc.
x_cam2_pix_to_motor2_steps = 75
x_cam2_pix_to_motor4_steps = 27


# Look at "matrix notes.nb" for the math behind these matrices
    # columns are motor numbers, rows are camera numbers for the non-inverted matrices
# The motivation for this is that this is a MIMO system, not a SISO (multiple/single input, m/s output)
    # I found that treating this as a pair of SISO systems (two linked pairs of one mirror to one camera)
    # leads there to be two competing PI controllers, which does bad things to stability.
    # Making these matrices should hopefully treat it as a MIMO system
    #
    # Another way of looking at it is that these matrices change from the measurement vector basis into a more
    # natural eigenbasis, whose vectors are a linear combination of the measurement basis

y_determinant = y_cam1_pix_to_motor1_steps*y_cam2_pix_to_motor3_steps - y_cam2_pix_to_motor1_steps*y_cam1_pix_to_motor3_steps
Y_matrix = np.array([[y_cam2_pix_to_motor3_steps, -y_cam1_pix_to_motor3_steps],
                     [-y_cam2_pix_to_motor1_steps, y_cam1_pix_to_motor1_steps]]) * (1/y_determinant)
#noninverted_y_matrix = [[y_cam1_pix_to_motor1_steps, y_cam1_pix_to_motor3_steps],
#                        [y_cam2_pix_to_motor1_steps, y_cam2_pix_to_motor3_steps]]


x_determinant = x_cam1_pix_to_motor2_steps*x_cam2_pix_to_motor4_steps - x_cam2_pix_to_motor2_steps*x_cam1_pix_to_motor4_steps
X_matrix = np.array([[x_cam2_pix_to_motor4_steps, -x_cam1_pix_to_motor4_steps],
                     [-x_cam2_pix_to_motor2_steps, x_cam1_pix_to_motor2_steps]]) * (1/x_determinant)
#noninverted_x_matrix = [[x_cam1_pix_to_motor2_steps, x_cam1_pix_to_motor4_steps],
#                        [x_cam2_pix_to_motor2_steps, x_cam2_pix_to_motor4_steps]]

if __name__ == "__main__":
    print("Wrong file: This file stores setup values for other files to use")