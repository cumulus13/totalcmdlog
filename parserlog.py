import os
import sys
import win32file
import datetime
import syslog
import time
import traceback
import re
import configset
import sender
from pysqlite2 import dbapi2 as sqlite
from configfile import Config

my_name = os.path.splitext(os.path.basename(__file__))[0]
pid = "pid = " + str(os.getpid()) + ", sender = " + my_name
sender.main(pid)

try:
    import MySQLdb
except:
    msg = "You not have module \"MySQLdb\", please download before ! \n"
    sender.main(msg)
    pass

filedata = configset.read_config()
dataconf = configset.read_config()
filenamelog = filedata.setting[0].datalog
ftplog = filedata.setting[0].ftplog
roundtime = filedata.setting[0].roundtime
host = filedata.setting[0].host
port = filedata.setting[0].port
user = filedata.setting[0].username
passwd = filedata.setting[0].password
db = filedata.setting[0].database
table = filedata.setting[0].table
tableftp = filedata.setting[0].tableftp
conn = MySQLdb.connect(host,user,passwd,db)
cursor = conn.cursor()

IP_SYSLOG_SERVER = '127.0.0.1'
PORT_SYSLOG_SERVER = 514

conn2 = sqlite.connect('dtemp.db')
curs = conn2.cursor()

