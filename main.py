#encoding=utf-8
import requests
from wox import Wox,WoxAPI
import json
from urllib import parse
import hashlib


#用户写的Python类必须继承Wox类 https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
#这里的Wox基类做了一些工作，简化了与Wox通信的步骤。
class Main(Wox):

  def request(self,url):
    #如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
    if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
      proxies = {
        "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
        "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
      return requests.get(url,proxies = proxies)
    else:
      return requests.get(url)

  #必须有一个query方法，用户执行查询的时候会自动调用query方法
  def query(self,key):
    #r = self.request('https://news.ycombinator.com/')
    #bs = BeautifulSoup(r.text)
    text = key

    #生成MD5签名
    md5str = appID+text+salt+appKey
    #生成一个md5对象
    m1 = hashlib.md5()
    #使用md5对象里的update方法md5转换
    m1.update(md5str.encode("utf-8"))
    token = m1.hexdigest()
    md5 = token.upper()
    results = []

    payload = {'q': parse.quote(text), 'from': 'EN', 'to': 'zh-CHS', 'appKey': appID,'salt':salt, 'sign': md5}
    r = requests.get("http://openapi.youdao.com/api", params=payload)
    res = json.loads(r.text)

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
  salt = api['salt']
  Main()