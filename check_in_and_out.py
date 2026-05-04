import pandas as pd

def check_in_and_out_function(input_data):

    # 先读取需要的数据
    softphone_usage_report_for_agents = pd.read_excel(
        'row_data.xlsx',
        sheet_name='座席软电话应用统计表',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    softphone_usage_report_for_agents['工号'] = softphone_usage_report_for_agents['工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    print('开始计算，首次签入，末次签出，这两列')

    # 接下来开始遍历每一名员工
    for i in range(input_data.shape[0]):

        staff_id = input_data.loc[i, '工号']
        softphone_usage_report_for_agents_linshi = softphone_usage_report_for_agents.loc[(
            softphone_usage_report_for_agents['工号'] == staff_id
        ), :].reset_index(drop=True, inplace=False)

        if softphone_usage_report_for_agents_linshi.shape[0] != 0:
            # 如果该员工的首次签入签出的数据是存在的

            first_check_in_time = softphone_usage_report_for_agents_linshi.loc[
                :, '首次签入时间'].to_list()[0]
            last_check_out_time = softphone_usage_report_for_agents_linshi.loc[
                :, '末次签出时间'].to_list()[0]

            first_check_in_time = pd.to_datetime(
                first_check_in_time).strftime('%Y-%m-%d %H:%M:%S')
            last_check_out_time = pd.to_datetime(
                last_check_out_time).strftime('%Y-%m-%d %H:%M:%S')

            input_data.loc[i, '首次签入'] = first_check_in_time
            input_data.loc[i, '末次签出'] = last_check_out_time
        else:
            input_data.loc[i, '首次签入'] = '无'
            input_data.loc[i, '末次签出'] = '无'

    output_data = input_data
    return output_data

