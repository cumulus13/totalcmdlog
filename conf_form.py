# -*- coding: utf-8 -*-

# self implementation generated from reading ui file 'config.ui'
#
# Created: Mon Feb 06 11:17:15 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import config

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Config_Form(QtGui.QMainWindow):
    #closed = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(Config_Form, self).__init__(parent)
        self.parent = parent
    #def setupUi(self, self):
    
        self.setObjectName(_fromUtf8("Form"))
        self.setFixedSize(472, 425)
        self.lineEdit = QtGui.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(110, 30, 51, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        
        self.lineEdit_host = QtGui.QLineEdit(self)
        self.lineEdit_host.setGeometry(QtCore.QRect(110,135, 200, 20))
        self.lineEdit_host.setObjectName(_fromUtf8("lineedit_host"))
        
        self.lineEdit_port = QtGui.QLineEdit(self)
        self.lineEdit_port.setGeometry(QtCore.QRect(110,165, 51, 20))
        self.lineEdit_port.setObjectName(_fromUtf8("lineedit_port"))
        
        self.lineEdit_username = QtGui.QLineEdit(self)
        self.lineEdit_username.setGeometry(QtCore.QRect(110,195, 200, 20))
        self.lineEdit_username.setObjectName(_fromUtf8("lineedit_username"))
        
        self.lineEdit_password = QtGui.QLineEdit(self)
        self.lineEdit_password.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_password.setGeometry(QtCore.QRect(110,225, 200, 20))
        self.lineEdit_password.setObjectName(_fromUtf8("lineedit_password"))
        
        self.lineEdit_database = QtGui.QLineEdit(self)
        self.lineEdit_database.setGeometry(QtCore.QRect(110,255, 200, 20))
        self.lineEdit_database.setObjectName(_fromUtf8("lineedit_database"))
        
        self.textEdit_table = QtGui.QLineEdit(self)
        self.textEdit_table.setGeometry(QtCore.QRect(110, 285, 200, 20))
        self.textEdit_table.setObjectName(_fromUtf8("textEdit_table"))
        self.textEdit_datalog = QtGui.QTextEdit(self)
        self.textEdit_datalog.setGeometry(QtCore.QRect(110, 60, 351, 65))
        self.textEdit_datalog.setObjectName(_fromUtf8("textEdit_datalog"))
        self.label_seconds = QtGui.QLabel(self)
        self.label_seconds.setGeometry(QtCore.QRect(170, 30, 46, 13))
        self.label_seconds.setObjectName(_fromUtf8("label_seconds"))
        self.label_timeround = QtGui.QLabel(self)
        self.label_timeround.setGeometry(QtCore.QRect(20, 30, 81, 16))
        self.label_timeround.setObjectName(_fromUtf8("label_timeround"))
        self.label_table = QtGui.QLabel(self)
        self.label_table.setGeometry(QtCore.QRect(67,286, 67,16))
        self.label_table.setObjectName(_fromUtf8("label_table"))
        self.label_datalog = QtGui.QLabel(self)
        self.label_datalog.setGeometry(QtCore.QRect(52, 80, 81, 20))
        self.label_datalog.setObjectName(_fromUtf8("label_datalog"))
        
        self.label_host = QtGui.QLabel(self)
        self.label_host.setGeometry(QtCore.QRect(70,136, 37,16))
        self.label_host.setObjectName(_fromUtf8("label_host"))
        
        self.label_port = QtGui.QLabel(self)
        self.label_port.setGeometry(QtCore.QRect(72,166, 35,16))
        self.label_port.setObjectName(_fromUtf8("label_port"))
        
        self.label_username = QtGui.QLabel(self)
        self.label_username.setGeometry(QtCore.QRect(40,196, 67,16))
        self.label_username.setObjectName(_fromUtf8("label_username"))
        
        self.label_password = QtGui.QLabel(self)
        self.label_password.setGeometry(QtCore.QRect(40,226, 67,16))
        self.label_password.setObjectName(_fromUtf8("label_password"))
        
        self.label_database = QtGui.QLabel(self)
        self.label_database.setGeometry(QtCore.QRect(42,256, 67,16))
        self.label_database.setObjectName(_fromUtf8("label_database"))
        
        self.label_info = QtGui.QLabel(self)
        self.label_info.setGeometry(QtCore.QRect(20, 320, 441, 71))
        self.label_info.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.label_info.setObjectName(_fromUtf8("label_info"))
        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(20, 395, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 395, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.setcenter()
        self.read_config()
    
    def setcenter(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - self.width())/2, (screen.height() - self.height())/6)

    def retranslateUi(self):
        self.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_seconds.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Seconds</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_timeround.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Time Round : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_table.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Table : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_datalog.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Log File : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_host.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Host : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_port.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Port : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_username.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Username : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_password.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Password : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_database.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; font-weight:600;\">Database : </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_info.setText(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic; color:#660101;\">Time Round is Time  long for repeat task before its.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-style:italic; color:#660101;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic; color:#660101;\">Access Log is Place of File Access Log Apache</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt; font-style:italic; color:#660101;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic; color:#660101;\">Error Log is Place of File Error Log Apache</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.connect(self.pushButton_2, QtCore.SIGNAL('clicked()'), self.write_config)
        self.pushButton.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.quit)
        
    def write_config(self):
        print "line edit= ", self.lineEdit.text()
        print "edit text 1 = ", self.textEdit_table.text()
        print "edit text 2 = ", self.textEdit_datalog.toPlainText()
        data = []
        data.append(int(self.lineEdit.text()))
        data.append(str(self.textEdit_table.text()))
        data.append(str(self.textEdit_datalog.toPlainText()))
        data.append(int(self.lineEdit_port.text()))
        data.append(str(self.lineEdit_username.text()))
        data.append(str(self.lineEdit_password.text()))
        data.append(str(self.lineEdit_database.text()))
        data.append(str(self.lineEdit_host.text()))
        """
        if str(self.lineEdit.text()) == ' ':
            data.append('0')
        else:
            data.append(int(self.lineEdit.text()))
        if str(self.textEdit_table) != ' ':
            data.append(str(self.textEdit_table.toPlainText()))
        else:
            data.append('0')
        if str(self.textEdit_datalog) != ' ':
            data.append(str(self.textEdit_datalog.toPlainText()))
        else:
            data.append('0')
        """
        print "data = ", data
        config.write_config(data)
        self.hide()
        
    def read_config(self):
        data = config.read_config()
        self.lineEdit.setText(str(data.setting[0].roundtime))
        self.textEdit_table.setText(str(data.setting[0].table))
        self.textEdit_datalog.setText(str(data.setting[0].datalog))
        self.lineEdit_port.setText(str(data.setting[0].port))
        self.lineEdit_username.setText(str(data.setting[0].username))
        self.lineEdit_password.setText(str(data.setting[0].password))
        self.lineEdit_database.setText(str(data.setting[0].database))
        self.lineEdit_host.setText(str(data.setting[0].host))
        
    def quit(self):
        self.hide()
        #import sys
        #sys.exit()
        
    def closeEvent(self, event):
        self.hide()
        #import sys
        #sys.exit()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    self = QtGui.QWidget()
    ui = Config_Form()
    #ui.setupUi(self)
    ui.show()
    sys.exit(app.exec_())

