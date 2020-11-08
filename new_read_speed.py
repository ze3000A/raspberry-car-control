#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020.11.06    09:33
@author: XHR
超声测距函数，调用distance函数，返回值为一个浮点值，单位cm
"""
#霍尔脉冲读取函数

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  #使用bcm引脚编号方式
GPIO.setwarnings(False)  #禁用警告。如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，会有警告信息。

lu_pin = 19  #编码器连接引脚定义
ld_pin = 26
ru_pin = 16
rd_pin = 20

GPIO.setup(lu_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #gpio口设置为上拉，输入模式
GPIO.setup(ld_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(ru_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)  
GPIO.setup(rd_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)   


'''
chan_list = [19,26,16,20]  #bcm编号的引脚，对应board引脚的35，37，36，38
GPIO.setup(chan_list, GPIO.IN,pull_up_down=GPIO.PUD_UP)
'''

lu_counter=0      #左前轮脉冲初值
ld_counter=0     #左后轮脉冲初值
ru_counter=0      #右前轮脉冲初值
rd_counter=0     #右后轮脉冲初值
 
def my_lu_callback(lu_channel):          #边缘检测回调函数，详情在参见链接中
 global lu_counter  #设置为全局变量
 if GPIO.event_detected(lu_pin):        #检测到一个脉冲则脉冲数加1
  lu_counter++         
def my_ld_callback(ld_channel):          #边缘检测回调函数，详情在参见链接中
 global ld_counter                 #设置为全局变量
 if GPIO.event_detected(ld_pin):        #检测到一个脉冲则脉冲数加1
  ld_counter++
def my_ru_callback(ru_channel):          #边缘检测回调函数，详情在参见链接中
 global ru_counter                 #设置为全局变量
 if GPIO.event_detected(ru_pin):        #检测到一个脉冲则脉冲数加1
  ru_counter++
def my_rd_callback(rd_channel):          #边缘检测回调函数，详情在参见链接中
 global rd_counter                 #设置为全局变量
 if GPIO.event_detected(rd_pin):        #检测到一个脉冲则脉冲数加1
  rd_counter++

GPIO.add_event_detect(lu_pin,GPIO.RISING,callback=my_lu_callback) #在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(ld_pin,GPIO.RISING,callback=my_ld_callback) #在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(ru_pin,GPIO.RISING,callback=my_ru_callback) #在引脚上添加上升临界值检测再回调
GPIO.add_event_detect(rd_pin,GPIO.RISING,callback=my_rd_callback) #在引脚上添加上升临界值检测再回调


GPIO.cleanup()   #释放gpio口

def read_io_speed(io_pin):
 
