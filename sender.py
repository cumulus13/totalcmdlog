
from PyQt4 import QtCore, QtGui, QtNetwork
import sys
import config

class Sender(QtGui.QDialog):
    def __init__(self, msg, parent=None):
        super(Sender, self).__init__(parent)
        self.msg = str(msg)
        self.dataconf = config.read_config()
        
        self.setGeometry(0,0,0,0)
        self.timer = QtCore.QTimer(self)
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.timer.timeout.connect(self.broadcastDatagramm)

        self.broadcastDatagramm()
        #self.destroy()

    def broadcastDatagramm(self):
        self.udpSocket.writeDatagram(self.msg, QtNetwork.QHostAddress(QtNetwork.QHostAddress.Broadcast), int(self.dataconf.setting[0].port))
        self.udpSocket.close()

def main(msg):
        app = QtGui.QApplication(sys.argv)
        sender = Sender(msg)
        
if __name__ == '__main__':
    main(sys.argv[1])
