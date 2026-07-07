**中文** | [English](./README_EN.md)

# Kindle-Dowloader-And-Cropper — Kindle电子书自动截图 + 批量裁剪

两个配合使用的小工具,把锁在专有阅读器里导不出来的电子书弄成干净的图片:

- `capture_book_gui.py` — 自动翻页 + 截图,带置顶控制面板,想开始就开始、想停就停
- `crop_pages.py` — 在第一张截图上拖个框,把全部截图批量裁掉四周的界面杂物,只留书页正文

只在本文件夹里干活:截图存进 `book_pages`,裁剪结果存进 `book_pages_cropped`,不进子文件夹、不碰别处文件,原始截图一张不动。你要想删掉自己手动删就行了。

## 使用方法

1. 下载上面俩脚本,就这俩:`capture_book_gui.py` 和 `crop_pages.py`,其他别下,放进同一个文件夹
2. 打开黑窗口(Win+R 输入 cmd),进入该文件夹,运行 `pip install pyautogui pillow keyboard`(只需装这一次)
3. 打开你的电子书阅读器,翻到第一页
4. 运行 `python capture_book_gui.py`,弹出置顶控制面板。点「开始」(或按 F8),3 秒内用鼠标点回阅读器窗口,然后撒手不管,它自己翻页截图。抓完按 F9 停止
5. 运行 `python crop_pages.py`,弹出第一张截图。按住左键拖红框圈出书页正文,按回车,自动批量裁剪全部图片
6. 享受!干净的正文图片在同目录的 `book_pages_cropped` 文件夹里

## 说明

- 需要电脑装有 Python 3(Windows 可从 [python.org](https://www.python.org) 安装,安装时勾选 "Add Python to PATH")
- 截图工具快捷键全局有效:F8 开始/暂停,F9 停止,阅读器全屏时也能用;急停保险丝:鼠标猛甩到屏幕左上角,程序立即中断
- 默认按键盘右方向键(→)翻页;如果你的阅读器只认鼠标点击翻页,打开 `capture_book_gui.py` 把配置区的 `TURN_MODE` 改成 `"click"` 并填上点击坐标
- 每页默认停留 3 秒等待渲染,页面加载慢可在配置区调大 `DELAY`
- 建议先抓五六页按 F9 停下,检查 `book_pages` 里的图对不对,再放开正式抓
- 裁剪工具拖歪了不要紧,重新拖,以最后一次为准;裁坏了也没损失,原图都在,重跑一次重新框就行
- 拖框裁剪能一框通吃的前提:截图全程阅读器窗口没挪动过位置
