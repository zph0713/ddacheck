from core import ddack,mail
from conf import settings
import argparse


def runCheck(ddatypes,interval):
    all_data = []
    for ddatype in ddatypes:
        ddatype_instance = ddack.DDAcheck(ddatype,interval)
        ddatype_instance.queryDDAaas()
        dda_issue_data = ddatype_instance.dda_abnormal_data
        dda_issue_file = ddatype_instance.file_path
        dda_total = ddatype_instance.dda_total
        format_data = {ddatype:{'total':dda_total,'data':dda_issue_data,'path':dda_issue_file}}

        if dda_issue_file != []:
            flag = 0
            for issuetype in dda_issue_file:
                if settings.Alert_Threshold[issuetype] < dda_issue_data[issuetype]:
                    flag = 1
            if flag == 1:
                all_data.append(format_data)
    att_list = []
    for i in all_data:
        att_list.append(i.values()[0]['path'].values()[0])
    if all_data != []:
        mail_instance = mail.SendMail()
        message = mail_instance.generateMail(interval,all_data)
        mail_instance.sendMail(message,att_list)

def checkAll():
    parser = argparse.ArgumentParser(add_help=True,description='DDAaasIssueCheck')
    exclusive_group = parser.add_mutually_exclusive_group(required=True)
    exclusive_group.add_argument('-t','--ddatype',nargs='+')
    parser.add_argument('-i','--interval',help="interval",type=int,default=1)
    obj = parser.parse_args()
    if obj.ddatype != None:
        runCheck(obj.ddatype,obj.interval)

def main():
    checkAll()

if __name__ == '__main__':
    main()
