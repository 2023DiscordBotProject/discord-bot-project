import discord


# 자격증 일정
def certificate():
    embed = discord.Embed(title='자격증 명령어', color=0x6E17E3)
    embed.add_field(name='!자격증일정 년도 자격증명', value="!자격증일정 2023 정보처리기사", inline=False)

    return embed


# 학점계산기
def creditCalculator():
    embed = discord.Embed(title='학점계산기 명령어', color=0x6E17E3)
    embed.add_field(name="!학점계산기", value="", inline=False)

    return embed


# 북마크
def bookmark():
    embed = discord.Embed(title='북마크 명령어', color=0x6E17E3)
    embed.add_field(name="!북마크목록", value="", inline=False)
    embed.add_field(name="!북마크등록 [이름]링크", value="ex)!북마크등록 [네이버]https://www.naver.com", inline=False)
    embed.add_field(name="!북마크삭제", value="", inline=False)
    embed.add_field(name="!북마크 이름", value="ex)!북마크 네이버", inline=False)
    embed.add_field(name="!북마크초기화", value="", inline=False)
    return embed


# 투표
def vote():
    embed = discord.Embed(title='투표 명령어', color=0x6E17E3)
    embed.add_field(name='!투표만들기 [투표명]항목1 항목2 항목3', value='ex)투표만들기 [점심 메뉴]한식 중식 일식', inline=False)
    embed.add_field(name='!진행중인투표', value='진행 중인 투표 목록이 보여집니다.', inline=False)
    embed.add_field(name='!투표종료 투표명', value='ex)!투표종료 점심 메뉴', inline=False)
    embed.add_field(name='!투표 투표명', value='ex)!투표 점심 메뉴', inline=False)
    embed.add_field(name='!투표현황 투표명', value='ex)!투표현황 점심 메뉴', inline=False)

    return embed


# 번역기
def translate():
    embed = discord.Embed(title='번역기 사용법', color=0x6E17E3)
    embed.add_field(name='디스코드의 ‘반응 추가하기’ 기능을 이용해서 국기(flag)를 추가하여 사용', value='이용 가능한 언어는 한국어, 영어, 일본어, 중국어(번체, 간체), 베트남어, 인도네시아어, 태국어, 독일어, 러시아어, 스페인어, 이탈리아어, 프랑스어', inline=False)

    return embed


# 사전
def dictionary():
    embed = discord.Embed(title='사전 명령어', color=0x6E17E3)
    embed.add_field(name='!사전 검색어', value="ex) !사전 지우개", inline=False)

    return embed


# 문법
def grammar():
    embed = discord.Embed(title='맞춤법검사기 명령어', color=0x6E17E3)
    embed.add_field(name='!맞춤법 문장', value="ex)!맞춤법 안녕 하세요", inline=False)

    return embed


# 음악봇
def music():
    embed = discord.Embed(title='음악 명령어', color=0x6E17E3)
    embed.add_field(name="!재생 노래제목", value="", inline=False)
    embed.add_field(name="!url 노래링크", value="", inline=False)
    embed.add_field(name="!멜론차트", value="", inline=False)
    embed.add_field(name="!연결끊기", value="", inline=False)
    embed.add_field(name="!일시정지", value="", inline=False)
    embed.add_field(name="!일시정지해제", value="", inline=False)
    embed.add_field(name="!스킵", value="", inline=False)
    embed.add_field(name="!지금노래", value="", inline=False)
    embed.add_field(name="!목록", value="", inline=False)
    embed.add_field(name="!삭제 삭제할노래번호", value="", inline=False)
    embed.add_field(name="!초기화", value="", inline=False)

    return embed


# 주사위
def dice():
    embed = discord.Embed(title='주사위 명령어', color=0x6E17E3)
    embed.add_field(name="!주사위", value="", inline=False)
    embed.add_field(name="!주사위대결", value="", inline=False)

    return embed


# 가위바위보
def rockPaperScissors():
    embed = discord.Embed(title='가위바위보 명령어', color=0x6E17E3)
    embed.add_field(name='!가위바위보', value="일반적인 가위바위보입니다.", inline=False)
    embed.add_field(name='!대결 유저', value="상대방을 정한 상태로 게임이 진행됩니다.", inline=False)
    embed.add_field(name='!판대결 유저 게임횟수', value="다전제 게임입니다. 상대방을 정한 상태로 게임이 진행됩니다.\nex)!판대결 유저 3", inline=False)
    embed.add_field(name='!무작위대결', value="특별한 명령어가 필요 없습니다. 두명이 무작위로 선택되어 게임이 진행됩니다.\nex)!무작위대결", inline=False)
    embed.add_field(name='!아무나대결', value="특별한 명령어가 필요 없습니다. 본인은 고정이고 상대방만 무작위로 정합니다.\nex)!아무나대결", inline=False)

    return embed


# 숫자야구 게임
def NumberbaseBall():
    embed = discord.Embed(title='숫자야구 명령어', color=0x6E17E3)
    embed.add_field(name="!숫자야구규칙", value="숫자야구 규칙 설명", inline=False)
    embed.add_field(name="!게임시작", value="숫자야구 게임 시작", inline=False)
    embed.add_field(name="!게임종료", value="게임 종료", inline=False)
    embed.add_field(name="!정답 ???", value="??? => 숫자 입력", inline=False)
    return embed


# 팀짜기
def team():
    embed = discord.Embed(title='팀만들기 명령어', color=0x6E17E3)
    embed.add_field(name='!팀만들기 명수 팀수 팀당인원수', value='ex)!팀만들기 6 2 3', inline=False)

    return embed


# 뽑기
def drawing():
    embed = discord.Embed(title='뽑기 명령어', color=0x6E17E3)
    embed.add_field(name='!뽑기 가지수 뽑을개수', value='ex)!뽑기 5 2', inline=False)

    return embed


# 공지
def notification():
    embed = discord.Embed(title='공지 명령어', color=0x6E17E3)
    embed.add_field(name='!공지알림 켜기', value='', inline=False)
    embed.add_field(name='!공지알림 끄기', value='', inline=False)
    embed.add_field(name='!공지검색 검색어 개수', value='ex)!공지검색 근로 3', inline=False)

    return embed


# 명령어 목록
def commandList(text):
    list = ['자격증', '학점계산기', '북마크', '투표', '번역', '사전', '맞춤법검사기', '음악', '주사위', '가위바위보', '숫자야구', '팀만들기', '뽑기', '공지']
    if text == '목록':
        embed = discord.Embed(title="명령어 목록", color=0x6E17E3)
        for i in list:
            embed.add_field(name='!명령어 ' + str(i), value='', inline=False)
    elif text == '자격증':
        embed = certificate()
    elif text == '학점계산기':
        embed = creditCalculator()
    elif text == '북마크':
        embed = bookmark()
    elif text == '투표':
        embed = vote()
    elif text == '번역':
        embed = translate()
    elif text == '사전':
        embed = dictionary()
    elif text == '맞춤법검사기':
        embed = grammar()
    elif text == '음악':
        embed = music()
    elif text == '주사위':
        embed = dice()
    elif text == '가위바위보':
        embed = rockPaperScissors()
    elif text == '숫자야구':
        embed = NumberbaseBall()
    elif text == '팀만들기':
        embed = team()
    elif text == '뽑기':
        embed = drawing()
    elif text == '공지':
        embed = notification()
    else:
        embed = discord.Embed(title='명령어 목록', color=0x6E17E3)
        embed.add_field(name='제공하지 않는 기능입니다.', value='', inline=False)

    return embed


