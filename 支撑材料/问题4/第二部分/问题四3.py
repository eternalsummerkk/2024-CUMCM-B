import numpy as np

# 定义状态和动作
states = ['合格', '次品']  # 状态: 合格或次品
actions = ['检测', '跳过检测', '拆解', '跳过拆解']  # 动作: 检测或跳过检测, 拆解或跳过拆解

# 定义奖励函数
def reward_function(state, action, part, case):
    if action == '检测':
        return -case[part]['检测成本']  # 检测成本
    elif action == '跳过检测':
        defective_loss = float(case[part]['次品率'].strip('%')) / 100 * case['成品']['调换损失']
        return -(case[part].get('购买单价', case[part].get('装配成本', 0)) + defective_loss)
    elif action == '拆解':
        return -case[part].get('拆解费用', 0)  # 如果没有'拆解费用'字段，默认值为0
    elif action == '跳过拆解':
        product_value = case[part].get('购买单价', case[part].get('装配成本', 0))
        return min(product_value, case[part].get('拆解费用', 0))  # 默认拆解费用为0
    return 0

# 计算净利润
def calculate_total_profit(case, detect_parts, dismantle_parts, detect_final_product, dismantle_final_product):
    N_total = 1000  # 成品数量

    # 计算零配件和半成品的联合次品率
    part_defective_rates = [float(case[part]['次品率'].strip('%')) / 100 for part in detect_parts]
    delta_Pd = 1 - np.prod([1 - P for P in part_defective_rates])  # 联合次品率公式

    # 计算半成品的次品率
    semifinished_parts = [part for part in case if part.startswith('半成品')]
    semifinished_defective_rates = [float(case[part]['次品率'].strip('%')) / 100 for part in semifinished_parts]
    delta_semifinished_Pd = 1 - np.prod([1 - P for P in semifinished_defective_rates])

    # 计算成品次品率，合并零配件和半成品的影响
    product_defect_rate = float(case['成品']['次品率'].strip('%')) / 100
    N_defective = N_total * (product_defect_rate + (0 if all(detect_parts.values()) else delta_Pd) + (0 if all([detect_parts[part] for part in semifinished_parts]) else delta_semifinished_Pd))

    N_qualified = N_total - N_defective

    # 检测成本
    check_cost = sum(case[part]['检测成本'] * N_total for part, detect in detect_parts.items() if detect)
    final_check_cost = case['成品']['检测成本'] * N_total if detect_final_product else 0

    # 调换成本
    replace_cost = N_defective * case['成品']['调换损失']

    # 拆解成本
    dismantle_cost = 0
    for part, dismantle in dismantle_parts.items():
        if dismantle:
            dismantle_cost += case[part].get('拆解费用', 0) * N_defective  # 使用get()避免KeyError
        else:
            product_value = case[part].get('购买单价', case[part].get('装配成本', 0))
            dismantle_cost += N_defective * min(product_value, case[part].get('拆解费用', 0))  # 如果缺少'拆解费用'，则默认为0

    # 拆解成品
    if dismantle_final_product:
        dismantle_cost += N_defective * case['成品']['拆解费用']
    else:
        product_value = sum(case[part].get('购买单价', case[part].get('装配成本', 0)) for part in detect_parts) + case['成品']['装配成本']
        dismantle_cost += N_defective * min(product_value, case['成品']['拆解费用'])

    # 总成本
    total_cost = check_cost + final_check_cost + replace_cost + dismantle_cost

    # 总收益
    total_revenue = N_qualified * case['成品']['市场售价']

    # 净利润
    net_profit = total_revenue - total_cost

    return total_cost, total_revenue, net_profit

