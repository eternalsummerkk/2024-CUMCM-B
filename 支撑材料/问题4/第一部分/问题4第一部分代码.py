# 更新后的次品率
updated_cases = {
    1: {
        '零配件 1 次品率': 0.1350,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 2,
        '零配件 2 次品率': 0.1450,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 3,
        '成品 次品率': 0.1200,
        '成品 装配成本': 6,
        '成品 检测成本': 3,
        '成品 市场售价': 56,
        '成品 调换损失': 6,
        '成品 拆解费用': 5
    },
    2: {
        '零配件 1 次品率': 0.2400,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 2,
        '零配件 2 次品率': 0.2300,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 3,
        '成品 次品率': 0.2300,
        '成品 装配成本': 6,
        '成品 检测成本': 3,
        '成品 市场售价': 56,
        '成品 调换损失': 6,
        '成品 拆解费用': 5
    },
    3: {
        '零配件 1 次品率': 0.1050,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 2,
        '零配件 2 次品率': 0.1250,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 3,
        '成品 次品率': 0.1150,
        '成品 装配成本': 6,
        '成品 检测成本': 3,
        '成品 市场售价': 56,
        '成品 调换损失': 30,
        '成品 拆解费用': 5
    },
    4: {
        '零配件 1 次品率': 0.2150,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 1,
        '零配件 2 次品率': 0.2250,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 1,
        '成品 次品率': 0.2050,
        '成品 装配成本': 6,
        '成品 检测成本': 2,
        '成品 市场售价': 56,
        '成品 调换损失': 30,
        '成品 拆解费用': 5
    },
    5: {
        '零配件 1 次品率': 0.1100,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 8,
        '零配件 2 次品率': 0.1900,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 1,
        '成品 次品率': 0.1050,
        '成品 装配成本': 6,
        '成品 检测成本': 2,
        '成品 市场售价': 56,
        '成品 调换损失': 10,
        '成品 拆解费用': 5
    },
    6: {
        '零配件 1 次品率': 0.0600,
        '零配件 1 采购单价': 4,
        '零配件 1 检测成本': 2,
        '零配件 2 次品率': 0.0650,
        '零配件 2 采购单价': 18,
        '零配件 2 检测成本': 3,
        '成品 次品率': 0.0550,
        '成品 装配成本': 6,
        '成品 检测成本': 3,
        '成品 市场售价': 56,
        '成品 调换损失': 10,
        '成品 拆解费用': 40
    }
}

# 成品的总收益和总成本计算函数
def calculate_total_cost_revenue(case, detect_part_1, detect_part_2, detect_product):
    P1 = case['零配件 1 次品率']
    P2 = case['零配件 2 次品率']
    Pd = case['成品 次品率']
    
    # 成品市场售价和调换损失
    market_price = case['成品 市场售价']
    replace_cost = case['成品 调换损失']
    
    # 成本参数
    assemble_cost = case['成品 装配成本']
    dismantle_cost = case['成品 拆解费用']
    
    # 检测成本
    check_cost_1 = case['零配件 1 检测成本'] if detect_part_1 else 0
    check_cost_2 = case['零配件 2 检测成本'] if detect_part_2 else 0
    check_cost_product = case['成品 检测成本'] if detect_product else 0
    
    # 计算不检测零配件时成品次品率增加值
    if not detect_part_1 and not detect_part_2:
        delta_Pd = P1 + P2 - P1 * P2
    elif not detect_part_1:
        delta_Pd = P1
    elif not detect_part_2:
        delta_Pd = P2
    else:
        delta_Pd = 0

    # 计算成品的次品率
    final_Pd = Pd + delta_Pd
    
    # 不检测成品直接进入市场的不合格品数量
    N_total = 1000  # 假设总成品数量为1000
    N_defective = N_total * final_Pd
    N_qualified = N_total - N_defective
    
    # 成本计算
    total_check_cost = (check_cost_1 + check_cost_2 + check_cost_product) * N_total
    total_replace_cost = N_defective * replace_cost
    total_assemble_cost = assemble_cost * N_total
    
    # 总成本
    total_cost = total_check_cost + total_replace_cost + total_assemble_cost
    
    # 总收益
    total_revenue = N_qualified * market_price
    
    # 净利润
    net_profit = total_revenue - total_cost
    
    return total_cost, total_revenue, net_profit

# 对每个情况进行计算
results = {}
for i, case in updated_cases.items():
    total_cost, total_revenue, net_profit = calculate_total_cost_revenue(case, detect_part_1=1, detect_part_2=1, detect_product=1)
    results[i] = {
        '总成本': total_cost,
        '总收益': total_revenue,
        '净利润': net_profit
    }

# 打印结果
for case_num, result in results.items():
    print(f"情形 {case_num}:")
    print(f"总成本: {result['总成本']:.2f}, 总收益: {result['总收益']:.2f}, 净利润: {result['净利润']:.2f}")
    print("-----------")
