# Wox有道词典翻译插件

## 概述

本项目采用python编写，基于C#版本有道词典插件实现，C#版本[地址](https://github.com/Wox-launcher/Wox.Plugin.Youdao)

## 注意

1. 本项目仍处于开发中，虽然C#插件已经多年无人维护，但除非无法使用，在日常使用中仍然推荐使用C#版插件。
2. 由于有道词典api政策的变化，现在已经无法申请api免费账户，若想要使用本插件，需要在有道智云的[官网](https://ai.youdao.com)申请开发者账户，每个账户开通后会有100RMB的体验金，足够使用很长时间了。申请完之后请在`api.json`文件内填上自己的`appID`和`appKey`。C#版本无需申请开发者账户即可使用。
3. 有道api文档 [地址](https://ai.youdao.com/docs/doc-trans-api.s#p01) ，有道api接口参数经常调整，虽然旧的接口依旧可用，但请一切以官方文档为准。

