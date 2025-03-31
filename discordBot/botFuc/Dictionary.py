import discord
import urllib
import json
import requests
import lxml
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from .hanspell import spell_checker

load_dotenv(dotenv_path="./.env")
KORDICT_KEY = os.getenv("KORDICT_KEY")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")


# Korean dictionary
def dictionary(ctx):
    searched_other_lang = []
    edited_txt = ctx

    # 한국어기초사전 api 사용
    kordict_url = f'https://krdict.korean.go.kr/api/search?key={KORDICT_KEY}&part=word&translated=y&trans_lang=1,2&advanced=y&target=1&method=exact&q={edited_txt}'
    request = requests.get(kordict_url, verify=False)
    xml = request.text
    soup = BeautifulSoup(xml, 'xml')
    try:
        data = soup.find('definition').string
        other_lang = soup.find_all('trans_word', limit=2)

    except:
        embed = discord.Embed(title='사전 검색 결과', colour=discord.Colour.red())
        embed.add_field(name='검색 결과가 없습니다.', value='', inline=False)
        return embed

    for i in other_lang:
        searched_other_lang.append(str(i.string))

    embed = discord.Embed(
        title=edited_txt,
        description=data,
        colour=discord.Colour.green()
    )
    embed.add_field(name='다른 언어', value=searched_other_lang[0], inline=False)
    embed.add_field(name='', value=searched_other_lang[1], inline=False)
    return embed


# Translator Kor <-> Eng
def translation(txt, target_lang):  # 이모지 입력을 감지
    # 입력된 언어를 감지, 네이버 파파고 api 사용
    client_id = NAVER_CLIENT_ID
    client_secret = NAVER_CLIENT_SECRET
    encQuery = urllib.parse.quote(txt.content)
    data = "query=" + encQuery
    url = "https://openapi.naver.com/v1/papago/detectLangs"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        data = json.loads(response_body)
        searched_lang = data['langCode']
    else:
        print("Error Code:" + rescode)

    # 네이버 파파고 api 사용
    encText = urllib.parse.quote(txt.content)
    data = f"source={searched_lang}&target={target_lang}&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        data = json.loads(response_body)
        searched_txt = data['message']['result']['translatedText']
    else:
        print("Error Code:" + rescode)

    embed = discord.Embed(
        title='번역결과',
        description=searched_txt,
        colour=discord.Colour.green()
    )
    return embed


# Translator language selector
def lang_selector(payload):
    if str(payload.emoji) == "\U0001F1FA\U0001F1F2" or str(payload.emoji) == "\U0001F1FA\U0001F1F8":
        target_lang = 'en'  # print(target_lang)
    if str(payload.emoji) == "\U0001F1F0\U0001F1F7":
        target_lang = 'ko'
    if str(payload.emoji) == "\U0001F1EF\U0001F1F5":
        target_lang = 'ja'
    if str(payload.emoji) == "\U0001F1E8\U0001F1F3":
        target_lang = 'zh-CN'
    if str(payload.emoji) == "\U0001F1F9\U0001F1FC":
        target_lang = 'zh-TW'
    if str(payload.emoji) == "\U0001F1FB\U0001F1F3":
        target_lang = 'vi'
    if str(payload.emoji) == "\U0001F1EE\U0001F1E9":
        target_lang = 'id'
    if str(payload.emoji) == "\U0001F1F9\U0001F1ED":
        target_lang = 'th'
    if str(payload.emoji) == "\U0001F1E9\U0001F1EA":
        target_lang = 'de'
    if str(payload.emoji) == "\U0001F1F7\U0001F1FA":
        target_lang = 'ru'
    if str(payload.emoji) == "\U0001F1EA\U0001F1F8":
        target_lang = 'es'
    if str(payload.emoji) == "\U0001F1EE\U0001F1F9":
        target_lang = 'it'
    if str(payload.emoji) == "\U0001F1EB\U0001F1F7" or str(payload.emoji) == "\U0001F1F2\U0001F1EB":
        target_lang = 'fr'

    return target_lang


# Korean spelling
def kor_spelling(ctx):
    # 맞춤법 라이브러리를 통해 교정
    txt = ctx.message.content
    edited_txt = txt.strip("!맞춤법")
    result = spell_checker.check(edited_txt)
    corrected_txt = result[2]

    embed = discord.Embed(
        title='교정결과',
        description=corrected_txt,
        colour=discord.Colour.green()
    )
    return embed
