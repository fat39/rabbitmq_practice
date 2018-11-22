# 一、要求
```
rabbitmq练习 可以对指定机器异步的执行多个命令
例子：
>>:run ""df -h"" --hosts 192.168.3.55 10.4.3.4
task id: 45334
>>: check_task 45334
>>:     注意，每执行一条命令，即立刻生成一个任务ID,不需等待结果返回，通过命令check_task TASK_ID来得到任务结果 "
```

# 二、使用说明
1.controller 控制端  
	入口：bin/controller  
2.server 服务器端  
	入口：server.py  
	
# 三、目录结构
```
│  .gitignore
│  README.md
│
├─controller                             # 控制端
│  ├─bin
│  │      controller.py                                 # server端主入口
│  │
│  ├─conf
│  │  │  settings.py
│  │  │
│  │  └─__pycache__
│  │          settings.cpython-36.pyc
│  │
│  ├─lib
│  │  │  logger.py
│  │  │
│  │  └─__pycache__
│  │          logger.cpython-36.pyc
│  │
│  ├─log
│  │  │  cmd_history.log                                    # cmd操作记录
│  │  │
│  │  └─cmd_result                                          # cmd返回的结果
│  │          584d9d1e-10bf-4366-9f8b-2523b6175800
│  │          59121afd-1740-4a5c-8a1a-5c3c491a4da7
│  │          8e6962a0-221e-4107-a826-3836177f47d3
│  │          9afc64bf-fe18-4bf3-ac91-7e21235acb3e
│  │
│  └─src
│      │  core.py                                          # 主逻辑
│      │
│      └─__pycache__
│              core.cpython-36.pyc
│
└─server                               # server端，放置在各服务器
        server.py
```

# 四、使用
```
######################## server1 ########################
listen to channel >>:1.1.1.1
正在监听1.1.1.1收到的数据...
 [.] run (dir)

 ######################## server2 ########################
listen to channel >>:2.2.2.2
正在监听2.2.2.2收到的数据...
 [.] run (dir)
 [.] run (ipconfig)

 ######################## controller ########################
 C:\Python\Python36\python.exe D:/Python相关/python_project/老男孩/rabbitmq/rabbitmq_practice/controller/bin/controller.py
>>:run ""dir"" --hosts 1.1.1.1 2.2.2.2
d91bd277-b1fd-4772-8f06-bdc4e3dadec2
>>:check_task d91bd277-b1fd-4772-8f06-bdc4e3dadec2
********************1.1.1.1********************
 驱动器 D 中的卷是 文档

 卷的序列号是 000F-3273



 D:\Python相关\python_project\老男孩\rabbitmq\rabbitmq_practice\server 的目录



2018/03/29  17:16    <DIR>          .

2018/03/29  17:16    <DIR>          ..

2018/03/29  17:03             4,137 server.py

               1 个文件          4,137 字节

               2 个目录 50,766,532,608 可用字节

********************2.2.2.2********************
 驱动器 D 中的卷是 文档

 卷的序列号是 000F-3273



 D:\Python相关\python_project\老男孩\rabbitmq\rabbitmq_practice\server 的目录



2018/03/29  17:16    <DIR>          .

2018/03/29  17:16    <DIR>          ..

2018/03/29  17:03             4,137 server.py

               1 个文件          4,137 字节

               2 个目录 50,766,532,608 可用字节

>>:run ""ipconfig"" --hosts 2.2.2.2
e82eab10-086d-4b40-9013-17eddf2401b8
>>:check_task e82eab10-086d-4b40-9013-17eddf2401b8
********************2.2.2.2********************


Windows IP 配置





以太网适配器 以太网:



   连接特定的 DNS 后缀 . . . . . . . :

   本地链接 IPv6 地址. . . . . . . . : fe80::65f0:66c8:1581:d22c%15

   IPv4 地址 . . . . . . . . . . . . : 10.132.11.140

   子网掩码  . . . . . . . . . . . . : 255.255.255.0

   默认网关. . . . . . . . . . . . . :



无线局域网适配器 本地连接* 2:



   媒体状态  . . . . . . . . . . . . : 媒体已断开连接

   连接特定的 DNS 后缀 . . . . . . . :



以太网适配器 VMware Network Adapter VMnet1:



   连接特定的 DNS 后缀 . . . . . . . :

   本地链接 IPv6 地址. . . . . . . . : fe80::9dec:4a2a:993d:32f7%12

   IPv4 地址 . . . . . . . . . . . . : 1.1.1.1

   子网掩码  . . . . . . . . . . . . : 255.255.255.0

   默认网关. . . . . . . . . . . . . :



以太网适配器 VMware Network Adapter VMnet8:



   连接特定的 DNS 后缀 . . . . . . . :

   本地链接 IPv6 地址. . . . . . . . : fe80::b1e0:7bac:9d93:9701%9

   IPv4 地址 . . . . . . . . . . . . : 192.168.93.1

   子网掩码  . . . . . . . . . . . . : 255.255.255.0

   默认网关. . . . . . . . . . . . . :



无线局域网适配器 WLAN:



   连接特定的 DNS 后缀 . . . . . . . :

   本地链接 IPv6 地址. . . . . . . . : fe80::c464:e8d7:3b22:c5fb%17

   IPv4 地址 . . . . . . . . . . . . : 27.39.67.188

   子网掩码  . . . . . . . . . . . . : 255.255.255.0

   默认网关. . . . . . . . . . . . . : fe80::1%17

                                       27.39.67.1



隧道适配器 本地连接* 11:



   媒体状态  . . . . . . . . . . . . : 媒体已断开连接

   连接特定的 DNS 后缀 . . . . . . . :

>>:
```
