# Susceptible –> Infected –> Recovered
import argparse
from enum import IntEnum
import matplotlib.pyplot as plt
import matplotlib.animation as animation  # 制作动图
import numpy as np
import random

# infected为255, susceptible
class State(IntEnum):
    susceptible = 0
    infected = 255
    removed = 100

# 计算周围的活细胞个数
def _count(data, row, col):
    shape = data.shape[0]-1
    up    = row-1 if row-1 > 0 else 0
    down  = row+1 if row+1 < shape else shape
    right = col+1 if col+1 < shape else shape
    left  = col-1 if col-1 > 0 else 0
    return (data[row, right] + data[row, left] +
            data[up, col] + data[down, col]) // 255 # 周围总颜色和除以255获得活细胞的个数
            
def count(initial, data, row, col):
    total = _count(initial, row, col)
    # 如果该元胞是感染的, removed
    if initial[row, col] == State.infected:
        data[row, col] = State.removed
    # 如果是易感的
    elif initial[row, col] == State.susceptible:
        # 如果周围有
        if total != 0:
            data[row, col] = np.random.choice(
                [State.susceptible, State.infected], 
                p=[1-transmission_rate, transmission_rate])

NUM = 0

# 更新每一帧图像所需数据的函数
def generate(frame_num, img, plt, initial):
    global NUM
    NUM += 1
    plt.title(f'{NUM} generation')

    data = initial.copy() # initial保持不变, 修改data
    rows, cols = data.shape
    # 遍历每个格子
    for row in range(rows):
        for col in range(cols):
            count(initial, data, row, col)
    img.set_data(data)
    initial[:] = data[:]
    return img

# 制作动图
def update(data): 
    update_interval = 150 #更新频率，以ms计
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    img = ax.imshow(data, cmap='Blues', interpolation='nearest')
    _ = animation.FuncAnimation(fig, generate, fargs=(img, plt, data),
                                  frames=30, #动画长度, 一次循环包含的帧数
                                  interval=update_interval) #更新频率，以ms计
    plt.show()

def initial_data(length):
    data = np.zeros(shape=(length,length))
    data[length//2, length//2] = State.infected
    return data


def main():
    data = initial_data(length) 
    update(data)


if __name__ == "__main__":
    transmission_rate = 0.40 # 感染概率0~1
    length = 19 # 宽度
    main()
