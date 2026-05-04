import pandas as pd

def call_traffic_function(input_data):

    calling_record_telephone = pd.read_excel(
        'row_data.xlsx', sheet_name='座席通话记录查询表-电话',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    calling_record_telephone['工号'] = calling_record_telephone['工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    condition = calling_record_telephone['电话号码'].astype(str).str.startswith('9')
    calling_record_telephone = calling_record_telephone.loc[~condition, :]

    print('开始遍历计算每一名员工的话务量')
    for i in range(input_data.shape[0]):

        staff_id = input_data.loc[i, '工号']
        emergency_start_time = pd.to_datetime(
            input_data.loc[i, '应急开始时间']).timestamp()
        emergency_end_time = pd.to_datetime(
            input_data.loc[i, '应急结束时间']).timestamp()

        calling_record_telephone_linshi = calling_record_telephone.loc[
            calling_record_telephone['工号'] == staff_id, :
        ].reset_index(drop=True, inplace=False)
        calling_time_start_list = calling_record_telephone_linshi['通话开始时间'].to_list()
        if calling_time_start_list != []:
            calling_time_start_list = [pd.to_datetime(i).timestamp()
                                       for i in calling_time_start_list]
            calling_time_start_list = [i for i in calling_time_start_list if
                                       emergency_start_time <= i <= emergency_end_time]
            input_data.loc[i, '话务量'] = len(calling_time_start_list)
        else:
            input_data.loc[i, '话务量'] = 0

    output_data = input_data
    return output_data

