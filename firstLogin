#-*- coding: utf-8 -*-
__author__ = 'Wu_cf'
# Build-in / Std
import os, sys, time, platform, random
import re, json, cookielib
import requests, termcolor
import webbrowser;

#会话形式,程序执行会在这里检查一下cookie
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')

try:
    requests.cookies.load(ignore_discard=True)
except:
    pass

def download_captcha():
    url = "http://www.zhihu.com/captcha.gif"
    #请求验证码的url http://www.zhihu.com/captcha.gif?r=1448195049209
    r = requests.get(url, params={"r": random.random()} )
    #请求成功会返回code
    if int(r.status_code) != 200:
        print u"验证码请求失败"
    image_name = u"verify." + r.headers['content-type'].split("/")[1]
    #wb：以二进制模式读写（图片嘛，很自然这样）
    open( image_name, "wb").write(r.content)
    #调用浏览器打开gif图片，接着自己输入就可以啦
    webbrowser.open(image_name)
    captcha_code = raw_input( u"请输入验证码: ")
    return captcha_code

def search_xsrf():
    url = "http://www.zhihu.com/"
    r = requests.get(url)
    if int(r.status_code) != 200:
        print u"验证码请求失败"
    #<input type="hidden" name="_xsrf" value="c06acd97151a9f46fc42fd3e7cf4259d"/>
    #就是匹配这一段的正则，\s是匹配任意空白字段符，S+匹配字符任意次
    results = re.compile(r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\"", re.DOTALL).findall(r.text)
    if len(results) < 1:
        print u"提取XSRF 代码失败"
        return None
    return results[0]

def build_form(account, password):
    if re.match(r"^1\d{10}$", account):
        account_type = "phone_num"
    elif re.match(r"^\S+\@\S+\.\S+$", account):
        account_type = "email"
    else:
        print u"帐号类型错误"
    form = {account_type: account, "password": password, "remember_me": True }
    #xsrf
    form['_xsrf'] = search_xsrf()
    #验证码
    form['captcha'] = download_captcha()
    return form

def upload_form(form):
    if "email" in form:
        url = "http://www.zhihu.com/login/email"
    elif "phone_num" in form:
        url = "http://www.zhihu.com/login/phone_num"
    #请求头
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
    #此处即真正的模仿浏览器进行请求
    r = requests.post(url, data=form, headers=headers)
    if int(r.status_code) != 200:
        print u"表单上传失败!"

    if r.headers['content-type'].lower() == "application/json":
        try:
            # 修正  justkg 提出的问题: https://github.com/egrcc/zhihu-python/issues/30
            result = json.loads(r.content)
            # {u'msg': u'\u767b\u9646\u6210\u529f', u'r': 0}
            print result
        except Exception as e:
            pass
            result = {}
        if result["r"] == 0:
            print u"登录成功！"
            return {"result": True}
        elif result["r"] == 1:
            print u"登录失败！"
            return {"error": {"code": int(result['errcode']), "message": result['msg'], "data": result['data'] } }
        else:
            print u"表单上传出现未知错误: \n \t %s )" % ( str(result) )
            return {"error": {"code": -1, "message": u"unknow error"} }
    else:
        print u"无法解析服务器的响应内容: \n \t %s " % r.text
        return {"error": {"code": -2, "message": u"parse error"} }


def islogin():
    # check session
    url = "http://www.zhihu.com/settings/profile"
    #底下的allow_redirects为禁止服务器重定向设置
    r = requests.get(url, allow_redirects=False)
    status_code = int(r.status_code)
    if status_code == 301 or status_code == 302:
        # 未登录
        return False
    elif status_code == 200:
        return True
    else:
        print u"网络故障"
        return None

def login(account=None, password=None):
    if islogin() == True:
        print u"你已经登录过咯"
        return True
    if account == None:
        account  = raw_input(u"请输入登录帐号: ")
        password = raw_input(u"请输入登录密码: ")
    #建立表单
    form_data = build_form(account, password)
    #上传表单，其实就是进行url请求
    result = upload_form(form_data)
    if "error" in result:
        if result["error"]['code'] == 1991829:
            # 验证码错误
            print u"验证码输入错误，请准备重新输入。"
            return login()
        else:
            print u"unknow error."
            return False
    elif "result" in result and result['result'] == True:
        # 登录成功,保存cookies,以便下次直接登录
        print u"登录成功！"
        requests.cookies.save()
        return True

if __name__ == "__main__":
    # login(account="xxxx@email.com", password="xxxxx")
    login()