def calculate_best_decisions(case):
    best_decision = None
    best_profit = float('-inf')

    print(f"\n计算最佳检测与拆解决策:\n")

    # 零配件部分：只检测，不拆解
    parts = [part for part in case if part.startswith('零配件')]
    
    # 半成品部分：检测并考虑拆解
    semifinished_parts = [part for part in case if part.startswith('半成品')]

    # 遍历所有组合的检测和拆解策略
    for detect_parts_combination in range(1 << len(parts)):
        detect_parts = {parts[i]: (detect_parts_combination >> i) & 1 for i in range(len(parts))}
        
        # 保证所有零配件的拆解状态为 False (不拆解)
        dismantle_parts = {part: 0 for part in parts}

        for detect_semifinished_combination in range(1 << len(semifinished_parts)):
            detect_semifinished = {semifinished_parts[i]: (detect_semifinished_combination >> i) & 1 for i in range(len(semifinished_parts))}
            for dismantle_semifinished_combination in range(1 << len(semifinished_parts)):
                dismantle_semifinished = {semifinished_parts[i]: (dismantle_semifinished_combination >> i) & 1 for i in range(len(semifinished_parts))}
                
                # 合并零配件和半成品的检测和拆解策略
                detect_combined = {**detect_parts, **detect_semifinished}
                dismantle_combined = {**dismantle_parts, **dismantle_semifinished}
                
                for detect_final_product in [True, False]:
                    for dismantle_final_product in [True, False]:
                        total_cost, total_revenue, net_profit = calculate_total_profit(
                            case,
                            detect_parts=detect_combined,
                            dismantle_parts=dismantle_combined,
                            detect_final_product=detect_final_product,
                            dismantle_final_product=dismantle_final_product
                        )

                        # 将0和1转换为T和F，输出当前策略和计算结果
                        detect_combined_TF = {part: 'T' if val == 1 else 'F' for part, val in detect_combined.items()}
                        dismantle_combined_TF = {part: 'T' if val == 1 else 'F' for part, val in dismantle_combined.items()}
                        detect_final_product_TF = 'T' if detect_final_product else 'F'
                        dismantle_final_product_TF = 'T' if dismantle_final_product else 'F'

                        print(f"当前策略 - 零配件/半成品检测: {detect_combined_TF}, 零配件/半成品拆解: {dismantle_combined_TF}, "
                              f"检测成品: {detect_final_product_TF}, 拆解成品: {dismantle_final_product_TF}")
                        print(f"总成本: {total_cost:.2f}, 总收益: {total_revenue:.2f}, 净利润: {net_profit:.2f}\n")

                        # 更新最佳决策
                        if net_profit > best_profit:
                            best_profit = net_profit
                            best_decision = (detect_combined, dismantle_combined, detect_final_product, dismantle_final_product,
                                             total_cost, total_revenue, net_profit)

    # 输出最佳决策
    if best_decision:
        detect_combined, dismantle_combined, detect_final_product, dismantle_final_product, total_cost, total_revenue, best_profit = best_decision

        detect_combined_TF = {part: 'T' if val == 1 else 'F' for part, val in detect_combined.items()}
        dismantle_combined_TF = {part: 'T' if val == 1 else 'F' for part, val in dismantle_combined.items()}
        detect_final_product_TF = 'T' if detect_final_product else 'F'
        dismantle_final_product_TF = 'T' if dismantle_final_product else 'F'

        print(f"最佳决策 - 零配件/半成品检测: {detect_combined_TF}, 零配件/半成品拆解: {dismantle_combined_TF}, 检测成品: {detect_final_product_TF}, 拆解成品: {dismantle_final_product_TF}")
        print(f"总成本: {total_cost:.2f}, 总收益: {total_revenue:.2f}, 净利润: {best_profit:.2f}")
    else:
        print("未能找到有效的最佳决策。")

# 使用更新后的case数据
cases_updated = {
    "零配件1": {"次品率": "12.20%", "购买单价": 2, "检测成本": 1},
    "零配件2": {"次品率": "13.48%", "购买单价": 8, "检测成本": 1},
    "零配件3": {"次品率": "11.93%", "购买单价": 12, "检测成本": 2},
    "零配件4": {"次品率": "13.00%", "购买单价": 2, "检测成本": 1},
    "零配件5": {"次品率": "12.36%", "购买单价": 8, "检测成本": 1},
    "零配件6": {"次品率": "11.93%", "购买单价": 12, "检测成本": 2},
    "零配件7": {"次品率": "11.56%", "购买单价": 8, "检测成本": 1},
    "零配件8": {"次品率": "11.13%", "购买单价": 12, "检测成本": 2},
    "半成品1": {"次品率": "10.76%", "装配成本": 8, "检测成本": 4, "拆解费用": 6},
    "半成品2": {"次品率": "13.53%", "装配成本": 8, "检测成本": 4, "拆解费用": 6},
    "半成品3": {"次品率": "13.96%", "装配成本": 8, "检测成本": 4, "拆解费用": 6},
    "成品": {
        "次品率": "11.51%",
        "装配成本": 8,
        "检测成本": 6,
        "拆解费用": 10,
        "市场售价": 200,
        "调换损失": 40
    }
}
# 运行最佳决策计算
calculate_best_decisions(cases_updated)