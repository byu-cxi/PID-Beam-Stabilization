Ptychography requires extremely fine beam control, meaning that even tiny variations in the beam can cause large problems with reconstruction.
This code stabilizes a beam by finding the center of mass of a beam on a camera, and moving a mirror to put that center of mass back to the original location.
It doesn't change the beam shape: it only stabilizes the Poynting vector of the beam
