# bupt-classrooom-searcher

北京邮电大学教三空闲教室查询脚本

## 简单介绍

本脚本通过 Python 实现对教务系统-空闲教室抓包的数据进行处理，其中抓包部分需由用户自行完成，在下面会详细介绍如何抓包

## 说明

- 北邮教务系统电脑端官网并未提供空闲教室的入口，唯一的入口位于企业微信的微教学中，而微教学中的链接不支持用普通浏览器打开，因此需要通过抓包获得 json 数据。
- 此脚本现在仅支持北邮本部教三的抓包，因为本人也只需要这一个功能。若要新增其他教室其实很简单，只需要在代码中修改“3-”改为自己需要查询的教室的头文字即可。沙河校区同理。

## 准备工具

VScode 部署 Python 环境，下载 fiddler 抓包软件，官网https://www.telerik.com/fiddler，下载安装

## 详细步骤

### 1.打开 fiddler

- 左侧如果往外蹦一堆东西出来可以全选并 delete，当然你也可以使用筛选功能
  ![Alt text](image-1.png)

- 电脑端打开企业微信，找到“我的查询”
  ![Alt text](image-2.png)

- 进入今日空闲教室，此时抓包工具会出现 host 为 jwglwx 开头的包
  ![Alt text](image-3.png)

- 选择上图中的那个包，在右侧的 json 可以看到详细信息为 CLASSROOM 等信息
  ![Alt text](image-4.png)

- 对此包右键选择..and Open as Local File
  ![Alt text](src/IMG_20231113_105007.jpgIMG_20231113_105007.jpg)
