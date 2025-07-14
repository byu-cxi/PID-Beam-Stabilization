Written by Hyrum Taylor (hct10000 at gmail dot com)

Ptychography requires extremely fine beam control, meaning that even tiny variations in the beam can cause large problems with reconstruction.
This code stabilizes a beam by finding the center of mass of a beam on two cameras, and moving two mirrors to put that center of mass back to the original location in real time.
In essence, it stabilizes 4 degrees of freedom: two vertical, and two horizontal.
It shouldn't change the beam shape: it only stabilizes the position of the beam on the cameras.

Setting up the proper conda environment is tricky, so I wrote notes in `Conda Environment Creation.txt`, although I have not tested the sequence on another machine. `Minimal test motor.py` and `minimal test camera.py` can be used to check if the environment is set up correctly. There is also an `environment backup.yml` file, if the txt file doesn't work completly.

This code is designed for two cameras and two motorized mirrors (meaning four motors), which allows it to correct both Position and Poynting error. It assumes that error in the X direction can be corrected with limited impact on the Y error, and vise versa.

Getting started:
- Follow instructions for the physical setup by watching the video (Box.byu.edu  "/HHGsetup/PID Beam Stabilization documentation video.mp4", or in Hyrum Taylor's personal folder, main directory in the lab box folder).
- Set up the Conda environment, as described in `Conda Environment Creation.txt`. Verify the environment is working using the minimal test codes.
- Use `auto-calibration.py` to set parameters in `vals.py`. 
- Run `main.py`, manually add some noise, and make sure it is stabilizing correctly. If it isn't stabilizing well, tune the PID values in `helper.py`.
- You should be good to go!

Here are descriptions of what the most important files do:
- `Main.py` - This is the actual stabilization code. After all the parameters are set, this is what is actually run. It takes images from the cameras, decides how much to move motors to fix the errors, and then moves motors to fix them.
- `Helper.py` - This is a file that stores small functions that are useful across multiple files, or that would clutter up the `main.py` file. Think of this as an extension of `main.py` that can be easily accessed by other programs in the folder. Note that the PID controller function is in this file.
- `Auto-calibration.py` - This file helps set parameters in `vals.py`. Instead of making a lot of precise measurements to model each new setup this code is used on, instead we can simply move one of the motors, and record how much the laser moves on the cameras. This significantly reduces the amount of work when moving to a new setup. Note that many picomotors have slightly different step sizes in one direction than the other, so it is a good idea to move the motors forward AND backward, and record the average of the two values.
- `Vals.py` - This is a file used to store variables that ideally shouldn't change from run to run: parameters related to the cameras, motors, etc. I recommend keeping binning off, and adjusting the gain to capture the beam without saturation. The 8 variables named @_cam#_pix_to_motor#_steps will need to be modified for every new setup.
- `Detailed csv analysis.py` - When the code runs, it saves a CSV file to record what it does. `Detailed csv analysis.py` is a program that takes the saved CSV file and makes a good-looking plot of error and motor steps over time. This is a useful diagnostic tool, especially when needing to tune PID parameters.
- `Minimal test motor.py`, `minimal test camera.py` - These files are, as the names suggest, a quick check to make sure that the environment is set up to properly connect to the motors and cameras. If the conda environment was set up correctly, these should run without failing. Also, the `minimal motor test.py` file is useful for moving motors without changing anything else, which is useful more often than you might think.

Some of the less immediately relevant, but still useful files are:
- `Matrix notes.nb` - This file has some of the math describing how I turn the camera beam location into the number of motor steps. 
- `Recons/cross-correlation.py` - This code crops and cross-correlates two images, then saves the files. This is useful if trying to use Fourier Ring Correlation to determine the resolution of reconstructed images.
- `Fancy_pictures.py` - This was used to generate good looking images for my senior thesis.
- `Dll_folder/Mightex/*` - This stores DLL files (drivers?) for the cameras. Don't touch these unless switching camera types.
- `Code Reference/*` - This is where I stored the original example files for how to connect to the motor and cameras. Likely not useful to someone walking into the setup, but if you're really digging into the code, it might be worth looking at?
- `Camera numbering order.py` - I used this code to confirm that the cameras are assigned numbers in order of their serial numbers. For example, when connecting to cameras 004 and 005, "cam_dll.SSClassicUSB_AddDeviceToWorkingSet(1)" will connect to camera 004, and "cam_dll.SSClassicUSB_AddDeviceToWorkingSet(2)" will connect to camera 005.
