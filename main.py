from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, Group, Member

from kernel import *
from initialize import *


@app.broadcast.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, app: Ariadne, friend: Friend):
    command = normalize(message)
    result = await kernel(command, str(friend.id))
    if result:
        try:
            await app.send_message(friend, MessageChain([result]))
        except Exception as ex:
            print('## ', ex)
            await app.send_message(friend, MessageChain([Plain(str(ex))]))


@app.broadcast.receiver('GroupMessage')
async def group_message_handler(message: MessageChain, app: Ariadne, group: Group, member: Member):
    command = normalize(message)
    result = await kernel(command, f'{group.id}-{member.id}')
    if debugMode:
        print(result)
        return
    if result:
        try:
            await app.send_message(group, MessageChain([result]))
        except Exception as ex:
            print('## ', ex)
            await app.send_message(group, MessageChain([Plain(str(ex))]))


app.launch_blocking()
