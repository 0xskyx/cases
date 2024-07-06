import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QCheckBox, QDialog
from PyQt6.QtCore import Qt
from custom import CustomListWidget, CustomTableWidget, CustomDialog
from databae import CRUDHelper, Case
from utils import export_to_excel


class Cases(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.set_ui()
        self.set_layout()
        self.set_event()

        # 用例库
        self.crud = CRUDHelper('sqlite:///cases.db')
        # 初始化用例库数据到cases_table
        self.cases_reset()
        # 最终用例
        self.result_date = []

    def set_ui(self):
        self.setWindowTitle('安全测试用例辅助工具')
        self.resize(1250, 700)

        # top
        self.check_box = QCheckBox('全选', self)
        self.funcs_button = QPushButton('填入功能', self)

        self.key_info = QLineEdit('搜索关键字...', self)
        self.select_button = QPushButton('选择', self)
        self.export_button = QPushButton('导出', self)
        self.h_spacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # mid
        self.cases_table = CustomTableWidget(self)
        self.cases_table.setColumnCount(6)
        self.cases_table.setHorizontalHeaderLabels(
            ['编号', '名称', '风险', '描述', '步骤', '整改'])
        self.func_list = CustomListWidget(self)

        # down
        self.result_table = CustomTableWidget(self)
        self.result_table.setColumnCount(8)
        self.result_table.setHorizontalHeaderLabels(
            ['编号', '名称', '风险', '描述', '步骤', '整改', '功能', '结果'])

    def set_layout(self):
        # 顶部
        self.top_layout = QHBoxLayout()
        self.top_layout.addWidget(self.check_box)
        self.top_layout.addWidget(self.funcs_button)

        # 左边
        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.top_layout)
        self.left_layout.addWidget(self.func_list)

        # 右边
        self.up_layout = QHBoxLayout()
        self.up_layout.addWidget(self.key_info)
        self.up_layout.addWidget(self.select_button)
        self.up_layout.addWidget(self.export_button)
        self.up_layout.addItem(self.h_spacer)

        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.up_layout)
        self.right_layout.addWidget(self.cases_table)
        self.right_layout.addWidget(self.result_table)

        # 底部
        self.down_layout = QHBoxLayout()
        self.down_layout.addLayout(self.left_layout)
        self.down_layout.addLayout(self.right_layout)

        # all
        self.all_layout = QVBoxLayout()
        self.all_layout.addLayout(self.top_layout)
        self.all_layout.addLayout(self.down_layout)
        self.setLayout(self.all_layout)

    def set_event(self):
        self.select_button.clicked.connect(self.add_result)
        self.check_box.stateChanged.connect(lambda e: self.box_change(e))
        self.funcs_button.clicked.connect(self.show_dialog)
        self.key_info.textChanged.connect(lambda e: self.select_change(e))
        self.export_button.clicked.connect(self.export_data_to_excel)

    def add_result(self):
        row = self.cases_table.currentRow()
        row_data = []
        if row >= 0:
            for column in range(self.cases_table.columnCount()):
                item = self.cases_table.item(row, column)
                if item:
                    row_data.append(item.text())
                else:
                    row_data.append('')

            # 将新行数据填充到新行中
        funcs_list = self.func_list.get_checked_items()
        if len(list(filter(lambda x: x != '', row_data))) == 6 and len(funcs_list) > 0 and self.cases_table.currentRow() >= 0:
            for i in funcs_list:
                temp = row_data.copy()
                temp.extend([i, ''])
                # print(temp)
                if not any(sorted(l) == sorted(temp) for l in self.result_table.get_table_data()):
                    self.result_table.add_text_row(temp)

    def box_change(self, event):
        # print(event)
        for index in range(self.func_list.count()):
            item = self.func_list.item(index)
            if event:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)

    def show_dialog(self):
        dialog = CustomDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 处理LineEdit中的文本
            for i in set(dialog.edit.toPlainText().split('\n')):
                if i != '':
                    self.func_list.add_item(i)

    def cases_reset(self):
        self.cases_table.setRowCount(0)
        for i in [x.to_list() for x in self.crud.get_all(Case)]:
            self.cases_table.add_text_row(i)

    def select_change(self, event):
        if len(event) == 0:
            self.cases_table.setRowCount(0)
            self.cases_reset()
        elif len(event) > 0:
            self.cases_table.setRowCount(0)
            for i in [x.to_list() for x in self.crud.get_by_name_like(Case, event)]:
                self.cases_table.add_text_row(i)

    def export_data_to_excel(self):
        datas = self.result_table.get_table_data()
        try:
            if len(datas) > 0:
                export_to_excel(datas)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    cases = Cases()
    cases.show()
    sys.exit(app.exec())
