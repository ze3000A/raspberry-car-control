#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020.11.21    17:10
在原来的test1文件中尝试加入超声测距函数
@author: XHR
"""

from __future__ import division
import time
import Adafruit_PCA9685
import serial
import string
import RPi.GPIO as GPIO
from ultrasonic import *

CarSpeedControl = 2000
g_CarState = 0

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


'''
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
'''

pwm.set_pwm_freq(50)
Car_Speed=2048
print(" all is down")

#最大频率是4096，4096时达到最高速度，1024，2048，3072

#向前，两个舵机向相同方向旋转
#四个轮子都向前转时，轴向速度相互抵消，只剩下向前的速度，则小车向前，后退同理

def straight_car(Speed):
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU1,0,Speed)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD1,0,Speed)
    pwm.set_pwm(RD2,0,0)
    print('car straight with the speed of ',Speed/4096)

def back_car(Speed):
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(RU2,0,Speed)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD1,0,0)
    pwm.set_pwm(RD2,0,Speed)
    print('car back with the speed of ',Speed/4096)

#而左上方B轮反转，右下方A轮反转的时候，合速度为向左的速度，则小车向左，向右平移同理
def left_car(Speed):
    pwm.set_pwm(LU1,0,Speed)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(LD2,0,Speed)
    pwm.set_pwm(RD1,0,0)
    pwm.set_pwm(RD2,0,0)
    print('car left with the speed of ',Speed/4096)

def right_car(Speed):
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(LU2,0,Speed)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD1,0,Speed)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD1,0,0)
    pwm.set_pwm(RD2,0,0)
    print('car right with the speed of ',Speed/4096)

#底盘左侧轮子正转右侧轮子反转，实现底盘向右旋转，即顺时针旋转。逆时针旋转同理。左右左右
def turnleft_car(Speed):
    pwm.set_pwm(LU2,0,Speed)
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(RU2,0,Speed)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD1,0,Speed)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(RD1,0,Speed)
    pwm.set_pwm(RD2,0,0)
    print('car round left with the speed of ',Speed/4096)

def turnright_car(Speed):
    pwm.set_pwm(LU1,0,Speed)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU1,0,Speed)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(LD2,0,Speed)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD2,0,Speed)
    pwm.set_pwm(RD1,0,0)
    print('car round right with the speed of ',Speed/4096)

def brake():
    pwm.set_pwm(LU1,0,0)
    pwm.set_pwm(LU2,0,0)
    pwm.set_pwm(RU2,0,0)
    pwm.set_pwm(RU1,0,0)
    pwm.set_pwm(LD2,0,0)
    pwm.set_pwm(LD1,0,0)
    pwm.set_pwm(RD1,0,0)
    pwm.set_pwm(RD2,0,0)
    print('car stop')

#这段代码奇奇怪怪的，没用，但可以用作保留
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 50       # 50 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

#这段代码是舵机角度控制代码，通道指前面定义的act1 ，act2之类的，angle指输入0---180的角度
'''
def set_servo_angle(channel,angle):
    angle=4096*((angle*11)+500)/20000
    pwm.set_pwm(channel,0,int(angle))
    print('舵机',channel,'工作,角度为',angle,'度')
'''
def convert_angle(angle):
    ms=0.5+(angle/135)
    return 4096*ms*54/1000

def set_servo_angle(channel,angle):
    #angle=4096*((angle*11)+500)/20000
    angle=convert_angle(angle)
    pwm.set_pwm(channel,0,int(angle))
    print('steering',channel,' had worked,the angle is',angle,' degree')


def serialEvent(str,Car_Speed):
    if str=='w':
        straight_car(Car_Speed)
    elif str=='s':
        back_car(Car_Speed)
    elif str=='a':
        left_car(Car_Speed)
    elif str=='d':
        right_car(Car_Speed)
    elif str=='q':
        turnleft_car(Car_Speed)
    elif str=='e':
        turnright_car(Car_Speed)
    elif str=='x':
        brake()
    elif str=='t':
        dist=distance()
        if dist <500:
            print("Measured Distance = {:.2f} cm".format(dist))
        else:
            print("distance measure out of range")
    else:
        print('no car command')

    try:
        num=int(str[0])
        angle=int(str[1:4])
        set_servo_angle(num,angle)
    except :
        print('no steering command')


if __name__ == "__main__":
    try:

        while True:
            in_str = raw_input('请输入控制指令：')
            #print(in_str,' direction recevied')
            time.sleep(1)
            if in_str=='c':
                Car_Speed = int(raw_input('请输入速度：'))
                in_str=pre_str
            #print(Car_Speed,' car speed recevied')
            time.sleep(1)
            serialEvent(in_str,Car_Speed)
            pre_str=in_str


    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




