# This code is the bare minimum to make a Newport motor move

from pylablib.devices import Newport
import time

print("num devices =", Newport.get_usb_devices_number_picomotor())
with Newport.Picomotor8742() as nwpt:
    for i in range(2):
        #print("available axes =", nwpt.get_all_axes())
        #mot_axis = 1 # 1=Y, 2=X
        nwpt.move_by(2, 1000)
        #nwpt.move_by(2, -1)
        while (nwpt.is_moving(axis=1)):
            time.sleep(.001)
        # while (nwpt.is_moving(axis=2)):
        #     time.sleep(.001)

#nwpt.close()
"""
with Newport.Picomotor8742() as nwpt:
    print("available axes =", nwpt.get_all_axes())
    mot_axis = 1 # 1=Y, 2=X
    nwpt.set_position_reference(mot_axis,0)
    nwpt.move_by(mot_axis, -4000)
"""

print("Program finished")