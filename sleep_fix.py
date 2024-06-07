import time
import ctypes
import ctypes.wintypes
import contextlib

winmm = ctypes.windll.winmm
winmm.timeBeginPeriod.argtypes = [ctypes.c_uint]
winmm.timeEndPeriod.argtypes = [ctypes.c_uint]

class TIMECAPS(ctypes.Structure):
    _fields_ = (('wPeriodMin', ctypes.wintypes.UINT),
                ('wPeriodMax', ctypes.wintypes.UINT))

@contextlib.contextmanager
def SleepModifier(min_sleep):
    caps = TIMECAPS()
    winmm.timeGetDevCaps(ctypes.byref(caps), ctypes.sizeof(caps))
    min_sleep = min(max(min_sleep, caps.wPeriodMin), caps.wPeriodMax)
    winmm.timeBeginPeriod(min_sleep)
    yield
    winmm.timeEndPeriod(min_sleep)


def Sleeper(delay_ms):
    with SleepModifier(.001):
        t1 = time.time()
        time.sleep(delay_ms/1000)
        t2 = time.time()
    return (t2-t1)


num = 10
tot = 0
delay = 1
for i in range(num):
    s = Sleeper(delay)
    print("slept for", f'{s:.5}')
    tot += s

print("requested delay =", delay, "ms")
print(f"average = {tot/num:.5}")