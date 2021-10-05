# determine speed of looping operations

import machine
import utime

print("Speed Tests\n")


# loop speed

N = 100000

# while loop

print(f"Execute {N} while loops: ", end="")
tic = utime.ticks_us()
count = 0
while count < N:
    count += 1
toc = utime.ticks_us()
print(f"{(toc-tic)/N:0.2f} microseconds per loop")

# for loop

print(f"Execute {N} for loops: ", end="")
tic = utime.ticks_us()
for n in range(N):
    pass
toc = utime.ticks_us()
print(f"{(toc-tic)/N:0.2f} microseconds per loop")

# look up

print(f"Look up {N} values in a dictionary: ", end="")
d = {n: n for n in range(100)}
tic = utime.ticks_us()
for k in range(N):
    x = d[k % 100]
toc = utime.ticks_us()
print(f"{(toc-tic)/N:0.2f} microseconds per loop")


print(f"Look up {N} values in a list: ", end="")
d = [n for n in range(100)]
tic = utime.ticks_us()
for k in range(N):
    x = d[k % 100]
toc = utime.ticks_us()
print(f"{(toc-tic)/N:0.2f} microseconds per loop")

