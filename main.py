#encoding=utf-8
import requests
from wox import Wox,WoxAPI
import json
from urllib import parse
import hashlib


appID = '5ad5f54f99d85b29'
appKey = '9UHXVW93LNJ0ig54NXBHzsO8M807ECTE'
md5 = ''
salt='233'



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
    basic = res['basic']

    results.append({
      "Title": format(res['translation']).strip('[]\'') + " " + basic['phonetic'],
      "SubTitle": "基本释义:" + " " + format(basic['explains']).strip('\'[]'),
      "IcoPath":"Images/app.ico", 
      "ContextData": "ctxData"
        })
    return results
    '''
    for i in bs.select(".comhead"):
      title = i.previous_sibling.text
      url = i.previous_sibling["href"]
      results.append({
        "Title": title ,
        "SubTitle":title,
        "IcoPath":"Images/app.ico",
        "JsonRPCAction":{
          #这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
          #方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
          "method": "openUrl",
          #参数必须以数组的形式传过去
          "parameters":[url],
          #是否隐藏窗口
          "dontHideAfterAction":True
        }
      })
      '''
  


#以下代码是必须的
if __name__ == "__main__":
  Main()