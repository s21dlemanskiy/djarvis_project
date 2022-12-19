import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import client
import json
client.SERVER = "158.160.23.155"


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
        self.pushButton_2.clicked.connect(self.confirm_list_page)
        self.pushButton_3.clicked.connect(self.download_results)

    def download_results(self):
        data = client.download_confirmed()
        with open("Results.json", 'w', encoding='utf-8') as f:
            json.dump(obj=data, fp=f, indent=4)
        self.massage_page(self.main_page, "Saved in 'Results.json'")

    def confirm_list_page(self):
        loadUi("./surce/confirm_list.ui", self)
        # Loading...
        confirm_list = client.get_list_for_cofirm()
        self.pushButton.clicked.connect(lambda: (self.pushButton.setText('Loading...'),
                                                self.confirm_page(confirm_list)))
        print(f"confirm list:{confirm_list}")
        self.listWidget.addItems(map(lambda x: f"file_path: {x[1]} desctiption: {x[2]}", confirm_list))





    def confirm_page(self, confirm_list):
        file_data = None
        cv_result = None
        loadUi("./surce/confirm_page.ui", self)
        self.pushButton.clicked.connect(self.main_page)
        self.pushButton_2.clicked.connect(lambda: self.confirm(confirm_list, file_data))
        if len(confirm_list) == 0:
            self.massage_page(self.main_page, "all confirmed")
            return
        file_data = confirm_list[0]
        file, cv_result = client.get_file_to_confirm(file_data[0])
        if file:
            with open('1.jpg', 'bw') as f:
                f.write(file)
            self.textEdit.setPlainText(cv_result.replace(",", ",\n"))
            pixmap = QPixmap()
            pixmap.loadFromData(file)
            self.label.setPixmap(pixmap)
        else:
            self.label.setPixmap(QPixmap('./surce/not_found.png'))

    def confirm(self, confirm_list, file_data):
        self.pushButton_2.setText('Loading...')
        id1 = file_data[0]
        user_result = self.textEdit.toPlainText()
        modified_rows = client.confirm_result(id1, user_result)
        confirm_list.remove(file_data)
        if modified_rows > 0:
            self.massage_page(self.confirm_page, "whrited", confirm_list)
        else:
            self.massage_page(self.confirm_page, "smth gone wrong \n nothing was whrited", confirm_list)

    #
    def browse_page(self):
        loadUi("./surce/browse_page.ui", self)
        self.label_5.hide()
        self.buttonBox.rejected.connect(self.main_page)
        self.buttonBox.accepted.connect(self.put_file)
        self.pushButton.clicked.connect(self.browse_file)

    def browse_file(self):
        fname=QFileDialog.getOpenFileName(self, 'Open file', './', '*.png *.xmp *.jpg')
        self.lineEdit.setText(fname[0])



    def put_file(self):
        self.label_5.show()
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
