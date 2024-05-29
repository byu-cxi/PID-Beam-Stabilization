# This code is the bare minimum to make a Newport motor move

from pylablib.devices import Newport

print("num devices =", Newport.get_usb_devices_number_picomotor())
with Newport.Picomotor8742() as nwpt:
    print("available axes =", nwpt.get_all_axes())
    mot_axis = 1 # 1=Y, 2=X
    nwpt.set_position_reference(mot_axis,0)
    nwpt.move_by(mot_axis, 1000)



print("Program finished")