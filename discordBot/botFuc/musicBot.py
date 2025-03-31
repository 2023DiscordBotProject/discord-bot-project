import datetime
import bs4
import discord
import yt_dlp
from discord import FFmpegPCMAudio
from discord.ext import commands
from discord.utils import get
from selenium import webdriver

#-----------------------------------------------------------------------------------------------------------------------


##### 노래봇 코드 : 원하는 노래의 유튜브 링크나 제목 검색을 통해 노래 재생 및 다양한 명령어로 이를 제어


#-----------------------------------------------------------------------------------------------------------------------


##### 기본 코드


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


#-----------------------------------------------------------------------------------------------------------------------


### 노래봇 사용에 필요한 배열 선언


now = [] # 현재 출력되는 노래 배열
user = [] # 유저가 입력한 노래 정보
music_title = [] # 가공된 정보의 노래 제목
song_link = [] # 가공된 정보의 노래 링크


#-----------------------------------------------------------------------------------------------------------------------


### 함수 1 : 노래 제목과 유튜브 링크를 변수로 받기 위한 함수


def Title(msg):
    global music
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(options = options)
    driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'html.parser')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    music_title.append(music)
    now.append(music)
    test = entireNum.get('href')
    url = 'https://www.youtube.com' + test
    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']
    driver.quit()
    return music, URL


#-----------------------------------------------------------------------------------------------------------------------


### 함수 2 : 노래 재생을 위한 함수


def play(ctx):
    global vc
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_link[0]
    del user[0]
    del music_title[0]
    del song_link[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL, **ffmpeg_options), after=lambda e: next(ctx))


#-----------------------------------------------------------------------------------------------------------------------


### 함수 3 : 다음 노래 재생을 위한 함수


def next(ctx):
    if len(now) - len(user) >= 2:
        for i in range(len(now) - len(user) - 1):
            del now[0]
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not v_channel.is_playing():
            del now[0]
            URL = song_link[0]
            del user[0]
            del music_title[0]
            del song_link[0]
            v_channel.play(discord.FFmpegPCMAudio(URL,**ffmpeg_options), after=lambda e: next(ctx))


#-----------------------------------------------------------------------------------------------------------------------


### 재생 코드 : 유튜브에 검색할 검색어를 입력 받아 최적의 영상을 찾아 재생


