import numpy as np
import matplotlib.pyplot as plt
import csv
import os

csv_name = "2025-05-17 19-35-56_PI_testing.csv"
csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
arr1 = []
arr2 = []
with open(csv_file_path, 'r') as f:
    data = csv.reader(f)
    next(data)
    for line in data:
        if (line[0] != ""): # If one array was longer than the other, filled in time steps with None
            arr1.append(line[:4])
        if (line[4] != ""):
            arr2.append(line[4:])
    arr1 = np.array(arr1).astype(float) # time_steps1, y_err1, x_err1, tot_err1, time_steps2, y_err2, x_err2, tot_err2
    arr2 = np.array(arr2).astype(float)


# --- Now that I have the data pulled out of the file, I can make graphs with it! (first index is time, second is data type)
#           ["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]


tstart = min(arr1[0,0],arr2[0,0])
tend = max(arr1[-1,0],arr2[-1,0])
time_elapsed = tend - tstart
arr1[:,0] -= tstart
arr2[:,0] -= tstart


if True:  # This graph shows the x and y error for both cameras over time

    fig, ax = plt.subplots(2,1, figsize=(8,5))
    plt.suptitle(csv_name, fontweight="bold")

    tstart = min(arr1[0,0], arr2[0,0])

    ax[0].plot(arr1[:,0], arr1[:,1],'.-b', label="y err 1")
    ax[0].plot(arr1[:,0], arr1[:,2],'.-r', label="x err")
    #ax[0].plot(arr1[:,0], arr1[:,3],'.-', color="black", label="total err")
    ax[0].set_title("camera 1")
    ax[0].set_xlabel("time")
    ax[0].set_ylabel("pixels")
    ax[0].legend(loc="upper right")#, fancybox=True, framealpha=1)
    ax[0].set_xlim(-.03*time_elapsed, 1.03*time_elapsed) # make graphs have same (asethetic) time length

    ax[1].plot(arr2[:,0], arr2[:,1],'.-b', label="y err 2")
    ax[1].plot(arr2[:,0], arr2[:,2],'.-r', label="x err")
    #ax[1].plot(arr2[:,0], arr2[:,3],'.-', color="black", label="total err")
    ax[1].set_title("camera 2")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("pixels")
    ax[1].legend(loc="upper right")#, fancybox=True, framealpha=1)
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