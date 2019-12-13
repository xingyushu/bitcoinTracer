# bitcoinTracer
提供一种解决思路，使用深度学习的方法监控和溯源比特币的交易

![整体思路](https://github.com/xingyushu/coinTracer/blob/master/images/g3.PNG)

## 1  block parser：区块解析


区块解析器从官方比特币客户端填充的本地.bitcoin文件夹中读取区块和交易，并将区块链数据导出到区块链数据库

[一种C++的解析方法](https://github.com/znort987/blockparser)   <br/>
[其它解析方法](https://blog.csdn.net/boke14122621/article/details/103162435)

## 2  cluster：地址集群的提取器

群集器的目标是找到属于同一用户的地址组。 它使用两种启发式方法增量读取区块链数据库并生成-更新地址集群。 第一个启发式方法利用具有多个输入的事务，而第二个启发式则利用事务中的“更改”概念这些集群存储在集群文件中。

(1) 多交易输入的地址   <br/>
(2) 跳板地址     <br/>
(3) 找零地址等等   <br/>
##### 新增的点： 增加对数据的统计分析
[ref:bds](https://bds-console.jdcloud.com/dashboard/2)     <br/>
(1)  活跃交易：比如每天转入、转出交易量为top 100的数字货币地址     <br/>
(2)  总结大额转入、大批量小额转出等，或者大批量小额转入，大额转入等交易模式  <br/>
(3)   博彩、勒索软件、走私贩毒等数字货币的交易模式通过模块3完成  

## 3  Scrapers：爬虫模块 

一组Scrapers会在网络上搜寻要关联比特币地址的真实用户，自动收集更新以下类别的内容： <br/>
{平台上的用户名，即Bitcoin Talk论坛和Bitcoin-OTC mar-ketplace（来自论坛签名和数据库） <br/>
{由Casascius（https://www.casascius.com）创建的实物硬币，以及它们的比特币价值和状态 <br/>
{已知的骗子，通过自动识别具有重要意义的用户对Bitcoin-OTC和Bitcoin Talk信任系统的负面反馈。  <br/>
{证券交易所的股东（目前仅限于BitFunder）  <br/>
{开源数据库：https://blockchain.info/tags} <br/>
##### 新增更多的来源：如暗网的论坛/电报等社交工具


## 4  Grapher:图模块

包括：交易图/用户图/网络图   <br/>
Grapher以增量方式读取区块链数据库和集群文件，以分别生成交易图和用户图。 在交易图中，地址是节点，单个交易是边。在用户图中，用户（即集群）被表示为节点，而它们之间的聚合交易被表示为边。  <br/>
图数据库暂时采用[neo4j](https://www.w3cschool.cn/neo4j/)  <br/>
##### 新增的点： 增加对网络节点的测量

[实现参考](https://github.com/ayeowch/bitnodes)

基本思路：通过nodes seeds 找到邻居节点，通过ping-pong协议等去抓取网络节点的信息，获取ip后通过[geoip](https://geoip2.readthedocs.io/en/latest/#geoip2.models.ISP)获取ASN等号，其他区块链可以参考实现。


## 5   Classfier:分类器

分类器读取Grapher生成的交易图和用户图，然后继续使用特定注释自动标记单个地址和群集。 标签的示例包括：Bitcoin Talk和Bitcoin-OTC用户名，来自直接或联合采矿，与赌博站点，交易所，网络钱包，其他已知的BitcoinTalk或Bitcoin-OTC用户，赠品和捐赠地址的交易比例。 也有其他Tag，例如一次性地址，旧地址，新地址，空地址，骗子，矿工，股东，联邦调查局，丝绸之路，杀手级和恶意软件。  分类可以在整个区块链上全局进行，也可以选择性地在指定的列表上进行地址和感兴趣的集群。 结果存储在数据库中，并可进行增量更新。  <br/>
#####  采用的方法：聚类/决策树/或参考下联邦学习的方法（可以把前面的做好之后完成，本质是一个分类问题，稍微能够提升点准确率就是一个创新点） <br/>
[思路](https://mp.weixin.qq.com/s/vayPuQeI61kdpPH2uJwLiw)

## 6  Exporter：导出器

导出器允许以几种格式导出和过滤交易图和用户图（的一部分），并通过在此类图上找到简单路径（即没有重复节点的路径）来支持手动分析。 更准确地说，它可以导出发生在集群内部或源自集群的事务。 它也可以找到从一个地址到另一个地址，从一个地址到一个群集，从一个群集到一个地址的最短或所有简单路径，或者
在两个集群之间。   <br/> 
[Gephi](https://www.jianshu.com/p/86145943695a)
