from machine import UART, Pin
import time

wifi_ssid = ("ND-guest")

class ESP01S():
    
    def __init__(self, uart_port=0, txPin=16, rxPin=17):
        self.uart = UART(0, baudrate=115200, tx=Pin(txPin), rx=Pin(rxPin))
        self.echo(False)

    def echo(self, enable=False):
        if enable:
            self.send("ATE1")
        else:
            self.send("ATE0")
        
    def send(self, cmd):
        self.uart.write(cmd + "\r\n")

        rxData = ""
        while True:
            if self.uart.any() > 0:
                break
        while self.uart.any() > 0:
            rxData += str(self.uart.read(1))
        rxData = rxData.replace("b'", "")
        rxData = rxData.replace("\\r", "")
        rxData = rxData.replace("\\n", "\n")
        rxData = rxData.replace("'", "")
        return rxData
    
        
esp = ESP01S()
print(esp.send('AT+CIPMUX=1'))
esp.echo(True)
print(esp.send("AT"))