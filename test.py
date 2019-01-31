import requests
import json
from urllib import parse
import hashlib
text = '你好'
appID = '5ad5f54f99d85b29'
appKey = '9UHXVW93LNJ0ig54NXBHzsO8M807ECTE'
md5 = ''
salt='233'

md5str = appID+text+salt+appKey
#生成一个md5对象
m1 = hashlib.md5()
#使用md5对象里的update方法md5转换
m1.update(md5str.encode("utf-8"))
token = m1.hexdigest()
md5 = token.upper()

print(md5)
payload = {'q': parse.quote(text), 'from': 'auto', 'to': 'uu', 'appKey': appID,'salt':salt, 'sign': md5}

r = requests.get("http://openapi.youdao.com/api", params=payload)
print(r.url)
res = json.loads(r.text)
print(json.loads(r.text))
print(type(res))
basic = res['basic']
print(basic['explains'])
print(format(basic['explains']))
print(format(basic['explains']).strip('\'[]'))
print(res.__contains__('basic'))

results=[]
web = res['web']
for web_res in web:
    results.append({
    "Title": web_res['value'],
    "SubTitle": web_res['key'],
    "IcoPath":"Images/app.ico", 
    })

print(results)