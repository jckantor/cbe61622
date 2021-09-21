import machine
import time

# machine characteristics
print(f"machine characteristics")

# machine unique id.
print(f"    unique id = {machine.unique_id()}")

# machine frequency
print(f"    frequency = {machine.freq()}")

# machine reset
machine.soft_reset()