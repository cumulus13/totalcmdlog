import sys
import os
from PyQt4 import QtCore, QtGui, QtNetwork
import parserlog
import config
import conf_form
import time
import traceback
#from multiprocessing import Process
from pysqlite2 import dbapi2 as sqlite
import pysqlite2
import re
import subprocess
import controll_stop
import sender


class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self._parser = parserlog.parser()
        self.dataconf = config.read_config()
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.statusText = "Stop"
        
        self.sqlA = '''CREATE TABLE IF NOT EXISTS [datatemp](
                       [id] BIGINT(100) NOT NULL PRIMARY KEY,
                       [pid] VARCHAR(255) NOT NULL,
                       [name] VARCHAR(255) NOT NULL,
                       [addinfo] VARCHAR(255) NOT NULL)'''
        
        #self.conn = sqlite.connect(os.environ['TEMP'] + '\\' + 'dtemp.db')
        self.conn = sqlite.connect('dtemp.db')
        self.curs = self.conn.cursor()
        self.process = QtCore.QProcess()
        
        #self.createIconGroupBox()
        #self.createMessageGroupBox()

        #self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

        self.createActions()
        self.createTrayIcon()
        self.setIcon()

        #QtCore.QObject.connect(self.showMessageButton,
        #        QtCore.SIGNAL("clicked()"), self.showMessage)
        #QtCore.QObject.connect(self.showIconCheckBox,
        #        QtCore.SIGNAL("toggled(bool)"), self.trayIcon,
        #        QtCore.SLOT("setVisible(bool)"))
        #QtCore.QObject.connect(self.iconComboBox,
        #        QtCore.SIGNAL("currentIndexChanged(int)"), self.setIcon)
        #QtCore.QObject.connect(self.trayIcon,
        #        QtCore.SIGNAL("messageClicked()"), self.messageClicked)
        #QtCore.QObject.connect(self.trayIcon,
        #        QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),
        #        self.iconActivated)

        #mainLayout = QtGui.QVBoxLayout()
        #mainLayout.addWidget(self.iconGroupBox)
        #mainLayout.addWidget(self.messageGroupBox)
        #self.setLayout(mainLayout)

        #self.iconComboBox.setCurrentIndex(1)
        self.trayIcon.show()

        #self.setWindowTitle(self.tr("Systray"))
        #self.resize(400, 300)

    #def setVisible(self, visible):
    #    self.minimizeAction.setEnabled(visible)
    #    self.maximizeAction.setEnabled(not self.isMaximized())
    #    self.restoreAction.setEnabled(self.isMaximized() or not visible)
    #    QtGui.QWidget.setVisible(self, visible)

    #def closeEvent(self, event):
    #    if self.trayIcon.isVisible():
    #        QtGui.QMessageBox.information(self, self.tr("Systray"),
    #                self.tr("The program will keep running in the system "
    #                    "tray. To terminate the program, choose <b>Quit</b> "
    #                    "in the context menu of the system tray entry."))
    #        self.hide()
    #        event.ignore()

    def setIcon(self, index=0):
        #icon = self.iconComboBox.itemIcon(index)
        icon = QtGui.QIcon("images/totalcmd.png")
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

        #self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

    #def iconActivated(self, reason):
    #    if reason == QtGui.QSystemTrayIcon.Trigger \
    #            or reason == QtGui.QSystemTrayIcon.DoubleClick:
    #        self.iconComboBox.setCurrentIndex(
    #                (self.iconComboBox.currentIndex() + 1)
    #                % self.iconComboBox.count())
    #    elif reason == QtGui.QSystemTrayIcon.MiddleClick:
    #        self.showMessage()

    #def showMessage(self):
    #    icon = QtGui.QSystemTrayIcon.MessageIcon(
    #         self.typeComboBox.itemData(
    #             self.typeComboBox.currentIndex()).toInt()[0])
    #    self.trayIcon.showMessage(self.titleEdit.text(),
    #            self.bodyEdit.toPlainText(), icon,
    #            self.durationSpinBox.value() * 1000)

    #def messageClicked(self):
    #    QtGui.QMessageBox.information(None, self.tr("Systray"),
    #            self.tr("Sorry, I already gave what help I could.\nMaybe you "
    #                "should try asking a human?"))

    #def createIconGroupBox(self):
    #    self.iconGroupBox = QtGui.QGroupBox(self.tr("Tray Icon"))

    #    self.iconLabel = QtGui.QLabel("Icon:")

    #    self.iconComboBox = QtGui.QComboBox()
    #    self.iconComboBox.addItem(QtGui.QIcon("LifeJack.jpg"),
    #            self.tr("Bad"))

    #    self.showIconCheckBox = QtGui.QCheckBox(self.tr("Show icon"))
    #    self.showIconCheckBox.setChecked(True)

    #    iconLayout = QtGui.QHBoxLayout()
    #    iconLayout.addWidget(self.iconLabel)
    #    iconLayout.addWidget(self.iconComboBox)
    #    iconLayout.addStretch()
    #    iconLayout.addWidget(self.showIconCheckBox)
    #    self.iconGroupBox.setLayout(iconLayout)

    #def createMessageGroupBox(self):
    #    self.messageGroupBox = QtGui.QGroupBox(self.tr("Balloon Message"))

    #    self.typeLabel = QtGui.QLabel(self.tr("Type:"))

    #    self.typeComboBox = QtGui.QComboBox()
    #    self.typeComboBox.addItem(self.tr("None"),
    #            QtCore.QVariant(QtGui.QSystemTrayIcon.NoIcon))
    #    self.typeComboBox.addItem(self.style().standardIcon(
    #            QtGui.QStyle.SP_MessageBoxInformation), self.tr("Information"),
    #            QtCore.QVariant(QtGui.QSystemTrayIcon.Information))
    #    self.typeComboBox.addItem(self.style().standardIcon(
    #            QtGui.QStyle.SP_MessageBoxWarning), self.tr("Warning"),
    #            QtCore.QVariant(QtGui.QSystemTrayIcon.Warning))
    #    self.typeComboBox.addItem(self.style().standardIcon(
    #            QtGui.QStyle.SP_MessageBoxCritical), self.tr("Critical"),
    #            QtCore.QVariant(QtGui.QSystemTrayIcon.Critical))
    #    self.typeComboBox.setCurrentIndex(1)

    #    self.durationLabel = QtGui.QLabel(self.tr("Duration:"))

    #    self.durationSpinBox = QtGui.QSpinBox()
    #    self.durationSpinBox.setRange(5, 60)
    #    self.durationSpinBox.setSuffix(" s")
    #    self.durationSpinBox.setValue(15)

    #    self.durationWarningLabel = QtGui.QLabel(self.tr("(some systems might "
        #           "ignore this hint)"))
    #    self.durationWarningLabel.setIndent(10)

    #    self.titleLabel = QtGui.QLabel(self.tr("Title:"))

    #    self.titleEdit = QtGui.QLineEdit(self.tr("Cannot connect to network"))

    #    self.bodyLabel = QtGui.QLabel(self.tr("Body:"))

    #    self.bodyEdit = QtGui.QTextEdit()
    #    self.bodyEdit.setPlainText(self.tr("Don't believe me. Honestly, I "
    #            "don't have a clue.\nClick this balloon for details."))

    #    self.showMessageButton = QtGui.QPushButton(self.tr("Show Message"))
    #    self.showMessageButton.setDefault(True)

    #    messageLayout = QtGui.QGridLayout()
    #    messageLayout.addWidget(self.typeLabel, 0, 0)
    #    messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
    #    messageLayout.addWidget(self.durationLabel, 1, 0)
    #    messageLayout.addWidget(self.durationSpinBox, 1, 1)
    #    messageLayout.addWidget(self.durationWarningLabel, 1, 2, 1, 3)
    #    messageLayout.addWidget(self.titleLabel, 2, 0)
    #    messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
    #    messageLayout.addWidget(self.bodyLabel, 3, 0)
    #    messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
    #    messageLayout.addWidget(self.showMessageButton, 5, 4)
    #    messageLayout.setColumnStretch(3, 1)
    #    messageLayout.setRowStretch(4, 1)
    #    self.messageGroupBox.setLayout(messageLayout)

    def createActions(self):

        self.runAction = QtGui.QAction(self.tr("&Run"), self)
        self.runAction.setIcon(QtGui.QIcon('images/run.png'))
        #QtCore.QObject.connect(self.runAction,
        #                       QtCore.SIGNAL("triggered()"), self,
        #                       QtCore.SLOT("self.test"))
        self.runAction.connect(self.runAction, QtCore.SIGNAL("triggered()"), self.start_server)
                               

        self.stopAction = QtGui.QAction(self.tr("&Stop"), self)
        self.stopAction.setIcon(QtGui.QIcon('images/stop.png'))
        self.stopAction.connect(self.stopAction, QtCore.SIGNAL("triggered()"), self.stop)
        #QtCore.QObject.connect(self.stopAction,
        #                       QtCore.SIGNAL("triggered()"), self,
        #                       QtCore.SLOT("stop()"))
        
        self.quitAction = QtGui.QAction(self.tr("&Quit"), self)
        self.quitAction.setIcon(QtGui.QIcon('images/quick.png'))
        self.quitAction.connect(self.quitAction, QtCore.SIGNAL("triggered()"), self.quit)
        #QtCore.QObject.connect(self.quitAction, QtCore.SIGNAL("triggered()"),
        #                      QtGui.qApp, QtCore.SLOT("quit()"))

        self.status = QtGui.QAction(self.tr("&Status "), self)
        self.status.setIcon(QtGui.QIcon('images/status.png'))
        self.status.connect(self.status, QtCore.SIGNAL("triggered()"), self._status)
        #QtCore.QObject.connect(self.status,
         #                      QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("status()") )
        
        self.confAction = QtGui.QAction(self.tr("Config"), self)
        self.confAction.setIcon(QtGui.QIcon('images/config.png'))
        #QtCore.QObject.connect(self.confAction,
        #                       QtCore.SIGNAL("triggered()"), self, QtCore.SLOT("conf()") )
        self.confAction.connect(self.confAction, QtCore.SIGNAL("triggered()"), self.show_config)

    def createTrayIcon(self):
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.runAction)
        self.trayIconMenu.addAction(self.stopAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.status)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.confAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)

    def start_server(self):
        try:
            self.udpSocket.bind(int(self.dataconf.setting[0].port))
            self.udpSocket.readyRead.connect(self.processPendingDatagrams)
            self._showMsg("Starting Server ...")
            #self.start()
            self.statusText = "Running"
            self.startCommand()
        except:
            print "Error = ", str(traceback.format_exc())
            self._showMsg(str(traceback.format_exc()))
            pass
            
    def getmax_id(self):
        try:
            sql = "SELECT count(id) FROM datatemp"
            self.curs.execute(sql)
            self.conn.commit()
        except:
            self.curs.execute(self.sqlA)
            self.conn.commit()
            sql = "SELECT count(id) FROM datatemp"
            self.curs.execute(sql)
            self.conn.commit()
            
    def processPendingDatagrams(self):
        try:
            while self.udpSocket.hasPendingDatagrams():
                datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
    
                try:
                    # Python v3.
                    datagram = str(datagram, encoding='ascii')
                except TypeError:
                    # Python v2.
                    pass
    
                #self.statusLabel.setText("Received datagram: \"%s\"" % datagram)
                self._showMsg(datagram)
                if "pid = " in datagram:
                    #datad = str(datagram).split(' = ')
                    datad = re.split(',|=',datagram)
                    pid = str(datad[1]).strip()
                    name = str(datad[3]).strip()
                    if len(datad) > 3:
                        try:
                            infoadd = datad[4]
                        except:
                            infoadd = ""
                    print "pid = ", pid
                    print "name = ", name
                    maxid = self.getmax_id()
                    if maxid == 0 or maxid == None:
                        maxid = 1
                    else:
                        maxid = maxid + 1
                    self.logout()
                    SQL = "INSERT INTO datatemp VALUES(" + str(maxid) + ",\"" + str(pid) + "\",\"" + str(name) + "\",\"" + str(infoadd) + "\")"  
                    self.curs.execute(self.sqlA)
                    self.conn.commit()
                    self.curs.execute(SQL)
                    self.conn.commit()
                    
                return datagram
        except:
            datae = traceback.format_exc()
            print " Error = ", str(datae)
    """
    def runA(self):
        f = self.dataconf.setting[0].errorlog
        f_time = self.dataconf.setting[0].roundtime
        data = open(f).readlines()
        if os.path.isfile(f):
            if len(data) > 2:
                print "len f = ", len(data)
                print "ADA 1"
                self._parser.parser_error(f)
                time.sleep(int(f_time))
                self.runB()
            else:
                #time.sleep(int(f_time))
                self.runB()
        else:
            msg = "Can't Found Log File ! "
            self._showMsg(msg)
            #sys.exit()
            self.runB()
        
    def runB(self):
        f = self.dataconf.setting[0].errorlog
        f_time = self.dataconf.setting[0].roundtime
        data = open(f).readlines()
        if len(data) > 2:
            print "ADA 2"
            self.runA()
        else:
            time.sleep(int(f_time))
            print "TIDAK ADA"
            self.runA()
    """        
    def runC(self):
        os.startfile("parserlog.pyw")
        
    def stop(self):
        try:
            try:
                self.curs.execute(self.sqlA)
                self.conn.commit()
            except:
                pass
            SQL = "SELECT pid FROM datatemp WHERE name = 'parserlog' "
            self.curs.execute(SQL)
            self.conn.commit()
            data = self.curs.fetchall()
            print "data pid = ", data
            pid = int((data[0][0]))
            print "data pid 2 = ", pid
            controll_stop.kill_4(int(pid))
            self._showMsg("Kill Process with pid = " + str(pid))
            self.statusText = "Stopped"
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            sender.main(msg)
            print "Error Script = ", msg
            #pass
            return
            
    def start(self):
        a = subprocess.Popen(r'c:\Python26\python.exe ' + ' ' + str(os.path.join(os.getcwd(), 'apachelogparser.py')))
        self._showMsg(str(a.pid))
        return a.pid
    
    def _status(self):
        msg = "Server is " + self.statusText
        self._showMsg(msg)
    
    def stoplite(self):
        pass
    
    def startCommand(self):
        try:
            self.process.start(r"c:\Python26\python.exe", QtCore.QStringList(["parserlog.py"]))
            #self._showMsg(str(self.process.pid()))
            #return self.process.pid()
        except:
            self._showMsg(QtGui.QString(self.process.readLineStderr()))
            
    def stopCommand(self):
        try:
            self.process.start(r"c:\Python26\python.exe", QtCore.QStringList(["parserlog.py"]))
            self._showMsg(self.process.pid())
            return self.process.pid()
        except:
            self._showMsg(QtGui.QString(self.process.readLineStderr()))
    
            
    def show_config(self):
        conf_win = conf_form.Config_Form(self)
        conf_win.show()
        
    def _showMsg(self,msg,tmsg='info'):
        print msg
        icon = self.trayIcon.MessageIcon(self.trayIcon.Information)
        self.trayIcon.showMessage('Info',str(msg), icon, 3000)
        
    def quit(self):
        self.stop()
        sys.exit()
    
    def logout(self):
        sql0 = '''DROP TABLE IF EXISTS datatemp'''
        self.curs.execute(sql0)
        self.conn.commit()
        
    def test(self):
        print "hello gays 1 \n"
      
    #show_config
        
if __name__=='__main__':
    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, QtCore.QObject.tr(app, "Systray"),
                                   QtCore.QObject.tr(app, "I couldn't detect any system tray on "
                                                     "this system."))
        sys.exit(1)

    window = Window()
    window.stoplite()
    #window.show()
    sys.exit(app.exec_())