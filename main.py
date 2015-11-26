import sys
import os
from PyQt4 import QtCore, QtGui, QtNetwork
import parserlog
import configset
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
        self.dataconf = configset.read_config()
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.statusText = "Stop"

        self.sqlA = '''CREATE TABLE IF NOT EXISTS [datatemp](
                       [id] BIGINT(100) NOT NULL PRIMARY KEY,
                       [pid] VARCHAR(255) NOT NULL,
                       [name] VARCHAR(255) NOT NULL,
                       [addinfo] VARCHAR(255) NOT NULL)'''

        self.conn = sqlite.connect('totalcmd_dtemp.db')
        self.curs = self.conn.cursor()
        self.process = QtCore.QProcess()

        self.createActions()
        self.createTrayIcon()
        self.setIcon()
        self.trayIcon.show()

    def setIcon(self, index=0):
        #icon = self.iconComboBox.itemIcon(index)
        icon = QtGui.QIcon("images/totalcmd.png")
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

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
            self.statusText == "Stopped Error"
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
                elif "IOError" in datagram:
                    self.statusText = "Restart Server  ....."
                    try:
                        self.stop()
                    except:
                        pass
                    self.start_server()
                    self._showMsg("Restart Server .....")
                elif "OperationalError" in datagram:
                    self.statusText = "Restart Server  ....."
                    try:
                        self.stop()
                    except:
                        pass
                    self.start_server()
                    self._showMsg("Restart Server .....")
                elif "SystemExit" in datagram:
                    self.statusText = "Restart Server  ....."
                    try:
                        self.stop()
                    except:
                        pass
                    self.start_server()
                    self._showMsg("Restart Server .....")

                return datagram
        except:
            datae = traceback.format_exc()
            print " Error = ", str(datae)
        
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
            if pid != []:
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
        a = subprocess.Popen(self.dataconf.setting[0].python + ' ' + str(os.path.join(os.getcwd(), 'parserlog.py')))
        self._showMsg(str(a.pid))
        return a.pid

    def _status(self):
        SQL = "SELECT pid FROM datatemp WHERE name = 'parserlog' "
        self.curs.execute(SQL)
        self.conn.commit()
        data = self.curs.fetchall()
        pid = int((data[0][0]))
        msg = "Server is " + self.statusText + "\n" + "PID = " + str(pid)
        self._showMsg(msg)

    def stoplite(self):
        pass

    def startCommand(self):
        try:
            print "Parser Running ...."
            maxid = self.getmax_id()
            if maxid == 0 or maxid == None:
                maxid = 1
            else:
                maxid = maxid + 1
            infoadd = ""
            print "self.dataconf.setting[0].python =",self.dataconf.setting[0].python
            self.process.start(self.dataconf.setting[0].python, QtCore.QStringList(["parserlog.py"]))
            self._showMsg("Parser Running: " + str(self.process.pid()))
            SQL = "INSERT INTO datatemp VALUES(" + str(maxid) + ",\"" + str(self.process.pid()) + "\",\" parserlog.py \",\"" + str(infoadd) + "\")"  
            self.curs.execute(SQL)
            self.conn.commit()
            return self.process.pid()
        except:
            self._showMsg(QtGui.QString(self.process.readLineStderr()))

    def stopCommand(self):
        try:
            self.process.start(self.dataconf.setting[0].python, QtCore.QStringList(["parserlog.py"]))
            self._showMsg("Parser Stopping: " + str(self.process.pid()))
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