__author__ = 'Administrator'

#1 。 定义fib函数
#2. 声明接收指令的队列名rpc_queue
#3. 开始监听队列，收到消息后 调用fib函数
#4 把fib执行结果，发送回客户端指定的reply_to 队列
import subprocess
import pika
import time

# class CMDRpcServer(object):
#     def __init__(self):
#         credentials = pika.PlainCredentials('admin', 'admin123')
#         parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
#         self.connection = pika.BlockingConnection(parameters)
#         self.channel = self.connection.channel()  # 队列连接通道
#         self.channel.queue_declare(queue='rpc_queue2')
#
#
#     def run_cmd(self,cmd):
#         cmd_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         result = cmd_obj.stdout.read() + cmd_obj.stderr.read()
#
#         return result
#
#
#     def on_request(self,ch, method, props, body):
#         cmd = body.decode("utf-8")
#
#         print(" [.] run (%s)" % cmd)
#         response = self.run_cmd(cmd)
#
#         ch.basic_publish(exchange='',
#                          routing_key=props.reply_to,  # 队列
#                          properties=pika.BasicProperties(correlation_id= \
#                                                              props.correlation_id),
#                          body=response)
#
#         ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
#     def consume(self):
#         self.channel.basic_consume(self.on_request, queue='rpc_queue2')
#         print(" [x] Awaiting RPC requests")
#         self.channel.start_consuming()
#
#
#
# def run():
#     server = CMDRpcServer()
#     server.consume()
#
#
# if __name__ == '__main__':
#     run()


class CMDRpcServer(object):
    def __init__(self,rk_list):
        credentials = pika.PlainCredentials('admin', 'admin123')
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()  # 队列连接通道
        self.exchange = 'controller2server'
        queue_obj = self.channel.queue_declare(exclusive=True)  # 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        self.queue_name = queue_obj.method.queue
        for rk in rk_list:
            print("正在监听{}收到的数据...".format(rk))
            self.channel.queue_bind(exchange=self.exchange,
                               queue=self.queue_name,
                               routing_key=rk)  # 绑定队列到Exchange


    def run_cmd(self,cmd):
        cmd_obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = cmd_obj.stdout.read() + cmd_obj.stderr.read()
        return result


    def on_request(self,ch, method, props, body):
        """接收到controller的cmd，执行cmd并向controller返回结果"""
        cmd = body.decode("utf-8")

        print(" [.] run (%s)" % cmd)
        response = self.run_cmd(cmd)
        response = bytes("********************{}********************\n".format(props.message_id),encoding="utf-8") + response
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,  # 队列
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def consume(self):
        # self.channel.basic_consume(self.on_request, queue=self.queue_name,no_ack=True)
        self.channel.basic_consume(self.on_request, queue=self.queue_name)
        # print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


def run():
    # server_ip = ["1.1.1.1","2.2.2.2"]
    server_ip = input("listen to channel >>:").split(" ")
    server = CMDRpcServer(server_ip)
    server.consume()


if __name__ == '__main__':
    run()

