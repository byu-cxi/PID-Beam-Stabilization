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
from PIL import Image as im

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

# Senior Thesis: Fancy pictures of the Correlated reconstruction images
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

    ax[0,0].imshow(im1_stable, cmap='grey') # top, left
    ax[0,0].set_title("Stable Scan 1:1", fontsize=9)
    ax[0,0].set_xticks(())
    ax[0,0].set_yticks(())

    ax[0,1].imshow(im3_stable, cmap='grey') # top, middle
    ax[0,1].set_title("Stable Scan 2:1", fontsize=9)
    ax[0,1].set_xticks(())
    ax[0,1].set_yticks(())

    ax[0,2].imshow(im5_stable, cmap='grey') # top, right
    ax[0,2].set_title("Stable Scan 3:1", fontsize=9)
    ax[0,2].set_xticks(())
    ax[0,2].set_yticks(())


    ax[1,0].imshow(im2_stable, cmap='grey') # second, left
    ax[1,0].set_title("Stable Scan 1:2", fontsize=9)
    ax[1,0].set_xticks(())
    ax[1,0].set_yticks(())

    ax[1,1].imshow(im4_stable, cmap='grey') # second, middle
    ax[1,1].set_title("Stable Scan 2:2", fontsize=9)
    ax[1,1].set_xticks(())
    ax[1,1].set_yticks(())

    ax[1,2].imshow(im6_stable, cmap='grey') # second, right
    ax[1,2].set_title("Stable Scan 3:2", fontsize=9)
    ax[1,2].set_xticks(())
    ax[1,2].set_yticks(())


    ax[2,0].imshow(im1_unstable, cmap='grey') # third, left
    ax[2,0].set_title("Unstable Scan 1:1", fontsize=9)
    ax[2,0].set_xticks(())
    ax[2,0].set_yticks(())

    ax[2,1].imshow(im3_unstable, cmap='grey') # third, middle
    ax[2,1].set_title("Unstable Scan 2:1", fontsize=9)
    ax[2,1].set_xticks(())
    ax[2,1].set_yticks(())

    ax[2,2].imshow(im5_unstable, cmap='grey') # third, right
    ax[2,2].set_title("Unstable Scan 3:1", fontsize=9)
    ax[2,2].set_xticks(())
    ax[2,2].set_yticks(())


    ax[3,0].imshow(im2_unstable, cmap='grey') # bottom, left
    ax[3,0].set_title("Unstable Scan 1:2", fontsize=9)
    ax[3,0].set_xticks(())
    ax[3,0].set_yticks(())

    ax[3,1].imshow(im4_unstable, cmap='grey') # bottom, middle
    ax[3,1].set_title("Unstable Scan 2:2", fontsize=9)
    ax[3,1].set_xticks(())
    ax[3,1].set_yticks(())

    ax[3,2].imshow(im6_unstable, cmap='grey') # bottom, right
    ax[3,2].set_title("Unstable Scan 3:2", fontsize=9)
    ax[3,2].set_xticks(())
    ax[3,2].set_yticks(())
    ob = AnchoredHScaleBar(size=71.4, label="200 microns", loc=4, frameon=True, pad=0.4, sep=2, linekw=dict(color="crimson"), ax=ax[3,2]) 
    ax[3,2].add_artist(ob)

    f.supylabel("    Unstabilized                                         Stabilized", fontweight='bold', fontsize=12)
    #f.tight_layout()
    #plt.show()
    plt.savefig("Recon Comparison")

