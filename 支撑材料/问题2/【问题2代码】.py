# 定义6种情形数据
cases = [
    {'defect_rate_1': 0.1, 'defect_rate_2': 0.1, 'check_cost_1': 2, 'check_cost_2': 3, 'assemble_cost': 6,
     'check_cost': 3, 'market_price': 56, 'replace_cost': 6, 'dismantle_cost': 5, 'N_total': 1000},
    {'defect_rate_1': 0.2, 'defect_rate_2': 0.2, 'check_cost_1': 2, 'check_cost_2': 3, 'assemble_cost': 6,
     'check_cost': 3, 'market_price': 56, 'replace_cost': 6, 'dismantle_cost': 5, 'N_total': 1000},
    {'defect_rate_1': 0.1, 'defect_rate_2': 0.1, 'check_cost_1': 2, 'check_cost_2': 3, 'assemble_cost': 6,
     'check_cost': 3, 'market_price': 56, 'replace_cost': 30, 'dismantle_cost': 5, 'N_total': 1000},
    {'defect_rate_1': 0.2, 'defect_rate_2': 0.2, 'check_cost_1': 1, 'check_cost_2': 1, 'assemble_cost': 6,
     'check_cost': 2, 'market_price': 56, 'replace_cost': 30, 'dismantle_cost': 5, 'N_total': 1000},
    {'defect_rate_1': 0.1, 'defect_rate_2': 0.2, 'check_cost_1': 8, 'check_cost_2': 1, 'assemble_cost': 6,
     'check_cost': 2, 'market_price': 56, 'replace_cost': 10, 'dismantle_cost': 5, 'N_total': 1000},
    {'defect_rate_1': 0.05, 'defect_rate_2': 0.05, 'check_cost_1': 2, 'check_cost_2': 3, 'assemble_cost': 6,
     'check_cost': 3, 'market_price': 56, 'replace_cost': 10, 'dismantle_cost': 40, 'N_total': 1000}
]
# 调整后的计算不合格品数量的逻辑
def calculate_defective_products(case, detect_part_1, detect_part_2):
    N = case["N_total"]
    P1 = case["defect_rate_1"]
    P2 = case["defect_rate_2"]
    
    if detect_part_1 == 1 and detect_part_2 == 1:
        return N * 0.1  # 两个零配件都检测，不合格率固定为10%
    elif detect_part_1 == 1:
        return N * (0.1 + P2)  # 仅检测零配件1
    elif detect_part_2 == 1:
        return N * (0.1 + P1)  # 仅检测零配件2
    else:
        delta_Pd = P1 + P2 - P1 * P2  # 不检测时次品率提高值
        return N * (0.1 + delta_Pd)  # 两个零配件都不检测

# 计算退回的不合格品数量
def calculate_return_defective_products(case, detect_part_1, detect_part_2):
    N = case["N_total"]
    P1 = case["defect_rate_1"]
    P2 = case["defect_rate_2"]
    
    # 根据检测情况计算不合格品数量
    if detect_part_1 == 1 and detect_part_2 == 1:
        return N * 0.1  # 两个零配件都检测
    elif detect_part_1 == 1:
        return N * (0.1 + P2)  # 仅检测零配件1
    elif detect_part_2 == 1:
        return N * (0.1 + P1)  # 仅检测零配件2
    else:
        delta_Pd = P1 + P2 - P1 * P2  # 两个零配件都不检测时的次品率
        return N * (0.1 + delta_Pd)

# 计算成本
def calculate_costs(case, detect_part_1, detect_part_2, detect_final_product, dismantle, return_products=False):
    N = case["N_total"]
    
    # 根据给出的公式，计算不合格品数量
    defective_products = calculate_defective_products(case, detect_part_1, detect_part_2)
    qualified_products = N - defective_products

    # 检测成本
    check_costs = (case["check_cost_1"] * detect_part_1 + case["check_cost_2"] * detect_part_2 + case["check_cost"] * detect_final_product) * N
    
    # 替换成本（不检测时已包含期望替换成本）
    replace_costs = defective_products * case["replace_cost"]
    
    # 拆解成本（根据不合格品的拆解决策）
    dismantle_costs = dismantle * defective_products * case["dismantle_cost"]
    
    # 装配成本
    assemble_costs = case["assemble_cost"] * N
    
    # 总成本
    total_cost = check_costs + replace_costs + dismantle_costs + assemble_costs
    return total_cost, qualified_products

# 计算总收益
def calculate_revenue(case, qualified_products):
    return qualified_products * case["market_price"]

# 动态规划逻辑，包括退回的不合格品处理
def dynamic_programming(case, case_index, handle_returns=False):
    detect_part_1, detect_part_2, detect_final_product, dismantle = 0, 0, 0, 0
    max_net_profit = float('-inf')
    best_decision = (0, 0, 0, 0)

    for detect_part_1 in [0, 1]:
        for detect_part_2 in [0, 1]:
            for detect_final_product in [0, 1]:
                for dismantle in [0, 1]:
                    total_cost, qualified_products = calculate_costs(case, detect_part_1, detect_part_2, detect_final_product, dismantle)
                    total_revenue = calculate_revenue(case, qualified_products)
                    net_profit = total_revenue - total_cost

                    # 处理退回的不合格品（这里不会产生新的市场收益，也不产生新的成本）
                    if handle_returns:
                        print(f"情况 {case_index + 1}: 无需额外处理退回品，未产生新的成本和收益")
                    
                    if net_profit > max_net_profit:
                        max_net_profit = net_profit
                        best_decision = (detect_part_1, detect_part_2, detect_final_product, dismantle)
                        print(f"情况 {case_index + 1} - 当前最佳决策: 零配件1检测={detect_part_1}, 零配件2检测={detect_part_2}, 成品检测={detect_final_product}, 拆解={dismantle}, 净利润={net_profit:.2f}")

    return max_net_profit, best_decision

# 主函数
def main():
    for case_index, case in enumerate(cases):
        max_net_profit, best_decision = dynamic_programming(case, case_index, handle_returns=True)
        initial_cost, qualified_products = calculate_costs(case, *best_decision)
        initial_revenue = calculate_revenue(case, qualified_products)
        
        # 退回处理阶段不再产生新成本
        print(f"情况 {case_index + 1}: 退回品已处理，未产生新的退回成本。")

        # 最终净利润 = 初始阶段的净利润（无新的退回处理成本）
        final_net_profit = initial_revenue - initial_cost

        print(f"情况 {case_index + 1} - 最终最佳决策: 零配件1检测={best_decision[0]}, 零配件2检测={best_decision[1]}, 成品检测={best_decision[2]}, 拆解={best_decision[3]}")
        print(f"初始总成本: {initial_cost:.2f}, 初始总收益: {initial_revenue:.2f}")
        print(f"最终净利润: {final_net_profit:.2f}")
        print("-" * 30)

# 执行程序
main()
