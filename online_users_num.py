import pandas as pd


def online_users_num_function(input_data):

    # 自助工单-电子
    self_service_work_order_elec = pd.read_excel(
        'row_data.xlsx', sheet_name='自助工单-电子',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    self_service_work_order_elec['受理人员工号'] = self_service_work_order_elec['受理人员工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    # 会话查询
    conversation_query_elec = pd.read_excel(
        'row_data.xlsx', sheet_name='会话查询-电子',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str})
    conversation_query_elec['受理人员'] = conversation_query_elec['受理人员'].str.replace(
        '^0209', '0200', regex=True, n=1)

    # 开始计算在线量
    print('遍历每一个员工，计算每一名员工的在线量')
    for i in range(input_data.shape[0]):

        # 从表格中，提取当前员工的信息
        stuff_id = input_data.loc[i, '工号']
        emergency_start_time = pd.to_datetime(
            input_data.loc[i, '应急开始时间']).timestamp()
        emergency_end_time = pd.to_datetime(
            input_data.loc[i, '应急结束时间']).timestamp()

        # 获取当前员工的服务请求时间，并且转换为秒级时间戳
        self_service_work_order_elec_linshi = self_service_work_order_elec.loc[
            self_service_work_order_elec['受理人员工号'] == stuff_id, :
        ].reset_index(drop=True, inplace=False)
        service_request_time = self_service_work_order_elec_linshi['服务请求时间'].to_list()
        if service_request_time != []:
            service_request_time = [
                pd.to_datetime(i).timestamp() for i in service_request_time]
            service_request_time = [ts for ts in service_request_time if
                                    emergency_start_time <= ts <= emergency_end_time]
            self_service_work_order_num = len(service_request_time)
        else:
            self_service_work_order_num = 0
        # 上面是，获取，自助工单，提供的业务量

        # 下面开始计算会话查询提供的业务量
        conversation_query_elec_linshi = conversation_query_elec.loc[
            conversation_query_elec['受理人员'] == stuff_id, :
        ].reset_index(drop=True, inplace=False)
        session_start_time = conversation_query_elec_linshi['会话开始时间'].to_list()
        if session_start_time != []:
            session_start_time = [
                pd.to_datetime(i).timestamp() for i in session_start_time]
            session_start_time = [ts for ts in session_start_time if
                                  emergency_start_time <= ts <= emergency_end_time]
            conversation_query_elec_num = len(session_start_time)
        else:
            conversation_query_elec_num = 0

        # 开始计算在线量
        # 自助工单量*1+会话量*0.9
        online_num = self_service_work_order_num + conversation_query_elec_num * 0.9
        input_data.loc[i, '在线量'] = online_num


    output_data = input_data
    return output_data


