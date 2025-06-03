Ptychography requires extremely fine beam control, meaning that even tiny variations in the beam can cause large problems with reconstruction.
This code stabilizes a beam by finding the center of mass of a beam on a camera, and moving a mirror to put that center of mass back to the original location in real time.
It shouldn't change the beam shape: it only stabilizes the position of the beam on the camera.

To use this code, start with `main.py`: The other essential files to run the code are `helper.py`, `vals.py`, and the DLL files in `dll_folder`. In addition, `auto-calibration.py` is needed to set variables in `vals.py`, but that is a one-time thing. Also, `detailed csv analysis.py` has various graphing codes that are useful for debugging and figure creation: it uses error and motor step data that are automatically saved in the `CSV/` directory when running `main.py`. All the other codes can be helpful to look at for someone trying to modify the code, but are not needed for code execution.

Setting up the proper conda environment is tricky, so I wrote notes in `Conda Environment Creation.txt`, although I have not tested the sequence on another machine.

This code is designed for two cameras and two motorized mirrors (meaning four motors), which allows it to correct both Position and Poynting error. It assumes that error in the X direction can be corrected with limited impact on the Y error, and vise versa.
