import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# 生成一个长度为21的冲激信号，冲激位置在第11个位置
impulse = signal.unit_impulse(21, 'mid')

# 绘制冲激信号
plt.stem(np.arange(-10, 11), impulse)
plt.title('Impulse Function')
plt.xlabel('n')
plt.ylabel('Amplitude')
plt.show()
