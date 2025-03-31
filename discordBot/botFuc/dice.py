import random
import discord
from discord.ext import commands

#-----------------------------------------------------------------------------------------------------------------------


##### 기본 코드


TOKEN = ""
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


#-----------------------------------------------------------------------------------------------------------------------


##### 주사위 코드 : 1부터 6까지의 수 중 무작위로 숫자 하나 출력


@bot.command()
async def dice(ctx):
    Color = discord.Colour.greyple()
    dic = {1: ":one:", 2: ":two:", 3: ":three:", 4: ":four:", 5: ":five:", 6: ":six:"}
    # 1부터 6까지의 수 중 무작위로 선택
    result = dic[random.randint(1, 6)]
    # embed를 활용하여 결과 출력
    embed = discord.Embed(title="주사위 결과", description=result, color=Color)
    await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


##### 주사위대결 코드 : 사용자와 봇 간의 주사위 눈 대소 비교를 통해 대결 결과를 출력


@bot.command()
async def diceBattle(ctx):
    # 1부터 6까지의 수 중 사용자의 수와 봇의 수를 무작위로 선택
    bot = random.randint(1, 6)
    me = random.randint(1, 6)
    # 사용자의 수와 봇의 수의 대소 비교를 통해 출력값 결정
    if me > bot:
        result = "Win!!!"
        Color = discord.Colour.blue()
    elif me == bot:
        result = "Draw~~~"
        Color = discord.Colour.yellow()
    else:
        result = "Lose..."
        Color = discord.Colour.red()
    # embed를 활용하여 결과 출력
    embed = discord.Embed(title="주사위 대결 결과", description="", color=Color)
    embed.add_field(name=ctx.author.name + "의 :game_die: : " + str(me), value="", inline=False)
    embed.add_field(name="\"봇 이름\"의 :game_die: : " + str(bot), value="", inline=False)
    embed.add_field(name=result, value="", inline=False)
    await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------