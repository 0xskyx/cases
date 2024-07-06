from databae import CRUDHelper, Case
from utils import read_xlsx_to_dict


def import_database():
    # 使用示例
    path_to_file = '安全测试用例.xlsx'
    cases_list = []
    data = read_xlsx_to_dict(path_to_file)
    for key in data.keys():
        for index, case in enumerate(data[key]):
            if index == 0 or str(case[0]) == 'nan':
                continue
            cases_list.append([case[0], case[1], case[4], case[11], case[7]])

    success_count = 0
    error_count = 0
    for i in cases_list:
        new_case = Case(
            name=str(i[0]),
            risk=str(i[1]),
            description=str(i[2]),
            step=str(i[3]),
            caur=str(i[4])
        )
        print(new_case)
        added_case = crud_helper.add(new_case)
        if added_case:
            success_count += 1
        else:
            error_count += 1

    print(f'总共{len(cases_list)}条，成功{success_count}条，失败{error_count}条。')


if __name__ == '__main__':
    crud_helper = CRUDHelper('sqlite:///cases.db')
    # crud_helper.db.drop_tables()
    # crud_helper.db.create_tables()

    all_list = crud_helper.get_all(Case)

    temp = [x.to_list() for x in all_list]
    print(*temp, sep='\n')
