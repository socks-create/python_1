
import requests,re
import os
import json
import logging
import time
import zipfile
import sys
import time
logging.getLogger("requests").setLevel(logging.WARNING)
requests.packages.urllib3.disable_warnings()
import threading
global mailaddr

import logging
logging.basicConfig(filename='log.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)



hosturl = "https://192.168.1.1:7071"
username = "admin"
password = "pass"
def get_admin_token():
    my_headers = {'Host': '192.168.1.1:7071',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Accept': '*/*',
                'Referer': 'https://192.168.1.1:7071/zimbraAdmin/',
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'Cookie': 'ZM_TEST=true; ZM_AUTH_TOKEN=0_8e3e0b572980032a1a78ae636ce56b3d1b3a71c1_69643d33363a36656531396665622d376663362d343737312d396662302d6265356531386364313862323b6578703d31333a313532323635303437343235323b747970653d363a7a696d6272613b7469643d393a3435333838323731313b76657273696f6e3d31333a382e362e305f47415f313135333b637372663d313a313b; JSESSIONID=7owo6b3t2tsx1vzpwef9avwfo'
                }
    value = "<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"><soap:Header><context xmlns=\"urn:zimbra\"><userAgent xmlns=\"\" name=\"ZimbraWebClient - FF59 (Win)\"/><session xmlns=\"\"/><authTokenControl xmlns=\"\" voidOnExpired=\"1\"/><format xmlns=\"\" type=\"js\"/></context></soap:Header><soap:Body><AuthRequest xmlns=\"urn:zimbraAdmin\"><name xmlns=\"\">admin</name><password xmlns=\"\">pass</password><virtualHost xmlns=\"\">192.168.1.1</virtualHost></AuthRequest></soap:Body></soap:Envelope>"
    r = requests.post('%s/service/admin/soap/AuthRequest' % hosturl,headers=my_headers,data=value,verify=False,timeout=10)
    token = re.search(re.compile(r'{"Header".*?type":"(.*?)","id.*?{"_content":"(.*?)"}.*?"}'),r.text)
    token =  token.group(2)
    return token

def get_user_id(admintoken,user):
    headers1 = {'Host': '192.168.1.1:7071',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'https://192.168.1.1:7071/zimbraAdmin/',
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'Content-Length': '1224',
                'Cookie': 'ZM_TEST=true; ZM_ADMIN_AUTH_TOKEN=%s; ZM_AUTH_TOKEN=0_0b8d33c9f89c42ced25a614463039a7e830e829e_69643d33363a30366632643936662d393861362d343233302d623763372d6138386331386263303663353b6578703d31333a313532323439383732353735313b6169643d33363a36656531396665622d376663362d343737312d396662302d6265356531386364313862323b747970653d363a7a696d6272613b7469643d31303a313437373533313738363b76657273696f6e3d31333a382e362e305f47415f313135333b; JSESSIONID=1ks45osfz0neh12fd1t7y8ga2b' % admintoken
                }
    date1 = '<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"><soap:Header><context xmlns=\"urn:zimbra\"><userAgent xmlns=\"\" name=\"ZimbraWebClient - FF59 (Win)\"/><session xmlns=\"\" id=\"371\"/><format xmlns=\"\" type=\"js\"/></context></soap:Header><soap:Body><BatchRequest xmlns=\"urn:zimbra\" onerror=\"continue\"><SearchDirectoryRequest xmlns=\"urn:zimbraAdmin\" offset=\"0\" limit=\"50\" sortBy=\"name\" sortAscending=\"1\" applyCos=\"false\" applyConfig=\"false\" attrs=\"displayName,zimbraId,zimbraAliasTargetId,cn,sn,zimbraMailHost,uid,zimbraCOSId,zimbraAccountStatus,zimbraLastLogonTimestamp,description,zimbraIsSystemAccount,zimbraIsDelegatedAdminAccount,zimbraIsAdminAccount,zimbraIsSystemResource,zimbraAuthTokenValidityValue,zimbraIsExternalVirtualAccount,zimbraMailStatus,zimbraIsAdminGroup,zimbraCalResType,zimbraDomainType,zimbraDomainName,zimbraDomainStatus\" types=\"accounts,aliases,distributionlists,resources,domains,coses\"><query xmlns=\"\">(|(mail=%s)(cn=%s)(sn=%s)(gn=%s)(displayName=%s)(zimbraMailDeliveryAddress=%s)(zimbraDomainName=%s)(uid=%s)(zimbraMailAlias=%s)(uid=%s)(zimbraDomainName=%s)(cn=%s))</query></SearchDirectoryRequest></BatchRequest></soap:Body></soap:Envelope>' % (user,user,user,user,user,user,user,user,user,user,user,user)
    recon = requests.post('%s/service/admin/soap/BatchRequest' % hosturl,headers=headers1,data=date1,verify=False,timeout=10)
    #print(recon.text)
    id1 = re.search(re.compile(r'{.*?"name":"(.*?)","id":"(.*?)",.*?}'), recon.text)
    print ("%s :  %s" % (id1.group(1),id1.group(2)))
    global mailaddr
    mailaddr = id1.group(1)
    id = id1.group(2)
    return id


def get_user_token(admintoken,id):
    headers1 = {'Host': '192.168.1.1:7071',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'Accept': '*/*',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Referer': 'https://192.168.1.1:7071/zimbraAdmin/',
                'Content-Type': 'application/soap+xml; charset=utf-8',
                'Content-Length': '1224',
                'Cookie': 'ZM_TEST=true; ZM_ADMIN_AUTH_TOKEN=%s; ZM_AUTH_TOKEN=0_852cf2d9e24c069bd02f2852647de78e8bf8c7cc_69643d33363a65333634303762382d326237662d346231382d383866342d3038316335373231353865323b6578703d31333a313532323530343134303236353b6169643d33363a36656531396665622d376663362d343737312d396662302d6265356531386364313862323b747970653d363a7a696d6272613b7469643d393a3835373836333739343b76657273696f6e3d31333a382e362e305f47415f313135333b; JSESSIONID=ba8b45ex2p4k179xuxtzyo8pf' % admintoken
                }
    date = '<soap:Envelope xmlns:soap=\"http://www.w3.org/2003/05/soap-envelope\"><soap:Header><context xmlns=\"urn:zimbra\"><userAgent xmlns=\"\" name=\"ZimbraWebClient - FF59 (Win)\"/><session xmlns=\"\" id=\"371\"/><format xmlns=\"\" type=\"js\"/></context></soap:Header><soap:Body><DelegateAuthRequest xmlns=\"urn:zimbraAdmin\"><account xmlns=\"\" by=\"id\">%s</account></DelegateAuthRequest></soap:Body></soap:Envelope>' % id
    recon = requests.post('%s/service/admin/soap/DelegateAuthRequest' % hosturl,headers=headers1,data=date,verify=False,timeout=10)
    #print (recon.text)
    user_token = re.search(re.compile(r'{"Header".*?authToken.*?:"(.*?)"}.*?}'), recon.text)
    user_token = user_token.group(1)
    return user_token

def get_mailid(admintoken,user_token,mailaddr):
    url = "https://192.168.1.1:8443/service/preauth?authtoken=" + user_token + "&isredirect=1&adminPreAuth=1"

    my_hearders = {'Host': '192.168.1.1:8443',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                    'Accept-Encoding': 'gzip, deflate',
                    'X-Zimbra-Csrf-Token': '0_583076b0aa905c7c0a72fae8a84e911e2209f80a',
                    'Referer': 'https://192.168.1.1:8443/mail?adminPreAuth=1',
                    'Cookie': 'ZM_ADMIN_AUTH_TOKEN=%s; ZM_AUTH_TOKEN=%s; JSESSIONID=10ep7pc4bfmf04lcwozokm2af' % (admintoken,user_token),
                    'Cache-Control': 'max-age=0'
                    }
    #global mailaddr
    url2 = "https://192.168.1.1:8443/service/soap/SearchRequest"
    date = '{\"Header\":{\"context\":{\"_jsns\":\"urn:zimbra\",\"userAgent\":{\"name\":\"ZimbraWebClient - FF59 (Win)\",\"version\":\"8.6.0_GA_1153\"},\"session\":{\"_content\":161,\"id\":161},\"account\":{\"_content\":\"%s\",\"by\":\"name\"},\"csrfToken\":\"0_583076b0aa905c7c0a72fae8a84e911e2209f80a\"}},\"Body\":{\"SearchRequest\":{\"_jsns\":\"urn:zimbraMail\",\"sortBy\":\"dateDesc\",\"header\":[{\"n\":\"List-ID\"},{\"n\":\"X-Zimbra-DL\"},{\"n\":\"IN-REPLY-TO\"}],\"tz\":{\"id\":\"Asia/Hong_Kong\"},\"locale\":{\"_content\":\"zh_CN\"},\"offset\":0,\"limit\":100,\"query\":\"is:anywhere after:20180407\",\"types\":\"conversation\",\"recip\":\"0\",\"fullConversation\":1,\"needExp\":1}}}'% mailaddr
    conre2 = requests.post(url2,headers=my_hearders,data=date,verify=False,timeout=60)
    print (conre2.text)
    mailid = re.findall(re.compile('{.*?"-(.*?)".*?}'),conre2.text)
    print(mailid)
    for i in range(len(mailid)):
        mailid1 = mailid[i]
        url = "https://192.168.1.1:8443/service/home/~/?auth=co&loc=zh_CN&id=" + str(mailid1) + "&fmt=zip"
        print (url)
        rd = requests.get('%s' % url,headers = my_hearders,verify = False,timeout = 60)
        path = "E:\\pycode\\zimbra\\mailfile\\" + str(mailaddr)
        print (path)
        if not os.path.isdir(path):
            os.makedirs(path)
        downfilepath = path + "\\" + mailid1 + ".zip"
        print (downfilepath)
        logging.info('%s ,  %s  ' % (mailaddr,downfilepath))
        try:
            with open('%s' % downfilepath, "wb") as code:
                code.write(rd.content)
                code.close()
        except:
            print ("%s write file faile" % downfilepath)
        try:
            fzz = zipfile.ZipFile(downfilepath, 'r')
            for file in fzz.namelist():
                fzz.extract(file, path)
                fzz.close()
        except:
            print ("%s unzip file faile" % downfilepath)
        try:
            if os.path.exists(downfilepath):
                os.remove(downfilepath)
        except:
            os.system("del /F /Q %s" % downfilepath)


def main():
    global mailaddr
    threads = []
    admintoken = get_admin_token()
    print (admintoken)
    user = ['admin','user','user1']
    for i in range(len(user)):
        id = get_user_id(admintoken,user[i])
        #print (id)
        user_token = get_user_token(admintoken,id)
        #print (user_token)
        #mailid = get_mailid()
        t1 = threading.Thread(target=get_mailid, args=(admintoken,user_token,mailaddr))
        t1.Daemon = True
        threads.append(t1)
    for t in threads:
        t.start()

if __name__ == "__main__":
    main()