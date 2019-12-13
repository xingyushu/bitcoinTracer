
bitcoingraph_modify_version:
通过本地RPC的方式解析比特币数据成csv格式并导入到neo4j图数据库中 <br/>
#####  对源代码进行了相关修改，兼容自己的需求

[![Build Status](https://travis-ci.org/behas/bitcoingraph.svg?branch=master)](https://travis-ci.org/behas/bitcoingraph)

## 准备

### 比特币核心客户端的安装及配置

首先, 安装 Bitcoin Core (v.11.1),可以从 [source](https://github.com/bitcoin/bitcoin) 或者 [pre-compiled executable](https://bitcoin.org/en/download)，[京东云](https://github.com/jdcloud-bds/bds-btc)

安装之后可以使用 `bitcoind` (= 全节点), `bitcoin-qt` (= GUI 可选择不要), and `bitcoin-cli` (RPC command line interface)：

    bitcoind -printtoconsole

接着，修改配置文件bitcoin.conf(默认在/root/.bitcoin/下） [Bitcoin Core configuration file][bc_conf] 如下:

    # server=1 tells Bitcoin-QT to accept JSON-RPC commands.
    server=1

    # You must set rpcuser and rpcpassword to secure the JSON-RPC api
    rpcuser=your_rpcuser
    rpcpassword=your_rpcpass

    # How many seconds bitcoin will wait for a complete RPC HTTP request.
    # after the HTTP connection is established.
    rpctimeout=30

    # Listen for RPC connections on this TCP port:
    rpcport=8332

测试 JSON-RPC 接口是否能使用：

    curl --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }' -H 'content-type: text/plain;' http://your_rpcuser:your_rpcpass@localhost:8332/


开启比特币交易索引，不仅可以查询交易池里的交易还可以查询区块链上的交易：
可以在 `bitcoin.conf`里添加，或者启动时候添加参数

    txindex=1

...重启 Bitcoin core peer:

    bitcoind -reindex

通过获取任意交易ID并使用CURL发出以下请求去测试非钱包交易数据访问：

    curl --data-binary '{"jsonrpc": "1.0", "id":"curltest", "method": "getrawtransaction", "params": ["110ed92f558a1e3a94976ddea5c32f030670b5c58c3cc4d857ac14d7a1547a90", 1] }' -H 'content-type: text/plain;' http://your_rpcuser:your_rpcpass@localhost:8332/

最后，开启Bitcoin Core的HTTP REST接口，该接口使用以下参数启用：


    bitcoind -rest

测试是否能够使用：

    http://localhost:8332/rest/block/000000000000000e7ad69c72afc00dc4e05fc15ae3061c47d3591d07c09f2928.json


完成后配置成功 终止所有正在运行的比特币实例，并启动具有启用的REST接口的新后台守护程序：

    bitcoind -daemon -rest

#####  注意： ”bitcoind  > = 0.16.0的话需要对源码进行以下修改： 
在 bitcoingraph/bitcoingraph.py on line 53 getinfo ：
```
   getinfo()  ==> getcount()  本库已经修改完毕下载即可使用
```


### 库安装


    python --version

 > = python 3.4 即可


Now clone Bitcoingraph...

git clone https://github.com/xingyushu/bitcoinTracer.git  or  <br/>
    git clone https://github.com/behas/bitcoingraph.git (需要修改源码）


...测试并安装:

    cd bitcoingraph
    pip install -r requirements.txt
    py.test
    python setup.py install


### Mac OSX \

Running bitcoingraph on a Mac requires coreutils to be installed

    homebrew install coreutils


## 解析数据到图数据库（Neo4J）

bitcoingraph在Neo4J图形数据库实例中将带标记的图形的比特币交易存储为定向图形。 可以通过加载初始的区块链转储，如[Ron and Shamir]（https://eprint.iacr.org/2012/584.pdf）所述，对整个转储执行实体计算来引导数据库，把它运行成Neo4J实例。

### Step 1: Create transaction dump from blockchain

Bitcoingraph provides the `bcgraph-export` tool for exporting transactions in a given block range from the blockchain. The following command exports all transactions contained in block range 0 to 1000 using Neo4Js header format and separate CSV header files:

    bcgraph-export 0 1000 -u your_rpcuser -p your_rpcpass

The following CSV files are created (with separate header files):

* addresses.csv: sorted list of Bitcoin addressed  比特币地址的列表
* blocks.csv: list of blocks (hash, height, timestamp)  区块列表：哈希/高度/时间戳
* transactions.csv: list of transactions (hash, coinbase/non-coinbase)  交易列表：哈希/（创币/非创币）
* outputs.csv: list of transaction outputs (output key, id, value, script type)  交易输出数据（输出公钥，id，金额，脚本类型）
* rel_block_tx.csv: relationship between blocks and transactions (block_hash, tx_hash) 区块和交易的关系（区块哈希，交易哈希）
* rel_input.csv: relationship between transactions and transaction outputs (tx_hash, output key) 交易和交易输出的关系（交易哈希，输出key)
* rel_output_address.csv: relationship between outputs and addresses (output key, address)  交易输出和地址的关系(交易公钥，地址）
* rel_tx_output.csv: relationship of transactions & transaction outputs (tx_hash, output key) 交易和交易输出的关系（交易哈希，输出公钥）


### Step 2: Compute entities over transaction dump

The following command computes entities for a given blockchain data dump:

    bcgraph-compute-entities -i blocks_0_1000

Two additional files are created:

* entities.csv: list of entity identifiers (entity_id)  实体
* rel_address_entity.csv: assignment of addresses to entities (address, entity_id)  实体地址

########  blocks_0_1000  -  为导出的数据csv格式



### Step 3: Ingest pre-computed dump into Neo4J

Download and install [Neo4J][neo4j] community edition (>= 2.3.0):

    tar xvfz neo4j-community-2.3.0-unix.tar.gz
    export NEO4J_HOME=[PATH_TO_NEO4J_INSTALLATION]

Test Neo4J installation:

    $NEO4J_HOME/bin/neo4j start
    http://localhost:7474/


Install  and make sure is not running and pre-existing databases are removed:

    $NEO4J_HOME/bin/neo4j stop
    rm -rf $NEO4J_HOME/data/*


Switch back into the dump directory and create a new database using Neo4J's CSV importer tool:

    $NEO4J_HOME/bin/neo4j-import --into $NEO4J_HOME/data/graph.db \
    --nodes:Block blocks_header.csv,blocks.csv \
    --nodes:Transaction transactions_header.csv,transactions.csv \
    --nodes:Output outputs_header.csv,outputs.csv \
    --nodes:Address addresses_header.csv,addresses.csv \
    --nodes:Entity entities.csv \
    --relationships:CONTAINS rel_block_tx_header.csv,rel_block_tx.csv \
    --relationships:OUTPUT rel_tx_output_header.csv,rel_tx_output.csv \
    --relationships:INPUT rel_input_header.csv,rel_input.csv \
    --relationships:USES rel_output_address_header.csv,rel_output_address.csv \
    --relationships:BELONGS_TO rel_address_entity.csv


Then, start the Neo4J shell...:

    $NEO4J_HOME/bin/neo4j-shell -path $NEO4J_HOME/data

and create the following uniquness constraints:

    CREATE CONSTRAINT ON (a:Address) ASSERT a.address IS UNIQUE;

    CREATE CONSTRAINT ON (o:Output) ASSERT o.txid_n IS UNIQUE;


Finally start Neo4J

    $NEO4J_HOME/bin/neo4j start

![实现效果](https://github.com/xingyushu/bitcoinTracer/blob/master/images/neo4j1.PNG)

### Step 4: Enrich transaction graph with identity information

Some bitcoin addresses have associated public identity information. Bitcoingraph provides an example script which collects information from blockchain.info.

    utils/identity_information.py

The resulting CSV file can be imported into Neo4j with the Cypher statement:

    LOAD CSV WITH HEADERS FROM "file://<PATH>/identities.csv" AS row
    MERGE (a:Address {address: row.address})
    CREATE a-[:HAS]->(i:Identity
      {name: row.tag, link: row.link, source: "https://blockchain.info/"})


### Step 5: Install Neo4J entity computation plugin

Clone the git repository and compile from source. This requires Maven and Java JDK to be installed.

    git clone https://github.com/romankarl/entity-plugin.git
    cd entity-plugin
    mvn package

Copy the JAR package into Neo4j's plugin directory.

    service neo4j-service stop
    cp target/entities-plugin-0.0.1-SNAPSHOT.jar $NEO4J_HOME/plugins/
    service neo4j-service start



### Step 6: Enable synchronization with Bitcoin block chain

Bitcoingraph provides a synchronisation script, which reads blocks from bitcoind and writes them into Neo4j. It is intended to be called by a cron job which runs daily or more frequent. For performance reasons it is no substitution for steps 1-3.

    bcgraph-synchronize -s localhost -u RPC_USER -p RPC_PASS -S localhost -U NEO4J_USER -P NEO4J_PASS --rest

