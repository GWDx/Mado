from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.message.elements.internal import Plain

from kernel import *
from initialize import *

import sys

debugMode = len(sys.argv) > 1


@bcc.receiver('FriendMessage')
async def friend_message_listenerasync(message: MessageChain, app: GraiaMiraiApplication, friend: Friend):
    command = normalize(message)
    result = kernel(command, str(friend.id))
    if result:
        try:
            await app.sendFriendMessage(friend, MessageChain.create([result]))
        except Exception as ex:
            print('## ', ex)
            await app.sendFriendMessage(friend, MessageChain.create([Plain(str(ex))]))


@bcc.receiver('GroupMessage')
async def group_message_handler(message: MessageChain, app: GraiaMiraiApplication, group: Group, member: Member):
    if debugMode:
        return
    command = normalize(message)
    result = kernel(command, f'{group.id}-{member.id}')
    if result:
        try:
            await app.sendGroupMessage(group, MessageChain.create([result]))
        except Exception as ex:
            print('## ', ex)
            await app.sendGroupMessage(group, MessageChain.create([Plain(str(ex))]))


app.launch_blocking()
