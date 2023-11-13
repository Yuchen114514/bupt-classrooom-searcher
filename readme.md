# bupt-classrooom-searcher

北京邮电大学教三空闲教室查询脚本

## 简单介绍

本脚本通过 Python 实现对教务系统-空闲教室抓包的数据进行处理，其中抓包部分需由用户自行完成，在下面会详细介绍如何抓包

## 说明

- 北邮教务系统电脑端官网并未提供空闲教室的入口，唯一的入口位于企业微信的微教学中，而微教学中的链接不支持用普通浏览器打开，因此需要通过抓包获得 json 数据。
- 抓取沙河校区和本部同理。

## 准备工具

VScode 部署 Python 环境，下载 fiddler 抓包软件，官网<https://www.telerik.com/fiddler>

## 详细步骤

### 1.打开 fiddler

- 左侧如果往外蹦一堆东西出来可以全选并 delete，当然你也可以使用筛选功能
  ![image-1.png](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/image-1.png)

- 电脑端打开企业微信，找到“我的查询”
  ![image-2.png](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/image-2.png)

- 进入今日空闲教室，此时抓包工具会出现 host 为 jwglwx 开头的包
  ![image-3.png](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/image-3.png)

- 选择上图中的那个包，在右侧的 json 可以看到详细信息为 CLASSROOM 等信息
  ![image-4.png](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/image-4.png)

- 对此包右键选择..and Open as Local File
  ![Alt text](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/IMG_20231113_105007.jpg)

### 运行脚本

- 将.json文件和.py放在相同目录中
- 使用vscode打开文件夹
- 启动运行
- 输出结果
 ![image-5.png](https://github.com/Yuchen114514/bupt-classrooom-searcher/blob/main/src/image-5.png)

### 后记

没有后记，计网一点不会呢期中还不知道怎么办，我为什么来写这个了？
