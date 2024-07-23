'''
PL：在城市环境中，可能在20dB到120dB之间，取决于距离和频率。
SH：标准偏差可能在3dB到8dB之间。
BL：可能在5dB到30dB之间，取决于障碍物的大小和类型。
WE：在毫米波频率下，可能在0.1dB/km到1dB/km之间。
AL：在恶劣天气条件下，可能在1dB到20dB以上。
P.S. 该信息源于kimi，我什么都不知道，只是搬运工。
'''
# 路径损耗
PL = 60
# 阴影衰落
SH = 5
# 阻挡效应
BL = 10
# 大气吸收损耗
WE = 0.5
# 天气影响损耗
AL = 5

coefficientAboutH = PL * SH * BL * WE * AL

# 一下开始计算H_s矩阵
'''
H_s = H_los + H_nlos
H 表示发射端的每个发射天线和接收端的每个接收天线之间的信道矩阵
'''

## 开始计算 Nlos

from calendar import c
import math
# import torch
import numpy as np
'''
对于定向天线，增益值会随着与天线主波束方向的偏离而降低。
合理的增益值可能从几dBi到20dBi或更高，具体取决于天线的设计和使用场景。
Los：就是直射，没有障碍物，没有反射，没有绕射，没有散射，没有衰减。
Nlos：就是非直射，有障碍物，有反射，有绕射，有散射，有衰减。需要天线簇。

'''

N_qpt = 10
M_nt = 5
## 载波频率
f_c = 2.4

for i in range(N_qpt):
    for j in range(M_nt):
        ## 2*1的转置矩阵
        ### 随机生成1到20的数
        num1= np.random.randint(1,20)
        num2 = np.random.randint(1,20)
        matrixNlos_1 = np.transpose(np.array([[num1],[num2]]))
        # print(matrixNlos_1.shape)
        # print(matrixNlos_1)
        matrixNlosnums1 = []
        u = 1
        for i in range(4):
            # 随机生成一个数服从 (0, 2 ]均匀分布的随机相位
            num3 = np.random.uniform(0,2*np.pi)
            # 创建一个纯虚数张量
            complex_number1 = 0+num3*1j
            # print(matrixNlosImaginaryNumber1)
            matrixNlosnums1.append(np.exp(complex_number1))
            
        matrixNlos_2 = np.array([[1+2j, 3+4j], [5+6j, 7+8j]])
        ### 交叉极化功率比
        k_mnt = 20
        ### 莱斯因子
        K_Rt = 10**(-1.51)
        ### 联合极化不均衡
        u = 1
        coefficientTemp1 = math.sqrt(u/k_mnt)
        coefficientTemp2 = math.sqrt(1/k_mnt)
        coefficientTemp3 = math.sqrt(u)
        matrixNlos_2[0][0] = matrixNlosnums1[0]
        matrixNlos_2[0][1] = coefficientTemp1*matrixNlosnums1[1]
        matrixNlos_2[1][0] = coefficientTemp2*matrixNlosnums1[2]
        matrixNlos_2[1][1] = coefficientTemp3*matrixNlosnums1[3]
        # print(matrixNlos_2.shape)
        # print(matrixNlos_2)

        ## 法拉第旋转角矩阵
        f_r = np.array([[0.1,0.1],[0.1,0.1]])
        f_r[0][0] = np.cos(180/(f_c*f_c))
        f_r[0][1] = np.sin(-1*180/(f_c*f_c))
        f_r[1][0] = np.sin(180/(f_c*f_c))
        f_r[1][1] = np.cos(180/(f_c*f_c))
        # print(f_r.shape)
        # print(f_r)

        # caculateMatrix1 = np.dot(matrixNlos_1,matrixNlos_2)
        # print(caculateMatrix1)

        num1= np.random.randint(1,20)
        num2 = np.random.randint(1,20)
        matrixNlos_3 = np.transpose(np.array([[num1],[num2]]))

        ### 十到五百的随机数
        power = np.sqrt(np.random.randint(100,500))

        ### 生成1到2的随机数(us)
        randTime = np.random.uniform(1,2)*1e-6

        complex_number2 = 2*np.pi*f_c*randTime*1j

        parameter1 = np.exp(complex_number2)

