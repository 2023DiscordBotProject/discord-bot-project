import random
import discord
import sqlite3

con = sqlite3.connect('./Database.db')

cur = con.cursor()
# cur.execute("DROP table if exists NumberBaseball")
cur.execute("CREATE TABLE if not exists NumberBaseball(serverID text, userID text, num text, tryCount Integer, "
            "primary key(serverID, userID)) ;")

global strike
global ball
global out


def numberBaseBallRole():
    embed = discord.Embed(title="숫자야구 게임 규칙", color=0x6E17E3)
    embed.add_field(name="0~9까지의 숫자로 이루어진 3자리를 숫자를 맞추는 게임입니다.", value="", inline=False)
    embed.add_field(name="컴퓨터가 랜덤으로 중복없이 3자리 숫자를 생성합니다.", value="", inline=False)
    embed.add_field(name="숫자와 자리의 위치가 맞으면 스트라이크!", value="", inline=False)
    embed.add_field(name="숫자만 맞으면 볼, 전부 틀리면 아웃입니다.", value="", inline=False)
    embed.add_field(name="이 과정을 통하여 3자리 숫자를 맞추면 됩니다.", value="", inline=False)
    embed.add_field(name="게임 시작을 원하시면 !게임시작 을 입력해주세요.", value="", inline=False)
    return embed


def checkRegister(serverID, userID):
    cur.execute("SELECT userID FROM NumberBaseball WHERE serverID=? and userID=?", (serverID, userID))

    list = []
    for row in cur:
        list.append(row)

    return list


def registerNumberBaseball(serverID, userID):
    list = checkRegister(serverID, userID)

    embed = discord.Embed(title="숫자야구", color=0x6E17E3)
    if int(len(list)) == 0:
        num = (random.sample(range(0, 9), 3))
        number = str(num[0]) + str(num[1]) + str(num[2])
        cur.execute("INSERT INTO NumberBaseball Values(?, ?, ?, ?)", (str(serverID), str(userID), number, 1))
        con.commit()
        embed.add_field(name='중복 되지 않도록 숫자를 3개 입력해주세요', value="", inline=False)
        embed.add_field(name='입력 예시 !정답 123', value="", inline=False)
    else:
        embed.add_field(name='진행 중인 게임이 있습니다.', value="", inline=False)

    return embed


def stopNumberBaseball(serverID, userID):
    list = checkRegister(serverID, userID)

    embed = discord.Embed(title="숫자야구", color=0x6E17E3)

    if int(len(list)) == 0:
        embed.add_field(name='진행 중인 게임이 없습니다.', value='', inline=False)
    else:
        cur.execute('DELETE FROM NumberBaseball WHERE serverID=? and userID=?', (serverID, userID))
        con.commit()

        list = checkRegister(serverID, userID)

        if int(len(list)) == 0:
            embed.add_field(name='게임이 종료되었습니다.', value='', inline=False)
        else:
            embed.add_field(name='Error', value='', inline=False)

    return embed


def checkNum(index, num):
    global strike
    global ball
    global out

    if num != -1 and num == index:
        strike = strike + 1
    elif num != -1 and num != index:
        ball = ball + 1
    else:
        out = out + 1


def answer(serverID, userID, text):
    list = checkRegister(serverID, userID)

    if int(len(list)) == 0:
        embed = discord.Embed(title='숫자야구게임', color=0x6E17E3)
        message = '진행 중인 게임이 없습니다.'
        embed.add_field(name=message, value='', inline=False)
        return embed

    global strike
    global ball
    global out

    value = [-1] * 10

    cur.execute("SELECT num FROM NumberBaseball WHERE serverID=? and userID=?", (serverID, userID))

    for row in cur:
        num = str(row[0])

    value[int(num[0])] = 0
    value[int(num[1])] = 1
    value[int(num[2])] = 2

    strike = 0
    ball = 0
    out = 0

    answerNum = text

    if len(answerNum) > 3:
        embed = discord.Embed(title='숫자 3자리만 입력해주세요', colour=discord.Colour.red())
        return embed

    try:
        for i in range(0, 3):
            temp = int(answerNum[i])
            checkNum(i, value[temp])

    except:
        embed = discord.Embed(title='숫자 3자리만 입력해주세요', colour=discord.Colour.red())
        return embed

    cur.execute("SELECT tryCount FROM NumberBaseball WHERE serverID=? and userID=?", (serverID, userID))

    for row in cur:
        count = row[0]

    if strike == 3:
        embed = discord.Embed(title='축하합니다~', color=0x6E17E3)
        message = str(count) + '번만에 맞추셨습니다.'
        embed.add_field(name=message, value="", inline=False)

        cur.execute('DELETE FROM NumberBaseball WHERE serverID=? and userID=?', (serverID, userID))
        con.commit()

    else:
        embed = discord.Embed(title=str(count) + " try", color=0x6E17E3)

    if strike != 0 and strike != 3:
        embed.add_field(name=str(strike) + "Strike", value="", inline=False)
    if ball != 0:
        embed.add_field(name=str(ball) + "Ball", value="", inline=False)
    if out != 0:
        embed.add_field(name=str(out) + "out", value="", inline=False)

    count = count + 1
    cur.execute("UPDATE NumberBaseball set tryCount=? WHERE serverID=? and userID=?", (count, serverID, userID))
    con.commit()

    return embed