# make third panel (FRC) for FiO-LS image below
if False:
    # Copied these tables from FiJi:
        # Spatial_Frequency, FRC, Smoothed_FRC, Threshold
    stable_frc = ((0.000000, 1.000000, 0.999719, 0.142800),
    (0.006494, 0.990768, 0.991786, 0.142800),
    (0.012987, 0.985462, 0.983648, 0.142800),
    (0.019481, 0.973818, 0.975816, 0.142800),
    (0.025974, 0.969152, 0.971913, 0.142800),
    (0.032468, 0.974127, 0.970575, 0.142800),
    (0.038961, 0.966695, 0.970544, 0.142800),
    (0.045455, 0.972708, 0.973281, 0.142800),
    (0.051948, 0.980721, 0.977091, 0.142800),
    (0.058442, 0.976057, 0.976615, 0.142800),
    (0.064935, 0.973342, 0.972855, 0.142800),
    (0.071429, 0.968928, 0.967585, 0.142800),
    (0.077922, 0.959823, 0.962673, 0.142800),
    (0.084416, 0.960671, 0.963109, 0.142800),
    (0.090909, 0.970035, 0.966994, 0.142800),
    (0.097403, 0.968778, 0.964817, 0.142800),
    (0.103896, 0.953685, 0.956088, 0.142800),
    (0.110390, 0.946987, 0.947052, 0.142800),
    (0.116883, 0.940517, 0.940026, 0.142800),
    (0.123377, 0.932335, 0.933625, 0.142800),
    (0.129870, 0.928660, 0.927151, 0.142800),
    (0.136364, 0.919716, 0.914309, 0.142800),
    (0.142857, 0.891886, 0.893151, 0.142800),
    (0.149351, 0.868474, 0.871924, 0.142800),
    (0.155844, 0.857112, 0.857446, 0.142800),
    (0.162338, 0.846915, 0.845588, 0.142800),
    (0.168831, 0.832083, 0.835647, 0.142800),
    (0.175325, 0.829697, 0.832181, 0.142800),
    (0.181818, 0.835988, 0.826118, 0.142800),
    (0.188312, 0.807806, 0.812185, 0.142800),
    (0.194805, 0.794918, 0.796985, 0.142800),
    (0.201299, 0.789249, 0.783445, 0.142800),
    (0.207792, 0.763308, 0.770330, 0.142800),
    (0.214286, 0.761893, 0.758845, 0.142800),
    (0.220779, 0.749834, 0.753424, 0.142800),
    (0.227273, 0.750314, 0.744457, 0.142800),
    (0.233766, 0.730337, 0.732694, 0.142800),
    (0.240260, 0.718594, 0.719931, 0.142800),
    (0.246753, 0.711521, 0.716162, 0.142800),
    (0.253247, 0.720657, 0.720342, 0.142800),
    (0.259740, 0.728695, 0.726970, 0.142800),
    (0.266234, 0.730709, 0.731270, 0.142800),
    (0.272727, 0.734682, 0.738454, 0.142800),
    (0.279221, 0.751830, 0.748733, 0.142800),
    (0.285714, 0.758160, 0.761471, 0.142800),
    (0.292208, 0.776054, 0.772423, 0.142800),
    (0.298701, 0.781266, 0.780619, 0.142800),
    (0.305195, 0.784220, 0.784670, 0.142800),
    (0.311688, 0.788748, 0.787715, 0.142800),
    (0.318182, 0.789670, 0.788581, 0.142800),
    (0.324675, 0.786789, 0.783843, 0.142800),
    (0.331169, 0.773619, 0.779349, 0.142800),
    (0.337662, 0.780461, 0.776639, 0.142800),
    (0.344156, 0.773953, 0.772013, 0.142800),
    (0.350649, 0.760668, 0.758239, 0.142800),
    (0.357143, 0.738900, 0.735301, 0.142800),
    (0.363636, 0.704561, 0.703857, 0.142800),
    (0.370130, 0.667764, 0.665612, 0.142800),
    (0.376623, 0.623449, 0.621738, 0.142800),
    (0.383117, 0.573157, 0.569497, 0.142800),
    (0.389610, 0.510083, 0.505558, 0.142800),
    (0.396104, 0.431204, 0.434731, 0.142800),
    (0.402597, 0.364643, 0.367797, 0.142800),
    (0.409091, 0.309099, 0.304411, 0.142800),
    (0.415584, 0.237179, 0.240230, 0.142800),
    (0.422078, 0.175915, 0.177244, 0.142800),
    (0.428571, 0.119293, 0.123963, 0.142800),
    (0.435065, 0.078982, 0.080671, 0.142800),
    (0.441558, 0.044570, 0.047082, 0.142800),
    (0.448052, 0.018930, 0.027242, 0.142800),
    (0.454545, 0.022322, 0.020234, 0.142800),
    (0.461039, 0.018421, 0.025948, 0.142800),
    (0.467532, 0.040809, 0.035351, 0.142800),
    (0.474026, 0.044132, 0.038922, 0.142800),
    (0.480519, 0.029259, 0.040174, 0.142800),
    (0.487013, 0.047552, 0.041952, 0.142800))
    stable_frc = np.array(stable_frc)

    unstable_frc = ((0.000000, 1.00000, 1.00195, 0.142800),
    (0.006494, 0.98743, 0.97800, 0.142800),
    (0.012987, 0.93623, 0.95663, 0.142800),
    (0.019481, 0.95630, 0.94442, 0.142800),
    (0.025974, 0.93490, 0.93993, 0.142800),
    (0.032468, 0.93106, 0.92845, 0.142800),
    (0.038961, 0.91808, 0.91708, 0.142800),
    (0.045455, 0.90159, 0.89265, 0.142800),
    (0.051948, 0.85386, 0.85312, 0.142800),
    (0.058442, 0.80355, 0.80651, 0.142800),
    (0.064935, 0.76358, 0.78264, 0.142800),
    (0.071429, 0.79018, 0.78296, 0.142800),
    (0.077922, 0.79158, 0.78346, 0.142800),
    (0.084416, 0.76461, 0.76023, 0.142800),
    (0.090909, 0.72234, 0.72124, 0.142800),
    (0.097403, 0.67623, 0.68343, 0.142800),
    (0.103896, 0.65526, 0.67863, 0.142800),
    (0.110390, 0.71593, 0.71235, 0.142800),
    (0.116883, 0.76409, 0.73847, 0.142800),
    (0.123377, 0.72276, 0.72136, 0.142800),
    (0.129870, 0.67653, 0.67055, 0.142800),
    (0.136364, 0.60941, 0.60578, 0.142800),
    (0.142857, 0.52962, 0.55067, 0.142800),
    (0.149351, 0.52337, 0.52466, 0.142800),
    (0.155844, 0.52164, 0.52921, 0.142800),
    (0.162338, 0.54634, 0.54710, 0.142800),
    (0.168831, 0.57369, 0.55586, 0.142800),
    (0.175325, 0.53878, 0.54660, 0.142800),
    (0.181818, 0.53119, 0.53968, 0.142800),
    (0.188312, 0.55324, 0.54786, 0.142800),
    (0.194805, 0.55649, 0.56509, 0.142800),
    (0.201299, 0.58976, 0.58595, 0.142800),
    (0.207792, 0.60973, 0.59368, 0.142800),
    (0.214286, 0.57362, 0.58287, 0.142800),
    (0.220779, 0.56981, 0.56653, 0.142800),
    (0.227273, 0.55455, 0.53660, 0.142800),
    (0.233766, 0.47658, 0.49350, 0.142800),
    (0.240260, 0.45769, 0.45427, 0.142800),
    (0.246753, 0.42684, 0.41436, 0.142800),
    (0.253247, 0.35241, 0.36449, 0.142800),
    (0.259740, 0.32019, 0.30443, 0.142800),
    (0.266234, 0.23292, 0.24201, 0.142800),
    (0.272727, 0.17739, 0.17528, 0.142800),
    (0.279221, 0.11450, 0.11783, 0.142800),
    (0.285714, 0.06326, 0.05830, 0.142800),
    (0.292208, -0.00529, -0.00780, 0.142800),
    (0.298701, -0.08260, -0.07104, 0.142800),
    (0.305195, -0.11955, -0.12559, 0.142800),
    (0.311688, -0.17761, -0.15844, 0.142800),
    (0.318182, -0.16870, -0.17853, 0.142800),
    (0.324675, -0.19414, -0.18115, 0.142800),
    (0.331169, -0.17422, -0.16590, 0.142800),
    (0.337662, -0.12524, -0.13347, 0.142800),
    (0.344156, -0.10500, -0.10081, 0.142800),
    (0.350649, -0.07011, -0.08128, 0.142800),
    (0.357143, -0.07424, -0.08090, 0.142800),
    (0.363636, -0.10164, -0.10705, 0.142800),
    (0.370130, -0.14792, -0.14830, 0.142800),
    (0.376623, -0.19552, -0.18787, 0.142800),
    (0.383117, -0.21640, -0.22191, 0.142800),
    (0.389610, -0.25651, -0.25805, 0.142800),
    (0.396104, -0.30199, -0.30646, 0.142800),
    (0.402597, -0.36310, -0.35681, 0.142800),
    (0.409091, -0.40223, -0.39578, 0.142800),
    (0.415584, -0.41882, -0.42115, 0.142800),
    (0.422078, -0.44354, -0.44937, 0.142800),
    (0.428571, -0.48863, -0.48026, 0.142800),
    (0.435065, -0.50449, -0.50602, 0.142800),
    (0.441558, -0.52570, -0.52633, 0.142800),
    (0.448052, -0.54911, -0.54340, 0.142800),
    (0.454545, -0.55257, -0.54783, 0.142800),
    (0.461039, -0.53946, -0.53484, 0.142800),
    (0.467532, -0.51022, -0.50904, 0.142800),
    (0.474026, -0.47687, -0.48789, 0.142800),
    (0.480519, -0.48203, -0.47205, 0.142800),
    (0.487013, -0.45293, -0.45692, 0.142800))
    unstable_frc = np.array(unstable_frc)

    # FRC plot
    plt.figure(figsize=(4,4))
    plt.plot(stable_frc[:,0], stable_frc[:,2], 'b.-')
    plt.plot(unstable_frc[:,0], unstable_frc[:,2], 'g^-')
    plt.axhline(y=1/7, linestyle=':')

    plt.scatter(1/2.346, 1/7, color='black', zorder=10)
    plt.text(1/2.346, 1/7, " .426\n", fontsize=8, color="black", zorder=10)
    plt.scatter(1/3.618, 1/7, color='black', zorder=10)
    plt.text(1/3.618, 1/7, " .276\n", fontsize=8, color="black", zorder=10)

    plt.ylim(0,1.05)
    plt.legend(["Stable","Unstable"])

    plt.xlabel("Spatial Frequency")
    plt.ylabel("Correlation")

    plt.savefig("frc_analysis")

