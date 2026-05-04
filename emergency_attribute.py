import pandas as pd


def emergency_attribute_function(input_data):

    total_value_command = pd.read_excel('row_data.xlsx', sheet_name='总值指令')
    work_schedule = pd.read_excel('row_data.xlsx', sheet_name='班次时间表')

    # 遍历每一行来计算应急属性
    # 遍历每一名员工来计算应急属性
    print('判断每一名员工的应急属性')
    for i in range(input_data.shape[0]):

        # 这一行（该员工）的，班组名称
        working_group = input_data.loc[i, '班组']
        command_start_time = input_data.loc[i, '指令开始']
        date_time = input_data.loc[i, '日期']

        # 通过客服部的表，的班组名称，对应到总值指令，找对应的，班次
        service_shift = total_value_command.loc[
            total_value_command['应急班组']==working_group, '应急班次']
        service_shift = list(set(service_shift.to_list()))[0]
        # 上面这个就是，班次
        # 通过班次，获取，班次时间表，里面的上下班时间

        work_schedule_linshi = work_schedule.loc[work_schedule['班次']==service_shift, :]

        work_start_time = work_schedule_linshi['上班时间'].to_list()[0]
        work_start_time = f'{date_time} {work_start_time}'
        work_start_time = pd.to_datetime(work_start_time)
        work_start_time = work_start_time.timestamp()

        work_end_time = work_schedule_linshi['下班时间'].to_list()[0]
        work_end_time = f'{date_time} {work_end_time}'
        work_end_time = pd.to_datetime(work_end_time)
        work_end_time = work_end_time.timestamp()

        # 指令开始时间转化为时间戳
        command_start_time = f'{date_time} {command_start_time}'
        command_start_time = pd.to_datetime(command_start_time)
        command_start_time = command_start_time.timestamp()

        # 接下来开始判断应急属性
        if command_start_time < work_start_time:
            emergency_attribute = '提前到岗'
        if work_start_time <= command_start_time < work_end_time:
            emergency_attribute = '在班应急'
        if command_start_time == work_end_time:
            emergency_attribute = '延班应急'
        if work_end_time < command_start_time:
            emergency_attribute = '下班到岗'

        # 开始赋值
        input_data.loc[i, '应急属性'] = emergency_attribute

    output_data = input_data
    return output_data


