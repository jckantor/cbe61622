from machine import I2C, Pin
import time
class LCD1602(object):
    #commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    #flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    #flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    #flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    #flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00
    
    def __init__(self, i2c, lines, dotsize, lcd_addr=0x3E):
        self.i2c = i2c
        self.lcd_address = lcd_addr
        self.line = lines
        self.currline = 0;
        self.display_control = self.LCD_DISPLAYON
        if (lines > 1):
            self.display_control |= self.LCD_2LINE
        #for some 1 line displays you can select a 10 pixel high font
        if (dotsize != 0 & lines == 1):
            self.display_control |= self.LCD_5x10DOTS

        #SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        #according to datasheet, we need at least 40ms after power rises above 2.7V
        #before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
        time.sleep_ms(50)
        
        #this is according to the hitachi HD44780 datasheet
        #page 45 figure 23

        #Send function set command sequence
        self.command(self.LCD_FUNCTIONSET | self.display_control)
        time.sleep_us(4500) #wait more than 4.1ms
        
        #second try
        self.command(self.LCD_FUNCTIONSET | self.display_control)
        time.sleep_us(150)
        
        #third go
        self.command(self.LCD_FUNCTIONSET | self.display_control)
        
        #finally, set # lines, font size, etc.
        self.command(self.LCD_FUNCTIONSET | self.display_control)

        #turn the display on with no cursor or blinking default
        self.display_mode = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        
        self.display()

        #clear it off
        self.clear()

        #Initialize to default text direction (for romance languages)
        self.display_mode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        #set the entry mode
        self.command(self.LCD_ENTRYMODESET | self.display_mode)  
        
    def clear(self):
        self.command(self.LCD_CLEARDISPLAY)   #clear display, set cursor position to zero
        time.sleep_ms(2)                  #this command takes a long time!
        
    def home(self):
        self.command(self.LCD_RETURNHOME)     #set cursor position to zero
        time.sleep_ms(2)                  #this command takes a long time!
        
    def setCursor(self, col, row):
        col = (col | 0x80) if row == 0 else (col | 0xc0)
        self.command(col)
    #Turn the display on/off (quickly)
    def no_display(self):
        self.display_control &= ~self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
        
    def display(self):
        self.display_control |= self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
    #Turns the underline cursor on/off
    def no_cursor(self):
        self.display_control &= ~self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
            
    def cursor(self):
        self.display_control |= self.LCD_CURSORON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
    #Turn on and off the blinking cursor    
    def no_blink(self):
        self.display_control &= ~self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
            
    def blink(self):
        self.display_control |= self.LCD_BLINKON
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
             
        
    def autoscroll(self):
        self.display_control |= self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
        
    def no_autoscroll(self):
        self.display_control &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.command(self.LCD_DISPLAYCONTROL  | self.display_control)
        
    def create_char(self, location, charmap):
        location &= 0x07
        self.command(LCD_SETCGRAMADDR | (location << 3))
        dta = bytearray([charmap])
        self.i2c.writeto_mem(self.address, 0x40, dta)
        
    def command(self, command):
        command = bytearray([command])
        self.i2c.writeto_mem(self.lcd_address, 0x80, command)        
        
    def write(self, command):
        command = bytearray([command])
        self.i2c.writeto_mem(self.lcd_address, 0x40, command)
        
    def print(self, text):
        for char in text:
            self.write(ord(char))


        
class LCD1602_RGB(LCD1602):
    # color define 
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3

    REG_RED = 0x04        # pwm2
    REG_GREEN = 0x03      # pwm1
    REG_BLUE = 0x02       # pwm0

    REG_MODE1 = 0x00
    REG_MODE2 = 0x01
    REG_OUTPUT = 0x08
    def __init__(self, i2c, lines, dotsize, lcd_addr=0x3E, rgb_addr=0x62):
        self.rgb_address = rgb_addr
        LCD1602.__init__(self, i2c, lines, dotsize, lcd_addr)
        
        #backlight init
        self.set_reg(0, 0)
        self.set_reg(1, 0)
        self.set_reg(0x08, 0xAA) #all led control by pwm
        self.set_rgb(255, 255, 255)

    def set_reg(self, addr, value):
        value = bytearray([value])
        self.i2c.writeto_mem(self.rgb_address, addr, bytearray([]))
        self.i2c.writeto_mem(self.rgb_address, addr, value)

    def set_rgb(self, red, green, blue):
        r = int(red)
        g = int(green)
        b = int(blue)
        self.set_reg(self.REG_RED, r)
        self.set_reg(self.REG_GREEN, g)
        self.set_reg(self.REG_BLUE, b)
    
    def set_color(self, color):
        if(color == 0):
            self.set_rgb(255, 255, 255)
        elif(color == 1):
            self.set_rgb(255, 0, 0)
        elif(color == 2):
            self.set_rgb(0, 255, 0)
        elif(color == 3):
            self.set_rgb(0, 0, 255)
        else:
            return
        
        