# FiO-LS Summary/Poster: Fancy pictures of the Correlated reconstruction images
if False:
    im1_unstable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'unstable8.tiff'))) # scan 8
    im1_stable = np.array(ti.imread(Path(os.getcwd(), 'recons', 'Correlated Images', 'stable8.tiff')))
    frc_analysis = np.array(im.open(Path(os.getcwd(), "frc_analysis.png")))
    
    f,ax = plt.subplots(1, 3, figsize=(8,3))
    plt.suptitle("Stabilized vs. Unstabilized Sector Star Ptychographic Reconstructions", fontweight='bold', fontsize=11)
    #f.subplots_adjust(top=.92)

    ax[0].imshow(im1_stable, cmap="Greys_r") # top
    ax[0].set_title("Stabilized", fontsize=9)
    ax[0].set_xticks(())
    ax[0].set_yticks(())
    ax[0].annotate("A", xy=(.05, .9), xycoords='axes fraction', bbox=dict(facecolor='0.7', edgecolor='white', pad=3.0))

    ax[1].imshow(im1_unstable, cmap="Greys_r") # bottom
    ax[1].set_title("Unstabilized", fontsize=9)
    ax[1].set_xticks(())
    ax[1].set_yticks(())
    ax[1].annotate("B", xy=(.05, .9), xycoords='axes fraction', bbox=dict(facecolor='0.7', edgecolor='white', pad=3.0))

    ob0 = AnchoredHScaleBar(size=71.4, label="200 µm", loc=4, frameon=True, pad=0.4, sep=2, linekw=dict(color="crimson"), ax=ax[0]) 
    ax[0].add_artist(ob0)
    ob1 = AnchoredHScaleBar(size=71.4, label="200 µm", loc=4, frameon=True, pad=0.4, sep=2, linekw=dict(color="crimson"), ax=ax[1]) 
    ax[1].add_artist(ob1)


    ax[2].imshow(frc_analysis)
    ax[2].set_title("FRC Analysis", fontsize=9)
    ax[2].set_xticks(())
    ax[2].set_yticks(())
    ax[2].axis("off")
    ax[2].annotate("C", xy=(.05, .82), xycoords='axes fraction', bbox=dict(facecolor='0.7', edgecolor='white', pad=3.0))


    f.tight_layout()
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

