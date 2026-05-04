def emergency_yes_or_not_function(input_data):

    input_data['应急业务量'] = input_data['应急业务量'].astype(float)

    # 开始计算是否参与应急
    for i in range(input_data.shape[0]):

        first_login = input_data.loc[i, '首次签入']
        if first_login == '无':
            input_data.loc[i, '是否参与应急'] = '不在岗'
        else:
            emergency_workload_value = input_data.loc[i, '应急业务量']
            if emergency_workload_value == 0:
                if input_data.loc[i, '备注'] == '班长':
                    input_data.loc[i, '是否参与应急'] = '-'
                else:
                    input_data.loc[i, '是否参与应急'] = '未参与应急'
            if emergency_workload_value > 0:
                input_data.loc[i, '是否参与应急'] = '-'

    output_data = input_data

    return output_data
