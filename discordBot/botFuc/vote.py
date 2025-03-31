import discord
from .HashFuc import hashFuc
from .database.voteDB import *
from discord.ui import Button, View


# createVote
def createVote(serverID, userID, text):
    if "[" not in text or "]" not in text:
        embed = discord.Embed(title="투표 생성", color=0xff0000)
        embed.add_field(name="양식에 맞게 입력 바랍니다.", value="", inline=False)
        embed.add_field(name="양식 : !투표생성 [투표명]항목1 항목2 항목3 ...", value="", inline=False)
        return embed
    else:
        temp = text.split("[")
        voteName, votingItems = temp[1].split("]")

        embed = discord.Embed(title='투표 만들기', color=0x6E17E3)
        if insertVoteList(serverID, userID, voteName, votingItems):
            embed.add_field(name="투표가 등록되었습니다.", value="", inline=False)
        else:
            embed.add_field(name="이미 진행중인 투표입니다.", value="", inline=False)

        return embed


# findAllVote
def voteAllList(serverID):
    voteList = selectAllVote(serverID)

    embed = discord.Embed(title='투표목록', color=0x6E17E3)

    if int(len(voteList)) == 0:
        embed.add_field(name="현재 진행중인 투표가 없습니다.", value="", inline=False)

    else:
        for value in voteList:
            embed.add_field(name=value, value="", inline=False)

    return embed


# finishVote
def finishVote(serverID, userID, voteName):
    check = checkVoteList(serverID, voteName)
    if check:
        if selectUserIDFromVote(serverID, userID, voteName):
            embed = voteStatus(serverID, voteName)
            deleteVote(serverID, voteName)
        else:
            embed = discord.Embed(title='투표 종료', color=0xff0000)
            embed.add_field(name="투표 만든 사람만 종료 가능합니다.", value="", inline=False)
    else:
        embed = discord.Embed(title='진행중인 투표가 없습니다.', color=0xff0000)
        embed.add_field(name="", value="", inline=False)

    return embed


# vote Button
class VoteButton:
    def __init__(self, button, voteName, item):
        self.button = button
        self.voteName = voteName
        self.item = item
        button.callback = self.button_callback

    async def button_callback(self: discord.ui.button, interaction):
        serverID = hashFuc(str(interaction.guild.id))
        userID = hashFuc(str(interaction.user.id))
        check = checkVoteList(serverID, self.voteName)
        if not check:
            await interaction.response.send_message("종료된 투표입니다.")
        else:
            if voting(serverID, userID, self.voteName, self.item):
                await interaction.response.send_message(interaction.user.nick + "님 투표 완료")
            else:
                await interaction.response.send_message(interaction.user.nick + "님은 이미 투표를 하셨습니다.")


# vote
def vote(serverID, voteName):
    voteItemValue = selectVotingItems(serverID, voteName)

    button = []
    view = View()
    index = 0
    for item in voteItemValue:
        button.append(Button(label=item, style=discord.ButtonStyle.green))
        VoteButton(button[index], voteName, item)
        view.add_item(button[index])
        index += 1

    return view


# voteStatus
def voteStatus(serverID, voteName):
    items, counts = status(serverID, voteName)
    print(items)
    print(counts)

    if len(items) == 0:
        embed = discord.Embed(title="투표 현황", color=0xff0000)
        embed.add_field(name="진행 중인 투표가 없습니다.", value="", inline=False)
    else:
        embed = discord.Embed(title="투표 현황", color=0x00FF00)
        for item, count in zip(items, counts):
            embed.add_field(name=item + ": " + str(count), value="", inline=False)

    return embed
