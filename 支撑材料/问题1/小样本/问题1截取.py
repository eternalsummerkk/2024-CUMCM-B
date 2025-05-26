import numpy as np

# A2 系数查找表
a2_table = {
    2: 1.88,
    3: 1.023,
    4: 0.729,
    5: 0.577,
    6: 0.483,
    7: 0.419,
    8: 0.373
}

# 随机生成次品率数据的函数 (模拟每组样本的次品率)
def generate_sample_data(m, n):
    return np.random.uniform(0.08, 0.12, (m, n))  # 假设次品率在10%上下波动

# 计算每组次品率均值和极差
def calculate_x_r(data):
    x_means = np.mean(data, axis=1)
    r_ranges = np.ptp(data, axis=1)
    return x_means, r_ranges

# 计算样本均值 X 和极差均值 R
def calculate_means(x_means, r_ranges):
    x_bar = np.mean(x_means)
    r_bar = np.mean(r_ranges)
    return x_bar, r_bar

# 计算控制限
def calculate_control_limits(x_bar, r_bar, n):
    A2 = a2_table.get(n, None)
    if A2 is None:
        raise ValueError("样本容量 n 无法找到对应的 A2 值")
    UCL = x_bar + A2 * r_bar
    LCL = x_bar - A2 * r_bar
    return UCL, LCL

# 判定是否接收批次 (基于95%和90%信度)
def judge_acceptance(x_means, UCL, LCL):
    rejected_batches_95 = np.sum(x_means > UCL)  # 信度95%：超过UCL拒收
    accepted_batches_90 = np.sum((x_means <= UCL) & (x_means >= LCL))  # 信度90%：LCL和UCL之间接收
    return rejected_batches_95, accepted_batches_90

# 主函数流程
def xr_control_chart(m_range, n_values):
    best_m = None
    for n in n_values:
        for m in m_range:
            # 生成模拟次品率数据
            data = generate_sample_data(m, n)
            
            # 计算每组次品率均值和极差
            x_means, r_ranges = calculate_x_r(data)
            
            # 计算样本均值 X 和极差均值 R
            x_bar, r_bar = calculate_means(x_means, r_ranges)
            
            # 计算控制限
            UCL, LCL = calculate_control_limits(x_bar, r_bar, n)
            
            # 判定是否接收批次
            rejected_95, accepted_90 = judge_acceptance(x_means, UCL, LCL)
            
            print(f"样本容量 n={n}, 组数 m={m}:")
            print(f"  样本均值: {x_bar:.5f}, 极差均值: {r_bar:.5f}")
            print(f"  控制限: UCL={UCL:.5f}, LCL={LCL:.5f}")
            print(f"  拒收批次数 (信度95%): {rejected_95}")
            print(f"  接收批次数 (信度90%): {accepted_90}")
            
            # 最小抽样次数记录
            if best_m is None or rejected_95 < best_m:
                best_m = m
                print(f"  最优抽样次数更新: m={best_m}")

# 参数范围设置
m_range = range(20, 26)  # 样本组数在 20-25 之间
n_values = [4, 5]  # 样本容量 n 为 4 或 5

# 运行控制图计算
xr_control_chart(m_range, n_values)
