#霍尔脉冲读取函数

import RPi.GPIO as GPIO


 GPIO.setup(24, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过18号引脚读取左轮脉冲数据
 GPIO.setup(25, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过35号引脚读取右轮脉冲数据
 GPIO.setup(27, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过18号引脚读取左轮脉冲数据
 GPIO.setup(28, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过35号引脚读取右轮脉冲数据
 counter=0      #左轮脉冲初值
 counter1=0     #右轮脉冲初值
 def my_callback(channel):          #边缘检测回调函数，详情在参见链接中
     global counter                 #设置为全局变量
     if GPIO.event_detected(18):        #检测到一个脉冲则脉冲数加1
         counter=counter+1
 def my_callback1(channel1):            #这里的channel和channel1无须赋确定值，但笔者测试过，不能不写
     global counter1
     if GPIO.event_detected(35):
         counter1=counter1+1
 GPIO.add_event_detect(18,GPIO.RISING,callback=my_callback) #在引脚上添加上升临界值检测再回调
 GPIO.add_event_detect(35,GPIO.RISING,callback=my_callback1)

