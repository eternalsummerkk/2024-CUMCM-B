import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 设置字体为 SimHei 或者其他支持中文的字体
rcParams['font.sans-serif'] = ['SimHei']  # 或者 'Microsoft YaHei'
rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# 贝叶斯更新函数
def bayesian_update(prior_alpha, prior_beta, n, k):
    posterior_alpha = prior_alpha + k
    posterior_beta = prior_beta + n - k
    return posterior_alpha, posterior_beta

# 计算每个零配件或成品的prior_alpha和prior_beta
def calculate_prior_params(defect_rate, sample_size):
    prior_alpha = defect_rate * sample_size
    prior_beta = (1 - defect_rate) * sample_size
    return prior_alpha, prior_beta

# 情形1数据
case_1 = {
    '零配件 1 次品率': 0.10,
    '零配件 2 次品率': 0.10,
    '成品 次品率': 0.10,
    'N_total': 1000
}

# 随机检测结果数据，零配件1的次品数量
sample_results_1 = 150  # 零配件1的次品数量

# 计算情形1的贝叶斯更新
defect_rate_1 = case_1['零配件 1 次品率']
prior_alpha_1, prior_beta_1 = calculate_prior_params(defect_rate_1, case_1['N_total'])

# 更新次品率
posterior_alpha_1, posterior_beta_1 = bayesian_update(prior_alpha_1, prior_beta_1, case_1['N_total'], sample_results_1)

# 可视化贝叶斯推理的先验分布和后验分布
x = np.linspace(0, 1, 100)

# 先验分布
prior_pdf = beta.pdf(x, prior_alpha_1, prior_beta_1)
plt.plot(x, prior_pdf, label="先验分布", color="blue")

# 后验分布
posterior_pdf = beta.pdf(x, posterior_alpha_1, posterior_beta_1)
plt.plot(x, posterior_pdf, label="后验分布", color="green")

# 计算并标注先验和后验分布的峰值
prior_peak = x[np.argmax(prior_pdf)]
posterior_peak = x[np.argmax(posterior_pdf)]

plt.axvline(prior_peak, color='blue', linestyle=':', label="先验峰值: {:.3f}".format(prior_peak))
plt.axvline(posterior_peak, color='green', linestyle=':', label="后验峰值: {:.3f}".format(posterior_peak))

# 添加更多图例
plt.axvline(defect_rate_1, color='red', linestyle='--', label="标称值: {:.2f}".format(defect_rate_1))
plt.fill_between(x, 0, prior_pdf, color="blue", alpha=0.1, label="先验分布区域")
plt.fill_between(x, 0, posterior_pdf, color="green", alpha=0.1, label="后验分布区域")

# 图像设置
plt.title("情形1：贝叶斯推理 - 零配件1")
plt.xlabel("次品率")
plt.ylabel("概率密度")
plt.legend()

# 显示图像
plt.show()


