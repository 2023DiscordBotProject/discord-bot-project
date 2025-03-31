import discord
import random


async def team(msg):
    # 명령어 총 명수, 팀수, 팀당 인원수 순으로 입력받고 message에 list형식으로 저장되는 코드
    message = msg.message.content
    message = message.split(' ')
    await msg.send("test")
    embed = discord.Embed(title="", color=0x6E17E3)
    if (len(message) != 4):
        embed.add_field(name="", value="양식을 지켜주세요.", inline=False)

    elif (int(message[3]) * int(message[2]) > int(message[1])):
        embed.add_field(name="", value='총 인원수 보다 많은 인원이 입력되었습니다', inline=False)

    else:
        team_size = message[3]
        team_count = message[2]

        # list에 있는 목록을 무작위로 섞는코드
        list = []
        for i in range(1, int(message[1]) + 1):
            list.append(i)
        random.shuffle(list)

        # 팀수 만큼 반복시켜 만들어진 팀을 embed에 저장하는 코드
        for i in range(0, int(team_count)):
            # 입력받은 명수를 기준으로 목록 인덱스 범위를 구하는 코드
            start_index = i * int(team_size)
            end_index = i * int(team_size) + int(team_size)

            # i + 1 번째 팀에 들어가는 목록을 plyer에 저장하는 코드
            player = ""
            for j in range(start_index, end_index):
                if (j == end_index - 1):
                    player += f"{list[j]}"
                else:
                    player += f"{list[j]}, "

            embed.add_field(name="", value=f'{i + 1}조 : {player}', inline=False)

    return embed


def choice(msg):
    # 명령어 총 가지수, 뽑을 개수 순으로 입력 받고 message에 list 형식 으로 저장 되는 코드
    message = msg.message.content
    message = message.split(' ')

    embed = discord.Embed(title="", color=0x6E17E3)
    if (len(message) == 3):
        list = []
        for i in range(1, int(message[1]) + 1):
            list.append(i)
        random.shuffle(list)

        count = int(message[2])  # 무작위로 뽑을 개수

        if (count > len(list)):
            embed.add_field(name="", value="총 가짓수 보다 많습니다.", inline=False)

        else:
            player = ""
            embed.add_field(name="", value=f'{count}가지을 뽑았습니다', inline=False)
            for i in range(0, count):
                if (i == count - 1):
                    player += f"{list[i]}"
                else:
                    player += f"{list[i]}, "

            embed.add_field(name="", value=f"{player}", inline=False)

    else:
        embed.add_field(name="", value="양식을 지켜주세요.", inline=False)

    return embed
