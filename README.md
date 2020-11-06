# raspberry-car-control

#### 小车控制
##### PCA设置pwm函数的代码：
```
def set_pwm(self, channel, on, off):
        """Sets a single PWM channel."""
        self._device.write8(LED0_ON_L+4*channel, on & 0xFF)
        self._device.write8(LED0_ON_H+4*channel, on >> 8)
        self._device.write8(LED0_OFF_L+4*channel, off & 0xFF)
        self._device.write8(LED0_OFF_H+4*channel, off >> 8)
```
调用的时候：
```
    pwm.set_pwm(LED8,0,Speed)
    pwm.set_pwm(LED9,0,0)
```
把led8和led9分别连接电机两端，就相当于 led9的那个端口是gnd，一直是0电位，led8的端口，输出pwm波，占空比是speed
例如：M1电AO1和AO2为电机的驱动（可以理解为正负极）由电机驱动芯片的AIN1和AIN2发送PWM控制，当AN1发PWM，AN2置0实现电机M1正转。
而在电路原理图上，led8就是AIN2；led9就是AIN1
##### PCA引脚定义及拓展板上的连接：
而PCA9685这个芯片是16路PWM驱动，其编号在驱动板左下角处,从LED0开始，一直到RINB（15），分别是编号0--15，为了方便写代码，我们调用的时候最好写如下的定义

```
LED8=8
LED9=9
LINA=12
LINB=13
SERVO=7
```
从led8开始，一直到led15，都连接在拓展板的电机驱动模块上，分别是AIN2,AIN1,BIN2,BIN1,3BIN1,3BIN2,3AIN1,3AIN2

我们令A口控制左上方轮子，B口控制右上方轮子。3A口控制坐下方轮子，3B口控制右下方轮子。

```
LU1=9
LU2=8
RU1=11
RU2=10
LD1=14
LD2=15
RD1=12
RD2=13
```

再定义3个舵机

```
Act1=0
Act2=1
Act3=2
```

#### 麦克纳姆轮分布方式
##### 正常情况的麦轮分布
根据轮子方向呈交叉形状，即

```
BA
AB
左前方和右后方为B轮
左后方和右前方为A轮
```
四个轮子都向前转时，轴向速度相互抵消，只剩下向前的速度，则小车向前，后退同理
而A轮正转，B轮反转的时候，向前向后的速度就会相互抵消，只剩下向左的速度。向右平移同理.BAAB
底盘左侧轮子正转右侧轮子反转，实现底盘向右旋转，即顺时针旋转。逆时针旋转同理。左右左右

##### 我们自己的麦轮分布

```
    B      这个打横
 B     A   这两个竖的
    A      这个打横
```
EMMMMM,有点奇怪，或者说，是这样的

```
BB    这四个轮子的镜像互相垂直，轴向呈交叉分布
AA    对角线上的两个轮子相互平行，且轴向在一条直线上
以这个为例子，轮子编号定义如上
```
于是有定义 正转方向和前后左右方向
四个轮子都向前转时，轴向速度相互抵消，合速度为向前的速度，则小车向前，后退同理
而左上方B轮反转，右下方A轮反转的时候，合速度为向左的速度，则小车向左，向右平移同理
底盘左侧轮子正转右侧轮子反转，实现底盘向右旋转，即顺时针旋转。逆时针旋转同理。

认真写代码的时候发现，如果要移动方向相同，我们的麦轮分布和正常的麦轮分布驱动方向是一样的（此处只考虑坐标轴方向的运动）

##### 超声波测距方法

##### 多线程读取轮子速度

```
 #霍尔脉冲读取函数
 GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过18号引脚读取左轮脉冲数据
 GPIO.setup(35, GPIO.IN,pull_up_down=GPIO.PUD_UP)   #通过35号引脚读取右轮脉冲数据
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
```
在边缘检测方式中，add_event_detect()函数运行后，会为回调函数另外开启一个线程，与主程序并发运行，因此不容易错过当 CPU 忙于处理其它事物时输入状态的改变。但同一进程内也最好不要有太过耗费CPU时间的部分，否则仍会导致脉冲的丢失，如果不可避免，可以用多进程去处理CPU密集型代码部分。

 RPi.GPIO 中允许通过软件的方式对配置 Broadcom SOC 来达到对gpio口的上拉和下拉：
 
```
 GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #上拉
```



##### 根据速度的反馈轮子控速方法

##### 根据位置的pid控速法
这个可以不搞，大概测距到垃圾还有30厘米，写个降速的函数，大概停在垃圾的3--5cm左右

##### 舵机控制
拾取整套动作，每个控制信号送出去的时候写个delay 20ms的函数吧，这样等一个舵机做完，下个舵机才开始运动

##### 蓝牙控制

##### 超声波测距
###### 模块原理
测量距离 = 传播速度X时间间隔/2
HS-SR04超声波模块： 
工作电压  5V   工作电流  15mA  测距范围：3cm---4m  测量角度：15度
Trig: 输入信号  10usTTL
Echo：输出信号   5V脉冲信号

注意：Echo返回的是5v信号，而树莓派的GPIO接受超过3.3V的信号可能会被烧毁，这里可能要一个分压电路
###### 测距过程
1.树莓派向 Trig 脚发送一个持续10us的脉冲信号。
2.HC-SR04接收到树莓派发送的脉冲信号，开始发送超声波，并把Echo置为高电平。然后准备接收返回的超声波。
3.当HC-SR04接收到返回的超声波时，把Echo置为低电平。

从上述过程可以看出， Echo 高电平持续的时间就是超声波从发射到返回所经过的时间间隔 
