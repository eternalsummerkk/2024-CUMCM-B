import numpy as np
import pandas as pd

# 简化的A2值查找表（样本量 n 对应的 A2 值）
a2_table = {
    2: 1.880,
    3: 1.023,
    4: 0.729,
    5: 0.577,
    6: 0.483,
    7: 0.419,
    8: 0.373,
    9: 0.337,
    10: 0.308,
    11: 0.285,
    12: 0.266,
    13: 0.249,
    14: 0.235,
    15: 0.2230,
    16: 0.2120,
    17: 0.2030,
    18: 0.1940,
    19: 0.1870,
    20: 0.1800,
    21: 0.1730,
    22: 0.1670,
    23: 0.1620,
    24: 0.1570,
    25: 0.1530,
}

def get_a2_value(n_over_m):
    """根据 n/m 的近似值查找 A2 值"""
    rounded_value = round(n_over_m)
    return a2_table.get(rounded_value, "A2 value not found for this rounded value")

def generate_valid_n_m():
    """生成满足 n/m <= 25 且 m < 98 的有效 m 和 n 值"""
    while True:
        m = np.random.randint(1, 98)  # 生成 1 到 97 之间的随机整数
        n = np.random.randint(1, 25 * m + 1)  # 生成 1 到 25*m 之间的随机整数
        if m < 98 and n / m <= 25:
            return m, n

def generate_data(m, n, mean=0.1, fluctuation=0.01):
    """生成 m 组，每组 n 个样本的次品率数据"""
    print(f"Generating data with m = {m}, n = {n}")  # 打印 m 和 n 的值
    n_over_m = n / m
    A2 = get_a2_value(n_over_m)
    if isinstance(A2, str):
        raise ValueError(A2)
    print(f"A2 value for n/m rounded to {round(n_over_m)} is {A2}")  # 打印 A2 值
    data = []
    for i in range(m):
        samples = np.random.uniform(mean - fluctuation, mean + fluctuation, n)
        print(f"Group {i+1} samples: {samples}")  # 打印每组的样本数据
        data.append(samples)
    return np.array(data), A2

# 计算每组次品率均值
def calculate_group_means(data):
    return np.mean(data, axis=1)

# 计算每组次品率的极差
def calculate_range(data):
    return np.ptp(data, axis=1)  # ptp = peak-to-peak (最大值 - 最小值)

# 计算控制图统计量
def calculate_control_limits(X_bar, R_bar, A2):
    UCL = X_bar + A2 * R_bar
    LCL = X_bar - A2 * R_bar
    return UCL, LCL

# 判定是否接受零配件
def check_acceptance(group_means, UCL, LCL):
    results = []
    for mean in group_means:
        if mean > UCL:
            results.append("Reject")
        elif mean < LCL:
            results.append("Reject")
        else:
            results.append("Accept")
    return results

# 穷举不同的 m 和 n 值，生成结果表格
def generate_exhaustive_results():
    results = []
    for _ in range(100):  # 生成 100 组随机的 m 和 n
        m, n = generate_valid_n_m()
        try:
            # 生成数据
            data, A2 = generate_data(m, n)
            
            # 计算每组次品率均值和极差
            group_means = calculate_group_means(data)
            ranges = calculate_range(data)
            
            # 计算总体均值和极差均值
            X_bar = np.mean(group_means)
            R_bar = np.mean(ranges)
            
            # 计算控制限
            UCL, LCL = calculate_control_limits(X_bar, R_bar, A2)
            
            # 判断每组是否接受
            results_status = check_acceptance(group_means, UCL, LCL)
            
            # 收集结果
            for i, status in enumerate(results_status, start=1):
                results.append({
                    'm': m,
                    'n': n,
                    'Group': i,
                    'Mean': group_means[i-1],
                    'Range': ranges[i-1],
                    'UCL': UCL,
                    'LCL': LCL,
                    'Status': status
                })
        except ValueError as e:
            print(f"Error for m = {m}, n = {n}: {e}")
    
    # 创建 DataFrame
    df = pd.DataFrame(results)
    return df

# 生成穷举结果并输出为表格
df_results = generate_exhaustive_results()
df_results.to_csv('control_chart_results.csv', index=False)
print("Results have been written to 'control_chart_results.csv'")
