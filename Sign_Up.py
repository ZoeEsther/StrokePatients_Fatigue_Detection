"""
Function: 该模块控制注册事件
"""

from PyQt5.QtWidgets import QLabel, QLineEdit, QWidget, QPushButton,QMessageBox, QApplication, QFrame
from PyQt5.QtGui import QFont
import Database
# from .Database import Database
import sys


class SignWindow(QWidget):
    def __init__(self):
        super(SignWindow, self).__init__()
        self.database = Database.Database(r'D:\projects_of_python\StrokePatients_Fatigue_Detection\predictor\data.db')
        self.setWindowTitle("用户注册")  # 设置标题
        self.resize(1000,562)  # 设置窗口的大小
        self.set_ui()  # 调用其他的设计方法

    def set_ui(self):  # 集合所有的设计
        self.set_signup_background_image()  # 设置背景的图片
        self.add_line_edit()
        self.add_button()
        self.add_label()

    def set_signup_background_image(self):
        """添加背景图片"""
        self.frame = QFrame(self)  # 这里采用 QFrame, 如果直接对self进行背景设置，似乎没有那么简单容易控制
        self.frame.resize(1000, 562)
        # self.frame.move(40, 150)
        self.frame.setStyleSheet(
            'background-image: url("./IMG/img_login.png");'
            'background-repeat: no-repeat; text-align:center;')

    def add_label(self):
        """添加相应的标签"""
        # 设置文本的字体
        label_font = QFont()
        label_font.setFamily('LiSu')
        label_font.setPixelSize(35)

        # 创建三个对应的标签，父窗口为 self
        self.username_label = QLabel(self)
        self.password_label = QLabel(self)
        self.confirm_label = QLabel(self)

        # 相应的标签设置文本
        self.username_label.setText("用户名")
        self.password_label.setText("密  码")
        self.confirm_label.setText("确  认")

        # 控制label的大小  fixedSize表示之后无法修改
        self.username_label.setFixedSize(240, 40)
        self.password_label.setFixedSize(240, 40)
        self.confirm_label.setFixedSize(240, 40)

        # 设置对应的位置，注意move不是移动多少，而是直接移动到
        self.username_label.move(185, 190)
        self.password_label.move(185, 260)
        self.confirm_label.move(185, 330)

        # 设置字体
        self.username_label.setFont(label_font)
        self.password_label.setFont(label_font)
        self.confirm_label.setFont(label_font)

    def add_line_edit(self):
        """添加输入框"""
        line_edit_font = QFont()
        line_edit_font.setFamily('LiSu')
        line_edit_font.setPixelSize(30)

        # 创建三个输入框，父窗口为 self
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.confirm_edit = QLineEdit(self)

        # 设置密码格式，输入密码的时候不可见密码
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_edit.setEchoMode(QLineEdit.Password)

        # 设置一下字体
        self.username_edit.setFont(line_edit_font)
        self.password_edit.setFont(line_edit_font)
        self.confirm_edit.setFont(line_edit_font)

        # 设置输入框中的占位符
        self.username_edit.setPlaceholderText("用户名")
        self.password_edit.setPlaceholderText("密码")
        self.confirm_edit.setPlaceholderText('再次输入密码')

        # 控制大小
        self.username_edit.setFixedSize(350, 40)
        self.password_edit.setFixedSize(350, 40)
        self.confirm_edit.setFixedSize(350, 40)

        # 控制位置
        self.username_edit.move(320, 190)
        self.password_edit.move(320, 260)
        self.confirm_edit.move(320, 330)

    def add_button(self):
        """添加按钮"""
        button_font = QFont()
        button_font.setFamily('LiSu')
        button_font.setPixelSize(30)

        self.sign_button = QPushButton(self)
        self.sign_button.setFixedSize(160, 50)
        self.sign_button.setFont(button_font)
        self.sign_button.move(750, 260)
        self.sign_button.setText("注册")

        self.sign_button.setShortcut('返回')

        self.sign_button.clicked.connect(self.sign_up)

    def sign_up(self):
        """实现注册功能"""
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm = self.confirm_edit.text()

        if not password or not confirm:  # 如果有一个密码或者密码确认框为空
            QMessageBox.information(self, 'Error', '请输入完整信息！',
                                    QMessageBox.Yes)
        elif self.database.is_has(username):  # 如果用户名已经存在
            QMessageBox.information(self, 'Error',
                                    '该用户已存在！',
                                    QMessageBox.Yes)
        else:
            if password == confirm and password:  # 如果两次密码一致，并且不为空
                if len(username) < 2:
                    QMessageBox.information(self, 'Error',
                                            '用户名应至少两个字符或汉字！',
                                            QMessageBox.Yes, QMessageBox.Yes)
                    return
                if len(password) < 6:
                    QMessageBox.information(self, 'Error',
                                            '密码应至少6个字符，请重新输入！',
                                            QMessageBox.Yes)
                    return
                else:
                    self.database.insert_table(username, password)  # 将用户信息写入数据库
                    QMessageBox.information(self, 'Successfully',
                                            '注册成功'.format(
                                                username),
                                            QMessageBox.Yes)
                    self.close()  # 注册完毕之后关闭窗口
            else:
                QMessageBox.information(self, 'Error',
                                        '两次密码不相同！',
                                        QMessageBox.Yes)

    def closeEvent(self, event):
        """关闭之后将输入框清空"""
        self.username_edit.setText('')
        self.confirm_edit.setText('')
        self.password_edit.setText('')

#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = SignWindow()
#     window.show()
#
#     sys.exit(app.exec_())