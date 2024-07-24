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
# from turtle import delay, st
# import torch
import numpy as np
import config
'''
对于定向天线，增益值会随着与天线主波束方向的偏离而降低。
合理的增益值可能从几dBi到20dBi或更高，具体取决于天线的设计和使用场景。
Los：就是直射，没有障碍物，没有反射，没有绕射，没有散射，没有衰减。
Nlos：就是非直射，有障碍物，有反射，有绕射，有散射，有衰减。需要天线簇。
'''

N_qpt = 10
M_nt = 5
## 载波频率
f_c = 5

import pandas as pd
### 加载方向图
def loadDirectionalDiagram():
    # 替换为你的Excel文件路径
    excel_path = 'Ephi.xlsx'
    # 使用pandas的read_excel函数读取Excel文件
    df = pd.read_excel(excel_path)
    # 将DataFrame转换为二维numpy数组
    array_2d = df.values
    return array_2d


def caculateGain(Hdegree,Vdegree):
    '''
    Hdegree: 水平角度 [-180,180]
    Vdegree: 垂直角度 [-90,90]
    '''
    # 读取方向图
    Ephi = config.Ephi
    shape = Ephi.shape
    # 计算方向图的水平角度和垂直角度
    Hindex = round((Hdegree+180)/(360/72))
    Vdegree = round((Vdegree+90)/(180/36))
    # 读取方向图的增益值
    gain = Ephi[Vdegree][Hindex]
    return gain

def FunctionForLos(x1,x2,y1,y2,z1,z2):
    azimuth_degrees_p,azimuth_degrees_q,\
        elevation_degrees_p,evalution_degrees_q \
            = caculateDegree(x1,x2,y1,y2,z1,z2)
    ans = 0.0
    num1= np.random.uniform(1,20)
    num2 = np.random.uniform(1,20)
    matrixLos_1 = np.transpose(np.array([[num1],[num2]]))
    # print(matrixNlos_1.shape)
    # print(matrixNlos_1)
    matrixLosnums1 = []
    for i in range(4):
        # 随机生成一个数服从 (0, 2 ]均匀分布的随机相位
        num3 = np.random.uniform(0,2*np.pi)
        # 创建一个纯虚数张量
        complex_number1 = 0+num3*1j
        # print(matrixNlosImaginaryNumber1)
        matrixLosnums1.append(np.exp(complex_number1))
                    
    matrixLos_2 = np.array([[1+2j, 3+4j], [5+6j, 7+8j]])
    ### 交叉极化功率比
    k_mnt = 2
    ### 莱斯因子
    K_Rt = 10**(-1.51)
    ### 联合极化不均衡
    u = 1

    matrixLos_2[0][0] = matrixLosnums1[0]
    matrixLos_2[0][1] = 0
    matrixLos_2[1][0] = 0
    matrixLos_2[1][1] = -1*matrixLosnums1[3]
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

    num1= np.random.uniform(1,20)
    num2 = np.random.uniform(1,20)
    matrixNlos_3 = np.array([[num1],[num2]])

    ### 生成1到2的随机数(us) 距离除以光速
    delayTime = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)/3e8

    complex_number2 = 2*np.pi*f_c*delayTime*1j

    parameter1 = np.exp(complex_number2)
                
    ### 相乘
    temp1 =  np.dot(matrixLos_1,matrixLos_2)
    temp2 = np.dot(f_r,matrixNlos_3)
    temp3 = np.dot(temp1,temp2)
    ans += parameter1*temp3[0][0]
    return ans

def FunctionForNlos(azimuthDegree,elevationDegree):
        ## 2*1的转置矩阵
        ### 随机生成1到20的数
        ans = 0.0
        for i in range(10):
            for j in range(10):
                ### 随机生成浮点数
                num1= np.random.uniform(1,20)
                num2 = np.random.uniform(1,20)
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
                k_mnt = 2
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

                num1= np.random.uniform(1,20)
                num2 = np.random.uniform(1,20)
                matrixNlos_3 = np.array([[num1],[num2]])

                ### 十到五百的随机数
                power = np.sqrt(np.random.randint(10,20))

                ### 生成1到2的随机数(us)
                randTime = np.random.uniform(1,2)*1e-6

                complex_number2 = 2*np.pi*f_c*randTime*1j

                parameter1 = np.exp(complex_number2)
                
                ### 相乘
                temp1 = np.dot(matrixNlos_1,matrixNlos_2)
                temp2 = np.dot(f_r,matrixNlos_3)
                temp3 = np.dot(temp1,temp2)
                ans += power*parameter1*temp3[0][0]

        return ans

# a = FunctionForNlos()
# b = FunctionForLos()
# print("Los:",b)
# print("Nlos:",a)

import random
# x1 = random.uniform(-10, 10)  # x坐标在-10到10之间
# y1 = random.uniform(-10, 10)  # y坐标在-10到10之间
# z1 = random.uniform(-10, 10)  # z坐标在-10到10之间

# # 生成第二个点的坐标
# x2 = random.uniform(-10, 10)  # x坐标在-10到10之间
# y2 = random.uniform(-10, 10)  # y坐标在-10到10之间
# z2 = random.uniform(-10, 10)  # z坐标在-10到10之间
x1=0
y1=0
z1=0

x2=2*math.sqrt(2)
y2=2*math.sqrt(2)
z2=5

config.Ephi = loadDirectionalDiagram()
Gain = caculateGain(0,90)
breakpoint = 1
def caculateDegree(x1,x2,y1,y2,z1,z2):
    # 计算两个点的水平方向（东-北方向）
    dx = x2 - x1
    dy = y2 - y1
    azimuth = math.atan2(dy, dx)  # atan2返回值的范围是-π到π
    azimuth_degrees_p = math.degrees(azimuth)  # 将弧度转换为度

    dx = x1-x2
    dy = y1-y2
    azimuth = math.atan2(dy, dx)  # atan2返回值的范围是-π到π
    azimuth_degrees_q = math.degrees(azimuth)  # 将弧度转换为度

    # 计算两个点的俯仰角
    dz = z2 - z1
    distance = math.sqrt(dx**2 + dy**2)
    elevation = math.atan2(dz, distance)  # 俯仰角
    elevation_degrees_p = math.degrees(elevation)  # 将弧度转换为度

    dz = z1 - z2
    distance = math.sqrt(dx**2 + dy**2)
    elevation = math.atan2(dz, distance)  # 俯仰角
    evalution_degrees_q = math.degrees(elevation)  # 将弧度转换为度

    return azimuth_degrees_p,azimuth_degrees_q,elevation_degrees_p,evalution_degrees_q

# 生成第一个点的坐标
x1 = random.uniform(-10, 10)  # x坐标在-10到10之间
y1 = random.uniform(-10, 10)  # y坐标在-10到10之间
z1 = random.uniform(-10, 10)  # z坐标在-10到10之间

# 生成第二个点的坐标
x2 = random.uniform(-10, 10)  # x坐标在-10到10之间
y2 = random.uniform(-10, 10)  # y坐标在-10到10之间
z2 = random.uniform(-10, 10)  # z坐标在-10到10之间

HLos = FunctionForLos(x1,x2,y1,y2,z1,z2)
print("HLos:",HLos)