from tqdm import tqdm


def emergency_workload_function(input_data):

    # 遍历每一个员工之前，先读取需要的数据

    for i in tqdm(range(input_data.shape[0]), desc='遍历计算每一个员工的应急业务量'):

        # 开始读取表格的，每一个员工的信息
        staff_id = input_data.loc[i, '工号']
        emergency_channel = input_data.loc[i, '应急渠道']

        if emergency_channel == '电话电子渠道':
            input_data.loc[i, '应急业务量'] = (
                    input_data.loc[i, '在线量'] +
                    input_data.loc[i, '回访量'] +
                    input_data.loc[i, '话务量']
            )
        if emergency_channel == '电话渠道':
            input_data.loc[i, '应急业务量'] = (
                    input_data.loc[i, '回访量'] +
                    input_data.loc[i, '话务量']
            )
        if emergency_channel == '电子渠道':
            input_data.loc[i, '应急业务量'] = input_data.loc[i, '在线量']


    output_data = input_data
    return output_data


