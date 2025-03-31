import discord
import random

rps_list = ['가위', '바위', '보자기']  # 가위바위보 기본 리스트


# Original Rock Paper Scissors
def rps(ctx):
    if ctx.message.author.nick == None:  # 메시지를 보내는 사람의 닉네임이 설정되어 있는지에 따라 이름을 사용할지 결정
        attacker = ctx.message.author.global_name
    else:
        attacker = ctx.message.author.nick
    embed = discord.Embed(
        title="이얍",
        description=f'시전자 : {attacker}\n{(random.choice(rps_list))}',  # 가위바위보 기본 리스트에서 하나 뽑아오기
        color=discord.Colour.blue()
    )
    return embed


# Man to man Rock Paper Scissors
def mtm_rps(ctx, user):
    attack = random.choice(rps_list)
    defense = random.choice(rps_list)
    result = 'result'
    if ctx.message.author.nick == None:  # 메시지를 보내는 사람의 닉네임이 설정되어 있는지에 따라 이름을 사용할지 결정
        attacker = ctx.message.author.global_name
    else:
        attacker = ctx.message.author.nick
    if user.nick == None:  # 대결 받는 사람의 닉네임이 설정되어 있는지에 따라 이름을 사용할지 결정
        defender = user.global_name
    else:
        defender = user.nick

    if attack == defense:  # 결과 내기
        result = '비겼습니다!'
        colour = discord.Colour.lighter_grey()
    elif (attack == '가위' and defense == '바위') or (attack == '바위' and defense == '보자기') or (
            attack == '보자기' and defense == '가위'):
        result = '졌습니다!'
        colour = discord.Colour.red()
    elif (attack == '가위' and defense == '보자기') or (attack == '바위' and defense == '가위') or (
            attack == '보자기' and defense == '바위'):
        result = '이겼습니다!'
        colour = discord.Colour.blue()

    embed = discord.Embed(
        title="대전 결과",
        description=(
            f'시전자 : {attacker} : {attack}'
            f'\n대결 상대  : {defender} : {defense}'
            f'\n시전자가 {result}'
        ),
        color=colour
    )
    return embed


