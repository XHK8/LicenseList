import disnake, asyncio
from disnake.ext import commands
import json
import random
import sqlite3
from datetime import datetime, timedelta

intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

token = "MTIxMTYwNjEwMTM1MTQ2OTA1Ng.GqeK2Y.1Z2MXqvmylbQN7zDw96WbtTwQqg90Q3Ib2T7Bw" # 봇토큰

def load_config():
    with open('config.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def save_config(data):
    with open('config.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

class Setting(disnake.ui.Modal):
    def __init__(self):

        components = [
        disnake.ui.TextInput(
            label="라이선스",
            placeholder="지급받은 라이선스입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=29,
            custom_id="pw",
        ),
        disnake.ui.TextInput(
            label="토큰",
            placeholder="F12에서 토큰정보를 받아오세요.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=130,
            custom_id="token",
        ),
        disnake.ui.TextInput(
            label="상태",
            placeholder="",
            required=True,
            value = "PLAYING",
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=10,
            custom_id="type",
        ),
        disnake.ui.TextInput(
            label="접두사",
            placeholder="",
            required=True,
            value = "!",
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=4,
            custom_id="prefix",
        )
        
        ]
        super().__init__(
            title=f"RPC 기본 설정",
            custom_id="setting1",
            components=components,
            timeout=10000
        )

class Photo(disnake.ui.Modal):
    def __init__(self):

        components = [
        disnake.ui.TextInput(
            label="라이선스",
            placeholder="지급받은 라이선스입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=29,
            custom_id="pw",
        ),
        disnake.ui.TextInput(
            label="큰 사진",
            placeholder="좌측에 나올 큰 사진입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="largeimage",
        ),
        disnake.ui.TextInput(
            label="작은 사진",
            placeholder="큰 사진 우측 하단에 나올 작은 사진입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="smallimage",
        ),
        disnake.ui.TextInput(
            label="큰 사진 글자",
            placeholder="큰 사진에 마우스를 올리면 나타나는 글자입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=50,
            custom_id="largete",
        ),
        disnake.ui.TextInput(
            label="작은 사진 글자",
            placeholder="작은 사진에 마우스를 올리면 나타나는 글자입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=50,
            custom_id="smallte",
        )
        
        ]
        super().__init__(
            title=f"RPC 사진 설정",
            custom_id="photo1",
            components=components,
            timeout=10000
        )

class Button(disnake.ui.Modal):
    def __init__(self):

        components = [
        disnake.ui.TextInput(
            label="라이선스",
            placeholder="지급받은 라이선스입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=29,
            custom_id="pw",
        ),
        disnake.ui.TextInput(
            label="상단버튼 텍스트",
            placeholder="상단 버튼에 표시될 텍스트입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="button1",
        ),
        disnake.ui.TextInput(
            label="하단버튼 텍스트",
            placeholder="하단 버튼에 표시될 텍스트입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="button2",
        ),
        disnake.ui.TextInput(
            label="상단 버튼 링크",
            placeholder="상단 버튼을 누르면 연결되는 링크입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=2000,
            custom_id="button1link",
        ),
        disnake.ui.TextInput(
            label="하단 버튼 링크",
            placeholder="하단 버튼을 누르면 연결되는 링크입니다.",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=2000,
            custom_id="button2link",
        )
        
        ]
        super().__init__(
            title=f"RPC 버튼 설정",
            custom_id="button1",
            components=components,
            timeout=10000
        )

class Ment(disnake.ui.Modal):
    def __init__(self):

        components = [
        disnake.ui.TextInput(
            label="라이선스",
            placeholder="지급받은 라이선스입니다.",
            required=True,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=29,
            custom_id="pw",
        ),
        disnake.ui.TextInput(
            label="상단멘트",
            placeholder="상단 멘트",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="details",
        ),
        disnake.ui.TextInput(
            label="하단멘트",
            placeholder="하단 멘트",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=300,
            custom_id="state",
        ),
        disnake.ui.TextInput(
            label="상태메시지 + 제목",
            placeholder="상태메시지 + 제목",
            required=False,
            style=disnake.TextInputStyle.short,
            min_length=1,
            max_length=20,
            custom_id="name",
        )
        
        ]
        super().__init__(
            title=f"RPC 멘트 설정",
            custom_id="ment1",
            components=components,
            timeout=10000
        )
"""@bot.command()
async def 생성(ctx, date: int):
    if not ctx.author.id == int(978910234166820864):
        return
    license_key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))

    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO licenses VALUES (?, ?)', (license_key, date))
    conn.commit()
    conn.close()

    await ctx.send(f'랜덤 라이센스: {license_key}\n날짜: {date}')"""




@bot.slash_command()
async def 등록(interaction: disnake.ApplicationCommandInteraction, license: str):
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()

    # 라이센스 조회 및 date 값을 가져옴
    cursor.execute('SELECT licenses, date FROM licenses WHERE licenses=?', (license,))
    result = cursor.fetchone()

    if result:
        licenses, date = result
        current_date = datetime.now()

        # date를 정수로 변환하고 현재 날짜에 더해서 만료 날짜 계산
        expiration_date = (current_date + timedelta(days=int(date))).strftime('%Y-%m-%d')

        # 라이센스 삭제
        cursor.execute('DELETE FROM licenses WHERE licenses=?', (license,))
        conn.commit()
        conn.close()

        try:
            with open('config.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []

        new_entry = {
            "id": str(interaction.author.id),
            "pw": license,
            "token": "",
            "prefix": "",
            "embed": False,
            "day": expiration_date,
            "type": "",
            "details": "",
            "state": "",
            "name": "",
            "largeimage": "",
            "smallimage": "",
            "largete": "",
            "smallte": "",
            "button1": "",
            "button2": "",
            "button1link": "",
            "button2link": ""
        }


        data['tokens'].append(new_entry)

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


        await interaction.response.send_message(embed=disnake.Embed(title="```등록완료!```", description=f'라이선스가 등록되었습니다.\n만료일: ```{expiration_date}```', color=0x59ff85), ephemeral=False)
    else:
        conn.close()
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description=f'라이선스가 존재하지 않습니다.', color=0xff4040), ephemeral=False)



@bot.slash_command(name='패널', description='RPC 세팅 패널')
async def 패널(interaction: disnake.ApplicationCommandInteraction):
    select = disnake.ui.Select(
        custom_id="testselect",
        placeholder="설정하려는 옵션을 선택해주세요.",
        options=[
            disnake.SelectOption(label="기본설정", description="RPC 기본설정 입니다.", emoji="<:HammerAndSpanner:1147091339348029543>", value="setting"),
            disnake.SelectOption(label="멘트설정", description="RPC에 뜨는 멘트관련 설정입니다.", emoji="<:HammerAndSpanner:1147091339348029543>", value="ment"),
            disnake.SelectOption(label="사진설정", description="RPC에 뜨는 사진관련 설정입니다.", emoji="<:HammerAndSpanner:1147091339348029543>", value="photo"),
            disnake.SelectOption(label="버튼설정", description="RPC에 뜨는 버튼관련 설정입니다.", emoji="<:HammerAndSpanner:1147091339348029543>", value="button"),
        ],
    )

    view = disnake.ui.View()
    view.add_item(select)
    await interaction.response.send_message(embed=disnake.Embed(title="```RPC 설정 패널```", description="RPC 세부사항을 설정할수 있는 패널입니다.", color=0x3D9EF4), ephemeral=True, view=view)

@bot.slash_command(name='생성', description='라이선스 생성 명령어')
async def 생성(interaction: disnake.ApplicationCommandInteraction, date: int):
    if not interaction.author.id =z= int(978910234166820864):
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='권한이 없습니다.', color=0xff4040), ephemeral=False)
    if date == int(0):
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='기한을 입력해주세요.', color=0xff4040), ephemeral=True)
    #license_key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)).join('-').join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)).join('-').join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)).join('-').join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)).join('-').join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    license_key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    conn = sqlite3.connect('license.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO licenses VALUES (?, ?)', (license_key, date))
    conn.commit()
    conn.close()
    await interaction.response.send_message(embed=disnake.Embed(title="```라이선스가 생성되었습니다.```", description=f'라이선스 키 : ```{license_key}```\n라이선스 기간 : ```{date}```', color=0x59ff85), ephemeral=True)
    await interaction.response.send_message({license_key})
    #await interaction.send(f'랜덤 라이센스: {license_key}\n날짜: {date}')    

