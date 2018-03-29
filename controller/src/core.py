# -*- coding:utf-8 -*-

__author__ = 'Administrator'

# 1.声明一个队列，作为reply_to返回消息结果的队列
# 2.  发消息到队列，消息里带一个唯一标识符uid，reply_to
# 3.  监听reply_to 的队列，直到有结果
import re
import queue
import pika
import uuid
from threading import Thread
import os
from conf import settings
from lib import logger

# class CMDRpcClient(object):
#     def __init__(self):
#         credentials = pika.PlainCredentials('admin', 'admin123')
#         parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
#         self.connection = pika.BlockingConnection(parameters)
#         self.channel = self.connection.channel()
#
#         queue_obj = self.channel.queue_declare(exclusive=True)
#         self.callback_queue = queue_obj.method.queue #命令的执行结果的queue
#
#         #声明要监听callback_queue
#         self.channel.basic_consume(self.on_response, no_ack=True,
#                                    queue=self.callback_queue)
#
#     def on_response(self, ch, method, props, body):
#         """
#         收到服务器端命令结果后执行这个函数
#         :param ch:
#         :param method:
#         :param props:
#         :param body:
#         :return:
#         """
#         if self.corr_id == props.correlation_id:
#             self.response = body.decode("gbk") #把执行结果赋值给Response
#
#     def call(self, n):
#         self.response = None
#         self.corr_id = str(uuid.uuid4()) #唯一标识符号
#         self.channel.basic_publish(exchange='',
#                                    routing_key='rpc_queue2',
#                                    properties=pika.BasicProperties(
#                                          reply_to = self.callback_queue,
#                                          correlation_id = self.corr_id,
#                                          ),
#                                    body=str(n))
#
#
#         while self.response is None:
#             self.connection.process_data_events()  #检测监听的队列里有没有新消息，如果有，收，如果没有，返回None
#             #检测有没有要发送的新指令
#         return self.response
#
#
# def run():
#     cmd_rpc = CMDRpcClient()
#     while True:
#         cmd = input(">>:")
#         if not cmd:continue
#         response = cmd_rpc.call(cmd)
#         print(response)

log_type = "cmd_history"  # 系统日志记录到文件中
system_logger = logger.logger(log_type)
# system_logger.info("")  # 用法


class CMDRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('admin', 'admin123')
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.exchange = 'controller2server'

        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

        queue_obj = self.channel.queue_declare(exclusive=True)  # 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        self.callback_queue = queue_obj.method.queue #命令的执行结果的queue

        # 声明要监听callback_queue
        self.channel.basic_consume(self.on_response, no_ack=True,queue=self.callback_queue)
        Thread(target=self.channel.start_consuming).start()

    def on_response(self, ch, method, props, body):
        """
        收到服务器端命令结果后执行这个函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            cmd_result_path = os.path.join(settings.CMD_RESULT["path"], props.correlation_id)
            with open(cmd_result_path,"a") as f:
                f.write(body.decode("gbk"))

    def call(self, rk_list,cmd):
        self.corr_id = str(uuid.uuid4()) #唯一标识符号
        for rk in rk_list:
            self.channel.basic_publish(exchange=self.exchange,
                                       routing_key=rk,
                                       properties=pika.BasicProperties(
                                           reply_to = self.callback_queue,
                                           correlation_id = self.corr_id,
                                           message_id=rk,
                                           ),
                                       body=cmd
                                       )
        print(self.corr_id)

    def run(self,allcmd):
        # 语法：allcmd = ""df -h"" --hosts 192.168.3.55 10.4.3.4
        re_allcmd = re.compile("^\"\"(.+)\"\" (.+?) (.+)$")
        cmd,option,rest_str = re_allcmd.findall(allcmd)[0]

        if option == "--hosts":
            host_list = rest_str.split(" ")
            self.call(host_list,cmd)
        else:
            print("run命令暂时不支持{}".format(option))

    def check_task(self,allcmd):
        '''语法：check_task xxx'''
        if len(allcmd.split())>1:
            print("命令格式错误，应为:check_task xxxxx")
        else:
            cmd_result_path = os.path.join(settings.CMD_RESULT["path"],allcmd)
            if os.path.isfile(cmd_result_path):
                with open(cmd_result_path,"r") as f:
                    for line in f:
                        print(line.rstrip())
            else:
                print("无返回结果")

    def execute(self,myinput):
        """
        run ""df -h"" --hosts 192.168.3.55 10.4.3.4
        check_task xxx
        :param myinput:
        :return:
        """
        try:
            action,allcmd = myinput.split(" ",1)
            if hasattr(self,action):
                func = getattr(self,action)
                func(allcmd)
                system_logger.info(myinput)
            else:  # 找不到该方法，则不支持
                print("不支持该命令")
        except Exception as e:
            print("命令格式错误")


def run():
    cmd_rpc = CMDRpcClient()
    while True:
        myinput = input(">>:").strip()
        if not myinput:continue
        cmd_rpc.execute(myinput)


if __name__ == '__main__':
    run()
