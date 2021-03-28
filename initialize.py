from graia.broadcast import Broadcast
from graia.application.session import Session
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain

import asyncio


# 过滤输入，图片解释为 MMA 格式
def normalize(message):
    try:
        valid = []
        for e in list(message)[1:]:
            if 'Plain' in str(e.type):
                valid.append(e)
            if 'Image' in str(e.type):
                valid.append(Plain('Import["' + str(e.url) + '"]'))
        ans = MessageChain.create(valid).asDisplay()
    
    except:
        ans = message.asDisplay()
        # raise RuntimeError('Interpret Error')
    
    return ans


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


help = '''
[1] epy : ExecutePython3
[2-1] ema : ExecuteMathematica
[2-2] ema -p : 以 PNG 格式返回
[3] pip install : Python 库安装
[4] esh : ExecuteBash（需要权限）
[5] help : 帮助
项目地址 : https://github.com/GWDx/mado
'''


if __name__=='__main__':
    print(help)