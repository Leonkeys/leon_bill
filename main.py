import os
import sys
import csv
from datetime import timedelta

# todo 设置固定开支。
# todo 创建月度账单。
# todo 创建年度账单。
# todo 累计收入情况。
# todo 计算年度收入。
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDockWidget, QListWidget, QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton,
    QTextEdit, QMessageBox, QDateTimeEdit, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDateEdit, QDialogButtonBox,
    QPushButton, QFileDialog, QTableWidgetItem, QTableWidget
)
from PyQt6.QtCore import Qt, QDateTime, QDate


class DateRangeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择日期范围")
        self.resize(300, 100)

        layout = QVBoxLayout()
        self.start_date = QDateEdit()
        self.end_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.end_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.end_date.setDate(QDate.currentDate())

        layout.addWidget(QLabel("起始日期："))
        layout.addWidget(self.start_date)
        layout.addWidget(QLabel("结束日期："))
        layout.addWidget(self.end_date)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_dates(self):
        return self.start_date.date(), self.end_date.date()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 窗口 + 菜单栏 + 侧边栏 + 表单")
        self.resize(800, 500)

        self.init_sidebar()
        self.set_style()
        self.central = QTextEdit("请选择左侧功能")
        self.setCentralWidget(self.central)
        self.base_dir_path = r"D:\leon\leon_bill\bill_data"

    def init_sidebar(self):
        self.dock = QDockWidget("侧边栏", self)
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea
        )
        self.list_widget = QListWidget()
        self.list_widget.addItems(["创建", "列表", "月度小结"])
        self.list_widget.currentTextChanged.connect(self.on_sidebar_item_clicked)

        self.dock.setWidget(self.list_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)

    def on_sidebar_item_clicked(self, text):
        if text == "创建":
            self.show_form()
        elif text == "列表":
            dialog = DateRangeDialog()
            if dialog.exec():
                start_date, end_date = dialog.get_dates()
                self.show_table(start_date, end_date)
        else:
            self.central.setText(f"你选择了：{text}")

    def show_form(self):
        form_widget = QWidget()
        form_layout = QFormLayout()
        self.pay_input = QLineEdit()  # 消费金额
        self.pay_type_input = QComboBox(form_widget)
        self.pay_type_input.addItems(["餐费", "烟", "零食", "菜"])
        self.pay_time = QDateTimeEdit(form_widget)
        self.pay_time.setDateTime(QDateTime.currentDateTime())
        self.pay_desc = QLineEdit()
        submit_button = QPushButton("提交")
        submit_button.clicked.connect(
            self.submit_form
        )
        form_layout.addRow("消费金额：", self.pay_input)
        form_layout.addRow("消费类型：", self.pay_type_input)
        form_layout.addRow("消费时间：", self.pay_time)
        form_layout.addRow("消费详情：", self.pay_desc)
        form_layout.addRow("", submit_button)
        form_widget.setLayout(form_layout)
        self.setCentralWidget(form_widget)

    def show_table(self, start_date, end_date):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["消费时间", "消费类型", "金额", "详情"])
        all_rows = []

        current_date = start_date
        while current_date <= end_date:
            file_name = current_date.toString("yyyy-MM-dd") + ".csv"
            file_path = os.path.join(self.base_dir_path, file_name)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="gbk") as f:
                    for line in f:
                        parts = line.strip().split(",")
                        if len(parts) == 4:
                            all_rows.append(parts)
            current_date = current_date.addDays(1)

        table.setRowCount(len(all_rows))
        for row_idx, row_data in enumerate(all_rows):
            for col_idx, item in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(item))

        self.setCentralWidget(table)

    def submit_form(self):
        pay = self.pay_input.text()
        pay_type = self.pay_type_input.currentText()
        pay_datetime = self.pay_time.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        pay_date = pay_datetime.split(" ")[0]
        pay_desc = self.pay_desc.text()
        file_path = f"{self.base_dir_path}/{pay_date}.csv"
        if os.path.exists(file_path):
            with open(file_path, "a") as f:
                f.write(f"{pay_datetime},{pay_type},{pay},{pay_desc}\n")
        else:
            with open(file_path, "w") as f:
                f.write(f"{pay_datetime},{pay_type},{pay},{pay_desc}\n")
        QMessageBox.information(
            self,
            "提交成功",
            f"提交成功!"
        )
        self.pay_input.clear()
        self.pay_desc.clear()
        self.pay_type_input.setCurrentIndex(0)  # 性别重置为第一个选项
        self.pay_time.setDateTime(QDateTime.currentDateTime())  #

    def set_style(self):
        self.setStyleSheet("""
            QMenuBar {
                background-color: #333;
                color: white;
            }
            QMenu::item:selected {
                background-color: #666;
            }
            QDockWidget {
                background-color: #f0f0f0;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
