import pandas as pd


def emergency_period_function(input_data):

    print('开始判断应急时段')

    for i in range(input_data.shape[0]):

        emergency_start_time = input_data.loc[i, '应急开始时间']
        emergency_end_time = input_data.loc[i, '应急结束时间']

        # 获取实际的，应急，开始、结束的时间戳
        emergency_start_time = pd.to_datetime(emergency_start_time).timestamp()
        emergency_end_time = pd.to_datetime(emergency_end_time).timestamp()

        # 获取相应的，和，实际应急时间，相互比较的，时间戳
        date_time = input_data.loc[i, '日期']

        # 设定几个时间点
        time_21 = '21:00'   # 晚上，21点
        time_03 = '3:00'    # 跨夜，凌晨三点
        time_06 = '6:00'    # 早上六点
        time_09 = '9:00'    # 早上九点
        # 几个时间点，结合日期，转化为时间戳
        time_21 = pd.to_datetime(f'{date_time} {time_21}').timestamp()
        time_03 = (pd.to_datetime(f'{date_time} {time_03}') +
                   pd.Timedelta(days=1)).timestamp()
        time_06 = pd.to_datetime(f'{date_time} {time_06}').timestamp()
        time_09 = pd.to_datetime(f'{date_time} {time_09}').timestamp()

        # 开始进行判断
        if ((time_21 <= emergency_start_time <= time_03) and
                (time_21 <= emergency_end_time <= time_03)):
            emergency_period_value = '晚间应急'
        elif ((time_06 <= emergency_start_time <= time_09) and
                (time_06 <= emergency_end_time <= time_09)):
            emergency_period_value = '早间应急'
        elif ((time_09 <= emergency_start_time <= time_21) and
                (time_09 <= emergency_end_time <= time_21)):
            emergency_period_value = '非早晚间应急'
        else:
            emergency_period_value = '跨段'

        input_data.loc[i, '应急时段'] = emergency_period_value

    output_data = input_data
    return output_data
