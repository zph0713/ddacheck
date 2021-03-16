import os,sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

LOGSDIR = os.path.join(BASEDIR,'logs')
CONFDIR = os.path.join(BASEDIR,'conf')
DATADIR = os.path.join(BASEDIR,'csvdata')

Config_file = os.path.join(CONFDIR,'config.ini')
LogConf_file = os.path.join(CONFDIR,'logger.conf')


#Current env#
ENV = {'Region':'US','Env':'prod'}

#Alert threshold#
Alert_Threshold = {'UNKNOWN':10,'Network Timeout':10,'DDAaaS Other Error':10}


#mail parameters#
MAILSET = {'Mail_Type':'plain'}#html/plain#
#mail receivers#
RECEIVERS = ['hamm_zhou@trendmicro.com.cn']
