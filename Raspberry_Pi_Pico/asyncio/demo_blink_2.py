import uasyncio as asyncio
import time

start = time.time()

async def blink(delay):
    await asyncio.sleep(delay)
    elapsed_time = time.time() - start
    print(f"Blink at {elapsed_time:6.2f}")

start = time.time()
async def main():
    for k in range(5):
        asyncio.create_task(blink(2))
    await asyncio.sleep(10)

asyncio.run(main())
