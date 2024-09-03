import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# 创建画布和子图
fig, ax = plt.subplots(figsize=(10, 6))

# 关闭坐标轴
ax.axis('off')

# 绘制流程图中的框和箭头
def draw_box(ax, xy, width, height, text):
    ax.add_patch(FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.3", edgecolor="black", facecolor="white"))
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center")

def draw_arrow(ax, start, end, text):
    ax.annotate(text, xy=start, xytext=end, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

# 绘制流程图
draw_box(ax, (0.1, 0.7), 0.3, 0.2, "数据采集和预处理")
draw_box(ax, (0.5, 0.7), 0.3, 0.2, "DETR模型训练")
draw_box(ax, (0.9, 0.7), 0.3, 0.2, "目标检测和识别")
draw_box(ax, (0.1, 0.4), 0.3, 0.2, "姿势估计")
draw_box(ax, (0.5, 0.4), 0.3, 0.2, "运动员行为分析")
draw_box(ax, (0.9, 0.4), 0.3, 0.2, "反馈与辅助训练")
draw_box(ax, (0.5, 0.1), 0.3, 0.2, "性能评估和优化")

draw_arrow(ax, (0.4, 0.8), (0.5, 0.7), "")
draw_arrow(ax, (0.8, 0.8), (0.9, 0.7), "")
draw_arrow(ax, (0.5, 0.6), (0.4, 0.4), "")
draw_arrow(ax, (0.5, 0.6), (0.5, 0.4), "")
draw_arrow(ax, (0.5, 0.6), (0.6, 0.4), "")
draw_arrow(ax, (0.9, 0.6), (0.9, 0.4), "")
draw_arrow(ax, (0.5, 0.3), (0.5, 0.1), "")

# 显示图形
plt.show()
