# Wox有道词典翻译插件

## 概述

本项目采用python编写，参照了C#版本有道词典插件代码并增加了多语言支持，C#版本[地址](https://github.com/Wox-launcher/Wox.Plugin.Youdao)
**演示:**
![演示](http://oss.wangjunchi.top/yd/3_small.png)

## 重要

1.  ~~本项目仍处于开发中，虽然C#插件已经多年无人维护，但除非无法使用，在日常使用中仍然推荐使用C#版插件。~~ 欢迎使用本插件，欢迎issue反馈。
2. 由于有道词典api政策的变化，现在已经无法申请api免费账户，若想要使用本插件，需要在有道智云的[官网](https://ai.youdao.com)申请开发者账户，每个账户开通后会有 __100RMB__ 的体验金，足够使用很长时间。申请完之后请在`api.json`文件内填上自己的`appID`和`appKey`。__C#版本无需申请开发者账户即可使用。__
3. 有道api文档 [地址](https://ai.youdao.com/docs/doc-trans-api.s#p01) ，有道api接口参数经常调整，虽然旧的接口依旧可用，但请一切以官方文档为准。
4. Wox[下载地址](http://www.wox.one/)

## 使用

### 安装

1. clone本项目或者直接下载zip压缩包并解压。
2. 将文件夹拷贝到`Wox`安装目录内的`plugin`文件夹内，示例路径：`C:\Users\wangj\AppData\Local\Wox\app-1.3.578\Plugins`，请确保进入文件夹后可以看到main.py等一系列文件而不是另一层文件夹。
3. 打开Wox的`设置-插件`菜单，如果发现名为`yd_translation`的插件，说明安装成功。
4. 重启Wox

### 配置

1. 注册有道智云的开发者账号，并创建一个接入方式为api的应用并绑定自然语言翻译服务。[教程](https://ai.youdao.com/doc.s#guide)
2. 将`api.json.example`重命名为`api.json`，用文本编辑器打开后在相应位置填入你的`appkey`（密钥）和`appID`，保存。

### 查询

1. 在Wox窗口中输入`ydt`激活插件，并在一个空格后输入想查询的单词或短语。

   示例：`ydt apple`
![演示](http://oss.wangjunchi.top/yd/1_small.png)
2. 可以在查询的单词或短语后加上一个`|`和[语言代码](https://ai.youdao.com/docs/doc-trans-api.s#p07)来指定翻译的目标语言。

   示例：`ydt hello|ja`（翻译成日语）
![演示](http://oss.wangjunchi.top/yd/2_small.png)
### 注意

1. 只有中英互译可以实现查词典的功能，其他小语种翻译大部分只有翻译功能。
2. 输入语言由有道服务器自动判断，当输入语言是中文时，默认目标语言是英语，且当目标语言代码错误时，服务器自动返回英语结果。当输入语言是非中文时，默认返回中文翻译结果。
3. 若返回错误代码，请查阅[官方文档-错误代码](https://ai.youdao.com/docs/doc-trans-api.s#p08)。
4. __不要分享自己的密钥。__
