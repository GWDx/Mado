from graia.broadcast import Broadcast
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, MiraiSession

import asyncio


# 过滤输入，图片解释为 MMA 格式
def normalize(message):
    try:
        valid = []
        for e in list(message)[1:]:
            if 'Plain' in str(e.type):
                valid.append(e)
            if 'Image' in str(e.type):
                valid.append(Plain(f'Import[{e.url}]'))
        ans = MessageChain.create(valid).asDisplay()

    except:
        ans = message.asDisplay()
        # raise RuntimeError('Interpret Error')

    return ans


loop = asyncio.get_event_loop()

broadcast = Broadcast(loop=loop)

app = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        host="http://localhost:8080",  # 填入 HTTP API 服务运行的地址
        verify_key="1234567890",  # 填入 verifyKey
        account=2944791899,  # 你的机器人的 qq 号
    ))

help = '''
[1] epy : ExecutePython3
[2-1] ema : ExecuteMathematica
[2-2] ema -p : 以 PNG 格式返回
[3] ecp : ExecuteCpp
[4] ejs : ExecuteJS
[5] erb : ExecuteRB
[6] pip install : Python 库安装
[7] help : 帮助
项目地址 : https://github.com/GWDx/Mado
'''

if __name__ == '__main__':
    print(help)
