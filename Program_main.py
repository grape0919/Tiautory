import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from view.main import Ui_MainWindow
from nohand.blogInfo import selProp
from nohand.blogInfo import ApiProp
from nohand.noHandBlogger import ApiBlogger, SeleniumBlogger

import static.staticValues as staticValues

class WindowClass(Ui_MainWindow) :

    running = False
    login = False

    def __init__(self) :
        super(WindowClass, self).__init__()
        self.setupUi(self)
        
        self.button_file.clicked.connect(self.showFileDialog)
        
        self.button_login.clicked.connect(self.login)

        self.button_write.clicked.connect(self.writeArticle)
        self.button_write.setEnabled(False)

        self.prop = selProp()
        # self.prop = ApiProp()
        self.edit_url.setText(self.prop.url)
        self.edit_id.setText(self.prop.id)
        self.edit_passwd.setText(self.prop.passwd)

        self.blogger = SeleniumBlogger()

    def login(self):
        self.prop.url = self.edit_url.text()
        self.prop.id = self.edit_id.text()
        self.prop.passwd = self.edit_passwd.text()
        self.prop.save()
        
        self.blogger.setProp(self.prop)

        checkLogin = self.blogger.login()

        if(checkLogin):
            self.login = True
            QMessageBox.about(self, "로그인", "로그인에 성공하였습니다.")
            self.button_login.setStyleSheet(staticValues.grayButtonStyleSheet)
            self.button_login.setEnabled(False)
            self.button_write.setStyleSheet(staticValues.blueButtonStyleSheet)
            self.button_write.setEnabled(True)
        else:
            self.login = False
            QMessageBox.about(self, "로그인", "로그인 실패하였습니다.\nurl, id, password 를 확인해주세요.")
            self.button_login.setStyleSheet(staticValues.redButtonStyleSheet)
            self.button_write.setStyleSheet(staticValues.grayButtonStyleSheet)
            self.button_write.setEnabled(False)

    def showFileDialog(self):
        print("Clicked button")
        fname = QFileDialog.getOpenFileName(self, 'Open excel for paragraph', 'Desktop',
                                            "Excel (*.xls *.xlsx)")
        if fname[0]:
            self._filePath = fname[0]
            self.edit_filePath.setText(fname[0])

    def writeArticle(self):
        print("Clicked write button")

        if(self.running == False):
            if(not self.edit_url.text().endswith(".com") and \
                not self.edit_url.text().endswith(".com/")):
                QMessageBox.about(self, "Warning", "url은 .com/ 까지만 작성해주세요.")
                return

            if(self.edit_filePath.text() == None or self.edit_filePath.text() == ""):
                QMessageBox.about(self, "Warning", "문단 파일을 먼저 선택하세요.")
                return
                
            if(self.edit_period.text() == '' or int(self.edit_period.text()) < 5 ):
                QMessageBox.about(self, "Warning", "게시 주기는 최소 5분 이상 설정할 수 있습니다..")
                return
                
            QMessageBox.about(self, "자동 게시 시작", "자동 글쓰기를 시작합니다.")
            self.button_write.setText("자동 등록 중")
            self.button_write.setStyleSheet(staticValues.redButtonStyleSheet)

            self.blogger.setDate(self.dateTime_upload.dateTime() ,int(self.edit_period.text()))

            self.running = True

            self.blogger.readExcelFile(self.edit_filePath.text())
            suc = self.blogger.postArticle()
            
            if(suc is not None and not suc[0]):
                QMessageBox.about(self, "경고", suc[1])
                self.button_write.setText("자동 등록 시작")
                self.button_write.setStyleSheet(staticValues.blueButtonStyleSheet)
                self.running = False
                self.blogger.running = False

        else:
            QMessageBox.about(self, "자동 포스팅 정지", "자동 포스팅을 정지합니다.")
            self.button_write.setText("자동 등록 시작")
            self.button_write.setStyleSheet(staticValues.blueButtonStyleSheet)
            self.running = False
            self.blogger.running = False

    def closeEvent(self, event):
       self.running = False
       self.blogger.running = False
       event.accept()
        


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()

#https://dudrhkd12.tistory.com/manage/entry/post