import botFuc
import asyncio
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv(dotenv_path=".env")
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('로그인중입니다.')
    print(f"봇={bot.user.name}로 연결중")
    print('연결이 완료되었습니다.')
    await bot.change_presence(status=discord.Status.online, activity=None)


#################################################################################

@bot.command()
async def 명령어(ctx, *, text):
    embed = botFuc.commandList(text)

    await ctx.send(embed=embed)


#################################################################################

# 특정 자격증의 시험일정을 알려주는 코드
@bot.command()
async def 자격증일정(msg):
    embed = discord.Embed(title="", color=0x6E17E3)
    embed.add_field(name="", value="잠시만 기다려 주세요.", inline=False)
    await msg.send(embed=embed)

    embed1 = botFuc.certificate_date(msg)

    for i in range(len(embed1)):
        embed = embed1[i]
        await msg.send(embed=embed)


#################################################################################

# 학점 계산기 코드 : 전공, 교양, 일선 순으로 학점을 입력 받아 계산하여 DM을 통해 성적표 고지
@bot.command()
async def 학점계산기(ctx):
    # 사용자 일치 여부 판별 함수
    def check_auth(m):
        return m.author == ctx.author

    embed = discord.Embed(title="", color=discord.Colour.light_grey())
    embed.add_field(name="", value="수강한 과목 수를 적어주세요.\n 30초동안 입력이 없으면 종료됩니다.", inline=False)
    await ctx.send(embed=embed)

    try:
        count = await bot.wait_for("message", check=check_auth, timeout=30.0)
        count = count.content
        # 입력 값이 숫자가 아닐 경우 예외 처리
        if count.isdigit():
            embed = discord.Embed(title="", color=discord.Colour.light_grey())
            embed.add_field(name="", value="이수구분 과목명 학점 성적 순으로 입력해주세요.", inline=False)
            embed.set_footer(text="입력이 정상적으로 진행될 때마다 입력한 내용이 지워지니 놀라지 마세요!")
            await ctx.send(embed=embed)

            count = int(count)

            major_score = []
            subject_score = []
            else_score = []
            for i in range(1, count + 1):
                subject = await bot.wait_for("message", check=check_auth, timeout=30.0)
                subject = subject.content
                subject = subject.split(" ")

                # 이수구분을 제외하고 과목 리스트에 저장
                if subject[0] == "전공":
                    subject.remove("전공")
                    major_score.append(subject)
                elif subject[0] == "교양":
                    subject.remove("교양")
                    subject_score.append(subject)
                elif subject[0] == "일선":
                    subject.remove("일선")
                    else_score.append(subject)
                else:
                    embed = discord.Embed(title="입력 오류", description="", color=discord.Colour.blue())
                    embed.add_field(name="", value="잘못된 입력으로 인해 기능을 종료합니다.", inline=False)
                    await ctx.send(embed=embed)
                    return

                # 과목 입력한 내용 가리기
                await ctx.channel.purge(limit=1)
                await ctx.send(f"{i}번째 과목이 입력되었습니다.")

            botFuc.score_list(major_score, subject_score, else_score)
            await botFuc.credit(ctx)

        else:
            await ctx.send(":exclamation: 숫자가 아닌 잘못된 입력이 발생하여 학점계산기가 종료됩니다. :exclamation:")
            return
    # 60초 동안 입력이 없을 경우 예외 처리
    except asyncio.TimeoutError:
        await ctx.send(":exclamation: 30초 동안 입력이 발생하지 않아 학점계산기가 종료됩니다. :exclamation:")
        return


#################################################################################

# Bookmark
@bot.command()
async def 북마크목록(ctx):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.searchAllLink(serverID)
    await ctx.send(embed=embed)


