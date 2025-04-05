# useful values that are good to have all over the place
import os
import numpy as np


height = 2560 # camera pixel dimensions
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)


dll_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/dll_folder/Mightex/SSClassic_USBCamera_SDK.dll'

bin_choice = 0 # ranges from    0 (no binning)  ->  2 (bin by 4)
binning = 2**bin_choice

# Get these values from auto-calibration.py code
# Assumption made that movement of the X motor doen't change the Y location (and vice versa)
    # Code doesn't break if this isn't true, but it becomes a bit less efficient
# Intuitively,  (Picomotor steps / pixel change) = these values
# 1 is upstream, 2 is downstream. motorX where X is the port number
y_cam1_pix_to_motor1_steps = -7.5  # How many motor steps on motor 1 does a 1 pixel y-shift on camera 1 correspond to?
y_cam1_pix_to_motor3_steps = -12.5 # etc.
y_cam2_pix_to_motor1_steps = -13
y_cam2_pix_to_motor3_steps = -20     # These numbers have units of (motor_steps / camera_pixels)

x_cam1_pix_to_motor2_steps = 13     # How many motor steps on motor 2 does a 1 pixel x-shift on camera 1 correspond to?
x_cam1_pix_to_motor4_steps = 6.5   # etc.
x_cam2_pix_to_motor2_steps = 21
x_cam2_pix_to_motor4_steps = 11



# ---------------------------------- No need to modify anything below this line -----------------------------------------------

# Look at "matrix notes.nb" for the math behind these matrices
    # columns are motor numbers, rows are camera numbers for the non-inverted matrices
# The motivation for this is that this is a MIMO system, not a SISO (multiple/single input, m/s output)
    # I found that treating this as a pair of SISO systems (two linked pairs of one mirror to one camera)
    # leads there to be two competing PI controllers, which does bad things to stability.
    # Making these matrices should hopefully treat it as a MIMO system
    #
    # Another way of looking at it is that these matrices change from the measurement vector basis into a more
    # natural eigenbasis, whose vectors are a linear combination of the measurement basis

ay = 1/y_cam1_pix_to_motor1_steps
by = 1/y_cam1_pix_to_motor3_steps
cy = 1/y_cam2_pix_to_motor1_steps
dy = 1/y_cam2_pix_to_motor3_steps

ax = 1/x_cam1_pix_to_motor2_steps
bx = 1/x_cam1_pix_to_motor4_steps
cx = 1/x_cam2_pix_to_motor2_steps
dx = 1/x_cam2_pix_to_motor4_steps

y_determinant = ay*dy - by*cy
x_determinant = ax*dx - bx*cx

if (y_determinant == 0) or (x_determinant == 0):
    raise Exception("One of the determinants is zeros, so that matrix is not invertible")


Y_matrix = np.array([[dy, -by], [-cy, ay]]) * (1/y_determinant)
#noninverted_Y_matrix = [[ay, by],[cy, dy]] # just for reference


X_matrix = np.array([[dx, -bx], [-cx, ax]]) * (1/x_determinant)
#noninverted_X_matrix = [[ax, bx],[cx, dx]] # just for reference

if __name__ == "__main__":
    print("Wrong file: This file stores setup values for other files to use")