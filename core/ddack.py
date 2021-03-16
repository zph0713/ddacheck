import os, sys

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

import ConfigParser
import threading
import csv
import json
import datetime
from elasticsearch import Elasticsearch

from conf import settings
from query import ESBuild
from logger import Logger

LOG = Logger('ddacheck')


class DDAcheck(object):
    def __init__(self,Scan_Type,Time_Interval=1):
        self._getConfig()
        self._instanceES()
        self.Scan_Type = Scan_Type
        self.Time_Interval = Time_Interval
        self.esquery = ESBuild(self.Scan_Type,self.Time_Interval)
        self.dda_total = int()
        self.dda_abnormal_data = {}
        self.file_path = {}

    def _getConfig(self):
        config = ConfigParser.RawConfigParser()
        config.read(settings.Config_file)
        self.es_server = config.get('elasticsearch', 'server')
        self.es_port = config.get('elasticsearch', 'port')

    def _instanceES(self):
        try:
            es = Elasticsearch(hosts=self.es_server,port=self.es_port)
            return es
        except Exception as e:
            LOG.error(e)

    def queryDDAaas(self):
        ddaquery_body = self.esquery.queryDDAaas()
        res = self._instanceES().search(body=ddaquery_body)
        result = res["aggregations"]["ATP_count"]["buckets"]
        self.dda_total = res['hits']['total']
        for i in result:
            if i['key'] in settings.Alert_Threshold.keys():
                self.dda_abnormal_data[i['key']] = i['doc_count']
        if self.dda_abnormal_data:
            thread_list = []
            for n in self.dda_abnormal_data:
                thread_run = threading.Thread(target=self.queryAbnormal,args=(n,))
                thread_list.append(thread_run)
                thread_run.start()
            for th in thread_list:
                th.join()
        
    def queryAbnormal(self,risklevel):
        result_data = []
        abnormalquery_body = self.esquery.queryAbnormal(risklevel)
        res = self._instanceES().search(body=abnormalquery_body)
        res_data = res['hits']['hits']
        if res_data != []:
            for i in res_data:
                result = i['_source']
                result_data.append(result)
        if result_data != []:
            self.formatToCVS(risklevel,result_data)

    def formatToCVS(self,risklevel,data):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        csv_dir = datetime.datetime.now().strftime("%Y-%m-%d")
        csv_file = datetime.datetime.now().strftime("%H_%M_%S-") + self.Scan_Type + '_' + risklevel.replace(' ','_') + '.csv'
        file_dir = settings.DATADIR + os.sep + csv_dir
        self.file_path[risklevel] = os.path.join(file_dir,csv_file)
        isExists = os.path.exists(file_dir)
        if not isExists:
            os.makedirs(file_dir)
        fields = []
        for field in data:
            fields = fields + field.keys()
        fieldnames = list(set(fields))
        with open(self.file_path[risklevel],'a') as csvf:
            writer = csv.DictWriter(csvf,fieldnames=fieldnames)
            writer.writeheader()
            for i in data:
                if i != {}:
                    writer.writerow(i)
