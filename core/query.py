import json
from conf import settings

class ESBuild(object):
    def __init__(self,Scan_Type,Time_Interval):
        self.Scan_Type = Scan_Type
        self.Time_Interval = Time_Interval

    def queryDDAaas(self):
        query_body = '{"size":0,"query":{"bool":{"filter":[{ "terms": { "tm_DDAaas_scan_type": ["%s" ] } },' \
                     '{"terms":{"tm_module":["scan-scanner"]}},' \
                     '{"terms":{"tm_security_filter_name":["Virtual Analyzer"]}},' \
                     '{"range":{"tm_timestamp":{"gte":"now-%dh"}}}]}},' \
                     '"aggs":{"ATP_count":{"terms":{"field":"tm_DDAaas_risk_level"}}}}' %(self.Scan_Type,self.Time_Interval)
        return query_body

    def queryAbnormal(self,risk_level):
        query_body = '{"size":10000,"query":{"bool":{"filter":[{ "terms": { "tm_DDAaas_scan_type": ["%s" ] } },' \
                     '{"terms":{"tm_module":["scan-scanner"]}},' \
                     '{"terms":{"tm_security_filter_name":["Virtual Analyzer"]}},' \
                     '{"terms":{"tm_DDAaas_risk_level":["%s"]}},' \
                     '{"range":{"tm_timestamp":{"gte":"now-%dh"}}}]}}}' %(self.Scan_Type,risk_level,self.Time_Interval)
        return query_body

