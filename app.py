import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import client
client.SERVER = "51.250.108.31"


class MainWindow(QMainWindow):
    def __init__(self):
        client.set_up()
        super(MainWindow, self).__init__()
        self.login_page()


    def login_page(self):
        loadUi("./surce/login.ui", self)
        self.pushButton.clicked.connect(self.login1)
        self.lineEdit.textChanged.connect(self.label_4.hide)
        self.lineEdit_2.textChanged.connect(self.label_4.hide)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label_4.hide()
        self.lineEdit_2.returnPressed.connect(self.login1)
        self.lineEdit.returnPressed.connect(self.lineEdit_2.setFocus)

    def login1(self):
        login = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if client.autarisation(login, password):
            # print(f"[+]login: <{login}>, password: <{password}>")
            self.main_page()
        else:
            self.label_4.show()


    def main_page(self):
        loadUi("./surce/main_page.ui", self)
        self.pushButton.clicked.connect(self.browse_page)
        self.pushButton_2.clicked.connect(self.confirm_page)

    def confirm_page(self):
        loadUi("./surce/confirm_page.ui", self)
        if None:
            pixmap = QPixmap()
            pixmap.loadFromData(file)
            self.label.setPixmap(pixmap)
        else:
            self.label.setPixmap(QPixmap('./surce/not_found.png'))

        self.browse.clicked.connect(self.browsefiles)
    #
    def browse_page(self):
        loadUi("./surce/browse_page.ui", self)
        self.buttonBox.rejected.connect(self.main_page)
        self.buttonBox.accepted.connect(self.put_file)
    #     fname=QFileDialog.getOpenFileName(self, 'Open file', 'D:\codefirst.io\PyQt5 tutorials\Browse Files', 'Images (*.png, *.xmp *.jpg)')
    #     self.filename.setText(fname[0])
    def put_file(self):
        try:
            file_path = self.lineEdit.text()
            if '.' not in file_path:
                print("strange file with no extension")
                return
            file_extension = '.'+ file_path.split(".")[-1]
            target_dir = self.lineEdit_2.text()
            file_type = self.lineEdit_3.text()
            description =  self.lineEdit_4.text()
            report = client.put_file(file_path, target_dir, file_type, description, file_extension)
            self.massage_page(self.main_page, report)
        except Exception as e:
            print(e)
            self.massage_page(self.main_page, str(e))

    def massage_page(self, next_page, massage, *args):
        loadUi("./surce/massage_page.ui", self)
        self.label.setText(massage.rstrip())
        self.pushButton.clicked.connect(lambda: next_page(*args))



# try:
app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
sys.exit(app.exec_())
# finally:
    # client.send(client.DISCONNECT_MESSAGE.encode("utf-8"))
