import pandas as pd
import json
from datetime import datetime


def get_current_timestamp():
    # 获取当前时间
    now = datetime.now()

    # 格式化时间戳，精确到毫秒
    timestamp = now.strftime('%Y-%m-%d %H.%M.%S.%f')[:-3]
    return str(timestamp)


def read_xlsx_to_dict(path):
    # 读取xlsx文件的所有sheet名称
    xls = pd.ExcelFile(path)
    sheet_names = xls.sheet_names

    # 初始化返回的字典
    data_dict = {}

    # 遍历每个sheet
    for sheet in sheet_names:
        # 读取sheet数据到DataFrame
        df = pd.read_excel(path, sheet_name=sheet)

        # 将列标题转换为list
        columns = df.columns.tolist()

        # 将DataFrame转换为list（list）
        sheet_data = df.values.tolist()

        # 在sheet_data的最前面加入包含列标题的子列表
        sheet_data_with_title = [columns] + sheet_data

        # 将数据加入到字典中
        data_dict[sheet] = sheet_data_with_title

    return data_dict


def export_to_excel(data, file_path=f'{get_current_timestamp()}.xlsx'):
    # 创建一个 DataFrame
    df = pd.DataFrame(
        data, columns=['编号', '名称', '风险', '描述', '步骤', '整改', '功能', '结果'])
    # 将 DataFrame 导出为 Excel 文件
    df.to_excel(file_path, index=False)


def write_dict_to_json(data_dict, json_path):
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)
