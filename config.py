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
    
    now = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))     
    fileName = path + '/' + str(now) + suffix
    if os.path.exists(fileName):
        raise NameError('Too Frequent')

    f = open(fileName, 'w', encoding='utf-8')
    f.write(code + "\n")
    f.close()
    return(fileName)


import subprocess

def runCMD(cmd):
    ret = subprocess.run(cmd, timeout = 15, encoding = "utf-8", shell=True,
                        stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    ans = ret.stdout.strip('\n')
    if ret.stderr != '':
        ans = '####\n' + ret.stderr.strip('\n') + '\n####\n' + ret.stdout
    if ret.returncode !=0 :
        ans = '>> returncode = ' + str(ret.returncode) + '\n' + ans
    if ans == '':
        ans = '>> returncode = ' + str(ret.returncode)
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
    [1, "epy" , "ExecutePython3"],
    [2-1, "ema [-t]" , "ExecuteMathematica 文本形式"],
    [2-2, "ema -p", "以图片格式返回"],
    [3, "pip install" , "Python 库安装"],
    [4, "help" , "帮助"] # ,
    # [5, "about", "关于"]
]

help = '\n'.join([str(l[0]) + '. ' + l[1] + '  : ' + l[2] for l in rawHelp])


def regularQ(firstLine,full,kernel):
    if firstLine.find(kernel)<=0:
        return False
    left = firstLine.split(kernel)[0]
    right = firstLine[len(left):].split(' ')[0]
    return "execute".startswith(left) and full.startswith(right)


if __name__=='__main__':
    # print(regularQ('epy','python','py'))
    ans = runCMD('python testPython.txt')
    print(ans)