# Senior Thesis: Fancy image of camera error tracking
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
    plt.savefig("Cam Error Comparison")

# Senior Thesis: create figure of how image is reconstructed over time
if True:
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

    ax[0,0].imshow(im1[low:high,low:high], cmap='grey')
    ax[0,0].set_title("Iteration "+str(iter_numbers[nums[0]]))
    ax[0,0].set_xticks(())
    ax[0,0].set_yticks(())

    ax[0,1].imshow(im2[low:high,low:high], cmap='grey')
    ax[0,1].set_title("Iteration "+str(iter_numbers[nums[1]]))
    ax[0,1].set_xticks(())
    ax[0,1].set_yticks(())

    ax[1,0].imshow(im3[low:high,low:high], cmap='grey')
    ax[1,0].set_title("Iteration "+str(iter_numbers[nums[2]]))
    ax[1,0].set_xticks(())
    ax[1,0].set_yticks(())

    ax[1,1].imshow(im4[low:high,low:high], cmap='grey')
    ax[1,1].set_title("Iteration "+str(iter_numbers[nums[3]]))
    ax[1,1].set_xticks(())
    ax[1,1].set_yticks(())

    ob = AnchoredHScaleBar(size=71.4, label="200 microns", loc=4, frameon=True, pad=0.2, sep=2, linekw=dict(color="crimson"),ax=ax[0,0]) 
    ax[0,0].add_artist(ob)

    #plt.show()
    plt.savefig("psi recon process")

# Senior Thesis: create comparison of where beam is over course of scan? (plot image center over course of scan)
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

# FiO-LS Summary/Poster: create comparison of where beam is over course of scan? (plot image center over course of scan)
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

    f,ax = plt.subplots(1,2, figsize=(4,5))
    f.suptitle("Beam Center Over Time Comparison\n", fontweight='bold', fontsize=14)

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
    plt.savefig("Beam Center Plot - Skinny")

