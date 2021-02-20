'''
!명령어
'''
import discord
import time
import json

token = '★토큰★'
admin = '관리자 닉'

def times():
    return time.time()

client = discord.Client()

@client.event
async def on_connect():
    print("ONLINE")

@client.event
async def on_member_join(member):
    with open('./setting.json', 'r') as boo:
        data = json.load(boo)
    setting = data['days']
    setting = int(setting)

    created = times() - member.created_at.timestamp()
    created = int(created) / 86400
    created = round(created)

    if created < setting:
        embed = discord.Embed(title='❗  계정 생성일 미달', description=f'계정 생성일이 {setting}일 미만이므로 **{member.guild}**에서 추방되었습니다')
        embed.set_footer(text=f'{admin}으로 문의주세요')
        await member.send(embed=embed)
        await member.kick(reason='계정 생성일 미달')

@client.event
async def on_message(message):
    if message.content == '!명령어' and message.author.guild_permissions.manage_messages:
        await message.channel.send('**!수정**: 기준 생성일을 수정합니다\n**!설정값**: 현재 설정된 기준 생성일을 보여줍니다')
    if message.content.startswith('!수정'):
        if message.author.guild_permissions.manage_messages:
            j = message.content.split(" ")
            try:
                edit_amount = j[1]
            except:
                embed = discord.Embed(title='!수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return

            if not edit_amount.isdecimal():
                embed = discord.Embed(title='!수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return
            elif edit_amount.isdecimal():
                with open('./setting.json', 'r') as boo:
                    data = json.load(boo)
                data['days'] = edit_amount
                with open('./setting.json', 'w', encoding='utf-8') as making:
                    json.dump(data, making, indent="\t")
                d = data['days']
                await message.channel.send(f'`{d}`일으로 수정됨')

    if message.content == '!설정값':
        if message.author.guild_permissions.manage_messages:
            with open('./setting.json', 'r') as boo:
                data = json.load(boo)
            d = data['days']
            embed = discord.Embed(description="")
            embed.set_author(name=f'{d}일으로 설정되어있습니다')
            await message.channel.send(embed=embed)

client.run(token)