# Man to man multiround Rock Paper Scissors
def mtm_multi_rps(ctx, user: discord.Member, number):
    number = int(number)
    attack_point = 0
    defense_point = 0
    result = 'result'
    if ctx.message.author.nick == None:  # 메시지를 보내는 사람의 닉네임이 설정되어 있는지에 따라 이름을 사용할지 결정
        attacker = ctx.message.author.global_name
    else:
        attacker = ctx.message.author.nick
    if user.nick == None:  # 대결 받는 사람의 닉네임이 설정되어 있는지에 따라 이름을 사용할지 결정
        defender = user.global_name
    else:
        defender = user.nick

    if number % 2 != 0:  # 대결 횟수가 짝수일 때
        while attack_point <= (number // 2) and defense_point <= (number // 2):
            attack = random.choice(rps_list)
            defense = random.choice(rps_list)
            if attack == defense:  # 결과 내기
                result = '비겼습니다!'
            elif (attack == '가위' and defense == '바위') or (attack == '바위' and defense == '보자기') or (
                    attack == '보자기' and defense == '가위'):
                result = '졌습니다!'
                defense_point += 1
            elif (attack == '가위' and defense == '보자기') or (attack == '바위' and defense == '가위') or (
                    attack == '보자기' and defense == '바위'):
                result = '이겼습니다!'
                attack_point += 1

            embed = discord.Embed(
                title="중간 결과",
                description=(
                    f'시전자 : {attacker}   {attack}'
                    f'\n대결 상대  : {defender}   {defense}'
                    f'\n점수 : {attack_point} : {defense_point}\n{result}\n-----------------------------'
                ),
            )
            yield embed

        if attack_point > defense_point:
            # await ctx.send(f'결과\n{attack_point} : {defense_point}\n시전자 승리!')
            result_message = '시전자 승리!'
            colour = discord.Colour.blue()
        elif attack_point < defense_point:
            # await ctx.send(f'결과\n{attack_point} : {defense_point}\n시전자 패배!')
            result_message = '시전자 패배!'
            colour = discord.Colour.red()
        embed = discord.Embed(
            title="판대결 결과",
            description=(
                f'결과\n{attack_point} : {defense_point}\n{result_message}'
            ),
            color=colour
        )
        yield embed

    else:  # 대결 횟수가 홀수일 때
        while attack_point <= (number // 2 + 1) and defense_point <= (
                number // 2 + 1) and attack_point + defense_point < number:
            attack = random.choice(rps_list)
            defense = random.choice(rps_list)
            if attack == defense:
                result = '비겼습니다!'
            elif (attack == '가위' and defense == '바위') or (attack == '바위' and defense == '보자기') or (
                    attack == '보자기' and defense == '가위'):
                result = '졌습니다!'
                defense_point += 1
            elif (attack == '가위' and defense == '보자기') or (attack == '바위' and defense == '가위') or (
                    attack == '보자기' and defense == '바위'):
                result = '이겼습니다!'
                attack_point += 1

            embed = discord.Embed(
                title="중간 결과",
                description=(
                    f'시전자 : {attacker}   {attack}'
                    f'\n대결 상대  : {defender}   {defense}'
                    f'\n점수 : {attack_point} : {defense_point}\n{result}\n-----------------------------'
                ),
            )
            yield embed

        if attack_point > defense_point:
            result_message = '시전자 승리!'
            colour = discord.Colour.blue()
        elif attack_point < defense_point:
            result_message = '시전자 패배!'
            colour = discord.Colour.red()
        else:
            result_message = '이걸 비겨...?'
            colour = discord.Colour.lighter_grey()

        embed = discord.Embed(
            title="판대결 결과",
            description=(
                f'결과\n{attack_point} : {defense_point}\n{result_message}'
            ),
            color=colour
        )
        yield embed


# Random Man to man Rock Paper Scissors
def random_mtm_rps(ctx):
    user_list = [(member.nick if member.nick != None else member.global_name) for member in ctx.guild.members if
                 member.bot == False]  # 서버 사용자 리스트
    attack = random.choice(rps_list)
    defense = random.choice(rps_list)
    player = random.sample(user_list, 2)
    result = 'result'

    if attack == defense:  # 결과 내기
        result = '비겼습니다!'
        colour = discord.Colour.lighter_grey()
    elif (attack == '가위' and defense == '바위') or (attack == '바위' and defense == '보자기') or (
            attack == '보자기' and defense == '가위'):
        result = '졌습니다!'
        colour = discord.Colour.red()
    elif (attack == '가위' and defense == '보자기') or (attack == '바위' and defense == '가위') or (
            attack == '보자기' and defense == '바위'):
        result = '이겼습니다!'
        colour = discord.Colour.blue()

    embed = discord.Embed(
        title="무작위대결 결과",
        description=(
            f'공격자 : {player[0]}   {attack}'
            f'\n수비자  : {player[1]}   {defense}'
            f'\n공격자가 {result}'
        ),
        color=colour
    )
    return embed


# Random Man to man Rock Paper Scissors (player is fixed)
def random_mtm_player_rps(ctx):
    user_list = [(member.nick if member.nick != None else member.global_name) for member in ctx.guild.members if
                 member.bot == False]  # 서버 사용자 리스트
    user_list.remove(ctx.message.author.nick)  # 서버 사용자 리스트에서 시전자 제외
    attack = random.choice(rps_list)
    defense = random.choice(rps_list)
    player = random.choice(user_list)
    result = 'result'

    if attack == defense:  # 결과 내기
        result = '비겼습니다!'
        colour = discord.Colour.lighter_grey()
    elif (attack == '가위' and defense == '바위') or (attack == '바위' and defense == '보자기') or (
            attack == '보자기' and defense == '가위'):
        result = '졌습니다!'
        colour = discord.Colour.red()
    elif (attack == '가위' and defense == '보자기') or (attack == '바위' and defense == '가위') or (
            attack == '보자기' and defense == '바위'):
        result = '이겼습니다!'
        colour = discord.Colour.blue()

    embed = discord.Embed(
        title="아무나대결 결과",
        description=(
            f'시전자 : {ctx.message.author.nick}   {attack}'
            f'\n수비자  : {player}   {defense}'
            f'\n시전자가 {result}'
        ),
        color=colour
    )
    return embed
