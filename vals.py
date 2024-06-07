# useful values that are good to have all over the place

height = 2560
width = 1920
metadata_size = 128
img_size = metadata_size + (height*width)

dll_path = "C:\\Users\\hct10\\Documents\\Classes\\CURRENT\\Sandberg Research\\Code\\Senior Project\\dll_folder\Mightex\\SSClassic_USBCamera_SDK.dll"

# Get these values from auto-calibration.py code
# Assumption made that movement of the X motor doen't change the Y location (and vise versa)
# Intuitively (Picomotor steps / pixel change)
y_pixel_to_motorstep_conversion = -23 # -2.9
x_pixel_to_motorstep_conversion = -20 #1.8

bin_choice = 0 # ranges from 0 (no binning) to 2 (bin by 4)
binning = 2**bin_choice
