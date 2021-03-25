from graia.application import GraiaMiraiApplication
from graia.application.message.elements.internal import Plain
from graia.application.message.chain import MessageChain
from graia.application.friend import Friend
from graia.application.group import Group, Member

from config import *
from kernel import *


@bcc.receiver("FriendMessage")
async def friend_message_listenerasync(
    message : MessageChain,
    app: GraiaMiraiApplication, 
    friend: Friend
):
    command = message.asDisplay()
    ans = kernel(command, str(friend.id))

    if ans != "":
        await app.sendFriendMessage(friend, MessageChain.create([Plain(ans)]))


@bcc.receiver("GroupMessage")
async def group_message_handler(
    message : MessageChain,
    app: GraiaMiraiApplication, 
    group: Group, member: Member
):
    command = message.asDisplay()
    ans = kernel(command, str(group.id) + ' ' + str(member.id))

    if ans != "":
        await app.sendGroupMessage(group, MessageChain.create([Plain(ans)]))


app.launch_blocking()
