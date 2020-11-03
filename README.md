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
于是有定义
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
根据轮子方向呈交叉形状，即
BA
AB
左前方和右后方为B轮
左后方和右前方为A轮
# 四个轮子都向前转时，轴向速度相互抵消，只剩下向前的速度，则小车向前，后退同理
# 而A轮正转，B轮反转的时候，向前向后的速度就会相互抵消，只剩下向左的速度。向右平移同理.BAAB
# 底盘左侧轮子正转右侧轮子反转，实现底盘向右旋转，即顺时针旋转。逆时针旋转同理。左右左右
