import os
#from configfile import Config
import configfile

default_time = '3'  # in seconds
TEMP = os.getenv('TEMP')
TMP = os.getenv('TMP')

#parent_dir = os.path.join(str(__file__).split('system')[0], 'system')
#this_temp = os.path.join(parent_dir,'temp')
os.environ.update({'TOTALCMDLOG':os.path.dirname(__file__)})

f = os.path.join(os.environ.get('TOTALCMDLOG'), 'totalcmdlog.ini')
#print "F = ", f
cfg = configfile.Config(f)
#print "cfg = ", cfg
#parent_dir_pre = str(__file__).split('system')[0]
#print this_temp

def testme():
    print "heloo .... "          
    print "cfg.message = ", cfg.setting

def write_config(data):
    if isinstance(data, list):
        if data[0] != '' or data[0] != None:
            roundtime = data[0]
        else:
            roundtime = '0'
        if data[1] != '' or data[1] != None:
            table = data[1]
        else:
            table = '0'
        if data[2] != '' or data[2] != None:
            datalog = data[2]
        else:
            datalog = 'c:\\TEMP\\totalcmd.log'
        if data[3] != '' or data[3] != None:
            port = data[3]
        else:
            port = 33333 # default
        if data[4] != '' or data[4] != None:
            username = data[4]
        else:
            uesrname = 'root' # default
        if data[5] != '' or data[5] != None:
            password = data[5]
        else:
            password = '' # defaultc
        if data[6] != '' or data[6] != None:
            database = data[6]
        else:
            database = 'syslogcenter' # default
        if data[7] != '' or data[7] != None:
            host = data[7]
        else:
            host= '127.0.0.1' # default
            
    else:
        raise "config error "
    out = file(f,'w')
    cfg.setting[0].roundtime = roundtime
    cfg.setting[0].table = table
    cfg.setting[0].datalog = datalog
    cfg.setting[0].port = port
    cfg.setting[0].username = username
    cfg.setting[0].password = password
    cfg.setting[0].database = database
    cfg.setting[0].host = host
    cfg.save(out)
    out.close()
    
def read_config():
    #print cfg.setting[0]
    return cfg

#print read_config()
    

