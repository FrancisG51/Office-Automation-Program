import pandas as pd


def required_attendance_duration_function(input_data):

    print('开始计算，应参与时长')

    input_data['start_time_linshi'] = pd.to_datetime(input_data['指令开始'], format='%H:%M')
    input_data['end_time_linshi'] = pd.to_datetime(input_data['指令结束'], format='%H:%M')

    # 处理跨天情况
    input_data.loc[input_data['end_time_linshi'] < input_data['start_time_linshi'],
                   'end_time_linshi'] += pd.Timedelta(days=1)

    # 计算应参与时长，并且保留小数点后两位
    input_data['应参与时长'] = (
        (input_data['end_time_linshi'] - input_data['start_time_linshi'])
        .dt.total_seconds().div(3600).round(2))

    output_data = input_data
    output_data.drop(['start_time_linshi', 'end_time_linshi'], axis=1, inplace=True)
    output_data.reset_index(drop=True, inplace=True)
    return output_data



