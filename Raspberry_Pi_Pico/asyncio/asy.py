import machine
import uasyncio as asyncio

x = 0

async def blink(gpio, time_ms):
    global x
    while True:
        await asyncio.sleep_ms(time_ms)
        print("Hi", x)
        led.toggle()
        
async def adc(gpio, time_ms):
    global x
    adc = machine.ADC(gpio)
    while True:
        await asyncio.sleep_ms(time_ms)
        x = adc.read_u16()
        print(x)

buffer = Buffer()
led = machine.Pin(25, machine.Pin.OUT)

async def main():
    asyncio.create_task(blink(led, 100))
    asyncio.create_task(adc(27, 2000))
    await asyncio.sleep(10)
    
asyncio.run(main())
