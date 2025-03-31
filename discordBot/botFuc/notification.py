import asyncio
import discord
from selenium import webdriver
from selenium.webdriver.common.by import By

# chromedriver_autoinstaller package 설치 방법
# chromedriver-autoinstaller package 설치 후 사용
import chromedriver_autoinstaller

# 공지 검색할 driver를 미리 실행
while True:
    try:
        # 버전에 맞는 chrome드라이버 설치
        chromedriver_autoinstaller.install()

        print("chromedriver 설치완료")

        # 창 숨기는 옵션
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.hs.ac.kr/kor/4953/subview")

        print("driver 실행 완료")
        break
    except:
        pass

on_off = False


# 공지검색기능
def notification_search(msg):
    message = msg.message.content
    message = message.split()

    global driver

    embed = discord.Embed(title="", color=0x6E17E3)
    if len(message) != 3:
        embed.add_field(name="", value=f"양식을 맞춰주세요.", inline=False)
        embed.add_field(name="", value=f"공지검색 (키워드) (개수)", inline=False)

    else:
        # 검색할 내용을 text_Field에 넣는 부분
        text_Field = driver.find_element(By.XPATH,
                                         '/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[1]/div/div[2]/fieldset/input')
        text_Field.send_keys(message[1])

        # 검색 버튼 클릭하는 부분
        search_box = driver.find_element(By.XPATH,
                                         '/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[1]/div/div[2]/fieldset/span/input')
        search_box.click()

        # 빠른 접근으로 인한 오류 방지용
        asyncio.sleep(1)

        # 검색한 공지를 embed에 저장
        for index in range(1, int(message[2]) + 1):
            info = driver.find_element(By.XPATH,
                                       f'/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[2]/table/tbody/tr[{index}]/td[2]/a')
            embed.add_field(name="", value=f"제목 : {info.text}\n링크 : {info.get_attribute('href')}", inline=False)

        # text_Field에 작성된 검색어 삭제
        text_Field = driver.find_element(By.XPATH,
                                         '/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[1]/div/div[2]/fieldset/input')
        text_Field.clear()

    return embed


def notification_alarm(msg, past_title):
    message = msg.message.content
    message = message.split()

    global on_off
    global driver

    embed = discord.Embed(title="", color=0x6E17E3)
    if len(message) != 2:
        embed.add_field(name="", value=f"양식을 맞춰주세요.", inline=False)
        embed.add_field(name="", value=f"공지알림 (켜기/끄기)", inline=False)

        return embed, False, past_title

    elif message[1] == "켜기":

        on_off = True
        embed = discord.Embed(title="", color=0x6E17E3)

        # 새로고침 코드
        search_box = driver.find_element(By.XPATH,
                                         '/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[1]/div/div[2]/fieldset/span/input')
        search_box.click()

        # 빠른 접근으로 인한 오류방지용 코드
        asyncio.sleep(1)

        # 최상단 공지의 제목 저장
        title = driver.find_element(By.XPATH,
                                    '/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[2]/table/tbody/tr[1]/td[2]/a').text

        # 직전 공지의 제목과 현재 공지의 제목 확인용
        print(f"past : {past_title}")
        print(f"title : {title}")

        # 최상단 공지가 새로 올라온 공지인지 확인
        info = title
        if past_title != info:
            # 직전 공지제목과 비교하여 새로 올라온 공지들만 embed에 저장
            for index in range(1, 5):
                info = driver.find_element(By.XPATH,
                                           f'/html/body/div/div[3]/div/div[2]/div/div/article/div/div[2]/form[2]/table/tbody/tr[{index}]/td[2]/a')
                embed.add_field(name="", value=f"제목 : {info.text}\n링크 : {info.get_attribute('href')}", inline=False)
                if info.text == past_title:
                    break

            past_title = title

            return embed, True, past_title

        # 직전 공지제목과 현재 공지 제목이 같을때 공지알림 실행 여부 반환
        else:
            if on_off:
                return None, True, past_title
            else:
                return None, False, past_title

    elif message[1] == "끄기":

        if on_off:
            embed.add_field(name="", value=f"공지 알림을 종료합니다.", inline=False)
        else:
            embed.add_field(name="", value=f"공지 알림이 실행되어 있지 않습니다.", inline=False)

        on_off = False
        return embed, False, past_title

    else:
        embed.add_field(name="", value=f"양식을 맞춰주세요.", inline=False)
        embed.add_field(name="", value=f"공지알림 (켜기/끄기)", inline=False)

        return embed, False, past_title
