"""
Function: 该模块控制登录事件,同时也是各个模块的集合
"""

import os
import sys
import Sign_Up
import Admin
import Database
import Main
# from Sign_Up import SignWindow  # 注册所需要的自定义库
# from Admin import AdminWindow
# from Database import Database
# from Main import Main

# try:
#     import PyQt5
# except ModuleNotFoundError:
#     os.system("pip install PyQt5")
#     from PyQt5.Qt import *
# else:
#     from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFrame, QMessageBox, QComboBox
#     from PyQt5.QtGui import QIcon, QFont
#     from PyQt5.QtCore import Qt, pyqtSignal

# import PyQt5


from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QFrame, QMessageBox, QComboBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal

class MyWindow(QWidget):

    _signal_send = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.icon = QIcon(r"D:\projects_of_python\StrokePatients_Fatigue_Detection\IMG\python-logo.png")
        self.database = Database.Database(r'D:\projects_of_python\StrokePatients_Fatigue_Detection\predictor\data.db')
        self.sign_up_win = Sign_Up.SignWindow()  # 创建的注册窗口
        self.admin_win = Admin.AdminWindow()  # 创建的用户管理窗口
        self.main_win = Main.Main()  # 登录后的主页面
        self.admin_win.set_main_window(self.main_win)
        self.setWindowTitle("基于面部特征和头部姿态的卒中患者疲劳度检测软件")
        self.setFixedSize(1000, 562)
        self.set_ui()


        self._signal_send.connect(self.main_win.get_Login_Name)
    def change_icon(self):
        """用来修改图像的图标"""
        self.setWindowIcon(self.icon)

    def set_ui(self):
        """设置界面"""
        self.set_background_image()  # 设置背景的图片
        self.change_icon()
        self.add_label()
        self.add_line_edit()
        self.add_button()

    def add_label(self):
        """添加相应的标签"""
        # 设置字体
        label_font = QFont()
        label_font.setFamily('LiSu')
        label_font.setBold(True)
        label_font.setPixelSize(35)

        label_name_font = QFont()
        label_name_font.setFamily("LiSu")
        label_name_font.setBold(True)
        label_name_font.setPixelSize(70)

        # 创建文本标签
        self.username_label = QLabel(self)
        self.password_label = QLabel(self)
        self.APP_Name = QLabel(self)

        # 设置标签中的文本
        self.username_label.setText("用户名")
        # self.username_label.setStyleSheet("color:#043a6a")
        self.password_label.setText("密  码")
        # self.password_label.setStyleSheet("color:#043a6a")
        self.APP_Name.setText("卒中患者疲劳度检测软件")
        # self.APP_Name.setStyleSheet("color:#043a6a")

        # 设置标签的大小
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)
        self.APP_Name.setFixedSize(900,60)

        # 设置标签的位置
        self.username_label.move(185, 350)
        self.password_label.move(185, 420)
        self.APP_Name.move(140,140)

        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)
        self.APP_Name.setFont(label_name_font)

    def add_line_edit(self):
        """添加输入框"""
        line_edit_font = QFont()
        line_edit_font.setFamily('LiSu')
        line_edit_font.setPixelSize(30)

        # 创建
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)

        # 设置密码格式
        self.password_edit.setEchoMode(QLineEdit.Password)

        # 设置字体
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)

        # 设置占位符
        self.username_edit.setPlaceholderText("请输入用户名")
        self.password_edit.setPlaceholderText("请输入密码")

        # 设置大小
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)

        # 设置位置
        self.username_edit.move(320, 355)
        self.password_edit.move(320, 425)

    def add_button(self):
        """添加按钮"""
        button_font = QFont()
        button_font.setFamily('LiSu')
        button_font.setPixelSize(30)

        # 创建按钮对象
        self.login_button = QPushButton("登录", self)
        self.sign_button = QPushButton(self)

        # 修改大小且不可变
        self.login_button.setFixedSize(160, 50)
        self.sign_button.setFixedSize(160, 50)

        # 设置字体
        self.login_button.setFont(button_font)
        self.sign_button.setFont(button_font)

        # 设置位置
        self.login_button.move(750, 350)
        self.sign_button.move(750, 420)

        # 设置文本提示内容
        self.login_button.setText("登录")
        self.sign_button.setText("注册")
        self.login_button.setToolTip('如果您是超级管理员，请使用特定账号登录！')

        # 实现功能，按钮点击之后执行的动作
        self.login_button.clicked.connect(self.login)
        self.sign_button.clicked.connect(self.sign_up_window)

        self.login_button.setShortcut("返回")  # 设置快捷键

    def set_background_image(self):
        """添加背景图片"""
        self.frame = QFrame(self)  # 这里采用 QFrame, 如果直接对self进行背景设置，似乎没有那么简单容易控制
        self.frame.resize(1000,562)
        # self.frame.move(40, 150)
        self.frame.setStyleSheet(
            'background-image: url("./IMG/img_login.png"); background-repeat: no-repeat; text-align:center;')

    def login(self):
        """登录功能实现"""

        username = self.username_edit.text()
        password = self.password_edit.text()
        data = self.database.find_password_by_username(username)  # 在数据库中查找数据
        if username and password:  # 如果两个输入框都不为空
            if data:
                if str(data[0][0]) == password:
                    # QMessageBox.information(self, 'Successfully', '登录成功 \n 欢迎用户 {}'.format(username),
                    #                         QMessageBox.Yes | QMessageBox.No)
                    self.password_edit.setText('') # 登录成功，将之前的用户信息清除
                    self.username_edit.setText('')
                    self.close()
                    if username == 'admin':  # 如果是管理员，进入管理界面

                        self.admin_win.show()
                    else:
                        self.main_win.show()
                        self._signal_send.emit(username)


                else:
                    QMessageBox.information(self, 'Failed', '密码错误, 请重新输入！',
                                            QMessageBox.Yes | QMessageBox.No)
            else:
                QMessageBox.information(self, 'Error', '不存在当前用户名！', QMessageBox.Yes)
        elif username:  # 如果用户名写了
            QMessageBox.information(self, 'Error', '请输入您的密码！', QMessageBox.Yes | QMessageBox.No)
        else:
            QMessageBox.information(self, 'Error', '请输入完整信息！', QMessageBox.Yes | QMessageBox.No)

    def sign_up_window(self):
        self.sign_up_win.setWindowIcon(self.icon)
        self.sign_up_win.move(self.x() + 50, self.y() + 50)  # 移动一下注册窗口，以免和之前的重复
        # frame = QFrame(self.sign_up_win)
        self.sign_up_win.setWindowFlag(Qt.Dialog)
        # frame.resize(1000, 562)
        # frame.setStyleSheet(
        #     'background-image: url("./IMG/img_login.png"); background-repeat: no-repeat; text-align:center;')
        # frame.move(40, 150)
        # 打开注册窗口时，清除原来的信息
        self.password_edit.setText('')
        self.username_edit.setText('')
        self.sign_up_win.show()

    def closeEvent(self, event):
        self.sign_up_win.close()  # 关闭登录窗口的时候，注册窗口也应该关闭


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()

    sys.exit(app.exec_())

