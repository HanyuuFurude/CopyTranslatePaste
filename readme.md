# CopyTranslatePaste
> [下载](https://github.com/HanyuuFurude/CopyTranslatePaste/releases)
* CopyTranslatePaste 是一个即时将您的输入/剪切板中的文字进行翻译的一个工具；
* 您可以直接复制待翻译的文本，该工具会自动翻译您的剪切内容进行翻译并放进您的剪切板中，只需选择粘贴就能粘贴译；。
* 本工具同时支持在cmd命令行下操作和图形界面操作；
* 由于调取剪切板使用的windows的API，本工具目前仅支持windows操作系统；
* 运行方法：
  * cmd/Powershell使用：
    * 将t.exe放进您在path文件夹中或者将该文件夹添加进path内，命令
     ``` cmd
     t [待翻译内容]
     ```
    * （命令行下未添加直接读取剪切板但是会将翻译结果放回剪切板）
  * 图形界面（GUI）使用：
    * 运行ui.exe即可，可以设置是否从剪切板读入和是否写回剪切板（开启从剪切板读入则输入框将不响应翻译）
# Log
* 2019/02/28
  * 第一版
  * 已知问题：
    * 当读取到剪切板中的非文字内容时，GUI程序停止响应
    * 开启剪切板读入时，输入框不响应翻译