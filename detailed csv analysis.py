import numpy as np
import matplotlib.pyplot as plt
import csv
import os

csv_name = "mar7 2 none running.csv"
csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
arr = []
with open(csv_file_path, 'r') as f:
    data = csv.reader(f)
    next(data)
    for line in data:
        arr.append(line)
    arr = np.array(arr).astype(float)


# --- Now that I have the data pulled out of the file, I can make graphs with it! (first index is time, second is data type)
#           ["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]


if False:  # This graph shows the x and y error for both cameras over time

    fig, ax = plt.subplots(2,1, figsize=(8,5))
    plt.suptitle(csv_name, fontweight="bold")

    ax[0].plot(arr[:,0]-arr[0,0], arr[:,1],'.-b', label="y err")
    ax[0].plot(arr[:,0]-arr[0,0], arr[:,2],'.-r', label="x err")
    ax[0].plot(arr[:,0]-arr[0,0], arr[:,3],'.-', color="black", label="total err")
    ax[0].set_title("camera 1")
    ax[0].set_xlabel("time")
    ax[0].set_ylabel("pixels")
    ax[0].legend(loc="upper right", fancybox=True, framealpha=1)

    ax[1].plot(arr[:,4]-arr[0,4], arr[:,5],'.-b', label="y err")
    ax[1].plot(arr[:,4]-arr[0,4], arr[:,6],'.-r', label="x err")
    ax[1].plot(arr[:,4]-arr[0,4], arr[:,7],'.-', color="black", label="total err")
    ax[1].set_title("camera 2")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("pixels")
    ax[1].legend(loc="upper right", fancybox=True, framealpha=1)

    plt.tight_layout()
    plt.show()


if False: # This graph recreates the one made in the main program, but better labeling and shape

    plt.figure(figsize=(8,4))
    plt.plot(arr[:,0]-arr[0,0], arr[:,3], '-.b', label="Cam 1")
    plt.plot(arr[:,4]-arr[0,4], arr[:,7], '-.r', label="Cam 2")

    time_elapsed = max(arr[-1,0],arr[-1,4]) - max(arr[0,0],arr[0,4])
    plt.title("Total error for cameras 1,2 over time={:.2f} s".format(time_elapsed), fontweight="bold")
    plt.legend(loc="upper right", fancybox=True, framealpha=1)
    plt.xlabel("time")
    plt.ylabel("pixels")
    plt.show()

if True: # This graph is for SRC presentation

    plt.figure(figsize=(4,4))
    plt.plot(arr[:,0]-arr[0,0], arr[:,3], '-.b', label="Cam 1")
    #plt.plot(arr[:,4]-arr[0,4], arr[:,7], '-.r', label="Cam 2")
    plt.ylim(0,20)

    time_elapsed = max(arr[-1,0],arr[-1,4]) - max(arr[0,0],arr[0,4])
    plt.title("Cam 1, no stabilization", fontweight="bold")
    plt.legend(loc="upper right", fancybox=True, framealpha=1)
    plt.xlabel("time")
    plt.ylabel("pixels")
    plt.savefig("c1,ns")