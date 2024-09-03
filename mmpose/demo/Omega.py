# 计算角度的函数 Omega，输入为:bones为三点坐标集，names为骨骼点名称，
# START，MID，END为计算角度的三组点
# length为插值倍数，为0时不进行插值，order为求导阶数
# 返回值为时间x，x对应的插值函数值y，和插值函数function
import numpy as np
from scipy.interpolate import CubicSpline
def Omega(bones, names, START, MID, END, time, length):

    start = bones[:,np.where(names == START)[0][0],:]
    mid   = bones[:,np.where(names == MID)  [0][0],:]
    end   = bones[:,np.where(names == END)  [0][0],:]
    angles = []
    # 遍历每一行数据。
    for i in range(len(time)):
        # 获取三点的坐标数据并转换为 NumPy 数组
        start_coords = np.array([0, start[i][1], start[i][2]])
        mid_coords   = np.array([0,   mid[i][1],   mid[i][2]])
        end_coords   = np.array([0,   end[i][1],   end[i][2]])
        
        # 定义三点组成的两个向量
        vector1 = start_coords - mid_coords
        vector2 = end_coords - mid_coords

        # 计算角度
        angle = np.rad2deg(np.arccos(np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))))
        # 将角度添加到列表中
        angles.append(angle)
    time = np.array(time)
    time = time/120
    print(time)
    #用时间作为横坐标，角度作为纵坐标进行三次样条插值
    func = CubicSpline(time, angles)
    #画出得到的函数图像
    x = np.linspace(time[0], time[-1], length)
    y = func(x)
    yy = func(x, 1)
    print(x)
    return x, y, yy, func