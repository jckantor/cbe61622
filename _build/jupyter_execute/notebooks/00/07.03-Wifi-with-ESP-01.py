%serialconnect

from machine import UART, Pin
import time

UART_DELAY_MS = 500

class ESP_Error(Exception):
    """Raise custom exceptions for ESP module."""
    pass


class ESP01():
    
    def __init__(self, uart_port=0, tx=16, rx=17, verbose=False):
        self.txPin = Pin(tx)
        self.rxPin = Pin(rx)
        self.uart = UART(0, baudrate=115200, tx=self.txPin, rx=self.rxPin, timeout=10)
        self.verbose = verbose
        if self.verbose:
            self.echo_on()
            print(self.send("AT"))
        else:
            self.echo_off()

    def send(self, cmd, timeout=UART_DELAY_MS):
        if self.verbose:
            print("+"*20 + "\n command:\t", cmd)
            print(" timeout:\t", timeout, "ms")

        # write AT command
        self.uart.write(cmd + "\r\n")
        
        # wait for data to appear in the buffer
        toc = time.ticks_ms()
        while time.ticks_ms() - toc < timeout:
            if self.uart.any():
                break
                
        # read buffer
        rxData = bytes()
        toc = time.ticks_ms()
        while True:
            if (time.ticks_ms() - toc) > timeout:
                break
            if self.uart.any():
                rxData += self.uart.read(1)
                toc = time.ticks_ms()
                
        # report response
        try:
            rxData = rxData.decode()
        except UnicodeError:
            if self.verbose:
                print("Unicode error encountered, returning byte string.")
        if self.verbose:
            print("response:\n", rxData)
            print("-"*20)
            
        if "OK" in rxData:
            status = "OK"
        elif "FAIL" in rxData:
            status = "FAIL"
        elif "busy p..." in rxData:
            status = "BUSY"
        elif "ERROR" in rxData:
            status = "ERROR"
        else:
            status = "UNKNOWN"
            
        if status != "OK":
            print("status = ", status)
            
        return rxData
            
        
    def echo_off(self):
        """Turn off the echo feature of the ESP-01."""
        return self.send("ATE0")
    
    def echo_on(self):
        """Turn on the echo feature of the ESP-01."""
        return self.send("ATE1")
    
    def restart(self):
        """Restart ESP8266 module."""
        return self.send("AT+RST", 500)
    
    def get_version(self):
        """Return firmware version."""
        return self.send("AT+GMR")
    
    def set_wifi_mode(self, mode=1):
        return self.send("AT+CWMODE_CUR=" + str(mode))
        
    def get_wifi_mode(self):
        response = self.send("AT+CWMODE_CUR?")
        if response is not None:
            if "1" in response:
                return "STA"
            elif "2" in response:
                return "SoftAP"
            elif "3" in response:
                return "SoftAP +  STA"
            else:
                raise ESP_Error("Unrecognized WiFi mode returned: \n" + response)
        return None
        
    def get_APs(self):
        return self.send("AT+CWLAP", 5000)
    
    def connect(self, ssid, pwd):
        cmd = "AT+CWJAP=" + '"' + ssid + '"' + ',' + '"' + pwd + '"'
        return self.send(cmd.encode(), timeout=10000)
    
    def get_IP_address(self):
        return self.send("AT+CIFSR")
    
    def set_connection_mode(self, mode=1):
        return self.send("AT+CIPMUX=1")
    
    def webserver(self):
        return self.send("AT+CIPSERVER=1,80", 2000)

# startup

esp = ESP01(verbose=True)
esp.restart()
esp.get_version()
esp.set_wifi_mode(1)

# connection
#esp.connect("Wilder\u2019s Edge", "FreyaWatson")
print(esp.connect("ND-guest", ""))
esp.set_connection_mode()
esp.get_IP_address()

# webserver

def read_http_request():
    req = ""
    while True:
        recv = bytes()
        line = 0
        if esp.uart.any():
            recv = esp.uart.readline()
        recv = recv.decode()
        recv = recv.replace("\r\n", "\n")
        if len(recv) == 1:
            break
        else:
            if len(recv) > 0:
                req += recv
    
    lines = req.split("\n")
    if "+IPD" in lines[0]:
        print("http request received")
    else:
        print("AT response received")
    for k, line in enumerate(lines):
         print(k, ":", line)
        
        
def send_line(msg):
    esp.send(f"AT+CIPSEND=0,{len(msg)+2}", 10)
    esp.send(msg, 10)
    
def send_http_response(n):
    send_line("HTTP/1.1 200 OK")
    send_line("Content-type:text/html")
    send_line("Connection: close")
    send_line("");
    send_line("<html><body>")
    send_line("<h1>Hello World!</h1>")
    send_line(f"message {n}")
    send_line("</body></html>")
    esp.send("AT+CIPCLOSE=0")
    
esp.webserver()
recv_buf = bytes()
toc = time.ticks_ms()
n = 0
while True:
    read_http_request()
    send_http_response(n)
    n += 1
    

    if esp.uart.any():
        recv_buf += esp.uart.readline()
    recv = recv_buf.decode()
    if len(recv) > 0:
        print(recv)
        recv_buf = bytes()
        if "+IPD" in recv:
            time.sleep(1)
            sendline("HTTP/1.1 200 OK")
            sendline("Content-type:text/html")
            sendline("Connection: close")
            sendline("")
            sendline("<h1>Hello World!</h1>")
            sendline(f"time = {(time.ticks_ms() - toc)/1000} seconds")
            esp.send("AT+CIPCLOSE=0")
            time.sleep(1)
            
            

print(esp.get_wifi_mode())

      
esp = ESP01S(verbose=True)
#print(esp.restart())
print(esp.version())
print(esp.set_wifi_mode(1))
print(esp.get_wifi_mode())
print(esp.send("AT+CWJAP?"))

print(esp.connect_wifi("Wilder\u2019s Edge", "FreyaWatson"))

print(esp.send("AT+CWJAP?"))

resp =  esp.get_wifi_APs() 

aps = [r for r in resp.split("\r\n") if "+CWLAP:" in r]
print(aps)


