import os
import sys
import datetime
import syslog
import time
import traceback
import re
import config
import sender

my_name = os.path.splitext(os.path.basename(__file__))[0]
pid = "pid = " + str(os.getpid()) + ", sender = " + my_name
sender.main(pid)

try:
    import MySQLdb
except:
    msg = "You not have module \"MySQLdb\", please download before ! \n"
    sender.main(msg)
    pass

class parser(object):
    def __init__(self,parent=None):
        super(parser, self).__init__()
        filedata = config.read_config()
        self.dataconf = config.read_config()
        self.filenamelog = filedata.setting[0].datalog
        self.host = filedata.setting[0].host
        self.port = filedata.setting[0].port
        self.user = filedata.setting[0].username
        self.passwd = filedata.setting[0].password
        self.db = filedata.setting[0].database
        self.table = filedata.setting[0].table
        self.conn = MySQLdb.connect(self.host,self.user,self.passwd,self.db)
        self.cursor = self.conn.cursor()

    def formatdate(self,data):
        d = datetime.datetime.strptime(str(data), "%m/%d/%Y %H:%M:%S")
        d2 = d.strftime('%Y-%m-%d %H:%M:%S')
        return d2
    
    def formatdate_return(self, data):
        d = datetime.datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S")
        d2 = d.strftime("%a %b %d %H:%M:%S %Y")
        return d2
    
    def get_maxtime(self):
        SQL = "SELECT time FROM totalcmdlog WHERE id = (SELECT MAX(id) FROM totalcmdlog)"
        self.cursor.execute(SQL)
        self.conn.commit()
        result = self.cursor.fetchall()[0][0]
        return result

    def _toDb(self,data):
        try:
            if isinstance(data, list):
                data_f = str(",").join(data)
                SQL1 = """CREATE TABLE IF NOT EXISTS """ + str(self.table) + """ (id int(11) PRIMARY KEY NOT NULL AUTO_INCREMENT, accessTimeDate datetime NOT NULL, actionMsg text NOT NULL, description text NOT NULL)"""
                SQL2 = """INSERT INTO """  + str(self.table) + """(accessTimeDate, actionMsg, description) values('""" + str(data[0]) + "', '" + str(data[1]) + "', \"" + str(data[2]) + "\")"
            else:
                msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " Data is not instance of list, Please insert the data ! "
                sender.main(msg)
                raise LookupError

            self.cursor.execute(SQL1)
            self.conn.commit()
            self.cursor.execute(SQL2)
            self.conn.commit()
            #result = cursor.fetchall()
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            sender.main(msg)
            print "Error Script = ", msg
            print " Error = ", datae
            print "SQL1 = ", SQL1
            print "SQL2 = ", SQL2
            print "DDate  = ", data[0]
            print "Facilty  = ", data[1]
            print "Text  = ", data[2]
            print "_" * 190
            pass

        

    def parser_error(self, f=None):
        try:
            if f == None:
                if self.filename != None:
                    f = self.filename_error
                else:
                    raise EOFError
            datalog = open(f).readlines()
            #print "datalog = ", datalog
            #format_01 = '\[(?:(?!\]).)+\]'
            #p = re.compile(format_01)
            for i in range(0, len(datalog)):
                if len(datalog[i]) > 1:
                    data = []
                    #data_pre_01 = p.findall(str(datalog[i]))
                    data_pre_01 = re.split('\[|\] |\n', datalog[i])
                    #print str(i) + ".  DATA PRE 01 = " , data_pre_01
                    #print str(i + 1) + ".  len datalog = ", len(datalog[i])
                    #print data_pre_01
                    if data_pre_01[0] == "" : 
                        DDate_pre_01 = data_pre_01[1]
                        #print "DDate_pre_01 = ", DDate_pre_01
                        Facility = data_pre_01[3]
                        if Facility == "warn":
                            Facility = "warning"
                        if data_pre_01[4] == "":
                            Text = str(" ").join(data_pre_01[5:])
                        else:
                            Text = str(" ").join(data_pre_01[4:])
                        #print "i A = ", i 
                    else:
                        #print "process B ..........................."
                        #if i == 0:
                        #    for v in range(0, len(datalog)):
                        #        if re.split('\[|\] |\n', datalog[i])[0] != "":
                        #            pass
                        #        else:
                        #            Date_pre_01 = re.split('\[|\] |\n', datalog[i])[1]
                        #            break
                        #else:
                        DDate_pre_01 = None
                        Facility = None
                        Text = str(" ").join(data_pre_01[0:])

                    if DDate_pre_01 == None:
                        #print "process C ..........................."
                        #print "i B = ", i
                        batas = []
                        for d in range(i, len(datalog)):
                            if len(datalog[d]) > 1:
                                if re.split('\[|\] |\n', datalog[d])[0] != "":
                                    #DDate_pre_01 = "0000-00-00 00:00:00"
                                    #print "d 1 = ", str(d)
                                    #print "data_pre_02 = ", datalog[d]
                                    pass
                                else:
                                    #print "d 2 = ", str(d)
                                    #print "data_pre_03 = ", datalog[d]
                                    #print "d = ", d
                                    #DDate_pre_01 = "0000-00-00 00:00:00"
                                    DDate_pre_01 = re.split('\[|\] |\n', datalog[d])[1]
                                    #batas = []
                                    #batas.append(d)
                                    #print "DATALOG = ", re.split('\[|\] |\n', datalog[d])
                                    try:
                                        Facility = re.split('\[|\] |\n', datalog[i])[3]
                                        if Facility == "warn":
                                            Facility = "warning"
                                            #print "DDate_pre_01 B = ",DDate_pre_01
                                        else:
                                            pass
                                    except:
                                        Facility = "Info"
                                        DDate_pre_01 = re.split('\[|\] |\n', datalog[d])[1]
                                        #print "DDate_pre_01 B = ",DDate_pre_01
                                    break
                                #print "DDate_pre_01 A 000 = ", DDate_pre_01
                                """
                                for x in range(-i,int(batas[0])):
                                    z = abs(x)
                                    #print "z = ", z
                                    print "batas = ", batas[0]
                                    print "-i = ", str(-i)
                                    print "z|x = ", z
                                    if re.split('\[|\] |\n', datalog[z])[0] != "":
                                        pass
                                    else:
                                        print "process D ..........................."
                                        #print "XXX = ", abs(x)
                                        DDate_pre_01 = re.split('\[|\] |\n', datalog[z])[1]
                                        print "DDate_pre_01 A = ", DDate_pre_01    
                                        try:
                                            Facility = re.split('\[|\] |\n', datalog[z])[3]
                                            if Facility == "warn":
                                                Facility = "warning"
                                                #print "DDate_pre_01 B = ",DDate_pre_01
                                            else:
                                                pass
                                        except:
                                            Facility = "Info"
                                            DDate_pre_01 = re.split('\[|\] |\n', datalog[z])[1]
                                            #print "DDate_pre_01 B = ",DDate_pre_01
                                        break
                                """
                            else:
                                pass
                        #print "DATE PRE B = ", DDate_pre_01

                    if DDate_pre_01 == None:
                        #DDate_pre_01 = "0000-00-00 00:00:00"
                        #data.append(self.formatdate(DDate_pre_01))
                        
                        DDate_pre_01 = self.formatdate_return(self.get_maxtime())
                        #self.conn.close()
                    else:
                        pass
                    #data.append(self.formatdate(DDate_pre_01))

                    #print "DATE = ", DDate_pre_01
                    
                    if Facility == None or Facility == '':
                        #print "process 001 ................"
                        if "Warning" in Text or "warning" in Text:
                            #print "process 002 ................"
                            #print "TEXT A = ", Text
                            Facility = "warning"
                            #data.append(Facility)
                            #print "FACILITY = ", Facility     
                        else:
                            #print "process 003 ................"
                            #print "TEXT B = ", Text
                            Facility = "alert"
                            #data.append(Facility)
                            #print "FACILITY = ", Facility     
                    #else:
                        #Facility = data_pre_01[3]
                        #  Facility = "info"
                        # data.append(Facility)
                    #print "FACILITY = ", Facility     
                    #print "TEXT = ", Text
                    data.append(self.formatdate(DDate_pre_01))
                    data.append(Facility)
                    Text2 = re.split('\]".', Text)
                    #print "TEXT  2 = ", Text2
                    data.append(str(Text2[0]).replace('"', " "))
                    if len(data) < 3:
                        #print "Data is less than corret data ! "
                        #print "DATA = ", data
                        #print "_"*100
                        sender.main("Data is less than corret data ! ")
                        filetemp_name = os.path.splitext(f)[0] + ".off1"
                        filetemp_01 = open(filetemp_name, 'w')
                        filetemp_01.close()
                        filetemp_01 = open(filetemp_name, 'a')
                        filetemp_01.write(str(i) + str(datalog[i]))
                        filetemp_01.close()
                        if len(data) == 2:
                            try:
                                datetime.datetime.strptime(str(data[0]), "%Y-%m-%d %H:%M:%S")
                                DDate_pre_01 = data[0]
                            except:
                                DDate_pre_01 = self.get_maxtime()
                            data = []
                            data.append(DDate_pre_01)
                            data.append("Emergency")
                            data.append(str(data[1]))
                            self._toDb('error',data)
                        else:
                            try:
                                datetime.datetime.strptime(str(data[0]), "%Y-%m-%d %H:%M:%S")
                                DDate_pre_01 = data[0]
                            except:
                                DDate_pre_01 = self.get_maxtime()
                            data = []
                            data.append(DDate_pre_01)
                            data.append("Emergency")
                            data.append(str(data[0]))
                            self._toDb('error',data)
                    else:
                        for w in data:
                            if w == None:
                                #print "Data None is Found !  "
                                #print "DATA = ", data
                                #print "_"*100
                                self.main("Data None is Found !  ")
                                filetemp_name = os.path.splitext(f)[0] + ".off2"
                                filetemp_01 = open(filetemp_name, 'w')
                                filetemp_01.close()
                                filetemp_01 = open(filetemp_name, 'a')
                                filetemp_01.write(str(i) + str(datalog[i]))
                                filetemp_01.close()
                                index = data.index(w)
                                
                                if index == 0:
                                    try:
                                        datetime.datetime.strptime(str(data[0]), "%Y-%m-%d %H:%M:%S")
                                        #DDate_pre_01 = data[0]
                                        pass
                                    except:
                                        DDate_pre_01 = self.get_maxtime()
                                        data.remove(w)
                                        data.insert(index,str(DDate_pre_01))
                                elif index == 1:
                                    data.remove(w)
                                    data.insert(index,"Emergency")
                                elif index == 2:
                                    data.remove(w)
                                    data.insert(index, " ")
                                else:
                                    pass
                                    
                                #data.remove(w)
                                #data = []
                                #data = ["0000-00-00 00:00:00", "unknow","unknow"]
                                self._toDb('error',data)
                            else:
                                pass
                                #print str(i) + ". DATA = ", data
                                #print "_"*100
                                #self._toDb('error',data)
                    print str(i) + ". DATA = ", data
                    self._toDb('error',data)
                else:
                    #print "i C = ", str(i)
                    pass
            try:
                f = self.dataconf.setting[0].errorlog
                df = open(f, 'w')
                df.write("\n")
                df.close()
                #self.conn.close()
            except:
                datae = traceback.format_exc()
                msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
                sender.main(msg)
                print "Error Script = ", msg
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            sender.main(msg)
            print "Error Script = ", msg

            print " Error = ", datae
            print "*"*80
            print "Line ", str(i+1)
            print "DDate  = ", DDate_pre_01
            print "Facilty  = ", Facility
            #print "Text  = ", Text2[0]
            print "_" * 100



    def parserlog(self, f=None):
        IP_SYSLOG_SERVER = '127.0.0.1'
        PORT_SYSLOG_SERVER = 514
        if f != None:
            filename = f
        else:
            filename = self.filenamelog
        try:
            if (os.path.isfile(filename) == True):
                try:
                    data = open(filename, "r").readlines()
                except:
                    time.sleep(5)
                    data = open(filename, "r").readlines()
                lendata = len(data)
                for i in range(0, len(data)):
                    #print i
                    data_pre = re.split(': ', data[i])
                    #print data_pre
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
                    DAction = str(data_pre[1]).strip()
                    #DMessage = "\"" + str(data_pre[2]).strip() + "\""
                    """
                    if str(data_pre[2]).strip() == "\\":
                        if str(data_pre[2]).strip()[-1] == "\\":
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], " ")
                        else:
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], "/")
                    """
                    try:
                        if str(data_pre[2]).strip()[-1] == "\\":
                            DMessage = str(str(data_pre[2]).strip()).replace(str(data_pre[2]).strip()[-1], " ")
                        else:
                            DMessage = str(data_pre[2]).strip()
                    except:
                        pass
                    #print "action = ", DAction
                    #print "message = ", DMessage
                    databank = []
                    databank.append(DDate)
                    databank.append(DAction)
                    databank.append(DMessage)
                    print "DATA BANK = ", databank
                    self._toDb(databank)
                
            else:
                syslog.syslog("TotalCmdLog : File " +  " Not Found ! \"",0,1,IP_SYSLOG_SERVER,PORT_SYSLOG_SERVER)
                sender.main("TotalCmdLog : File Not Found !")
                #sys.exit()
            try:
                df = open(self.filenamelog, 'w')
                df.close()
            except:
                pass
        
            #dataup = open(filename, "w")
            #dataup.write("")
            #dataup.close()
        except:
            print "\n"
            print "ERROR : "
            datae = traceback.format_exc()
            syslog.syslog(str(datae), 3,3,self.host,514)
            sender.main(str(datae))
            print datae
            pass
            
    def runA(self):
        try:
            f = self.dataconf.setting[0].datalog
            f_time = self.dataconf.setting[0].roundtime
            try:
                data = open(f).readlines()
            except:
                time.sleep(5)
                data = open(f).readlines()
            if os.path.isfile(f):
                if len(data) > 0:
                    print "len f = ", len(data)
                    print "ADA 1" 
                    sender.main("Totalcmd Log Monitor : Processing Data Log !")
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
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            sender.main(msg)
            syslog.syslog(msg, 3,3,self.host,514)
            print "Error Script = ", msg
            pass

    def runB(self):
        #sender.main("Totalcmd Log Monitor : Processing Data Log !")
        try:
            f = self.dataconf.setting[0].datalog
            f_time = self.dataconf.setting[0].roundtime
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
        except:
            datae = traceback.format_exc()
            msg = str(os.path.splitext(os.path.basename(str(__file__)))[0]) + " " + str(datae)
            sender.main(msg)
            syslog.syslog(msg, 3,3,self.host,514)
            print "Error Script = ", msg
            pass

    def test(self):
        f = self.dataconf.setting[0].datalog
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

        if os.path.isfile(data.setting[0].datalog):
            f = data.setting[0].datalog
        else:
            raise "Youre not have a log file ! \n"
        self.parser_error(f)


if __name__ == "__main__":
    myapp = parser()
    #myapp.parserlog()
    myapp.runA()
    #myapp.test2()
    #myapp.runA()
    #myapp.apache_state("apache2.2")