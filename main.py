import warnings
warnings.filterwarnings('ignore')

from creat_result_dataframe import *
from select_and_copy import *
from required_attendance_duration import *
from start_end_actually import *
from emergency_workload import *
from emergency_attribute import *
from emergency_period import *
from check_in_and_out import *
from online_users_num import *
from number_of_return_visits import *
from call_traffic import *
from emergency_yes_or_not import *


# 定义主函数
def main():

    # 第一步，先获取需要的结果表
    result_data = creat_result_dataframe_function()

    # 开始第二步，能复制粘贴的部分就复制粘贴
    result_data = select_and_copy_function(input_data=result_data)

    # 开始第三步，计算列：应参与时长
    result_data = required_attendance_duration_function(input_data=result_data)

    # 应急的开始和结束时间，实际的时间，不是安排的时间
    result_data = start_end_actually_function(input_data=result_data)

    # 开始计算，应急属性
    result_data = emergency_attribute_function(input_data=result_data)

    # 开始判断，应急时段
    result_data = emergency_period_function(input_data=result_data)

    # 开始计算，首次签入，末次签出，这两列
    result_data = check_in_and_out_function(input_data=result_data)

    # 开始计算，在线量
    result_data = online_users_num_function(input_data=result_data)

    # 开始计算，回访量
    result_data = number_of_return_visits_function(input_data=result_data)

    # 开始计算，话务量
    result_data = call_traffic_function(input_data=result_data)

    # 在计算完黄色区域的三列之后，再计算应急业务量
    # 开始计算，应急业务量
    result_data = emergency_workload_function(input_data=result_data)

    # 开始计算，是否参与应急
    result_data = emergency_yes_or_not_function(input_data=result_data)

    # 以上步骤处理完后，保存表格
    result_data.to_excel('result_data.xlsx', index=False)


main()
