import machine
import uasyncio

led = machine.Pin(25, machine.Pin.OUT)
btn = machine.Pin(22, machine.Pin.IN)

# corotuine 
async def blink(delay):
    while True:
        led.toggle()
        await uasyncio.sleep(delay)
        
async def button(btn):
    btn_prev = btn.value()
    while True:
        while (btn.value() == 1) or (btn.value() == btn_prev):
            btn_prev = btn.value()
            await uasyncio.sleep_ms(40)
        led.toggle()
        

async def main():
    uasyncio.create_task(blink(0.2))
    uasyncio.create_task(button(btn))
    await uasyncio.sleep(10)

    
uasyncio.run(main())