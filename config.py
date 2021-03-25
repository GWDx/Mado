import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.session import Session

import time
import os


def writeFile(id, suffix, code):
    path = 'temp/' + id
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    
    now = time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))     
    fileName = path + '/' + str(now) + suffix
    if os.path.exists(fileName):
        raise NameError('Too Frequent')

    f = open(fileName, 'w', encoding='utf-8')
    f.write(code + "\n")
    f.close()
    return(fileName)


def runCMD(cmd):
    result = os.popen(cmd)
    ans = result.read().strip("\n")
    return(ans)

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:8080", # 填入 httpapi 服务运行的地址
        authKey="1234567890", # 填入 authKey
        account=2944791899, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)


rawHelp = [
    [1, "epy" , "ExecutePython"],
    [2, "ema" , "ExecuteMathematica"],
    [3, "help" , "帮助"],
    [4, "pip install" , "Python 库安装"]
]

help = '\n'.join(['(' + str(l[0]) + ') ' + l[1] + '  : ' + l[2] for l in rawHelp])


def regularQ(firstLine,full,kernel):
    if firstLine.find(kernel)<=0:
        return False
    left = firstLine.split(kernel)[0]
    right = firstLine[len(left):].split(' ')[0]
    return "execute".startswith(left) and full.startswith(right)


if __name__=='__main__':
    print(regularQ('epy','python','py'))