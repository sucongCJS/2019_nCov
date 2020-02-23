import argparse
from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.animation as animation  # 制作动图
import numpy as np

# on为255, off为0
class State(IntEnum):
    on = 255
    off = 0

# 随机产生 length*length 的方阵, 返回类型np.array
def random_data(length = 7, seed = 420) -> np.array:
    np.random.seed(seed)
    return np.random.choice([State.off, State.on], size=(length, length), p=[0.5, 0.5])

# 计算周围的活细胞个数
def _count(data, row, col):
    shape = data.shape[0]
    up = (row - 1) % shape
    down = (row + 1) % shape
    right = (col + 1) % shape
    left = (col - 1) % shape
    return (data[up, right] + data[up, left] +
            data[down, right] + data[down, left] +
            data[row, right] + data[row, left] +
            data[up, col] + data[down, col]) // 255 # 周围总颜色和除以255获得活细胞的个数

def count(initial, data, row, col):
    total = _count(initial, row, col)
    # 周围存货的元胞太多或太少, 死掉
    if initial[row, col]:
        if (total < 2) or (total > 3):
            data[row, col] = State.off
    # 活下来
    else:
        if total == 3:
            data[row, col] = State.on

NUM = 0

# 更新每一帧图像所需数据的函数
def generate(frame_num, img, plt, initial):
    global NUM
    NUM += 1
    plt.title(f'{NUM} generation')
    data = initial.copy()
    rows, cols = data.shape
    for row in range(rows):
        for col in range(cols):
            count(initial, data, row, col)
    img.set_data(data)
    initial[:] = data[:]
    return img

# 制作动图
def update(data): 
    update_interval = 50 #更新频率，以ms计
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    img = ax.imshow(data, cmap='Blues', interpolation='nearest')
    _ = animation.FuncAnimation(fig, generate, fargs=(img, plt, data),
                                  frames=30, #动画长度, 一次循环包含的帧数
                                  interval=update_interval) #更新频率，以ms计
    plt.show()

def initial_data(length, seed):
    data = random_data(length, seed)
    return data

def main():
    data = initial_data(7, 400)
    update(data)


if __name__ == "__main__":
    main()
