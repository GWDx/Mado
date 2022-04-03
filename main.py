from graia.broadcast import Broadcast
from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import Friend, MiraiSession, Group, Member

from kernel import *
from initialize import *

import sys

debugMode = len(sys.argv) > 1


@broadcast.receiver("FriendMessage")
async def friend_message_listener(message: MessageChain, app: Ariadne, friend: Friend):
    command = normalize(message)
    result = kernel(command, str(friend.id))
    if result:
        try:
            await app.sendFriendMessage(friend, MessageChain.create([result]))
        except Exception as ex:
            print('## ', ex)
            await app.sendFriendMessage(friend, MessageChain.create([Plain(str(ex))]))


@broadcast.receiver('GroupMessage')
async def group_message_handler(message: MessageChain, app: Ariadne, group: Group, member: Member):
    command = normalize(message)
    result = kernel(command, f'{group.id}-{member.id}')
    if debugMode:
        print(result)
        return
    if result:
        try:
            await app.sendGroupMessage(group, MessageChain.create([result]))
        except Exception as ex:
            print('## ', ex)
            await app.sendGroupMessage(group, MessageChain.create([Plain(str(ex))]))


loop.run_until_complete(app.lifecycle())
