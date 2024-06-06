import time

def sleeper(delay):
    t1 = time.time()
    time.sleep(delay)
    t2 = time.time()
    return (t2-t1)


num = 10
tot = 0
delay = .001
for i in range(num):
    s = sleeper(delay)
    print(f'{s:.5}')
    tot += s

print("requested delay =", delay)
print(f"        average = {tot/num:.5}")