from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QListWidget, QTableWidget, QMenu, QMessageBox, QInputDialog, QListWidgetItem, QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox, QTableWidgetItem
from PyQt6.QtCore import Qt, QPoint


class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.init_ui()

        self.funcs_set = set()

    def init_ui(self):
        self.setMaximumWidth(240)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = QMenu()

        new_action = QAction('新增', self)
        edit_action = QAction('编辑', self)
        delete_action = QAction('删除', self)

        new_action.triggered.connect(self.new_item)
        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_checked_items)

        menu.addAction(new_action)
        menu.addAction(edit_action)
        menu.addAction(delete_action)

        menu.exec(self.mapToGlobal(position))

    def new_item(self):
        item_text, ok = QInputDialog.getText(
            self, 'New Item', 'Enter item text:')
        if ok and item_text:
            self.add_item(item_text)

    def add_item(self, item_text: str):
        item_text.strip()
        if item_text not in self.funcs_set:
            item = QListWidgetItem(item_text)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.funcs_set.add(item_text.strip())
            self.addItem(item)

    def edit_item(self):
        item = self.currentItem()
        if item:
            new_text, ok = QInputDialog.getText(
                self, 'Edit Item', 'Edit item text:', text=item.text())
            new_text.strip()
            if ok and new_text and new_text not in self.funcs_set:
                self.funcs_set.add(new_text.strip())
                item.setText(new_text)

    def delete_checked_items(self):
        for i in reversed(range(self.count())):
            item = self.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.takeItem(i)

    def get_checked_items(self):
        checked_items = []
        for index in range(self.count()):
            item = self.item(index)
            if item.checkState() == Qt.CheckState.Checked:
                checked_items.append(item.text())
        return checked_items


class CustomTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.right_click_row = -1

    def show_context_menu(self, position: QPoint):
        # 获取右键单击的行号
        self.right_click_row = self.rowAt(position.y())

        # 创建右键菜单
        self.context_menu = QMenu(self)

        # 添加新增一行的操作
        add_row_action = self.context_menu.addAction("新增一行")
        add_row_action.triggered.connect(self.add_new_row)

        # 添加删除当前行的操作
        delete_row_action = self.context_menu.addAction("删除当前行")
        delete_row_action.triggered.connect(self.confirm_delete_row)

        # 显示右键菜单
        self.context_menu.exec(self.viewport().mapToGlobal(position))

    def add_new_row(self):
        # 获取当前行数并插入新行
        self.insertRow(self.rowCount())

    def add_text_row(self, row: list):
        if row:
            row_count = self.rowCount()
            self.insertRow(row_count)  # 在表的末尾添加一行
            for i, item in enumerate(row):
                self.setItem(row_count, i, QTableWidgetItem(item))

    def confirm_delete_row(self):
        # 弹出确认对话框
        if self.right_click_row != -1:
            reply = QMessageBox.question(self, '确认删除', '你确定要删除这行吗?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.delete_current_row()

    def delete_current_row(self):
        # 删除右键单击的行
        if self.right_click_row != -1:
            self.removeRow(self.right_click_row)
            # 重置右键单击行号
            self.right_click_row = -1


    def get_table_data(self):
        table_data = []
        for row in range(self.rowCount()):
            row_data = []
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append('')
            table_data.append(row_data)
        
        # 打印获取到的数据
        # print(table_data)
        return table_data


class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("按行写入功能")
        self.resize(240, 600)
        layout = QVBoxLayout(self)

        self.edit = QTextEdit(self)
        layout.addWidget(self.edit)

        # 创建对话框按钮
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

        self.setLayout(layout)
