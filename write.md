pid算法控制电机转速

直流电机的速度控制采用电枢电压控制方法，用于额定转速以下的调速，而且效率较高

###开环控制

由自动控制理论分析可知，负载的存在相当于在控制系统中加入了扰动。扰动会导致输出（电机速度）偏离希望值。闭环控制能有效地抑制扰动，稳定控制系统的输出。
闭环控制原理方框图如图。当积分环节串联在扰动作用的反馈通道（即扰动作用点之前）时，即成为针对阶跃扰动时的I型系统，能消除阶跃信号扰动。
这样可以有效地补偿扰动对输出的主要影响，又大大减轻反馈通道的负担，对稳定性影响较小。


编码器

