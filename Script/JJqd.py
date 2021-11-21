# -*- coding: utf8 -*-
import requests,json
from requests.cookies import RequestsCookieJar


# 通知变量 详网企业微信
ID = ''
SECRET = ''
html = ''

# 账号信息
'''
usernames = ['账号1', '账号2']
passwords = ['密码1','密码2']
'''
usernames = ['*********']
passwords = ['*********']


count = min(len(usernames),len(passwords))


# 机场官网
url = 'https://j02.space'




sininUrl = url + '/signin' # 登录地址
checkinUrl = url + '/user/checkin' # 签到地址


# 使用账号密码自动登录并获取cookie
def getCookie(username,password):
    userInfo = {"email":username,'passwd':password}
    herder = {
        'Host':'j02.space',
        'Content-Type': 'application/json;charset=utf-8',
        'origin': 'https://j02.space',
        'referer': 'https://j02.space/signin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73' 
    }

    page = requests.post(sininUrl,data=json.dumps(userInfo),headers=herder)
    cookies = requests.utils.dict_from_cookiejar(page.cookies)
    cookie = ''
    for k,v in cookies.items():
        cookie += k + "=" + v + ";" 
    print(page.text)
    if 'email' in cookies and cookies['email'][0:3] == userInfo['email'][0:3]:
        print('获取cookie成功,cookie:')
        print(cookie)
        return cookies
    else:
        print('获取cookie失败')

# 签到
def checkin(cookie,username):
    checkinpage = requests.post(checkinUrl,cookies=cookie)
    print(json.loads(checkinpage.text)['msg'])
    text = json.loads(checkinpage.text)['msg']
    if checkinpage.status_code == 200:
        access_token = getAccessToken(ID,SECRET)
        sendMsg(access_token,1000002,'签到通知','2faaV00qNu2t1V0dOoOedOEmXmMKXlOtRR_iCKPcnfKM','Lee','http://47.98.166.168:5701',text,text+'\n\n本通知 by: Lee',username)


# 获取access_token 
# 详见：https://work.weixin.qq.com/api/doc/90000/90135/91039
# corpid 企业ID  获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/90665#corpid
# corpsecret 应用的凭证密钥  获取方式参考：https://work.weixin.qq.com/api/doc/90000/90135/90665#secret
def getAccessToken(corpid,secret):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + secret
    req = requests.get(url)
    try:
        msg = json.loads(req.text)
    except:
        print('access_token请求出错')
    print(msg)
    return msg['access_token']



# 推送消息
# agentId 应用ID
# title 消息标题
# media_id 图文消息缩略图的media_id key
# author 图文消息的作者
# content 消息内容
# digest 图文消息的描述
# url 阅读原文跳转的链接
def sendMsg(access_token,agentId,title,media_id,author,url,content,digest,username):
    sendUrl = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
    html = "<h3>用户:"+ username.split('@')[0] +"</h3></br>"+  content 
    data = {
    "touser" : "@all", #成员ID列表（消息接收者，最多支持1000个）
    #"toparty" : ["partyid1","partyid2","LinkedId1/partyid1","LinkedId2/partyid2"], # 部门ID列表，最多支持100个。
    #"totag" : ["tagid1","tagid2"], #本企业的标签ID列表
    "toall" : 0, #1表示发送给应用可见范围内的所有人（包括互联企业的成员），默认为0
    "msgtype" : "mpnews", # 消息类型，此时固定为：news 图文消息
    "agentid" : agentId, #企业应用的id，整型。可在应用的设置页面查看
    "mpnews" : {
       "articles" : [
            {
               "title" : title,
               "thumb_media_id": media_id,
               "author": author,
               "content_source_url": '',
               "content":html + '</br></br>本消息来自' + '<a href="https://gitee.com/lxfap">'+ author +' https://gitee.com/lxfap</a>',
               "digest": username+ '\n' + digest
           }
        ]
    }
    }
    sendreq = requests.post(sendUrl,json.dumps(data))
    if json.loads(sendreq.text)['errcode'] == 0:
        print('推送成功')

def main():
    cookies = []
    for i in range(count):
        ck = getCookie(usernames[i],passwords[i])
        cookies.append(ck)

    if cookies:
        for i in range(count):
            print('账号{}获取cookie成功，开始签到'.format(usernames[i].split('@')[0]))
            checkin(cookies[i],usernames[i])
        return '调用成功'
    else:
        print('获取cookie失败')

# 开始运行
main()
