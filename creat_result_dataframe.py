import numpy as np
import pandas as pd


def creat_result_dataframe_function():

    linshi_data = pd.read_excel('row_data.xlsx', sheet_name='客服部')
    columns_list = linshi_data.iloc[1, :].to_list()

    result_data = pd.DataFrame(columns=columns_list)
    result_data.loc[0, :] = np.nan

    return result_data

