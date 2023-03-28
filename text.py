#滚开留下
#温度距离显示屏

import RPi.GPIO as GPIO
import ADC0834
import time
import math
import requests
import smbus
while True:
    TRIG = 23
    ECHO = 24
    BUS = smbus.SMBus(1)
    LCD_ADDR = 0x27

    def init():

        ADC0834.setup()

    def setup():

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)
    def distance():
        GPIO.output(TRIG, 0)
        time.sleep(0.000002)

        GPIO.output(TRIG, 1)
        time.sleep(0.00001)
        GPIO.output(TRIG, 0)

        
        while GPIO.input(ECHO) == 0:
            a = 0
        time1 = time.time()
        while GPIO.input(ECHO) == 1:
            a = 1
        time2 = time.time()

        during = time2 - time1
        return during * 340 / 2 * 100

     
    def  loop():

    #         while True:
                analogVal = ADC0834.getResult()
                Vr = 5 * float(analogVal) / 255
                Rt = 10000 * Vr / (5 - Vr)
                temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
                Cel = temp - 273.15
                Fah = Cel * 1.8 + 32
                dis = distance()
                www = ('Celsius: %.2f °C  Fahrenheit: %.2f ℉' % (Cel, Fah))
                nnn = ('Distance: %.2f' % dis)
                global hhh
                hhh = int(dis)
                str1="20TE503"
                #str2= str(Cel) + str(dis)
                str5 = www + nnn
                xiaoming ={"tag":"20TE503","value":"36.5555555"}
                xiaoming["tag"]= str1
                xiaoming["value"]= str5
                data = xiaoming
                result = requests.post("http://allocator.daiichi-koudai.com/storeavalue", data=data)
                time.sleep(3)
                #return hhh
    def destroy():
        GPIO.cleanup()
    def send_command(comm):
        # Send bit7-4 firstly
        buf = comm & 0xF0
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        BUS.write_byte(LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (comm & 0x0F) << 4
        buf |= 0x04               # RS = 0, RW = 0, EN = 1
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        BUS.write_byte(LCD_ADDR ,buf)

    def send_data(data):
        # Send bit7-4 firstly
        buf = data & 0xF0
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        BUS.write_byte(LCD_ADDR ,buf)

        # Send bit3-0 secondly
        buf = (data & 0x0F) << 4
        buf |= 0x05               # RS = 1, RW = 0, EN = 1
        BUS.write_byte(LCD_ADDR ,buf)
        time.sleep(0.002)
        buf &= 0xFB               # Make EN = 0
        BUS.write_byte(LCD_ADDR ,buf)

    def init_lcd():
        try:
            send_command(0x33) # Must initialize to 8-line mode at first
            time.sleep(0.005)
            send_command(0x32) # Then initialize to 4-line mode
            time.sleep(0.005)
            send_command(0x28) # 2 Lines & 5*7 dots
            time.sleep(0.005)
            send_command(0x0C) # Enable display without cursor
            time.sleep(0.005)
            send_command(0x01) # Clear Screen
        except:
            return False
        else:
            return True

    def clear_lcd():
        send_command(0x01) # Clear Screen

    def open_light():  # Enable the backlight
        BUS.write_byte(0x27,0x08)
        BUS.close()

    def print_lcd(x, y, str):
        if x < 0:
            x = 0
        if x > 15:
            x = 15
        if y <0:
            y = 0
        if y > 1:
            y = 1

        # Move cursor
        addr = 0x80 + 0x40 * y + x
        send_command(addr)

        for chr in str:
            send_data(ord(chr))
    def zyb():
        smbus.clear()
        
    def zhang_yb():
        #distance()
        #dis = distance()
        #hhh = int(dis)
        #init_lcd()
        if hhh<1000:
             init_lcd()
             print_lcd(0, 0, 'Keep away!')
             print_lcd(8, 1, 'gun kai')
             open_light()
        else:
             init_lcd()

             print_lcd(0, 0, 'Dont leave!')
             print_lcd(8, 1, 'liu xia')
             open_light()
        #open_light()

    if __name__ == '__main__':

            init()
            setup()

            try:
                loop()
                zhang_yb()
            except KeyboardInterrupt:
                destroy()
                ADC0834.destroy()
                zyb()
                time.sleep(5)
