import time
from machine import Pin

class DHT11(object):
    def __init__(self, gpio):
        self.gpio = gpio
        self.pin = Pin(gpio, Pin.OUT)
        self.firstreading = True
        self.pin.value(1)
        self.lastreadtime = 0
        self.data=[0]*5
        self.temp = 0
        self.humid = 0

    def read(self):
        i=0
        j=0
        
        self.data[0] = [0]*5        
        
        # pull pin low for 20 milliseconds
        self.pin.value(0) 
        time.sleep_ms(20)
        
        # pull pin high for 40 microseconds
        self.pin.value(1)
        
        # listen on pin
        self.pin.init(mode=Pin.IN)
        time.sleep_us(200)
        
        time_cnt=0
        while(1 == self.pin.value()):
            time.sleep_us(5)   
            time_cnt = time_cnt + 1
            if(time_cnt > 16): 
                return         
        print(time_cnt)
        
        self.pin.init(mode=Pin.OUT)
        
    def junk(self):
        
        #DHT11将总线拉高至少80us，为发送传感器数据做准备。
        time_cnt=0
        while(1 == pinData.value()):
            time.sleep_us(5)   
            time_cnt = time_cnt+1
            if(time_cnt > 16): 
                return  
        
        
        for j in range(5):
            i = 0
            result=0
            PINC = 1
            for i in range(8):

                while(not (PINC & pinData.value())):  # wait for 50us
                    pass
                    #print('wait 50us')
                time.sleep_us(25)

                if(PINC & pinData.value()):
                    result |=(1<<(7-i))
                while(PINC & pinData.value()):  # wait '0' finish
                    time.sleep_us(5)   
                    time_cnt = time_cnt+1
                    if(time_cnt > 20): 
                        return  
                    #print('wait 1')
            self.data[j] = result

        pinData = Pin(self.Data_pin, Pin.OUT, None)
        pinData.value(1)   

        dht11_check_sum = (self.data[0]+self.data[1]+self.data[2]+self.data[3]&0xff)
        # check check_sum
        if(self.data[4] is not dht11_check_sum):
            print("DHT11 checksum error")
        #print(self.data) 
        if ((j >= 4) and ( self.data[4] == dht11_check_sum)):
            return True 
        return False
        
    def readHumidity(self):
        if (self.read()):
            self.humid = float(self.data[0])
            self.humid = self.humid + float(self.data[1]/10)
        return self.humid

    def readTemperature(self):
        if (self.read()):
            self.temp = float(self.data[2])
            self.temp = self.temp + float(self.data[3]/10)
        return self.temp
    
    def readTempHumid(self):
        if (self.read()):        
            self.temp = float(self.data[2])
            self.temp = self.temp + float(self.data[3]/10)
            self.humid = float(self.data[0])
            self.humid = self.humid + float(self.data[1]/10)
        return self.temp , self.humid

dht = DHT11(1)

while True:
    dht.read()
#while True:
    #dht.read()
    #print(dht.readHumidity())
    #print(dht.readTemperature())
    #print(dht.readTempHumid())
    #time.sleep(1)
    