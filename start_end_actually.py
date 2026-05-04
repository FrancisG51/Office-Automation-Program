import pandas as pd
from tqdm import tqdm
import copy


def start_end_actually_function(input_data):

    # 先把需要的数据导入进来，并且保证加载的工号是字符串，以及，先做工号的修改

    calling_record_telephone = pd.read_excel(
        'row_data.xlsx', sheet_name='座席通话记录查询表-电话',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    calling_record_telephone['工号'] = calling_record_telephone['工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    call_back_telephone = pd.read_excel(
        'row_data.xlsx', sheet_name='回访明细-电话',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str}, skiprows=1, header=0)
    call_back_telephone['受理工号'] = call_back_telephone['受理工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    self_service_work_order_elec = pd.read_excel(
        'row_data.xlsx', sheet_name='自助工单-电子',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    self_service_work_order_elec['受理人员工号'] = self_service_work_order_elec['受理人员工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    conversation_query_elec = pd.read_excel(
        'row_data.xlsx', sheet_name='会话查询-电子',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    conversation_query_elec['受理人员'] = conversation_query_elec['受理人员'].str.replace(
        '^0209', '0200', regex=True, n=1)

    # 先计算应急开始时间
    print('开始计算，实际应急时长')

    # 载入迁出记录
    check_out_sheet = pd.read_excel('row_data.xlsx', sheet_name='座席软电话明细查询', header=2,
                                    dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    check_out_sheet['工号'] = check_out_sheet['工号'].str.replace('^0209', '0200', regex=True, n=1)

    for i in tqdm(range(input_data.shape[0]), desc='遍历每一名员工计算实际应急时间'):

        # 遍历整个结果表的每一名员工来计算对应的，实际应急时间
        staff_id = input_data.loc[i, '工号']
        command_date = input_data.loc[i, '日期']
        command_start_time = input_data.loc[i, '指令开始']
        command_end_time = input_data.loc[i, '指令结束']
        emergency_channel = input_data.loc[i, '应急渠道']

        # 将具体时间转化为秒级时间戳，处理跨天的情况
        time_stamp_command_start = pd.to_datetime(command_date + ' ' + command_start_time)
        time_stamp_command_end = pd.to_datetime(command_date + ' ' + command_end_time)
        if time_stamp_command_end < time_stamp_command_start:
            time_stamp_command_end = time_stamp_command_end + pd.Timedelta(days=1)
        time_stamp_command_start = time_stamp_command_start.timestamp()
        time_stamp_command_end = time_stamp_command_end.timestamp()

        # 指令开始时间，前五分钟
        time_stamp_command_start_less_5min = time_stamp_command_start - 5 * 60
        # 指令开始时间，后五分钟
        time_stamp_command_start_after_5min = time_stamp_command_start + 5 * 60

        # 指令结束时间，前五分钟
        time_stamp_command_end_less_5min = time_stamp_command_end - 5 * 60

        # 开始针对每一名员工，分为电话、电子、电话-电子这三种情况来计算相应的实际应急时间
        # 这一步的if判断，最后需要返回该员工，相应渠道的，工作时间的时间戳的，list格式，并且排序好

        # 电话渠道的计算
        if emergency_channel == '电话渠道':

            # 两个表格，通过工号筛选
            calling_record_telephone_linshi = copy.deepcopy(
                calling_record_telephone.loc[calling_record_telephone['工号'] == staff_id, :])
            call_back_telephone_linshi = copy.deepcopy(
                call_back_telephone.loc[call_back_telephone['受理工号'] == staff_id, :])

            calling_record_telephone_linshi.reset_index(drop=True, inplace=True)
            call_back_telephone_linshi.reset_index(drop=True, inplace=True)

            # 设定一个列表，用于存储当前员工的时间，然后再将list里面所有的元素，转化为秒级时间戳
            # 含有datetime的list就是if判断的结果
            datetime_list = (
                    (pd.to_datetime(calling_record_telephone_linshi['通话开始时间'])).to_list() +
                    (pd.to_datetime(call_back_telephone_linshi['回访时间'])).to_list()
            )

        if emergency_channel == '电子渠道':

            # 电子渠道的两个表格，进行工号的筛选
            self_service_work_order_elec_linshi = copy.deepcopy(
                self_service_work_order_elec.loc[self_service_work_order_elec['受理人员工号'] == staff_id, :])
            conversation_query_elec_linshi = copy.deepcopy(
                conversation_query_elec.loc[conversation_query_elec['受理人员'] == staff_id, :])

            self_service_work_order_elec_linshi.reset_index(drop=True, inplace=True)
            conversation_query_elec_linshi.reset_index(drop=True, inplace=True)

            datetime_list = (
                    (pd.to_datetime(self_service_work_order_elec_linshi['座席受理时间'])).to_list() +
                    (pd.to_datetime(conversation_query_elec_linshi['会话开始时间'])).to_list()
            )

        if emergency_channel == '电话电子渠道':

            # 同时搜索电话、电子四个表的datetime
            calling_record_telephone_linshi = copy.deepcopy(
                calling_record_telephone.loc[calling_record_telephone['工号'] == staff_id, :])
            call_back_telephone_linshi = copy.deepcopy(
                call_back_telephone.loc[call_back_telephone['受理工号'] == staff_id, :])
            self_service_work_order_elec_linshi = copy.deepcopy(
                self_service_work_order_elec.loc[self_service_work_order_elec['受理人员工号'] == staff_id, :])
            conversation_query_elec_linshi = copy.deepcopy(
                conversation_query_elec.loc[conversation_query_elec['受理人员'] == staff_id, :])

            calling_record_telephone_linshi.reset_index(drop=True, inplace=True)
            call_back_telephone_linshi.reset_index(drop=True, inplace=True)
            self_service_work_order_elec_linshi.reset_index(drop=True, inplace=True)
            conversation_query_elec_linshi.reset_index(drop=True, inplace=True)

            datetime_list = (
                    (pd.to_datetime(calling_record_telephone_linshi['通话开始时间'])).to_list() +
                    (pd.to_datetime(call_back_telephone_linshi['回访时间'])).to_list() +
                    (pd.to_datetime(self_service_work_order_elec_linshi['座席受理时间'])).to_list() +
                    (pd.to_datetime(conversation_query_elec_linshi['会话开始时间'])).to_list()
            )

        # 跳出if

        # 跳出if，获取了全部都是datetime的list，然后将其转化为秒级时间戳
        timestamp_list = [dt.timestamp() for dt in datetime_list]
        timestamp_list.sort()

        # 指令开始时间的前后五分钟
        timestamp_list_commend_start_qian_hou_5_min = [
            ts for ts in timestamp_list if
            time_stamp_command_start_less_5min <= ts <= time_stamp_command_start_after_5min
        ]
        timestamp_list_commend_start_qian_hou_5_min.sort()

        # 前后五分钟的秒级时间戳已经转化完成
        # 开始判断
        if timestamp_list_commend_start_qian_hou_5_min == []:
            # 如果前后五分钟是空列表，那么开始时间就是，指令开始时间
            emergency_actually_start_time = time_stamp_command_start
        else:
            # 如果不是空列表，那么先取第一个话务的时间
            actually_start_time = timestamp_list_commend_start_qian_hou_5_min[0]
            # 不是空列表的话，进一步判断时间的先后
            if actually_start_time <= time_stamp_command_start:
                emergency_actually_start_time = time_stamp_command_start
            else:
                emergency_actually_start_time = actually_start_time
        # 这里获得了，实际的，应急开始时间

        # 找出筛选指令结束时间前的末通话务开始时间
        time_stamp_before_commend_end = [
            ts for ts in timestamp_list if
            time_stamp_command_start <= ts <= time_stamp_command_end
        ]
        time_stamp_before_commend_end.sort()

        # 有了指令结束时间前的时间戳list，然后开始做判断
        if time_stamp_before_commend_end == []:
            emergency_actually_end_time = time_stamp_command_end
        else:
            # 指令结束时间前的时间戳，不是空集，选出来结束时间前的末次，通话开始时间
            # 这个就是，筛选出的值
            actually_last_time_stamp = time_stamp_before_commend_end[-1]
            if time_stamp_command_end_less_5min <= actually_last_time_stamp <= time_stamp_command_end:
                emergency_actually_end_time = time_stamp_command_end

            else:
                # 未在结束前五分钟内的
                # 接下来是新的需求，需要签出时间表，先提取那个人、那个时间段内的迁出时间的表格
                check_out_sheet_linshi = check_out_sheet.loc[check_out_sheet['工号'] == staff_id, :]
                check_out_sheet_linshi = check_out_sheet_linshi.loc[check_out_sheet_linshi['动作'] == '签出', :]
                check_out_time_list = check_out_sheet_linshi['操作时间'].to_list()
                if len(check_out_time_list) >= 1:
                    check_out_time_list = [
                        int(pd.to_datetime(str, format='%Y-%m-%d %H:%M:%S').timestamp()) for str in check_out_time_list
                    ]
                    check_out_time_list = [timestamp_num for timestamp_num in check_out_time_list if
                                               time_stamp_command_start <= timestamp_num <= time_stamp_command_end]
                    if len(check_out_time_list) >= 1:
                        # 这种情况下，说明总值指令时间段内，存在签出记录，签出时间就是实际的结束时间
                        emergency_actually_end_time = check_out_time_list[-1]
                    else:
                        # 没有签出记录的话，结束时间按照总值指令时间输出
                        emergency_actually_end_time = actually_last_time_stamp
                else:
                    # 两个连续的else都是代表同一个意思，如果没有签出记录的话，那么应急结束时间就是指令结束时间
                    emergency_actually_end_time = actually_last_time_stamp
        # 这里获得了，实际的，应急结束时间

        # 计算实际应急时长
        # 需要考虑跨天的情况
        if emergency_actually_end_time >= emergency_actually_start_time:
            emergency_actually_duration = round((emergency_actually_end_time - emergency_actually_start_time) / 3600, 2)
        else:
            emergency_actually_end_time_new = emergency_actually_end_time + pd.Timedelta(days=1)
            emergency_actually_duration = round((emergency_actually_end_time_new - emergency_actually_start_time) / 3600, 2)

        # 将实际的，应急开始时间，应急结束时间，从秒级时间戳转化为datetime
        emergency_actually_start_time = pd.to_datetime(emergency_actually_start_time, unit='s')
        emergency_actually_end_time = pd.to_datetime(emergency_actually_end_time, unit='s')
        emergency_actually_start_time = emergency_actually_start_time.strftime('%Y/%m/%d %H:%M:%S')
        emergency_actually_end_time = emergency_actually_end_time.strftime('%Y/%m/%d %H:%M:%S')

        # 开始赋值
        input_data.loc[i, '应急开始时间'] = emergency_actually_start_time
        input_data.loc[i, '应急结束时间'] = emergency_actually_end_time
        input_data.loc[i, '应急时长（时）'] = emergency_actually_duration

    output_data = input_data
    return output_data

