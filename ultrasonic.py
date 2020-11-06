#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020.11.06    09:33
@author: XHR

超声测距函数，调用distance函数，返回值为一个浮点值，单位cm
"""

import RPi.GPIO as gpio
import time


def distance():
    try:
        gpio.setmode(gpio.BCM)   #统一设置为bcm编码格式
	trig_pin = 18  #树莓派输出口，设置为board上的12，发送10us的信号使超声波模块工作
	echo_pin = 23  #输入口，设置为board上的16
        gpio.setup(trig_pin, gpio.OUT)  
        gpio.setup(echo_pin, gpio.IN)    
	
	gpio.output(trig_pin, True)   # 把输出置1
	time.sleep(0.00001)  #10us
        gpio.output(trig_pin, False)   # 把输出置0
	
        while gpio.input(echo_pin) == 0:
            nosig = time.time()
	
        while gpio.input(echo_pin) == 1:
            sig = time.time()
	
        t1 = sig - nosig
	distance = t1 * 17150   #计数方式，假设声波速度343m/s。返回值为  xx cm
        gpio.cleanup()
        return distance
    except:
        distance = None  #异常处理，读不到就返回None
        gpio.cleanup()
        return distance

if __name__ == "__main__":
    try:
        while True:
            dist = distance()
            print("Measured Distance = {:.2f} cm".format(dist))
            time.sleep(1)
	
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()


