#encoding=utf-8
import requests
from wox import Wox,WoxAPI
import json
from urllib import parse
import hashlib
import time
import uuid
#用户写的Python类必须继承Wox类 https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#这里的Wox基类做了一些工作，简化了与Wox通信的步骤。
class Main(Wox):
  my_uuid=""
  curtime = ""
  def request(self,url):
    #如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
    if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
      proxies = {
        "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
        "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
      return requests.get(url,proxies = proxies)
    else:
      return requests.get(url)

  def sign(self,ID,q,key):
      self.curtime = str(int(time.time()))
      length = len(q)
      input=""
      if length>20:
        input = q[0:10] + str(length) + q[-10:]
      else:
        input = q
      self.my_uuid = uuid.uuid1().hex
      sha256 = hashlib.sha256()
      sha256.update((ID+input+self.my_uuid+self.curtime+key).encode("utf-8"))
      sign = sha256.hexdigest()
      return sign

  #必须有一个query方法，用户执行查询的时候会自动调用query方法
  def query(self,key):
    results = []
    query_params = key.split("|")
    '''
    results.append({
        "Title": format(query_params),
        "SubTitle": "debug",
        "IcoPath":"Images/app.ico"
        })
    '''
    
    target_language = 'zh-CHS'
    if len(query_params) >=2:
      text = query_params[0]
      if query_params[1]:
        target_language = query_params[1]
      else:
        results.insert(0,{
        "Title": "输入语言代码",
        "SubTitle": "常用小语种代码：日语:ja  法语:fr 德语:de",
        "IcoPath":"Images/app.ico"
        })
    elif len(query_params)==1:
      text = query_params[0]
      if text=='':
        results.append({
        "Title": "有道翻译",
        "SubTitle": "请输入要查询的单词或短语",
        "IcoPath":"Images/app.ico"
        })
        return results
        
    try:
      mysign = self.sign(appID,text,appKey)
    except:
      results.append({
        "Title": "DEBUG",
        "SubTitle": "sign计算异常",
        "IcoPath":"Images/app.ico"
        })
      return results
    payload = {'q': parse.quote(text), 'from': 'auto', 'to': target_language, 'appKey': appID,'salt':self.my_uuid, 'sign': mysign,'signType':'v3', 'curtime':self.curtime}
    
    '''
    request异常捕获
    '''
    try:
      r = requests.get(url, params=payload,timeout=1)
      res = json.loads(r.text)
    except requests.exceptions.Timeout:
      results.append({
        "Title": "连接超时",
        "SubTitle": "Timeout",
        "IcoPath":"Images/app.ico"
      })
      return results
    except requests.exceptions.ConnectionError:
      results.append({
        "Title": "连接错误",
        "SubTitle": "ConnectionError",
        "IcoPath":"Images/app.ico"
      })
      return results
    except requests.exceptions.HTTPError:
      results.append({
        "Title": "HTTP错误",
        "SubTitle": "HTTPError",
        "IcoPath":"Images/app.ico"
      })
      return results

    '''
    有道json文件异常代码
    '''
    if res['errorCode']!='0':
      results.append({
        "Title": "错误代码：" + res['errorCode'],
        "SubTitle": "请查询有道api文档查找错误原因",
        "IcoPath":"Images/app.ico"
      })
      return results

    basic_flag = res.__contains__('basic')
    web_flag = res.__contains__('web')
    if res['errorCode']=='0':
      if basic_flag:
        basic = res['basic']

      results.append({
        "Title": format(res['translation']).replace('[','').replace(']','').replace('\'','') + " " + (basic['phonetic'] if(basic_flag) else ''),
        "SubTitle": "翻译结果",
        "IcoPath":"Images/app.ico"
      })

      if basic_flag:
        results.append({
          "Title": format(basic['explains']).replace('[','').replace(']','').replace('\'',''),
          "SubTitle": "基本释义",
          "IcoPath":"Images/app.ico",
        })

      if web_flag:
        web = res['web']
        for i in range(len(web)):
          web_res = web[i]
          results.append({
          "Title": format(web_res['value']).replace('[','').replace(']','').replace('\'',''),
          "SubTitle": "网络释义: " + web_res['key'],
          "IcoPath":"Images/app.ico"
        })



    return results

#以下代码是必须的
if __name__ == "__main__":
  f = open("api.json", encoding='utf-8')
  api = json.load(f)
  url = api['url']
  appID = api['appID']
  appKey = api['appKey']
  Main()