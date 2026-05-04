import pandas as pd

def number_of_return_visits_function(input_data):

    # 读取回访明细的表格
    call_back_telephone = pd.read_excel(
        'row_data.xlsx', sheet_name='回访明细-电话',
        dtype={'工号': str, '受理工号': str, '受理人员': str, '受理人员工号': str}, skiprows=1, header=0)
    call_back_telephone['受理工号'] = call_back_telephone['受理工号'].str.replace(
        '^0209', '0200', regex=True, n=1)

    # 将回访时间，转化为统一的格式
    for i in range(call_back_telephone.shape[0]):
        if type(call_back_telephone.loc[i, '回访时间']) == float:
            call_back_telephone.loc[i, '回访时间'] = pd.to_datetime(
                call_back_telephone.loc[i, '回访时间'], unit='D', origin='1899-12-30')
            call_back_telephone.loc[i, '回访时间'] = call_back_telephone.loc[i, '回访时间'].round('s')

    print('遍历每一名员工，计算回访量')
    # 遍历循环input_data的每一行，遍历每一个员工
    for i in range(input_data.shape[0]):

        # 读取该员工的信息
        stuff_id = input_data.loc[i, '工号']
        emergency_start_time = pd.to_datetime(
            input_data.loc[i, '应急开始时间']).timestamp()
        emergency_end_time = pd.to_datetime(
            input_data.loc[i, '应急结束时间']).timestamp()

        call_back_telephone_linshi = call_back_telephone.loc[
            call_back_telephone['受理工号'] == stuff_id, :].reset_index(drop=True, inplace=False)

        # 回访成功
        call_back_telephone_linshi_success = call_back_telephone_linshi.loc[
            call_back_telephone_linshi['回访状态'] == '回访成功', :]
        success_time_stamp_list = call_back_telephone_linshi_success['回访时间'].to_list()

        # 回访失败
        call_back_telephone_linshi_fail = call_back_telephone_linshi.loc[
            call_back_telephone_linshi['回访状态'] == '回访失败', :]
        fail_time_stamp_list = call_back_telephone_linshi_fail['回访时间'].to_list()

        # 回访成功，回访失败，挨个判断
        if len(success_time_stamp_list) != 0:
            success_time_stamp_list = [
                i.timestamp() for i in success_time_stamp_list]
            success_time_stamp_list = [
                i for i in success_time_stamp_list if
                emergency_start_time <= i <= emergency_end_time]
            success_95598_num = len(success_time_stamp_list)
        else:
            success_95598_num = 0
        if len(fail_time_stamp_list) != 0:
            fail_time_stamp_list = [
                i.timestamp() for i in fail_time_stamp_list]
            fail_time_stamp_list = [
                i for i in fail_time_stamp_list if
                emergency_start_time <= i <= emergency_end_time]
            fail_95598_num = len(fail_time_stamp_list)
        else:
            fail_95598_num = 0

        # 运算结束，开始对于相应的变量赋值
        return_visit_num = success_95598_num * 0.65 + fail_95598_num * 0.3
        input_data.loc[i, '回访量'] = return_visit_num

    output_data = input_data
    return output_data