@bot.command()
async def p(ctx, msg):
    try:
        global v_channel
        v_channel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await v_channel.move_to(ctx.message.author.voice.channel)
        except:
            embed = discord.Embed(title="", description=f"{ctx.author.name}님이 음성채널에 먼저 접속하신 후, 다시 시도해 주세요.", color=discord.Colour.red())
            await ctx.send(embed=embed)
    # 현재 재생 중인 노래가 없을 경우 바로 재생
    if not v_channel.is_playing():
        global entiretext
        ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
        ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options = options)
        driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'html.parser')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entiretext = entireNum.text.strip()
        music_url = entireNum.get('href')
        url = 'https://www.youtube.com' + music_url
        driver.quit()
        now.insert(0, entiretext)
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['url']
        v_channel.play(discord.FFmpegPCMAudio(URL, **ffmpeg_options), after=lambda e: next(ctx))
        embed = discord.Embed(title="노래 재생 중", description=now[0] + " 재생 중",color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    # 현재 재생 중인 노래가 있을 경우 대기열에 추가
    else:
        user.append(msg)
        (result, link) = Title(msg)
        song_link.append(link)
        embed = discord.Embed(title="", description=result + " 을(를) 대기열에 추가했어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)




#-----------------------------------------------------------------------------------------------------------------------


### url 코드 : 유튜브 링크를 입력 받아 해당 영상을 재생


@bot.command()
async def P(ctx, link):
    try:
        global v_channel
        v_channel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await v_channel.move_to(ctx.message.author.voice.channel)
        except:
            embed = discord.Embed(title="", description=f"{ctx.author.name}님이 음성채널에 먼저 접속하신 후, 다시 시도해 주세요.", color=discord.Colour.red())
            await ctx.send(embed=embed)
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    # 현재 재생 중인 노래가 없을 경우 바로 재생
    if not v_channel.is_playing():
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(link, download=False)
        url = info['formats'][0]['url']
        title = info['title']
        runtime = str(datetime.timedelta(seconds=info['duration']))
        if len(runtime) < 8:
            runtime = '0' + runtime
        v_channel.play(FFmpegPCMAudio(url, **ffmpeg_options))
        embed = discord.Embed(title="노래 재생 중", description="", color=discord.Colour.brand_green())
        embed.add_field(name="제목", value=title, inline=False)
        embed.add_field(name="영상 길이", value=runtime, inline=False)
        embed.add_field(name="링크", value=link, inline=False)
        await ctx.send(embed=embed)
    # 현재 재생 중인 노래가 있을 경우 대기열에 추가
    else:
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(link, download=False)
        title = info['title']
        user.append(title)
        (result, link) = Title(title)
        song_link.append(link)
        embed = discord.Embed(title="", description=result + " 을(를) 대기열에 추가했어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 멜론차트 코드 : 유튜브에 존재하는 가장 최근 날짜의 멜론차트 영상 재생


@bot.command()
async def melonchart(ctx):
    try:
        global v_channel
        v_channel = await ctx.message.author.voice.channel.connect()
    except:
        try:
            await v_channel.move_to(ctx.message.author.voice.channel)
        except:
            embed = discord.Embed(title="", description=f"{ctx.author.name}님이 음성채널에 먼저 접속하신 후, 다시 시도해 주세요.", color=discord.Colour.red())
            await ctx.send(embed=embed)

    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
    ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                      'options': '-vn',
    }

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    global entiretext

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.youtube.com/results?search_query=멜론차트")
    source = driver.page_source

    bs = bs4.BeautifulSoup(source, 'html.parser')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    entiretext = entireNum.text.strip()
    musicurl = entireNum.get('href')
    url = 'https://www.youtube.com' + musicurl
    driver.quit()

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
    if not v_channel.is_playing():
        URL = info['url']
        v_channel.play(discord.FFmpegPCMAudio(URL, **ffmpeg_options))
        embed = discord.Embed(title="노래 재생 중", description=entiretext + " 재생 중", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)

    # 현재 재생 중인 노래가 있을 경우 대기열에 추가
    else:
        title = info['title']
        user.append(title)
        (result, link) = Title(title)
        song_link.append(link)
        embed = discord.Embed(title="", description=result + " 을(를) 대기열에 추가했어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 연결끊기 코드 : 음성채널에 연결된 봇의 연결 끊기


@bot.command()
async def disconnect(ctx):
    try:
        await v_channel.disconnect()
    except:
        embed = discord.Embed(title="", description="이미 음성채널에 존재하지 않아요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 일시정지 코드 : 현재 재생 중인 노래를 일시 정지


@bot.command()
async def stop(ctx):
    if v_channel.is_playing():
        v_channel.pause()
        embed = discord.Embed(title="일시정지", description=now[0] + " 을(를) 일시정지합니다.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="", description="현재 재생 중인 노래가 없어요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 일시정지해제 코드 : 현재 일시정지된 노래를 다시 재생


@bot.command()
async def run(ctx):
    try:
        v_channel.resume()
        embed = discord.Embed(title="일시정지해제", description=now[0] + " 을(를) 다시 재생합니다.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    except:
        embed = discord.Embed(title="", description="현재 재생 중인 노래가 없어요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 스킵 코드 : 현재 재생 중인 노래를 스킵


@bot.command()
async def skip(ctx):
    if v_channel.is_playing():
        v_channel.stop()
        embed = discord.Embed(title="skip", description=now[0] + " 을(를) 스킵합니다.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="", description="현재 재생 중인 노래가 없어요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 지금노래 코드 : 현재 재생 중인 노래 정보 출력


@bot.command()
async def nowMusic(ctx):
    if v_channel.is_playing():
        embed = discord.Embed(title="지금노래", description="현재 재생 중인 노래는 " + now[0] + " 입니다.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="", description="현재 재생 중인 노래가 없어요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 목록 코드 : 현재 노래 목록 출력


@bot.command()
async def queue(ctx):
    if len(music_title) == 0:
        embed = discord.Embed(title="", description="목록이 비어 있어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    else:
        global Text
        Text = ""
        for i in range(len(music_title)):
            Text = Text + "\n" + str(i + 1) + ". " + str(music_title[i])
        embed = discord.Embed(title="노래 목록", description=Text.strip(), color=discord.Colour.brand_green())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 삭제 코드 : 현재 노래 목록에서 원하는 노래 삭제


@bot.command()
async def delete(ctx, number):
    try:
        tmp = len(now) - len(user)
        del user[int(number) - 1]
        del music_title[int(number) - 1]
        del song_link[int(number) - 1]
        del now[int(number) + tmp - 1]
        embed = discord.Embed(title="", description=f"{number}번 노래가 삭제되었어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    except:
        # 목록이 빈 경우 예외 처리
        if len(music_title) == 0:
            embed = discord.Embed(title="", description="목록이 비어 있어 삭제할 수 없어요.", color=discord.Colour.red())
            await ctx.send(embed=embed)
        else:
            if number.isdigit():
                # 숫자가 범위를 벗어난 경우 예외 처리
                if len(music_title) < int(number):
                    embed = discord.Embed(title="", description="숫자의 범위가 목록 개수를 벗어 났어요.", color=discord.Colour.red())
                    await ctx.send(embed=embed)
            # 숫자가 아닐 경우 예외 처리
            else:
                embed = discord.Embed(title="", description="숫자를 입력해 주세요.", color=discord.Colour.red())
                await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------


### 초기화 코드 : 현재 노래 목록을 초기화


@bot.command()
async def reset(ctx):
    # 목록이 비어있지 않을 경우 초기화 실행
    if len(music_title) > 0:
        tmp = len(now) - len(user)
        del user[:]
        del music_title[:]
        del song_link[:]
        while True:
            try:
                del now[tmp]
            except:
                break
        embed = discord.Embed(title="초기화", description="목록이 초기화되었어요.", color=discord.Colour.brand_green())
        await ctx.send(embed=embed)
    # 목록이 빈 경우 예외 처리
    else:
        embed = discord.Embed(title="", description="아직 아무 노래도 등록하지 않았어요.", color=discord.Colour.red())
        await ctx.send(embed=embed)


#-----------------------------------------------------------------------------------------------------------------------
