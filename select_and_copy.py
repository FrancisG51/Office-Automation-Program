import pandas as pd


def select_and_copy_function(input_data):

    # 使用总值指令，粘贴人员名单
    total_value_command = pd.read_excel('row_data.xlsx', sheet_name='总值指令')
    staff_list = pd.read_excel('row_data.xlsx',
                               sheet_name='人员名单', dtype={'工号': str})

    # 遍历总值指令的每一行，每一行的信息，对于人员名单进行筛选过滤
    for i in range(total_value_command.shape[0]):

        # 应急班组
        emergency_class = total_value_command.loc[i, '应急班组']
        # 应急部门
        emergency_department = total_value_command.loc[i, '应急部门']
        # 指令时间
        emergency_time_period = total_value_command.loc[i, '应急时间段']
        commend_start_time, commend_end_time = emergency_time_period.split('-')
        # 应急渠道
        emergency_channel = total_value_command.loc[i, '应急渠道']
        # 应急日期，原本的格式是时间戳
        emergency_date = total_value_command.loc[i, '日期']
        emergency_date = pd.to_datetime(emergency_date, unit='D', origin='1899-12-30')
        emergency_date = emergency_date.strftime('%Y/%m/%d')

        # 开始使用这两个变量从客服人员名单中提取数据
        staff_list_linshi = staff_list.loc[(staff_list['部门'] == emergency_department) &
                                           (staff_list['班组'] == emergency_class), :]
        staff_list_linshi = staff_list_linshi[['姓名', '工号', '部门', '班组', '备注']]
        staff_list_linshi.reset_index(drop=True, inplace=True)

        # 给人员数据，加上指令开始时间，指令结束时间
        staff_list_linshi['指令开始'] = commend_start_time
        staff_list_linshi['指令结束'] = commend_end_time

        # 给人员表，添加上应急渠道
        staff_list_linshi['应急渠道'] = emergency_channel

        # 给人员的临时表，加上，当前总值指令的，日期
        staff_list_linshi['日期'] = emergency_date

        # 对于整理好的表格，和input_data进行拼接
        if staff_list_linshi.shape[0] != 0:
            # 如果数据存在，那么就开始粘贴表格
            input_data = pd.concat([input_data, staff_list_linshi],
                                   ignore_index=True, sort=False, axis=0, join='outer')
        else:
            print('报错：总值指令的班组和部门，与人员名单表，字符串不匹配，或者总值指令表存在空值')
            print('报错的总值指令的行：', i + 1)

    input_data = input_data.dropna(how='all')
    output_data = input_data.reset_index(drop=True, inplace=False)
    print('结果表格中，复制粘贴的部分已经完成')

    # 将表格中的0209改为0200
    output_data['工号'] = output_data['工号'].str.replace('^0209', '0200', regex=True, n=1)
    output_data.reset_index(drop=True, inplace=True)

    # 为表格添加序号
    output_data['序号'] = range(1, output_data.shape[0] + 1)

    return output_data



