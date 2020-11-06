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
	in_pin = 23 #输入口，设置为board上的16
        gpio.setup(18, gpio.OUT)  #输出口，设置为board上的12
        gpio.setup(in_pin, gpio.IN)    
        gpio.output(18, False)   # 先把输出置0
	
        while gpio.input(in_pin) == 0:
            nosig = time.time()
	
        while gpio.input(in_pin) == 1:
            sig = time.time()
	
        t1 = sig - nosig
	distance = t1 / 0.000058   #计数方式，返回值为  xx cm
        gpio.cleanup()
        return distance
    except:
        distance = None  #异常处理，统一返回值为100
        gpio.cleanup()
        return distance

if __name__ == "__main__":
    a=distance()
    print(a)

