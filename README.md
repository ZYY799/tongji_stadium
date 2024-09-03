# 同济大学体育馆场地预约自动化软件

[![Homepage](https://img.shields.io/badge/-Homepage-yellow)](https://www.zy66.online) ![v1.0](https://img.shields.io/badge/zy-tongji_stadium-blue)

## 🤔 部署方式

- exe执行文件窗口化运行

1. 下载解压最新发布!![image-20240902154449460](https://github.com/user-attachments/assets/2af27c1d-4609-44ee-ba9e-e0a75f859023)


2. 在本地得到![image-20240902154552873](https://github.com/user-attachments/assets/9aed7505-52c5-4b4c-920d-da8f0a2973c9)

3. 点击文件`credentials.txt`，在文件中填写你的学号及密码（注意区分大小写)，学号在第一行，密码第二行，不要有其它字符；特别注意右下角为`utf-8`编码格式；`password`打错了忽略！![image-20240902155017606](https://github.com/user-attachments/assets/19bbfdf4-5c3c-409d-bf24-8f220fb32c97)

4. 点击`tongji_stadium.exe`运行，设置相关参数后点击运行：

![image-20240902160143667](https://github.com/user-attachments/assets/edf5916d-dd90-4f43-ae33-f5ac53bf7a17)


特别说明：zy_model建议不要开启，开启后将暴力破解滑块，比手动慢很多；（暴力破解原理就是滑块的滑动距离是几个值随机出现，所以设定一个固定滑动距离赌运气）



- 源代码启动
    1. `conf_gui.py`是图形化界面执行文件；
    2. `conf.py`是执行源代码，可以尝试源码启动，并且配置好相关参数；不多赘述；

<br>

## 🤔 实现逻辑
- **v1.0.1修改逻辑完善**
  1. 首先完成学号密码读取并正确登录网站；
  2. 选择正确的运动类型及场馆；
  3. 默认预订当天后的第七天场地，因此网页会尝试寻找设定日期的场地，找不到则会一直刷新（建议在12:58左右开始运行）；
  4. 在选定的日期内优先选择对应的时间和场地：
      - 如果当前时间段和选定场地不可选（灰色），将从候选场地列表中逐一检查其它场地是否可选；
     - 如果当前时间段不可选，则将时间段加一，并重复上述步骤；
     - 如果在截至时间time_choice_limit内依然未能找到合适的场地，则终止程序；
  5. 选定后快速点击确认并提交；
  6. 到达验证码阶段时，如果未开启zy_model，需手动滑动滑块验证（开启后会自动破解，但不推荐）。

<br>

## [**项目技术路线说明文档**](https://zy66.online/index.php/archives/174)

<br>

仅用于学习交流，禁止传播！！！

