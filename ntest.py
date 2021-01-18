#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on 2020.11.08    11:29
@author: XHR
霍尔脉冲读取函数
"""

import RPi.GPIO as GPIO
import time
import threading

def my_lu_callback(lu_channel):
    global lu_counter
    if GPIO.event_detected(lu_pin):        #检测到一个脉冲则脉冲数加1
        lu_counter+=1 

def my_ld_callback(ld_channel):
    global ld_counter
    if GPIO.event_detected(ld_pin):        #检测到一个脉冲则脉冲数加1
        ld_counter+=1

def my_ru_callback(ru_channel):
    global ru_counter
    if GPIO.event_detected(ru_pin):        #检测到一个脉冲则脉冲数加1
        ru_counter+=1

def my_rd_callback(rd_channel):
    global rd_counter
    if GPIO.event_detected(rd_pin):        #检测到一个脉冲则脉冲数加1
        rd_counter+=1

def readspeed():
    '''
        GPIO.setwarnings(False)  #禁用警告。如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，会有警告信息。
        GPIO.setup(io_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #gpio口设置为上拉，输入模式
        io_counter=0      #左前轮脉冲初值
    '''

    GPIO.setmode(GPIO.BCM)  #使用bcm引脚编号方式
    GPIO.setwarnings(False)  #禁用警告。如果RPi.GRIO检测到一个引脚已经被设置成了非默认值，会有警告信息。

    
    GPIO.setup(lu_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #gpio口设置为上拉，输入模式
    GPIO.setup(ld_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.setup(ru_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)  
    GPIO.setup(rd_pin, GPIO.IN,pull_up_down=GPIO.PUD_UP)   
    
    '''
    chan_list = [19,26,16,20]  #bcm编号的引脚，对应board引脚的35，37，36，38
    GPIO.setup(chan_list, GPIO.IN,pull_up_down=GPIO.PUD_UP)
    '''
    
    global lu_counter
    global ld_counter
    global ru_counter
    global rd_counter
    
    lu_counter=0      #左前轮脉冲初值
    ld_counter=0     #左后轮脉冲初值
    ru_counter=0      #右前轮脉冲初值
    rd_counter=0     #右后轮脉冲初值
    
    GPIO.add_event_detect(lu_pin,GPIO.RISING,callback=my_lu_callback) #在引脚上添加上升临界值检测再回调
    GPIO.add_event_detect(ld_pin,GPIO.RISING,callback=my_ld_callback) #在引脚上添加上升临界值检测再回调
    GPIO.add_event_detect(ru_pin,GPIO.RISING,callback=my_ru_callback) #在引脚上添加上升临界值检测再回调
    GPIO.add_event_detect(rd_pin,GPIO.RISING,callback=my_rd_callback) #在引脚上添加上升临界值检测再回调
    
    time.sleep(1)
    print(lu_counter,ld_counter,ru_counter,rd_counter)
    GPIO.cleanup([lu_pin,ld_pin,ru_pin,rd_pin])   #释放gpio口
    return 0

def thread1_pid_control():
    run_flag=1
    while(run_flag):
        speed=readspeed()
	    run_flag=int(input('\n input 1 start next exam ,input 0 to shut down'))

if __name__ == "__main__":
    lu_pin = 19  #编码器连接引脚定义
    ld_pin = 26
    ru_pin = 16
    rd_pin = 20
    thread1 = threading.Thread(target = thread1_pid_control, args = ())

    try:
	    thread1.start()
        while True:
		    thread1.join()
            print(" return main  thread")
			time.sleep(10)
            #print(lu_counter，ld_counter,ru_counter,rd_counter)
	
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()