import numpy as np
import matplotlib.pyplot as plt

# 示例数据：赛艇运动员的关节坐标（取第一组数据）
joint_coordinates = [
    [327.84, 287.18], [332.78, 277.31], [313.03, 272.37], [332.78, 277.31],
    [273.54, 277.31], [337.72, 351.36], [214.29, 341.49], [396.95, 440.22],
    [209.36, 450.09], [426.58, 455.03], [308.09, 400.73], [288.35, 509.34],
    [229.10, 524.15], [441.39, 489.59], [387.08, 499.46], [530.25, 608.07]
]

# 将数据转换为NumPy数组以便更容易地进行计算
joint_coordinates = np.array(joint_coordinates)

# 绘制关节坐标
plt.figure(figsize=(10, 7))
for point in joint_coordinates:
    plt.plot(point[0], point[1], 'ro')  # 使用红色圆点标记关节位置

# 可以根据实际连接关系添加线条，这里简化为连接全部点
for i in range(len(joint_coordinates) - 1):
    plt.plot(joint_coordinates[i:i+2, 0], joint_coordinates[i:i+2, 1], 'b-')  # 使用蓝色线条连接点

plt.gca().invert_yaxis()  # 翻转Y轴，以符合图像坐标系统
plt.title('赛艇运动员姿势分析')
plt.xlabel('X坐标')
plt.ylabel('Y坐标')
plt.show()
