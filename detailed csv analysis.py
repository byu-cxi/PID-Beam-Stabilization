import numpy as np
import matplotlib.pyplot as plt
import csv
import os

csv_name = "2025-06-04 15-58-51_noise_correction.csv"
csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
arr1 = []
arr2 = []
with open(csv_file_path, 'r') as f:
    data = csv.reader(f)
    next(data)
    for line in data:
        if (line[0] != ""): # If one array was longer than the other, filled in time steps with None
            arr1.append(line[:6])
        if (line[4] != ""):
            arr2.append(line[6:])
    arr1 = np.array(arr1).astype(float) # "time_steps1","y_cam_err1","x_cam_err1","tot_cam_err1","y_mot_steps1","x_mot_steps1"
    arr2 = np.array(arr2).astype(float) # "time_steps2","y_cam_err2","x_cam_err2","tot_cam_err2","y_mot_steps2","x_mot_steps2"


# --- Now that I have the data pulled out of the file, I can make graphs with it! (first index is time, second is data type)
#           ["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]


tstart = min(arr1[0,0],arr2[0,0])
tend = max(arr1[-1,0],arr2[-1,0])
time_elapsed = tend - tstart
arr1[:,0] -= tstart
arr2[:,0] -= tstart


if True:  # This graph shows camera error vs motor steps over time
    plot_y_axis = True

    ind_t = 0 # index for time steps, same for arr1 and arr2

    ind_c = 1 # index for camera Y-axis, same for arr1 and arr2
    ind_m = 4 # index for motor Y-axis, same for arr1 and arr2s
    axis = "Y"

    if plot_y_axis == False:
        ind_c = 2 # index for camera X-axis, same for arr1 and arr2
        ind_m = 5 # index for motor X-axis, same for arr1 and arr2
        axis = "X"

    fig, ax = plt.subplots(2,1, figsize=(8,6))
    plt.suptitle(csv_name + " - steps vs. error for " + axis + " axis" , fontweight="bold")

    tstart = min(arr1[0,0], arr2[0,0])

    ax[0].plot(arr1[:,ind_t], arr1[:,ind_c],'.-b', label="Pixel Error 1")
    ax[0].plot(arr2[:,ind_t], arr2[:,ind_c],'.-r', label="Pixel Error 2")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("Camera error in pixels")
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Pixels")
    ax[0].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(-.03*time_elapsed, 1.03*time_elapsed) # make graphs have same (asethetic) time length
    ax[0].set_ylim(-1.5,1.5)
    ax[0].axhline(0, color="black", linewidth=.5)

    ax[1].plot(arr1[:,ind_t], arr1[:,ind_m],'.-g', label="Motor steps 1")
    ax[1].plot(arr2[:,ind_t], arr2[:,ind_m],'.-', label="Motor steps 2")
    #ax[1].plot(arr2[:,0], arr2[:,3],'.-', color="black", label="total err")
    ax[1].set_title("Motor steps recommended by the PID controller")
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Number of Steps")
    ax[1].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[1].set_xlim(-.03*time_elapsed, 1.03*time_elapsed)
    ax[1].axhline(0, color="black", linewidth=.5)

    plt.tight_layout()
    plt.show()

if False:  # This graph shows the x and y error for both cameras over time

    fig, ax = plt.subplots(2,1, figsize=(8,5))
    plt.suptitle(csv_name, fontweight="bold")

    tstart = min(arr1[0,0], arr2[0,0])

    ax[0].plot(arr1[:,0], arr1[:,1],'.-b', label="y err 1")
    ax[0].plot(arr1[:,0], arr1[:,2],'.-r', label="x err")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("camera 1")
    ax[0].set_xlabel("time")
    ax[0].set_ylabel("pixels")
    ax[0].legend(loc="lower right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(-.03*time_elapsed, 1.03*time_elapsed) # make graphs have same (asethetic) time length

    ax[1].plot(arr2[:,0], arr2[:,1],'.-b', label="y err 2")
    ax[1].plot(arr2[:,0], arr2[:,2],'.-r', label="x err")
    #ax[1].plot(arr2[:,0], arr2[:,3],'.-', color="black", label="total err")
    ax[1].set_title("camera 2")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("pixels")
    ax[1].legend(loc="lower right")#, fancybox=True, framealpha=1)
    ax[1].set_xlim(-.03*time_elapsed, 1.03*time_elapsed)


    plt.tight_layout()
    plt.show()

if False: # This graph recreates the one made in the main program, but better labeling and shape

    plt.figure(figsize=(8,4))
    plt.plot(arr1[:,0], arr1[:,3], '-.b', label="Cam 1")
    plt.plot(arr2[:,0], arr2[:,3], '-.r', label="Cam 2")

    plt.title("Total error for cameras 1,2 over time={:.2f} s".format(time_elapsed), fontweight="bold")
    plt.legend(loc="upper right", fancybox=True, framealpha=1)
    plt.xlabel("time")
    plt.ylabel("pixels")
    plt.show()

if False: # Saves images to a file

    plt.figure(figsize=(4,4))
    plt.plot(arr1[:,0], arr1[:,3], '-.b', label="Cam 1")
    #plt.plot(arr2[:,0], arr2[:,3], '-.r', label="Cam 2")
    plt.ylim(0,20)

    plt.title("Cam 1, no stabilization", fontweight="bold")
    plt.legend(loc="upper right", fancybox=True, framealpha=1)
    plt.xlabel("time")
    plt.ylabel("pixels")
    plt.savefig("c1,ns")