import asyncio
import discord
from discord.ext import commands


#-----------------------------------------------------------------------------------------------------------------------


##### 기본 코드


TOKEN = ""
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


#-----------------------------------------------------------------------------------------------------------------------


##### 학점 계산기 코드 : 전공, 교양, 일선 순으로 학점을 입력 받아 계산하여 DM을 통해 성적표 고지


major_score = []
subject_score = []
else_score = []

def score_list(major, subject, general):
    global major_score
    global subject_score
    global else_score

    major_score = major
    subject_score = subject
    else_score = general

### 학점 계산기 코드 : 전공, 교양, 일선 순으로 학점을 입력 받아 계산하여 DM을 통해 성적표 고지
@bot.command()
async def credit(ctx):
    global major_score
    global subject_score
    global else_score

    # 학점 환산값
    grade45 = {"A+": 4.5, "A0": 4.0, "A":4.0, "B+": 3.5, "B0": 3.0, "B": 3.0, "C+": 2.5, "C0": 2.0, "C": 2.0,
               "D+": 1.5, "D0": 1.0, "D": 1.0, "F": 0}
    grade43 = {"A+": 4.3, "A0": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B0": 3.0, "B": 3.0, "B-": 2.7,
               "C+": 2.3, "C0": 2.0, "C": 2.0, "C-": 1.7, "D+": 1.3, "D0": 1.0, "D-": 0.7, "F": 0}
    pnp = {"P": True, "NP": False}

    major_count = len(major_score)
    subject_count = len(subject_score)
    else_count = len(else_score)

    ### 학점 계산 코드
    embed = discord.Embed(title="학점 계산", description="", color=discord.Colour.light_grey())
    embed.add_field(name="학점 계산을 시작합니다.", value="", inline=False)
    embed.add_field(name="원하는 학점 버전을 클릭해주세요.", value="", inline=False)
    await ctx.send(embed=embed)

    # 성적표에 들어갈 내용 계산 코드
    result4 = 0 # 전공 이수 학점
    for i in range(int(major_count)):
        result4 += float(major_score[i][1])
    result5 = 0 # 교양 이수 학점
    for i in range(int(subject_count)):
        result5 += float(subject_score[i][1])
    result6 = 0 # 일선 이수 학점
    for i in range(int(else_count)):
        result6 += float(else_score[i][1])
    result3 = result4 + result5 + result6  # 전체 이수 학점


    ### 버튼 코드
    class SimpleView(discord.ui.View):

        ### 학점 계산 4.5ver 코드
        @discord.ui.button(label="학점계산(4.5ver)", style=discord.ButtonStyle.red)
        async def 학점계산5(self, interaction: discord.Interaction, button: discord.ui.button):

            # 성적표에 들어갈 내용 계산 코드
            total = 0
            part = 0

            check = True
            for i in range(int(major_count)):
                if major_score[i][2] in pnp.keys():
                    continue
                try:
                    total += float(major_score[i][1]) * grade45[major_score[i][2]]
                    part += float(major_score[i][1])
                except:
                    check = False
            if check:
                try:
                    result2 = total / part  # 전공 학점
                except ZeroDivisionError:
                    result2 = 0
                test = list(str(result2))
                try:
                    if test.index('.')+2 < len(test):
                        test = test[:test.index('.')+3]
                    result2 = "".join(test) # 절사한 전공 학점
                except:
                    result2 = 0
                for i in range(int(subject_count)):
                    if subject_score[i][2] in pnp.keys():
                        continue
                    total += float(subject_score[i][1]) * grade45[subject_score[i][2]]
                    part += float(subject_score[i][1])
                for i in range(int(else_count)):
                    if else_score[i][2] in pnp.keys():
                        continue
                    total += float(else_score[i][1]) * grade45[else_score[i][2]]
                    part += float(else_score[i][1])
                try:
                    result1 = total / part  # 전체 학점
                except ZeroDivisionError:
                    result1 = 0
                test = list(str(result1))
                try:
                    if test.index('.') + 2 < len(test):
                        test = test[:test.index('.') + 3]
                    result1 = "".join(test)  # 절사한 전체 학점
                except:
                    result1 = 0


                # embed를 활용하여 학점 계산 결과 확인 방법 출력
                embed = discord.Embed(title="학점 계산 4.5ver 완료", description="", color=discord.Colour.gold())
                embed.add_field(name="학점 계산이 완료되었습니다.", value="", inline=False)
                embed.add_field(name="DM으로 성적표를 전송했습니다.", value="", inline=False)
                embed.set_footer(text="DM이 오지 않는다면, 서버 이름 클릭 - 개인정보 보호 설정 - \"다이렉트 메시지\"를 허용해주세요.")
                await interaction.response.send_message(embed=embed)


                # embed를 활용하여 DM으로 성적표 전송 및 출력
                embed = discord.Embed(title=":trophy: "+ctx.author.name + " 님의 성적표 :trophy:", description="", color=discord.Colour.gold())
                for i in range(len(major_score)):
                    embed.add_field(name="", value=str(i+1)+".  "+major_score[i][0]+"  "+major_score[i][1]+"  "
                                                   +major_score[i][2], inline=False)
                for i in range(len(subject_score)):
                    embed.add_field(name="", value=str(i+1+len(major_score))+".  "+subject_score[i][0]+"  "
                                                   +subject_score[i][1]+"  "+subject_score[i][2], inline=False)
                for i in range(len(else_score)):
                    embed.add_field(name="", value=str(i+1+len(major_score)+len(subject_score))+".  "+else_score[i][0]+"  "
                                                   +else_score[i][1]+"  "+else_score[i][2], inline=False)
                embed.add_field(name="전체 학점", value=result1, inline=True)
                embed.add_field(name="전공 학점", value=result2, inline=True)
                embed.add_field(name="전체 이수 학점", value=result3, inline=False)
                embed.add_field(name="전공 이수 학점", value=result4, inline=False)
                embed.add_field(name="교양 이수 학점", value=result5, inline=False)
                embed.add_field(name="일선 이수 학점", value=result6, inline=False)

                dm_channel = await ctx.message.author.create_dm()
                await dm_channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Error!", description="", color=discord.Colour.red())
                embed.add_field(name="학점 계산 4.3ver를 이용해주세요.", value="", inline=False)
                await interaction.response.send_message(embed=embed)



        ### 학점 계산 4.3ver 코드
        @discord.ui.button(label="학점계산(4.3ver)", style=discord.ButtonStyle.red)
        async def 학점계산3(self, interaction: discord.Interaction, button: discord.ui.button):



            # 성적표에 들어갈 내용 계산 코드
            total = 0
            part = 0
            for i in range(int(major_count)):
                if major_score[i][2] in pnp.keys():
                    continue
                total += float(major_score[i][1]) * grade43[major_score[i][2]]
                part += float(major_score[i][1])
            try:
                result2 = total / part  # 전공 학점
            except ZeroDivisionError:
                result2 = 0
            test = list(str(result2))
            try:
                if test.index('.') + 2 < len(test):
                    test = test[:test.index('.') + 3]
                result2 = "".join(test)  # 절사한 전공 학점
            except:
                result2 = 0
            for i in range(int(subject_count)):
                if subject_score[i][2] in pnp.keys():
                    continue
                total += float(subject_score[i][1]) * grade43[subject_score[i][2]]
                part += float(subject_score[i][1])
            for i in range(int(else_count)):
                if else_score[i][2] in pnp.keys():
                    continue
                total += float(else_score[i][1]) * grade43[else_score[i][2]]
                part += float(else_score[i][1])
            try:
                result1 = total / part  # 전체 학점
            except ZeroDivisionError:
                result1 = 0
            test = list(str(result1))
            try:
                if test.index('.') + 2 < len(test):
                    test = test[:test.index('.') + 3]
                result1 = "".join(test)  # 절사한 전체 학점
            except:
                result1 = 0


            # embed를 활용하여 학점 계산 결과 확인 방법 출력
            embed = discord.Embed(title="학점 계산 4.3ver 완료", description="", color=discord.Colour.gold())
            embed.add_field(name="학점 계산이 완료되었습니다.", value="", inline=False)
            embed.add_field(name="DM으로 성적표를 전송했습니다.", value="", inline=False)
            embed.set_footer(text="DM이 오지 않는다면, 서버 이름 클릭 - 개인정보 보호 설정 - \"다이렉트 메시지\"를 허용해주세요.")
            await interaction.response.send_message(embed=embed)


            # embed를 활용하여 DM으로 성적표 전송 및 출력
            embed = discord.Embed(title=":trophy: "+ctx.author.name + " 님의 성적표 :trophy:", description="", color=discord.Colour.gold())
            for i in range(len(major_score)):
                embed.add_field(name="", value=str(i + 1) + ".  " + major_score[i][0] + "  " + major_score[i][1] + "  "
                                               + major_score[i][2], inline=False)
            for i in range(len(subject_score)):
                embed.add_field(name="", value=str(i + 1 + len(major_score)) + ".  " + subject_score[i][0] + "  "
                                               + subject_score[i][1] + "  " + subject_score[i][2], inline=False)
            for i in range(len(else_score)):
                embed.add_field(name="",
                                value=str(i + 1 + len(major_score) + len(subject_score)) + ".  " + else_score[i][
                                    0] + "  "
                                      + else_score[i][1] + "  " + else_score[i][2], inline=False)

            embed.add_field(name="전체 학점", value=result1, inline=True)
            embed.add_field(name="전공 학점", value=result2, inline=True)
            embed.add_field(name="전체 이수 학점", value=result3, inline=False)
            embed.add_field(name="전공 이수 학점", value=result4, inline=False)
            embed.add_field(name="교양 이수 학점", value=result5, inline=False)
            embed.add_field(name="일선 이수 학점", value=result6, inline=False)

            dm_channel = await ctx.message.author.create_dm()
            await dm_channel.send(embed=embed)

    view = SimpleView()
    await ctx.send(view=view)

    await asyncio.sleep(10)
    await ctx.channel.purge(limit=1)

#-----------------------------------------------------------------------------------------------------------------------
