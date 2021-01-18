import pigpio
pi = pigpio.pi()
pi.set_PWM_frequency(14, 50)#设定14号引脚产生的pwm波形的频率为50Hz，BCM编码格式
pi.set_PWM_range(14, 2000) 
#指定要把14号引脚上的一个pwm周期分成多少份，这里是分成2000份，这个数据的范围是25-40000		
pi.set_PWM_dutycycle(14,150) #指定pwm波形的占空比，这里的占空比为150/2000,2000是上一个函数设定的
