import sys
from pylablib.devices import Newport

if __name__ == "__main__":
    print("Num devices =", Newport.get_usb_devices_number_picomotor())

    with Newport.Picomotor8742():
        print("test")
