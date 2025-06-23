import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import datetime

csv_name = "2025-06-23 10-15-41_time_gap.csv"
ram_tsv = "logfile04.tsv"


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


tsv_file_path = os.path.join(os.getcwd(),'CSV','Memory Logs','log_file_tsvs',ram_tsv)
ram_arr = []
with open(tsv_file_path, 'r') as f:
    data = csv.reader(f,delimiter='\t')
    next(data) # first line is column description, not data
    for line in data:
        timestamp = datetime.datetime.strptime(line[0],'%m/%d/%Y %H:%M:%S.%f').timestamp()
        ram_arr.append([timestamp,line[1]])
    ram_arr = np.array(ram_arr).astype(float) # "time","free ram"


# --- Now that I have the data pulled out of the file, I can make graphs with it! (first index is time, second is data type)
#           ["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]


tstart = min(min(arr1[0,0],arr2[0,0]), ram_arr[0,0]) # used to scale the time axis on the graphs so it's equal on both
tend = max(max(arr1[-1,0],arr2[-1,0]), ram_arr[-1,0])
time_elapsed = tend - tstart
arr1[:,0] -= tstart
arr2[:,0] -= tstart
ram_arr[:,0] -= tstart


if True:  # This graph shows camera error vs motor steps over time
    plot_y_axis = True   # if set to false, it plots x axis instead

    ind_t = 0 # index for time steps, same for arr1 and arr2

    ind_c = 1 # index for camera Y-axis, same for arr1 and arr2
    ind_m = 4 # index for motor Y-axis, same for arr1 and arr2s
    axis = "Y"

    if plot_y_axis == False:
        ind_c = 2 # index for camera X-axis, same for arr1 and arr2
        ind_m = 5 # index for motor X-axis, same for arr1 and arr2
        axis = "X"

    fig, ax = plt.subplots(2,1, figsize=(8,6))
    plt.suptitle(csv_name + " - steps vs. free RAM for " + axis + " axis" , fontweight="bold")

    tstart = min(arr1[0,0], arr2[0,0])

    ax[0].plot(arr1[:,ind_t], arr1[:,ind_c],'.-b', label="Pixel Error 1")
    ax[0].plot(arr2[:,ind_t], arr2[:,ind_c],'.-r', label="Pixel Error 2")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("Camera error in pixels")
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Pixels")
    ax[0].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(-.03*time_elapsed, 1.03*time_elapsed) # make graphs have same (asethetic) time length
    #ax[0].set_ylim(-1.5,1.5)
    ax[0].axhline(0, color="black", linewidth=.5)

    ax[1].plot(ram_arr[:,0], ram_arr[:,1],'.-g', label="RAM usage")
    ax[1].set_title("Amount of free RAM over time")
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("MB")
    ax[1].legend(loc="lower right")#, fancybox=True, framealpha=1)
    ax[1].set_xlim(-.03*time_elapsed, 1.03*time_elapsed)
    ax[1].set_ylim(np.min(ram_arr[:,1]), np.max(ram_arr[:,1]))
    ax[1].axhline(0, color="black", linewidth=.5)

    plt.tight_layout()
    plt.show()