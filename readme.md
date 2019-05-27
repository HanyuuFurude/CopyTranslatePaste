# Seiji--CopyTranslatePaste
> [下载](https://github.com/HanyuuFurude/CopyTranslatePaste/releases)
* CopyTranslatePaste 是一个即时将您的输入/剪切板中的文字进行翻译的一个工具；
* 您可以直接复制待翻译的文本，该工具会自动翻译您的剪切内容进行翻译并放进您的剪切板中，只需选择粘贴就能粘贴译；。
* 本工具同时支持在cmd命令行下操作和图形界面操作；
* 由于调取剪切板使用的windows的API，本工具目前仅支持windows操作系统；
* 运行方法：
  * cmd/Powershell使用：
    * 手动翻译
      * 将t.exe放进您在path文件夹中或者将该文件夹添加进path内，命令
      ``` cmd
      t [待翻译内容]
      ```
    * ~~（命令行下未添加直接读取剪切板但是会将翻译结果放回剪切板）~~
    * 常驻后台模式（剪切板自动读取替换）
      ``` cmd
      t -b
      ```
      或者
      ``` cmd
      t --background
      ```
  * 图形界面（GUI）使用：
    
    * 运行ui.exe即可，可以设置是否从剪切板读入和是否写回剪切板（开启从剪切板读入则输入框将不响应翻译）
# 将要到来的新特性（咕咕咕~）
>（如果我很久都没有更新请把我从鸽子笼里[拯救](mailto:Furude_Hanyuu@outlook.com)出来谢谢）
* 2019/05/25
  * 图片翻译功能
  * 截图翻译功能
  * 快捷键响应
## [开发日志](develop.md)
