#task_worker.py
import time, sys, queue
from multiprocessing.managers import BaseManager
#创建QueueManager
class QueueManager(BaseManager):
    pass
#该Manager从网络上获取Queue 因此只使用名字注册
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
#连接到运行task_master的机器 Server (127.0.0.0是本机地址 使用时应改掉)
server_addr = '127.0.0.1'
print('Try to connect to server %s...' %server_addr)
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
m.connect()
#获取Queue对象
task = m.get_task_queue()
result = m.get_result_queue()
#从task_queue获取任务 记过写入result_queue
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('we get %s' %n)
        print('now we calculate %s * %s' % (n, n))
        r = n * n
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task_queue is empty, all work have done')

print('worker quit')