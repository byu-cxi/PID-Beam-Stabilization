# Note: For some reason, the conda environment that the rest of the code is in has a hard time with h5py, so 
    # for this file, create a new conda env: none of these are the messy packages, so it should be an easy install.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
from pathlib import Path
import os
import csv
import tifffile as ti
import h5py as h

# Stolen from stackoverflow.com/questions/43258638/is-there-a-convenient-way-to-add-a-scale-indicator-to-a-plot-in-matplotlib
class AnchoredHScaleBar(matplotlib.offsetbox.AnchoredOffsetbox):
    """ size: length of bar in data units
        extent : height of bar ends in axes units """
    def __init__(self, size=1, extent = 0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, 
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = matplotlib.offsetbox.AuxTransformBox(trans)
        line = Line2D([0,size],[0,0], **linekw)
        vline1 = Line2D([0,0],[-extent/2.,extent/2.], **linekw)
        vline2 = Line2D([size,size],[-extent/2.,extent/2.], **linekw)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = matplotlib.offsetbox.TextArea(label, textprops={'fontproperties':{'size':7}})
        self.vpac = matplotlib.offsetbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        matplotlib.offsetbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

# Fancy pictures of the Correlated reconstruction images
if False:
    # In the thesis, I changed scan numbers for reader understanding:
    # Scan 8 -> scan 1:1
    # Scan 9 -> scan 1:2
    # Scan 10 -> scan 2:1
    # Scan 11 -> scan 2:2
    # Scan 12 -> scan 3:1
    # Scan 13 -> scan 3:2

    im1_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable8.tiff'))) # scan 8
    im1_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable8.tiff')))
    im2_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable9.tiff'))) # scan 9
    im2_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable9.tiff')))
    shape12 = im1_stable.shape

    im3_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable10.tiff'))) # scan 10
    im3_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable10.tiff')))
    im4_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable11.tiff'))) # scan 11
    im4_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable11.tiff')))
    shape34 = im3_stable.shape

    im5_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable12.tiff'))) # scan 12
    im5_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable12.tiff')))
    im6_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable13.tiff'))) # scan 13
    im6_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable13.tiff')))
    shape56 = im5_stable.shape


    f,ax = plt.subplots(4,3, figsize=(6.4,9))
    plt.suptitle("Stabilized vs. Unstabilized Reconstructions", fontweight='bold', fontsize=15)
    f.subplots_adjust(top=.92)

    ax[0,0].imshow(im1_stable) # top, left
    ax[0,0].set_title("Stable Scan 1:1", fontsize=9)
    ax[0,0].set_xticks(())
    ax[0,0].set_yticks(())

    ax[0,1].imshow(im3_stable) # top, middle
    ax[0,1].set_title("Stable Scan 2:1", fontsize=9)
    ax[0,1].set_xticks(())
    ax[0,1].set_yticks(())

    ax[0,2].imshow(im5_stable) # top, right
    ax[0,2].set_title("Stable Scan 3:1", fontsize=9)
    ax[0,2].set_xticks(())
    ax[0,2].set_yticks(())


    ax[1,0].imshow(im2_stable) # second, left
    ax[1,0].set_title("Stable Scan 1:2", fontsize=9)
    ax[1,0].set_xticks(())
    ax[1,0].set_yticks(())

    ax[1,1].imshow(im4_stable) # second, middle
    ax[1,1].set_title("Stable Scan 2:2", fontsize=9)
    ax[1,1].set_xticks(())
    ax[1,1].set_yticks(())

    ax[1,2].imshow(im6_stable) # second, right
    ax[1,2].set_title("Stable Scan 3:2", fontsize=9)
    ax[1,2].set_xticks(())
    ax[1,2].set_yticks(())


    ax[2,0].imshow(im1_unstable) # third, left
    ax[2,0].set_title("Unstable Scan 1:1", fontsize=9)
    ax[2,0].set_xticks(())
    ax[2,0].set_yticks(())

    ax[2,1].imshow(im3_unstable) # third, middle
    ax[2,1].set_title("Unstable Scan 2:1", fontsize=9)
    ax[2,1].set_xticks(())
    ax[2,1].set_yticks(())

    ax[2,2].imshow(im5_unstable) # third, right
    ax[2,2].set_title("Unstable Scan 3:1", fontsize=9)
    ax[2,2].set_xticks(())
    ax[2,2].set_yticks(())


    ax[3,0].imshow(im2_unstable) # bottom, left
    ax[3,0].set_title("Unstable Scan 1:2", fontsize=9)
    ax[3,0].set_xticks(())
    ax[3,0].set_yticks(())

    ax[3,1].imshow(im4_unstable) # bottom, middle
    ax[3,1].set_title("Unstable Scan 2:2", fontsize=9)
    ax[3,1].set_xticks(())
    ax[3,1].set_yticks(())

    ax[3,2].imshow(im6_unstable) # bottom, right
    ax[3,2].set_title("Unstable Scan 3:2", fontsize=9)
    ax[3,2].set_xticks(())
    ax[3,2].set_yticks(())
    ob = AnchoredHScaleBar(size=71.4, label="200 microns", loc=4, frameon=True, pad=0.4, sep=2, linekw=dict(color="crimson"),) 
    ax[3,2].add_artist(ob)

    f.supylabel("    Unstabilized                                                 Stabilized", fontweight='bold', fontsize=12)
    #f.tight_layout()
    #plt.show()
    plt.savefig("Recon Comparison")

def GetArrFromCSV(csv_name):
        # Analyze csv files to make nice figures about error over time
    csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
    arr1 = []
    arr2 = []
    with open(csv_file_path, 'r') as f:
        data = csv.reader(f)
        next(data) # first line is column description, not data
        for line in data:
            if (line[0] != ""): # If one array was longer than the other, filled in time steps with None
                arr1.append(line[:6])
            if (line[4] != ""):
                arr2.append(line[6:])
        arr1 = np.array(arr1).astype(float) # "time_steps1","y_cam_err1","x_cam_err1","tot_cam_err1","y_mot_steps1","x_mot_steps1"
        arr2 = np.array(arr2).astype(float) # "time_steps2","y_cam_err2","x_cam_err2","tot_cam_err2","y_mot_steps2","x_mot_steps2"

    tstart = min(arr1[0,0],arr2[0,0])
    tend = max(arr1[-1,0],arr2[-1,0])
    time_elapsed = tend - tstart
    arr1[:,0] -= tstart
    arr2[:,0] -= tstart

    return arr1, arr2, time_elapsed

# Fancy image of camera error tracking
if False:
    arr11, arr12, time_elapsed1 = GetArrFromCSV("2025-07-03 19-33-00_unstabilized.csv")
    arr21, arr22, time_elapsed2 = GetArrFromCSV("2025-07-03 20-08-35_unstabilized.csv")

    ind_t = 0 # index for time steps, same for arr1 and arr2

    ind_c = 1 # index for camera Y-axis, same for arr1 and arr2
    ind_m = 4 # index for motor Y-axis, same for arr1 and arr2s

    fig, ax = plt.subplots(2,1, figsize=(8,6))
    plt.suptitle("Stabilized vs. Unstabilized Pixel Error Tracker - Y Direction - Scans 1:1" , fontweight="bold")

    tstart = min(arr11[0,0], arr12[0,0])

    ax[0].plot(arr11[:,ind_t], arr11[:,ind_c],'.-b', label="Camera 1")
    ax[0].plot(arr12[:,ind_t], arr12[:,ind_c],'.-r', label="Camera 2")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("Stabilized")
    ax[0].set_xlabel("Time (seconds)")
    ax[0].set_ylabel("Error (pixels)")
    ax[0].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(-.03*time_elapsed1, 1.03*time_elapsed1) # make graphs have same (asethetic) time length
    #ax[0].set_ylim(-1.5,1.5)
    ax[0].axhline(0, color="black", linewidth=.5)


    tstart = min(arr21[0,0], arr22[0,0])

    ax[1].plot(arr21[:,ind_t], arr21[:,ind_c],'.-b', label="Camera 1")
    ax[1].plot(arr22[:,ind_t], arr22[:,ind_c],'.-r', label="Camera 2")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[1].set_title("Unstabilized")
    ax[1].set_xlabel("Time (seconds)")
    ax[1].set_ylabel("Error (pixels)")
    ax[1].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[1].set_xlim(-.03*time_elapsed2, 1.03*time_elapsed2) # make graphs have same (asethetic) time length
    #ax[0].set_ylim(-1.5,1.5)
    ax[1].axhline(0, color="black", linewidth=.5)

    plt.tight_layout()
    plt.savefig("Error comparison")

# create figure of how image is reconstructed over time
if False:
    file_name = "modes[1, 1]_threshold5_adjusth_probe[2.64e-05, 0.075, 1.0, -1.0, 2.65e-05, 0]_crop2048_bin4_20250707_t105311_.hdf5"
    f = h.File(Path(os.getcwd(), 'recons', 'stabilized8', file_name))
    arr = np.array(f['obj_probe_series/obj_series'])
    iter_numbers = np.array(f['obj_probe_series/iteration_number'])

    nums = [0,1,3,99] # what stored values to look at? Setting them here makes it easy to modify final graph

    im1 = np.abs(arr[nums[0]+1,0,:,:])
    im2 = np.abs(arr[nums[1]+1,0,:,:])
    im3 = np.abs(arr[nums[2]+1,0,:,:])
    im4 = np.abs(arr[nums[3]+1,0,:,:])

    low = 450
    high = 800

    f,ax = plt.subplots(2,2, figsize=(5,5.5))
    plt.suptitle("Sample Reconstruction Process")

    ax[0,0].imshow(im1[low:high,low:high])
    ax[0,0].set_title("Iteration "+str(iter_numbers[nums[0]]))
    ax[0,0].set_xticks(())
    ax[0,0].set_yticks(())

    ax[0,1].imshow(im2[low:high,low:high])
    ax[0,1].set_title("Iteration "+str(iter_numbers[nums[1]]))
    ax[0,1].set_xticks(())
    ax[0,1].set_yticks(())

    ax[1,0].imshow(im3[low:high,low:high])
    ax[1,0].set_title("Iteration "+str(iter_numbers[nums[2]]))
    ax[1,0].set_xticks(())
    ax[1,0].set_yticks(())

    ax[1,1].imshow(im4[low:high,low:high])
    ax[1,1].set_title("Iteration "+str(iter_numbers[nums[3]]))
    ax[1,1].set_xticks(())
    ax[1,1].set_yticks(())

    ob = AnchoredHScaleBar(size=71.4, label="200 microns", loc=4, frameon=True, pad=0.2, sep=2, linekw=dict(color="crimson"),) 
    ax[0,0].add_artist(ob)

    #plt.show()
    plt.savefig("psi recon process")

# create comparison of where beam is over course of scan? (plot image center over course of scan)
if False:
    arr11, arr12, time_elapsed1 = GetArrFromCSV("2025-07-03 19-33-00_unstabilized.csv")
    arr21, arr22, time_elapsed2 = GetArrFromCSV("2025-07-03 20-08-35_unstabilized.csv")

    ind_x = 2 # index for camera Y-axis, same for arr1 and arr2
    ind_y = 1

    x_st = arr11[:,ind_x]
    y_st = arr11[:,ind_y]
    x_unst = arr21[:,ind_x]
    y_unst = arr21[:,ind_y]

    lhs = -3
    rhs = 3
    top = 11
    bot = -12

    f,ax = plt.subplots(1,2)
    f.suptitle("Beam Center on Camera 1 Throughout Scans 1:1\n", fontweight='bold', fontsize=14)

    ax[0].plot(x_st, y_st, '.')
    ax[0].set_ylim((bot,top))
    ax[0].set_xlim((lhs,rhs))
    ax[0].set_aspect('equal', adjustable='box')
    ax[0].set_xlabel("Horizontal error (pixels)")
    ax[0].set_ylabel("Vertical error (pixels)")
    ax[0].set_title("Stabilized", fontweight='bold', fontsize=10)

    ax[1].plot(x_unst, y_unst, '.')
    ax[1].set_ylim((bot,top))
    ax[1].set_xlim((lhs,rhs))
    ax[1].set_aspect('equal', adjustable='box')
    ax[1].set_xlabel("Horizontal error (pixels)")
    ax[1].set_ylabel("Vertical error (pixels)")
    ax[1].set_title("Unstabilized", fontweight='bold', fontsize=10)

    #plt.show()
    plt.savefig("Beam Center Plot")

