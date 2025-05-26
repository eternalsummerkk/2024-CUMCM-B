import math
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设定参数
p0 = 0.10  # 标称次品率
Z_alpha = 1.96  # 95% 信度对应的 Z 值
Z_beta = 1.645  # 90% 信度对应的 Z 值

# 定义样本量计算的函数
def calculate_sample_size(Z_value, p0, E):
    """
    计算给定误差范围内的样本量
    Z_value: Z 值（根据显著性水平）
    p0: 标称次品率
    E: 允许误差范围
    """
    return math.ceil((Z_value ** 2 * p0 * (1 - p0)) / E ** 2)

# 定义不同的允许误差范围
error_rates = [0.01, 0.02, 0.03, 0.04, 0.05]

# 计算不同误差范围下的样本量
sample_sizes_95 = [calculate_sample_size(Z_alpha, p0, E) for E in error_rates]
sample_sizes_90 = [calculate_sample_size(Z_beta, p0, E) for E in error_rates]

# 创建 DataFrame 展示结果
df_sample_sizes = pd.DataFrame({
    '允许误差': error_rates,
    '95% 信度下样本量': sample_sizes_95,
    '90% 信度下样本量': sample_sizes_90
})

# 打印结果
print(df_sample_sizes)
### 绘制灵敏度分析图
plt.figure(figsize=(10, 6))

# 绘制 95% 信度下样本量的灵敏度分析
plt.plot(error_rates, sample_sizes_95, marker='o', label='95% 信度下样本量')

# 绘制 90% 信度下样本量的灵敏度分析
plt.plot(error_rates, sample_sizes_90, marker='s', label='90% 信度下样本量')

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei']  # 用于显示中文标签
rcParams['axes.unicode_minus'] = False  # 用于正常显示负号

# 添加图例和标签
plt.title('允许误差率对样本量的灵敏度分析')
plt.xlabel('允许误差率')
plt.ylabel('样本量')
plt.legend()
plt.grid(True)

# 显示图表
plt.show()



