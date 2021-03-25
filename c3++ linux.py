import asyncio
from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain
from graia.application.session import Session
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend

import time
import os
import re
from config import *


@bcc.receiver("FriendMessage")
async def friend_message_listenerasync(
    message : MessageChain,
    app: GraiaMiraiApplication, 
    friend: Friend
):
    command = message.asDisplay()
    firstLine = command.split("\n")[0].lower()
    
    try:
        # ExecutePython
        if regularQ(firstLine,"python","py"):
            options = firstLine[(firstLine + ' ').find(' '):] # options
            code = command[(len(firstLine)+1):]
            fileName = writeFile(friend.id, ".py", code)
            ans = runCMD('python3 "' + fileName + '"').strip("\n")
            if ans != "":
                await app.sendFriendMessage(friend, MessageChain.create([Plain(ans)]))
        
        # ExecuteMathematica
        elif regularQ(firstLine,"mathematica","ma"):
            options = firstLine[(firstLine + ' ').find(' '):] # options
            code = "\n".join(command.split("\n")[1::])
            fileName = writeFile(friend.id, ".wl", code)
            ans = runCMD('/opt/vlab/mathematica-12/Executables/wolframscript -print all -f "' + fileName + '"').strip("\n")
            if ans != "":
                await app.sendFriendMessage(friend, MessageChain.create([Plain(ans)]))
        
        # help
        elif firstLine.startswith("help"):
            await app.sendFriendMessage(friend, MessageChain.create([Plain(help)]))
        
        # pip
        elif firstLine.startswith("pip "):
            firstLine = command.split("\n")[1]
            ans = runCMD(firstLine)
            await app.sendFriendMessage(friend, MessageChain.create([Plain(ans + "end")]))
    except:
        print('!! Error')
        await app.sendFriendMessage(friend, MessageChain.create([Plain("Error")]))

app.launch_blocking()
