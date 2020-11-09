#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020.11.04    09:08

@author: XHR
"""

from __future__ import division
import time
import Adafruit_PCA9685
import serial
import string
import RPi.GPIO as GPIO

CarSpeedControl = 2000
g_CarState = 0 
NewLineReceived = 0
InputStringcache = ''
pwm = Adafruit_PCA9685.PCA9685()

#电机驱动接口定义
LU1=9
LU2=8
RU1=11
RU2=10
LD1=14
LD2=15
RD1=12
RD2=13
#舵机接口定义
Act1=0
Act2=1
Act3=2

SERVO=7
InputString = ''



#状态值定义
enSTOP = 0
enRUN =1
enBACK = 2
enLEFT = 3
enRIGHT = 4
enTLEFT =5
enTRIGHT = 6

run_car  = '1'  #按键前
back_car = '2'  #按键后
left_car = '3'  #按键左
right_car = '4' #按键右
stop_car = '0'  #按键停
turn_clockwise = '5' #按键顺时针
turn_anticlockwise = '6' #按键逆时针

pwm.set_pwm_freq(50)

#最大频率是4096，4096时达到最高速度，1024，2048，3072

#向前，两个舵机向相同方向旋转
#四个轮子都向前转时，轴向速度相互抵消，只剩下向前的速度，则小车向前，后退同理

def straight_car(Speed):
    pwm.set_pwm(LU1,0,Speed)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU1,0,Speed)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD1,0,Speed)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD1,0,Speed)
    pwm.set_pwm(RD2,0,0)

def back_car(Speed):
    pwm.set_pwm(LU2,0,Speed)
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(RU2,0,Speed)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD2,0,Speed)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD2,0,Speed)
    pwm.set_pwm(RD1,0,0)	

#而左上方B轮反转，右下方A轮反转的时候，合速度为向左的速度，则小车向左，向右平移同理
def left_car(Speed):
    pwm.set_pwm(LU2,0,Speed)
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(RU1,0,Speed)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD1,0,Speed)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD2,0,Speed)
    pwm.set_pwm(RD1,0,0)
	
def right_car(Speed):
    pwm.set_pwm(LU1,0,Speed)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU2,0,Speed)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD2,0,Speed)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD1,0,Speed)
    pwm.set_pwm(RD2,0,0)

#底盘左侧轮子正转右侧轮子反转，实现底盘向右旋转，即顺时针旋转。逆时针旋转同理。左右左右
def turnleft_car(Speed):
    pwm.set_pwm(LU2,0,Speed)
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(RU1,0,Speed)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD2,0,Speed)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD1,0,Speed)
    pwm.set_pwm(RD2,0,0)
	
def turnright_car(Speed):
    pwm.set_pwm(LU1,0,Speed)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU2,0,Speed)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD1,0,Speed)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD2,0,Speed)
    pwm.set_pwm(RD1,0,0)

def brake():
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD1,0,0)
    pwm.set_pwm(RD2,0,0)
	
	
def serialEvent(str):
    global InputString
    global InputStringcache
    global StartBit
    global NewLineReceived
    InputString = ''
    if str=='w':
        straight_car(Car_Speed)
    if str=='s':
        doen_car(Car_Speed)
    if str=='a':
        left_car(Car_Speed)
    if str=='w':
        straight_car(Car_Speed)

if __name__ == "__main__":
    try:
        while True:
            str = input('请输入：')
            time.sleep(1)
	
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

	
	