@bot.slash_command()
async def 라이선스확인(interaction: disnake.ApplicationCommandInteraction):
    config = load_config()
    userid = str(interaction.user.id)
    licenval = ""
    for user_config in config['tokens']:
        if user_config.get("id") == userid:
            licenval = user_config.get("pw")
            await interaction.response.send_message(embed=disnake.Embed(title="```라이선스 조회가 완료되었습니다.```", description=f'라이선스 키 : ```{licenval}```', color=0x59ff85), ephemeral=True)
            


@bot.event
async def on_interaction(interaction: disnake.MessageInteraction):
    if interaction.type == disnake.InteractionType.component:
        if interaction.data.custom_id == "testselect":
            selected = interaction.data.values[0]
            
            if selected == 'setting':
                await interaction.response.send_modal(Setting())
                try:
                    modal_inter: disnake.ModalInteraction = await bot.wait_for(
                        "modal_submit",
                        check=lambda i: i.custom_id == "setting1" and i.author.id == interaction.author.id,
                        timeout=10000,
                    )

                except asyncio.TimeoutError:
                    return
                
                config = load_config()
                user_id = str(interaction.user.id)
                pw = modal_inter.text_values["pw"]


                for user_config in config['tokens']:
                    if user_config.get("id") == user_id and user_config.get("pw") == pw:
                        user_config['token'] = modal_inter.text_values["token"]
                        #user_config['type'] = modal_inter.text_values["type"]
                        user_config['type'] = "PLAYING"
                        user_config['prefix'] = modal_inter.text_values["prefix"]
                        save_config(config)
                        await modal_inter.send(embed=disnake.Embed(title="```적용완료!```", description=f'세팅이 저장되었습니다.', color=0x59ff85), ephemeral=True)
                        return

                await modal_inter.send(embed=disnake.Embed(title="```오류!```", description=f'ID 또는 PW가 일치하지 않습니다.', color=0xff4040), ephemeral=True)

            if selected == 'ment':
                await interaction.response.send_modal(Ment())
                try:
                    modal_inter: disnake.ModalInteraction = await bot.wait_for(
                        "modal_submit",
                        check=lambda i: i.custom_id == "ment1" and i.author.id == interaction.author.id,
                        timeout=10000,
                    )

                except asyncio.TimeoutError:
                    return
                
                config = load_config()
                user_id = str(interaction.user.id)
                pw = modal_inter.text_values["pw"]

                for user_config in config['tokens']:
                    if user_config.get("id") == user_id and user_config.get("pw") == pw:
                        user_config['details'] = modal_inter.text_values["details"]
                        user_config['state'] = modal_inter.text_values["state"]
                        user_config['name'] = modal_inter.text_values["name"]
                        save_config(config)
                        await modal_inter.send(embed=disnake.Embed(title="```적용완료!```", description=f'세팅이 저장되었습니다.', color=0x59ff85), ephemeral=True)
                        return

                await modal_inter.send(embed=disnake.Embed(title="```오류!```", description=f'ID 또는 PW가 일치하지 않습니다.', color=0xff4040), ephemeral=True)

            if selected == 'photo':
                await interaction.response.send_modal(Photo())
                try:
                    modal_inter: disnake.ModalInteraction = await bot.wait_for(
                        "modal_submit",
                        check=lambda i: i.custom_id == "photo1" and i.author.id == interaction.author.id,
                        timeout=10000,
                    )

                except asyncio.TimeoutError:
                    return
                
                config = load_config()
                user_id = str(interaction.user.id)
                pw = modal_inter.text_values["pw"]

                for user_config in config['tokens']:
                    if user_config.get("id") == user_id and user_config.get("pw") == pw:
                        user_config['largeimage'] = modal_inter.text_values["largeimage"]
                        user_config['smallimage'] = modal_inter.text_values["smallimage"]
                        user_config['largete'] = modal_inter.text_values["largete"]
                        user_config['smallte'] = modal_inter.text_values["smallte"]
                        save_config(config)
                        await modal_inter.send(embed=disnake.Embed(title="```적용완료!```", description=f'세팅이 저장되었습니다.', color=0x59ff85), ephemeral=True)
                        return

                await modal_inter.send(embed=disnake.Embed(title="```오류!```", description=f'ID 또는 PW가 일치하지 않습니다.', color=0xff4040), ephemeral=True)

            if selected == 'button':
                await interaction.response.send_modal(Button())
                try:
                    modal_inter: disnake.ModalInteraction = await bot.wait_for(
                        "modal_submit",
                        check=lambda i: i.custom_id == "button1" and i.author.id == interaction.author.id,
                        timeout=10000,
                    )

                except asyncio.TimeoutError:
                    return
                
                config = load_config()
                user_id = str(interaction.user.id)
                pw = modal_inter.text_values["pw"]

                for user_config in config['tokens']:
                    if user_config.get("id") == user_id and user_config.get("pw") == pw:
                        user_config['button1'] = modal_inter.text_values["button1"]
                        user_config['button2'] = modal_inter.text_values["button2"]
                        user_config['button1link'] = modal_inter.text_values["button1link"]
                        user_config['button2link'] = modal_inter.text_values["button2link"]
                        save_config(config)
                        await modal_inter.send(embed=disnake.Embed(title="```적용완료!```", description=f'세팅이 저장되었습니다.', color=0x59ff85), ephemeral=True)
                        return

                await modal_inter.send(embed=disnake.Embed(title="```오류!```", description=f'ID 또는 PW가 일치하지 않습니다.', color=0xff4040), ephemeral=True)


@bot.event
async def on_ready():
    activity = disnake.Game(name="XH RPC 관련 일")
    await bot.change_presence(status=disnake.Status.idle, activity=activity)
    print("Bot is ready!")

bot.run(token)