class parser(object):
    def __init__(self,parent=None):
        super(parser, self).__init__()
        #host = '127.0.0.1'
        
    def getdatetime_now(self):
        dt = datetime.datetime.now()
        d2 = dt.strftime('%Y-%m-%d %H:%M:%S')
        return d2
        

    def formatdate(self,data):
        d = datetime.datetime.strptime(str(data), "%m/%d/%Y %H:%M:%S")
        d2 = d.strftime('%Y-%m-%d %H:%M:%S')
        return d2
    
    def formatdate_ftp(self,data):
        d = datetime.datetime.strptime(str(data), "%m/%d/%Y %H:%M:%S %p")
        d2 = d.strftime('%Y-%m-%d %H:%M:%S')
        return d2

    def formatdate_return(self, data):
        d = datetime.datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S")
        d2 = d.strftime("%a %b %d %H:%M:%S %Y")
        return d2

    def get_maxtime(self):
        SQL = "SELECT time FROM totalcmdlog WHERE id = (SELECT MAX(id) FROM totalcmdlog)"
        cursor.execute(SQL)
        conn.commit()
        result = cursor.fetchall()[0][0]
        return result

    def _toDb(self,data, type):
        if type == "general":
            try:
                if isinstance(data, list):
                    data_f = str(",").join(data)
                    SQL1 = """CREATE TABLE IF NOT EXISTS """ + str(table) + """ (id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT, accessTimeDate datetime NOT NULL, actionMsg text NOT NULL, description text NOT NULL)"""
                    SQL2 = """INSERT INTO """  + str(table) + """(accessTimeDate, actionMsg, description) values('""" + str(data[0]) + "', '" + str(data[1]) + "', \"" + str(data[2]) + "\")"
                else:
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " Data is not instance of list, Please insert the data ! "
                    sender.main(msg)
                    raise LookupError
                try:
                    cursor.execute(SQL1)
                    conn.commit()
                except:
                    pass
                cursor.execute(SQL2)
                conn.commit()
                #result = cursor.fetchall()
            except:
                datae = traceback.format_exc()
                msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
                syslog.syslog(msg, 3,3,host,514)
                sender.main(msg)
                print "Error Script = ", msg
                print " Error = ", datae
                #print "SQL1 = ", SQL1
                #print "SQL2 = ", SQL2
                print "DDate  = ", data[0]
                print "Facilty  = ", data[1]
                print "Text  = ", data[2]
                print "_" * 190
                #pass
                sys.exit()
        elif type == "ftp":
            try:
                if isinstance(data, list):
                    data_f = str(",").join(data)
                    SQL1 = """CREATE TABLE IF NOT EXISTS """ + str(tableftp) + """ (id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT, accessTimeDate datetime NOT NULL, actionMsg text NOT NULL, description text NOT NULL)"""
                    SQL2 = """INSERT INTO """  + str(tableftp) + """(accessTimeDate, actionMsg, description) values('""" + str(data[0]) + "', '" + str(data[1]) + "', \"" + str(data[2]) + "\")"
                else:
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " Data is not instance of list, Please insert the data ! "
                    sender.main(msg)
                    raise LookupError
                try:
                    cursor.execute(SQL1)
                    conn.commit()
                except:
                    pass
                cursor.execute(SQL2)
                conn.commit()
                #result = cursor.fetchall()
            except:
                datae = traceback.format_exc()
                msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
                syslog.syslog(msg, 3,3,host,514)
                sender.main(msg)
                print "Error Script = ", msg
                print " Error = ", datae
                #print "SQL1 = ", SQL1
                #print "SQL2 = ", SQL2
                print "DDate  = ", data[0]
                print "Facilty  = ", data[1]
                print "Text  = ", data[2]
                print "_" * 190
                #pass
                sys.exit()
        else:
            datae = "Format Data is inValis ! \n"
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            syslog.syslog(msg, 3,3,host,514)
            sender.main(msg)
            print "Error Script = ", msg
            print "_" * 190
            #pass
            sys.exit()  




    def parserlog(self, f=None):
        IP_SYSLOG_SERVER = '127.0.0.1'
        PORT_SYSLOG_SERVER = 514
        try:
            if f != None:
                if os.path.isfile(f):
                    filename = f
                else:
                    datae = traceback.format_exc()
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " File Log Not Found; " + str(datae)
                    syslog.syslog(msg, 3,3,host,514)
                    sender.main(msg)
                    return
                
            else:
                if os.path.isfile(filenamelog):
                    filename = filenamelog
                else:
                    datae = traceback.format_exc()
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " File Log Not Found; " + str(datae)
                    syslog.syslog(msg, 3,3,host,514)
                    sender.main(msg)
                    return
        except:
            datae = "ERROR : " + str(i) + ". " + str(data[i])  + "; Traceback = " + str(traceback.format_exc())
            syslog.syslog(str(datae), 3,11,host,514)
            sender.main(str(datae))
            print datae
            return
           
        try:
            if (os.path.isfile(filename) == True):
                """
                try:
                    #print "Mode A = ", os.lstat(filename).st_mode
                    #print "Mode B = ", win32file.GetFileAttributes(filename)
                    data = open(filename, "r").readlines()
                except:
                    #print "Mode A = ", os.lstat(filename).st_mode
                    #print "Mode B = ", win32file.GetFileAttributes(filename)
                    time.sleep(5)
                    data = open(filename, "r").readlines()
                """
                while self.cekfile(filename) == False:
                    #print "Mode 1 = ", os.lstat(f).st_mode
                    #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                else:
                    data = open(filename, "r").readlines()
                    
                lendata = len(data)
                for i in range(0, len(data)):
                    #print i
                    data_pre = re.split(': ', data[i])
                    #print "len(data_pre) = ", len(data_pre)
                    print data_pre
                    if "a" in data_pre[0]:
                        DDate_pre = re.split('a',data_pre[0])[0]
                    elif "p" in data_pre[0]:
                        DDate_pre = re.split('p',data_pre[0])[0]
                    else:
                        DDate_pre = data_pre[0]
                    #print "DDate_pre = ", DDate_pre
                    try:
                        DDate = self.formatdate(DDate_pre)
                        #print "DDate AAA = ", DDate
                    except:
                        #print "i = ", str(i)
                        #print "ERROR :"
                        #print str(traceback.format_exc())
                        if i == 0:
                            if "a" in data_pre[0]:
                                #print "PROCESS A"
                                DDate_pre = re.split('\xef\xbb\xbf|a',data_pre[0])
                                #print "DDatePre A = " , DDate_pre[1]
                                DDate = self.formatdate(DDate_pre[1])
                            elif "p" in data_pre[0]:
                                #print "PROCESS A"
                                DDate_pre = re.split('\xef\xbb\xbf|p',data_pre[0])
                                #print "DDatePre A = " , DDate_pre[1]
                                DDate = self.formatdate(DDate_pre[1])
                            else:
                                #print "PROCESS B"
                                DDate_pre = re.split('\xef\xbb\xbf',data_pre[0])
                                #print "DDatePre B = " , DDate_pre[1]
                                DDate = self.formatdate(DDate_pre[1])
                        else:
                            pass
                    #print "DDate = ", DDate
                    #DAction = str(data_pre[1]).strip()
                    #DMessage = "\"" + str(data_pre[2]).strip() + "\""
                    if len(data_pre) > 2:
                        DAction = str(data_pre[1]).strip()
                        DMessage = str(data_pre[2]).strip()
                    else:
                        DMessage = str(data_pre[1]).strip()
                        if "start" in DMessage:
                            DAction = "Start"
                        elif "shutdown" in DMessage:
                            DAction = "Shutdown"
                        else:
                            DAction = "Unknow"
                    """
                    if str(data_pre[2]).strip() == "\\":
                        if str(data_pre[2]).strip()[-1] == "\\":
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], " ")
                        else:
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], "/")
                    """
                    try:
                        if str(data_pre[2][-1]).strip() == "\\":
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], " ")
                        else:
                            DMessage = str(data_pre[2]).strip()
                    except:
                        pass
                    #print "action = ", DAction
                    #print "message = ", DMessage
                    DMessage2 = str(DMessage).replace("\\","/")
                    databank = []
                    databank.append(DDate)
                    databank.append(DAction)
                    databank.append(DMessage2)
                    #print "DATA BANK = ", databank
                    self._toDb(databank,'general')

            else:
                syslog.syslog("TotalCmdLog : File " +  " Not Found ! \"",0,1,IP_SYSLOG_SERVER,PORT_SYSLOG_SERVER)
                sender.main("TotalCmdLog : File Not Found !")
                #sys.exit()
        
        except:
            print "\n"
            print "ERROR : "
            datae = traceback.format_exc()
            syslog.syslog(str(datae), 3,3,host,514)
            sender.main(str(datae))
            print datae
            pass
        
        try:
            df = open(filenamelog, 'w')
            df.close()
        except:
            datae = traceback.format_exc()
            syslog.syslog(str(datae), 3,3,host,514)
            sender.main(str(datae))
            pass

    def parserlog_ftp(self, f=None):
        IP_SYSLOG_SERVER = '127.0.0.1'
        PORT_SYSLOG_SERVER = 514
        try:
            if f != None:
                if os.path.isfile(f):
                    filename = f
                else:
                    datae = traceback.format_exc()
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " File Log Not Found; " + str(datae)
                    syslog.syslog(msg, 3,3,host,514)
                    sender.main(msg)
                    return
                
            else:
                if os.path.isfile(filenamelog):
                    filename = ftplog
                else:
                    datae = traceback.format_exc()
                    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " File Log Not Found; " + str(datae)
                    syslog.syslog(msg, 3,3,host,514)
                    sender.main(msg)
                    return
        except:
            datae = "ERROR : " + str(i) + ". " + str(data[i])  + "; Traceback = " + str(traceback.format_exc())
            syslog.syslog(str(datae), 3,11,host,514)
            sender.main(str(datae))
            print datae
            return
        try:
            if (os.path.isfile(filename) == True):
                while self.cekfile(filename) == False:
                        time.sleep(3)
                else:
                    data = open(filename, "r").readlines()
                    
                lendata = len(data)
                for i in range(0, len(data)):
                    #print i
                    data_pre = re.split(': |\n', data[i])
                    #print "len(data_pre) = ", len(data_pre)
                    #print str(i) + ". " , data_pre
                    
                    if len(data_pre) > 2:
                        if "ftp" in data_pre[1]:
                            data_pre_facility = re.split(" |\(|\)",data_pre[0])
                            Dmessage = str(" ").join(data_pre[1:]).strip()
                            DFacility = str(data_pre_facility[0]).strip()
                            DDate = self.formatdate_ftp(str(" ").join(data_pre_facility[2:5]).strip())
                            #print "DDate 1 = ", DDate
                            #print "DFacility 1 = ", DFacility
                            #print "DMessage 1 = ", Dmessage
                            #print str(i) + ". |" + "_" * 100
                        else:
                            if " PM" in data_pre[1] or " AM" in data_pre[1]:
                                data_pre_date = data_pre[1]
                                DDate = self.formatdate_ftp(re.split("\(|\)", data_pre_date)[1])
                                #print "DDate = " + str(i) + ". ", DDate
                                Dmessage = data_pre[0]
                                DFacility = "Info"
                                #print "DDate 2 = ", DDate
                                #print "DFacility 2 = ", DFacility
                                #print "DMessage 2 = ", Dmessage
                                #print str(i) + ". |" + "_" * 100
                            else:
                                Dmessage = str(" ").join(data_pre[0:])
                                DFacility = "Info"
                                for j in range(i, len(data)):
                                    data_pre = re.split(': |\n', data[j])
                                    if " PM" in data_pre[1] or " AM" in data_pre[1]:
                                        data_pre_date = data_pre[1]
                                        DDate = self.formatdate_ftp(re.split("\(|\)", data_pre_date)[1])
                                        break
                                #print "DDate 3 = ", DDate
                                #print "DFacility 3 = ", DFacility
                                #print "DMessage 3 = ", Dmessage
                                #print str(i) + ". |" + "_" * 100
                                        
                    else:
                        Dmessage = str(" ").join(data_pre[0:]).strip()
                        for k in range(i, len(data)):
                            #print "k = ", k
                            datapre =  re.split(': |\n', data[k])
                            if " PM" in datapre[1] or " AM" in datapre[1]:
                                datapre_date = datapre[1]
                                DDate = self.formatdate_ftp(re.split("\(|\)", datapre_date)[1])
                                print "DDATE A = ", DDate
                                break
                            else:
                                if "ftp" in datapre[1]:
                                    datapre_facility = re.split(" |\(|\)",datapre[0])
                                    #Dmessage = str(" ").join(data_pre[1:]).strip()
                                    DFacility = str(datapre_facility[0]).strip()
                                    DDate = self.formatdate_ftp(str(" ").join(datapre_facility[2:5]).strip())
                                    print "DDATE B = ", datapre 
                                    break
                                else:
                                    DDate = self.getdatetime_now()
                                    break
                                
                        DFacility = "Info"
                        #print "DDate 4 = ", DDate
                        #print "DFacility 4 = ", DFacility
                        #print "DMessage 4 = ", Dmessage
                        #print str(i) + ". |" + "_" * 100
                    #print "DDate 4 = ", DDate
                    #print "DFacility 4 = ", DFacility
                    #print "DMessage 4 = ", Dmessage
                    #print str(i) + ". |" + "_" * 100
                    if '"' in Dmessage:
                        Dmessage = str(Dmessage).replace('"', "'")
                    else:
                        Dmessage = str(Dmessage).replace("\\","/")
                    databank2 = []
                    databank2.append(DDate)
                    databank2.append(DFacility)
                    databank2.append(Dmessage)
                    
                    #print "DDate          = ", DDate
                    #print "DFacility      = ", DFacility
                    #print "DMessage   = ", Dmessage
                    #print str(i) + ". |" + "_" * 100
                    
                    self._toDb(databank2, "ftp")
        except:
            #print "DDate          = ", DDate
            print "DFacility      = ", DFacility
            print "DMessage   = ", Dmessage
            print str(i) + ". |" + "_" * 100
            print "\n"
            print "ERROR : "
            datae = "ERROR : " + str(i) + ". " + str(data[i])  + "; Traceback = " + str(traceback.format_exc())
            syslog.syslog(str(datae), 3,11,host,514)
            sender.main(str(datae))
            print datae
            pass
        
        try:
            df = open(ftplog, 'w')
            df.close()
        except:
            pass
        
    def cekfile(self, data):
        try:
            f = data
            filelog = open(f).readlines()
            return True
        except IOError, e:
            return False
            
    def cekprocess(self):
        try:
            SQL = "SELECT pid FROM datatemp WHERE name = 'parserlog' "
            curs.execute(SQL)
            conn2.commit()
            data = curs.fetchall()
            print "data 0 ", data
            pid = int((data[0][0]))
            datax = os.popen("tasklist ").readlines()
            #dataz = re.split(str(pid), datax)
            for i in datax:
                print i
            #print "datax = ", dataz
        except:
            datae = traceback.format_exc()
            print "ERROR = ", str(datae)
        
    def run1(self,f=None):
        try:
            round_time = roundtime
            if f == None:
                while 1:
                    f = filenamelog
                    while self.cekfile(f) == False:
                    #print "Mode 1 = ", os.lstat(f).st_mode
                    #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog = open(f).readlines()
                        
                    if len(filelog) > 0:
                        self.parserlog(f)
                        print "ADA 1"
                        time.sleep(int(round_time))
                    else:
                        print "TIDAK ADA 1"
                        time.sleep(int(round_time))
            else:
                while 1:
                    while self.cekfile(f) == False:
                    #print "Mode 1 = ", os.lstat(f).st_mode
                    #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog = open(f).readlines()

                    if len(filelog) > 0:
                        self.parserlog(f)
                        print "ADA 2"
                        time.sleep(int(round_time))
                    else:
                        print "TIDAK ADA 2"
                        time.sleep(int(round_time))
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            syslog.syslog(msg, 3,3,host,514)
            sender.main(msg)
            print "Error Script = ", msg
            pass  


    def run(self,f1=None, f2=None):
        try:
            roundtime = dataconf.setting[0].roundtime
            if f1 == None and f2 == None:
                while 1:
                    f1 = filenamelog
                    f2 = ftplog
                    while self.cekfile(f1) == False:
                        #print "Mode 1 = ", os.lstat(f).st_mode
                        #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog1 = open(f1).readlines()
                        if os.path.isfile(f2):
                            filelog2 = open(f2).readlines()
                            if len(filelog1) > 0 and len(filelog2) > 0:
                                print "ADA 1"
                                self.parserlog(f1)
                                self.parserlog_ftp(f2)
                                time.sleep(int(roundtime))
                            elif len(filelog1) > 0 and len(filelog2) < 2:
                                print "ADA 2"
                                self.parserlog(f1)
                                time.sleep(int(roundtime))
                            if len(filelog1) < 2 and len(filelog2) > 0:
                                #print "f2 = ", f2
                                self.parserlog_ftp(f2)
                                print "ADA 3"
                                time.sleep(int(roundtime))
                            else:
                                print "TIDAK ADA 1"
                                time.sleep(int(roundtime))
                        else:
                            if len(filelog1) > 0:
                                print "ADA 1A"
                                self.parserlog(f1)
                                #self.parserlog_ftp(f2)
                                time.sleep(int(roundtime))
                            else:
                                print "TIDAK ADA 1A"
                                time.sleep(int(roundtime))

            elif f1 != None and f2 == None:
                while 1:
                    f2 = ftplog
                    while self.cekfile(f1) == False:
                        #print "Mode 1 = ", os.lstat(f).st_mode
                        #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog1 = open(f1).readlines()
                        filelog2 = open(f2).readlines()

                    if len(filelog1) > 1 and len(filelog2) > 1:
                        print "ADA 4"
                        self.parserlog(f1)
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    elif len(filelog1) > 1 and len(filelog2) < 2:
                        print "ADA 5"
                        self.parserlog(f1)
                        time.sleep(int(roundtime))
                    if len(filelog1) < 2 and len(filelog2) > 1:
                        print "ADA 6"
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    else:
                        print "TIDAK ADA 2"
            elif f1 == None and f2 != None:
                while 1:
                    f1 = filenamelog
                    while self.cekfile(f1) == False:
                        #print "Mode 1 = ", os.lstat(f).st_mode
                        #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog1 = open(f1).readlines()
                        filelog2 = open(f2).readlines()

                    if len(filelog1) > 1 and len(filelog2) > 1:
                        print "ADA 7"
                        self.parserlog(f1)
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    elif len(filelog1) > 1 and len(filelog2) < 2:
                        print "ADA 8"
                        self.parser_error(f1)
                        time.sleep(int(roundtime))
                    if len(filelog1) < 2 and len(filelog2) > 1:
                        print "ADA 9"
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    else:
                        print "TIDAK ADA 3"
            else:
                while 1:
                    while self.cekfile(f1) == False:
                        #print "Mode 1 = ", os.lstat(f).st_mode
                        #print "Mode 2 = ", win32file.GetFileAttributes(f)
                        time.sleep(3)
                    else:
                        filelog1 = open(f1).readlines()
                        filelog2 = open(f2).readlines()

                    if len(filelog1) > 1 and len(filelog2) > 1:
                        print "ADA 10"
                        self.parserlog(f1)
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    elif len(filelog1) > 1 and len(filelog2) < 2:
                        print "ADA 11"
                        self.parser_error(f1)
                        time.sleep(int(roundtime))
                    if len(filelog1) < 2 and len(filelog2) > 1:
                        print "ADA 12"
                        self.parserlog_ftp(f2)
                        time.sleep(int(roundtime))
                    else:
                        print "TIDAK ADA 4"
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            syslog.syslog(msg, 3,3,host,514)
            sender.main(msg)
            print "Error Script = ", msg
            pass  
        
    def runA(self):
        #cdir = os.path.dirname(sys.argv[0])
        #print "chdir = ", cdir
        #try:
        f = filenamelog
        f_time = roundtime
        #os.chdir(cdir)
        #cfg = Config('conf.ini')
        #f = cfg.setting[0].datalog
        #f_time = cfg.setting[0].roundtime
        try:
            data = open(f).readlines()
        except:
            time.sleep(5)
            data = open(f).readlines()
        if os.path.isfile(f):
            if len(data) > 0:
                print "len f = ", len(data)
                print "ADA 1" 
                #sender.main("Totalcmd Log Monitor : Processing Data Log !")
                self.parserlog(f)
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
        #except:
        #    datae = traceback.format_exc()
        #    msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
        #    syslog.syslog(msg, 3,3,host,514)
            #sender.main(msg)
        #    print "Error Script = ", msg
        #    pass

    def runB(self):
        f = filenamelog
        f_time = roundtime
        try:
            data = open(f).readlines()
        except:
            time.sleep(5)
            data = open(f).readlines()
        if len(data) > 0:
            print "ADA 2"
            self.runA()
        else:
            time.sleep(int(f_time))
            print "TIDAK ADA"
            self.runA() 
        #except:
        #   datae = traceback.format_exc()
        #   msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
        #    syslog.syslog(msg, 3,3,host,514)
        #    #sender.main(msg)
        #    print "Error Script = ", msg
        #    pass

    def test(self):
        f = filenamelog
        parser_error(f)

    def test2(self):
        data_test = '[ERROR]'
        data_pre_01 = re.split('\[|\]|\n', data_test)
        print data_pre_01

    def sendInfo(self, msg):
        pass

    def main(self):
        #self.runA()
        data = config.read_config()
        #print data.setting[0].roundtime

        if os.path.isfile(filenamelog):
            self.parser_error(filenamelog)
        else:
            raise "Youre not have a log file ! \n"

if __name__ == "__main__":
    datalog = open(filenamelog).readlines()
    myapp = parser()
    myapp.run()
    #myapp.parserlog_ftp()
    
    """
    if len(datalog) > 0:
        try:
            sender.main("Totalcmd Log Monitor : Processing Data Log !")    
            myapp.run()
            #myapp.runA()
            #myapp.test2()
            #myapp.runA()
            #myapp.apache_state("apache2.2")
        except:
            a, msg,e = sys.exc_info()
            syslog.syslog(msg, 3,3,host,514)
    else:
        try:
            #myapp.runA()
            myapp.run()
        except:
            a, msg,e = sys.exc_info()
            syslog.syslog(msg, 3,3,host,514)
    """
    #myapp.cekprocess()