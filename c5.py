from graia.application import GraiaMiraiApplication
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.group import Group, Member
from graia.application.message.elements.internal import Plain

from config import *
from kernel import *


@bcc.receiver("FriendMessage")
async def friend_message_listenerasync(
    message : MessageChain,
    app: GraiaMiraiApplication, 
    friend: Friend
):
    command = message.asDisplay()
    result = kernel(command, str(friend.id))
    try:
        await app.sendFriendMessage(friend, MessageChain.create([result]))
    except Exception as ex:
        print('## ', ex)
        await app.sendFriendMessage(friend, MessageChain.create([Plain(str(ex))]))
       

@bcc.receiver("GroupMessage")
async def group_message_handler(
    message : MessageChain,
    app: GraiaMiraiApplication, 
    group: Group, member: Member
):
    command = message.asDisplay()
    result = kernel(command, str(group.id) + '-' + str(member.id))
    try:
        await app.sendGroupMessage(group, MessageChain.create([result]))
    except Exception as ex:
        print('## ', ex)
        await app.sendGroupMessage(group, MessageChain.create([Plain(str(ex))]))
        
app.launch_blocking()