@bot.command()
async def 북마크(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.searchLink(serverID, text)
    await ctx.send(embed=embed)


@bot.command()
async def 북마크등록(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.registerLink(serverID, text)
    await ctx.send(embed=embed)


@bot.command()
async def 북마크삭제(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.deleteBookmark(serverID, text)
    await ctx.send(embed=embed)


@bot.command()
async def 북마크초기화(ctx):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.deleteAllBookmark(serverID)
    await ctx.send(embed=embed)


#################################################################################

# 투표 목록을 입력받아 투표를 만드는 코드
@bot.command()
async def 투표만들기(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    userID = botFuc.hashFuc(str(ctx.author.id))
    embed = botFuc.createVote(serverID, userID, text)
    await ctx.send(embed=embed)


# 현재 개설된 투표의 목록을 보여주는 코드
@bot.command()
async def 진행중인투표(ctx):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.voteAllList(serverID)
    await ctx.send(embed=embed)


# 시작된 투표를 종료시키는 코드
@bot.command()
async def 투표종료(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    userID = botFuc.hashFuc(str(ctx.author.id))
    embed = botFuc.finishVote(serverID, userID, text)
    await ctx.send(embed=embed)


# 투표 하기
@bot.command()
async def 투표(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    check = botFuc.checkVoteList(serverID, text)
    if check:
        view = botFuc.vote(serverID, text)
        await ctx.send(text, view=view)
    else:
        embed = discord.Embed(title='진행중인 투표가 없습니다.', color=0xff0000)
        embed.add_field(name="", value="", inline=False)
        await ctx.send(embed=embed)


# 투표 진행 현황
@bot.command()
async def 투표현황(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    embed = botFuc.voteStatus(serverID, text)
    await ctx.send(embed=embed)


#################################################################################

# translate
@bot.event  # 명령어가 아닌 이모지를 누르는 것으로 번역을 실행
async def on_raw_reaction_add(payload):  # 이모지 입력을 감지'
    target_lang = botFuc.lang_selector(payload)
    channel = bot.get_channel(payload.channel_id)
    txt = await channel.fetch_message(payload.message_id)

    embed = botFuc.translation(txt, target_lang)
    await channel.send(embed=embed)


#################################################################################

# dictionary
@bot.command()
async def 사전(ctx, *, text):
    embed = botFuc.dictionary(text)
    await ctx.send(embed=embed)


#################################################################################

# grammar
@bot.command()
async def 맞춤법(ctx):
    embed = botFuc.kor_spelling(ctx)
    await ctx.send(embed=embed)


#################################################################################
# 노래봇 코드 : 원하는 노래의 유튜브 링크나 제목 검색을 통해 노래 재생 및 다양한 명령어로 이를 제어
# 재생 코드 : 유튜브에 검색할 검색어를 입력 받아 최적의 영상을 찾아 재생
@bot.command()
async def 재생(ctx, *, msg):
    await botFuc.p(ctx, msg)


# url 코드 : 유튜브 링크를 입력 받아 해당 영상을 재생
@bot.command(aliases=["URL", "URL재생", "url재생"])
async def url(ctx, *, link):
    await botFuc.P(ctx, link)


# 멜론차트 코드 : 유튜브에 존재하는 가장 최근 날짜의 멜론차트 영상 재생
@bot.command()
async def 멜론차트(ctx):
    await botFuc.melonchart(ctx)


# 연결끊기 코드 : 음성채널에 연결된 봇의 연결 끊기
@bot.command()
async def 연결끊기(ctx):
    await botFuc.disconnect(ctx)


# 일시정지 코드 : 현재 재생 중인 노래를 일시 정지
@bot.command()
async def 일시정지(ctx):
    await botFuc.stop(ctx)


# 일시정지해제 코드 : 현재 일시정지된 노래를 다시 재생
@bot.command()
async def 일시정지해제(ctx):
    await botFuc.run(ctx)


# 스킵 코드 : 현재 재생 중인 노래를 스킵
@bot.command()
async def 스킵(ctx):
    await botFuc.skip(ctx)


# 지금노래 코드 : 현재 재생 중인 노래 정보 출력
@bot.command()
async def 지금노래(ctx):
    await botFuc.nowMusic(ctx)


# 목록 코드 : 현재 노래 목록 출력
@bot.command()
async def 목록(ctx):
    await botFuc.queue(ctx)


# 삭제 코드 : 현재 노래 목록에서 원하는 노래 삭제
@bot.command()
async def 삭제(ctx, *, number):
    await botFuc.delete(ctx, number)


# 초기화 코드 : 현재 노래 목록을 초기화
@bot.command()
async def 초기화(ctx):
    await botFuc.reset(ctx)


#################################################################################

# 주사위 코드 : 1부터 6까지의 수 중 무작위로 숫자 하나 출력
@bot.command(aliases=["dice"])
async def 주사위(ctx):
    await botFuc.dice(ctx)


# 주사위대결 코드 : 사용자와 봇 간의 주사위 눈 대소 비교를 통해 대결 결과를 출력
@bot.command()
async def 주사위대결(ctx):
    await botFuc.diceBattle(ctx)


#################################################################################

# RockPaperScissors
@bot.command(aliases=['가바보', 'RPS', 'rps', 'RSP', 'rsp'])
async def 가위바위보(ctx):
    embed = botFuc.rps(ctx)
    await ctx.send(embed=embed)


@bot.command(aliases=['가바보대결', 'RPSF', 'rpsf', 'RSPF', 'rspf', 'FIGHT', 'fight'])
async def 대결(ctx, user: discord.Member):
    embed = botFuc.mtm_rps(ctx, user)
    await ctx.send(embed=embed)


@bot.command()
async def 판대결(ctx, user: discord.Member, number):
    for i in botFuc.mtm_multi_rps(ctx, user, number):
        embed = i
        await ctx.send(embed=embed)


@bot.command(aliases=['랜덤대결', 'RandomFight'])
async def 무작위대결(ctx):
    embed = botFuc.random_mtm_rps(ctx)
    await ctx.send(embed=embed)


@bot.command(aliases=['드루와'])
async def 아무나대결(ctx):
    embed = botFuc.random_mtm_player_rps(ctx)
    await ctx.send(embed=embed)


#################################################################################
# NumberBaseBall
@bot.command()
async def 숫자야구규칙(ctx):
    embed = botFuc.numberBaseBallRole()

    await ctx.send(embed=embed)


@bot.command()
async def 게임시작(ctx):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    userID = botFuc.hashFuc(str(ctx.author.id))
    embed = botFuc.registerNumberBaseball(serverID, userID)

    await ctx.send(embed=embed)


@bot.command()
async def 게임종료(ctx):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    userID = botFuc.hashFuc(str(ctx.author.id))
    embed = botFuc.stopNumberBaseball(serverID, userID)

    await ctx.send(embed=embed)


@bot.command()
async def 정답(ctx, *, text):
    serverID = botFuc.hashFuc(str(ctx.guild.id))
    userID = botFuc.hashFuc(str(ctx.author.id))
    embed = botFuc.answer(serverID, userID, text)

    await ctx.send(embed=embed)


#################################################################################

# 무작위로 팀을 짜주는 코드
@bot.command(aliases=['team', '조', '조만들기', '팀'])
async def 팀만들기(msg):
    embed = botFuc.team(msg)
    await msg.send(embed=embed)


# 목록에 저장된 내용을 무작위로 뽑는 코드
@bot.command(aliases=['가챠', '랜덤뽑기'])
async def 뽑기(msg):
    embed = botFuc.choice(msg)
    await msg.send(embed=embed)


#################################################################################

@bot.command()
async def 공지검색(msg):
    embed = botFuc.notification_search(msg)

    await msg.send(embed=embed)

past_title = ""
check = True


@bot.command()
async def 공지알림(msg):
    global past_title
    global check

    while True:
        embed, check, past_title = botFuc.notification_alarm(msg, past_title)
        try:
            await msg.send(embed=embed)
        except:
            pass

        if not check:
            break
        # await msg.send(f"작동테스트\n현재시각 : {datetime.datetime.now()}")
        await asyncio.sleep(300.0)


#################################################################################

bot.run(TOKEN)
