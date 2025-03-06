import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# # --- Save the error data! I want to make figures from this later! ---
# csv_name = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + ' 2_cam_stabilization.csv'
# with open(os.path.join(os.getcwd(),'CSV',csv_name), 'w', newline="") as f:
#     writer = csv.writer(f)
#     names = [["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]]

#     writer.writerows(names)
#     writer.writerows(np.transpose([time_steps_1,y_vals1,x_vals1,tot_err1, time_steps_2,y_vals2,x_vals2,tot_err2]))

csv_name = "mar5 1 fighting PI.csv"
csv_file_path = os.path.join(os.getcwd(),'CSV',csv_name)
with open(csv_file_path, 'r') as f:
    data = csv.reader(f)
    next(data)
    arr = []
    for line in data:
        arr.append(line)
    arr = np.array(arr).astype(float)
    print(arr.shape)

    #  [["time_steps1","y_err1","x_err1","tot_err1","time_steps2","y_err2","x_err2","tot_err2"]]

    fig, ax = plt.subplots(2,1, figsize=(8,5))
    plt.suptitle(csv_name, fontweight="bold")

    ax[0].plot(arr[:,0]-arr[0,0], arr[:,1],'.-b', label="y err")
    ax[0].plot(arr[:,0]-arr[0,0], arr[:,2],'.-r', label="x err")
    ax[0].plot(arr[:,0]-arr[0,0], arr[:,3],'.-', color="black", label="total err")
    ax[0].set_title("camera 1")
    ax[0].set_xlabel("time")
    ax[0].set_ylabel("pixels")
    ax[0].legend(loc="upper left")

    ax[1].plot(arr[:,4]-arr[0,4], arr[:,5],'.-b', label="y err")
    ax[1].plot(arr[:,4]-arr[0,4], arr[:,6],'.-r', label="x err")
    ax[1].plot(arr[:,4]-arr[0,4], arr[:,7],'.-', color="black", label="total err")
    ax[1].set_title("camera 2")
    ax[1].set_xlabel("time")
    ax[1].set_ylabel("pixels")
    ax[1].legend(loc="upper left")

    plt.tight_layout()
    plt.show()