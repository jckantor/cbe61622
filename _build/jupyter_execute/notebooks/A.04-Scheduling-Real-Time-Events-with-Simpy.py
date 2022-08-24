#!/usr/bin/env python
# coding: utf-8

# # Scheduling Real-Time Events with Simpy
# 
# [Simpy](https://simpy.readthedocs.io/en/latest/index.html) is a Python package for discrete-event simulation in Python. Simpy includes a provision for [real-time simulation](https://simpy.readthedocs.io/en/latest/topical_guides/real-time-simulations.html) which provides an potentially useful tool for coding laboratory experiments with complex scheduling requirements. 
# 
# Keep in mind that Python is not a designed for real-time use, and Simpy should not be trusted for applications requiring time accuracy tighter than, say, 100ms. Futher, it is not an asynchronous implementation, so your interpreter will be blocked during the course of the experiment. But for quick-and-dirty applications with modest performance requirements, Simpy real-time may be a simple solution.

# In[4]:


get_ipython().system('pip install simpy')


# ## Blinkers

# In[5]:


from pymata4 import pymata4
import simpy.rt
import time

led0 = 13
led1 = 9

def blinker(env, board, pin, period):
    board.set_pin_mode_digital_output(pin)
    while True:
        board.digital_write(pin, 1)
        end = time.perf_counter()
        print(f"led {pin:2d}  on at {end-start:5.3f}")
        yield env.timeout(period/2)
        board.digital_write(pin, 0)
        end = time.perf_counter()
        print(f"led {pin:2d} off at {end-start:5.3f}")
        yield env.timeout(period/2)

board = pymata4.Pymata4()

env = simpy.rt.RealtimeEnvironment()
env.process(blinker(env, board, led0, 2.0))
env.process(blinker(env, board, led1, 2.0))
start = time.perf_counter()
env.run(until=20)
board.shutdown()


# ## Asyncio

# In[25]:


import asyncio
from pymata4 import pymata4
import time

led0 = 13
led1 = 9

async def blinker(board, pin, period, start):
    board.set_pin_mode_digital_output(pin)
    while time.perf_counter() < start + 20:
        board.digital_write(pin, 1)
        print(f"led {pin:2d}  on at {round(time.perf_counter()-start, 2)}")
        k = round((time.perf_counter() - start)/(period/2))
        dt = (k+1)*period/2 - (time.perf_counter() - start)
        await asyncio.sleep(dt-0.05)
        board.digital_write(pin, 0)
        print(f"led {pin:2d} off at {round(time.perf_counter()-start, 2)}")
        k = round((time.perf_counter() - start)/(period/2))
        dt = (k+1)*period/2 - (time.perf_counter() - start)
        await asyncio.sleep(dt-0.05)

board = pymata4.Pymata4()

async def expt():
    start = time.perf_counter()
    coroutines = [
        blinker(board, led0, 2.0, start),
        blinker(board, led1, 2.0, start)
    ]
    await asyncio.gather(*coroutines)
    
await expt()
board.shutdown()


# In[ ]:




