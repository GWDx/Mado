import asyncio
from graia.broadcast import Broadcast
from graia.application.session import Session
from graia.application import GraiaMiraiApplication


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
    ["1", "epy" , "ExecutePython3"],
    ["2-1", "ema" , "ExecuteMathematica"],
    ["2-2", "ema -p ", "以图片格式返回"],
    ["3", "pip install" , "Python 库安装"],
    ["4", "esh", "ExecuteBash（需要权限）"],
    ["5", "help" , "帮助"] # ,
    # ["6", "about", "关于"]
]

help = '\n'.join(['[' + l[0] + '] ' + l[1] + '  : ' + l[2] for l in rawHelp])


if __name__=='__main__':
    print(help)