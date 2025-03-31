import discord
from .database.bookMarkDB import *


# search Bookmark
def searchLink(serverID, linkName):
    list = selectLink(serverID, linkName)

    embed = discord.Embed(title="링크 바로가기", color=0x6E17E3)
    if int(len(list)) == 0:
        text = '등록되어 있지 않습니다.'
        embed.add_field(name=text, value="", inline=False)
    else:
        embed.add_field(name=linkName, value=list[0], inline=False)

    return embed


# search All Bookmark
def searchAllLink(serverID):

    list, linkList = selectAllLink(serverID);

    embed = discord.Embed(title="링크 바로가기", color=0x6E17E3)
    if int(len(list)) == 0:
        text = '등록되어 있는 링크가 없습니다.'
        embed.add_field(name=text, value="", inline=False)
    else:
        for i in range(0, len(list)):
            linkName = str(list[i])
            embed.add_field(name=linkName, value="", inline=False)

            link = str(linkList[i])
            embed.add_field(name=link, value="", inline=False)

    return embed


# register Bookmark
def registerLink(serverID, text):

    if "[" not in text or "]" not in text:
        embed = discord.Embed(title="투표 생성", color=0xff0000)
        embed.add_field(name="양식에 맞게 입력 바랍니다.", value="", inline=False)
        embed.add_field(name="양식 : !투표생성 [북마크이름]북마크링크", value="", inline=False)
        return embed
    else:
        temp = text.split("[")
        linkName, link = temp[1].split("]")

    if "http://" not in link and "https://" not in link:
        embed = discord.Embed(title="북마크 오류", color=0xff0000)
        embed.add_field(name='정확한 링크를 입력해주세요', value='https:// or http://', inline=False)
        return embed

    else:
        embed = discord.Embed(title="링크 바로가기", color=0x6E17E3)
        if insertLink(serverID, linkName, link):
            embed.add_field(name='등록되었습니다', value="", inline=False)
        else:
            embed.add_field(name='이미 등록되어있습니다', value="", inline=False)

    return embed


# delete Bookmark
def deleteBookmark(serverID, linkName):

    embed = discord.Embed(title="북마크 삭제", color=0x6E17E3)
    if deleteLink(serverID, linkName):
        embed.add_field(name='삭제되었습니다.', value="", inline=False)
    else:
        embed.add_field(name='등록되어 있지 않습니다.', value="", inline=False)
        
    return embed


def deleteAllBookmark(serverID):
    embed = discord.Embed(title="링크 바로가기", color=0x6E17E3)
    if resetBookmark(serverID):
        embed.add_field(name='초기화 되었습니다.', value="", inline=False)
    else:
        embed.add_field(name='등록된 링크가 없습니다.', value="", inline=False)

    return embed
