# This code is to test if the motors will randomly stop working for a few minutes at a time?
    # Doesn't look like this is the case. I'll save this code anyways because deleting code is a bad idea

from pylablib.devices import Newport
import time

start_time = time.time()

parity = 1
prev_time = start_time
delta_times = []

with Newport.Picomotor8742() as nwpt:
    while time.time() < start_time + 120: # n second timer
        parity = -parity
        ax = 1
        nwpt.move_by(ax, parity)
        while (nwpt.is_moving(axis=ax)):
            time.sleep(.001)
        
        curr_time = time.time()
        delta_times.append(curr_time - prev_time)
        #time.sleep(.2)
        prev_time = time.time()

import matplotlib.pyplot as plt
import numpy as np

print("Max time is",str(np.array(delta_times).max()))

plt.plot(np.arange(0,len(delta_times)), delta_times)
plt.show()