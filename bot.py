import disnake, asyncio, json, random, sqlite3, os, httpx, requests
from disnake.ext import commands
from datetime import datetime, timedelta
from enum import Enum
intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

import subprocess

token = "MTI2ODg5Mjk5MzAxNzA5MDE4OA.Gho32W._OzbYmRhcHc5okdn-Dct2nZLHKvn7OLbjiNdYo" # 봇토큰

fdpath = os.getcwd()

def UpdateConfig(folderpath, commitmsg):
    try:
        subprocess.run(['git', '-C', folderpath ,'add', '.'], check=True)
        subprocess.run(['git', '-C', folderpath, 'commit', '-m', commitmsg], check=True)
        subprocess.run(['git', '-C', folderpath, 'push', '-u', 'origin', 'main'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False

def UpdateConfigWithForce(folderpath, commitmsg):
    try:
        subprocess.run(['git', '-C', folderpath ,'add', '.'], check=True)
        subprocess.run(['git', '-C', folderpath, 'commit', '-m', commitmsg], check=True)
        subprocess.run(['git', '-C', folderpath, 'push', '-u', 'origin', 'main', '--force'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def  load_config():
    with open('config.json', 'r', encoding="utf-8") as file:
        return json.load(file)

def  save_config(data):
    with open('config.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def getInviteCode(invite_code):
    if "discord.gg" not in invite_code:
        return invite_code
    if "discord.gg" in invite_code:
        invite = invite_code.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_code:
        invite = invite_code.split("https://discord.gg/")[1]
        return invite

Products = commands.option_enum({"ElecCity": "ec", "⭐⭐⭐⭐": "⭐⭐⭐⭐", "⭐⭐⭐": "⭐⭐⭐", "⭐⭐": "⭐⭐" , "⭐": "⭐"})

Models = commands.Param(choices=["ElecCity"]),

class Products(str, Enum):
    Electity = 'eleccity'


@bot.slash_command(name='제품키', description='라이선스 관리 명령어입니다.')
async def 제품키(interaction: disnake.ApplicationCommandInteraction):
    interaction.response.send_message(embed=disnake.Embed(title="**<:X_:1141002622896185426> | 오류 발생**", description='하위 명령어를 입력해주세요!', color=0xff4040), ephemeral=False)


@제품키.sub_command(name='생성', description="라이선스 생성 명령어")
async def 생성(
    interaction: disnake.ApplicationCommandInteraction,
    count: int,
    modelname: str = commands.Param(choices=["ElecCity"])
):
    if interaction.author.id == int(978910234166820864):
        if count == None:
            await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='제품 키 개수를 입력하세요.', color=0xff4040), ephemeral=False)
        else:
            if modelname == "ElecCity":
                licensetxt = open('licenses.txt', 'w')
                for i in range(count):
                    license_key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)) + "-" + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
                    conn = sqlite3.connect('eleccity.db')
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO licenses VALUES (?)', (license_key,))
                    licensetxt.write(f"{license_key}\n")
                    conn.commit()
                    conn.close()
                licensetxt.close()
                await interaction.response.send_message(embed=disnake.Embed(title="**<:CHECK:1141002471297253538> | 제품 키 생성 성공**", description=f"{modelname}의 라이선스를 {count}개 많큼 생성했어요!\n아래 파일을 열어 생성된 라이선스 키를 확인해보세요!", color=0x59ff85), file=disnake.File("licenses.txt"),)
                os.remove("licenses.txt")
    else:
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='권한이 없습니다.', color=0xff4040), ephemeral=False)

@bot.slash_command(name='정품인증', description='라이선스 등록 명령어')
async def 정품인증(
    interaction: disnake.ApplicationCommandInteraction,
    key: str,
    gameid: int,
    discordlink: str,
    modelname: str = commands.Param(choices=["ElecCity"])):
    if modelname == "ElecCity":
        conn = sqlite3.connect('eleccity.db')
        cursor = conn.cursor()
        cursor.execute('SELECT licenses FROM licenses WHERE licenses=?', (key,))
        result = cursor.fetchone()
        discordlink = getInviteCode(discordlink)
        invite_url = f"https://discord.com/api/v9/invites/{discordlink}"
        roblox_game_url = f"https://www.roblox.com/ko/games/{gameid}/"
        response = requests.get(invite_url)
        game_res = requests.get(roblox_game_url)
        if result:
            if response.status_code == 200:
                if game_res.status_code == 200:
                    licenses = result
                    cursor.execute('DELETE FROM licenses WHERE licenses=?', (key,))
                    conn.commit()
                    conn.close()
                    try:
                        with open('config.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                    except FileNotFoundError:
                        data = []

                    new_entry = {
                        "product" : "Eleccity",
                        "registerer": str(interaction.author.id),
                        "licensecode": key,
                        "gameid": str(gameid),
                        "discordlink": discordlink,
                        "licensed": True
                    }

                    data['eleccity'].append(new_entry)

                    with open('config.json', 'w', encoding='utf-8') as file:
                        json.dump(data, file, ensure_ascii=False, indent=4)

                    await interaction.response.send_message(embed=disnake.Embed(title="**<:CHECK:1141002471297253538> | 정품 인증 성공**", description=f">>> **일렉시티** 제품이 정품 인증되었습니다. \n\n**게임링크:** [**여기**를 눌러 이동하세요.](https://www.roblox.com/ko/games/{gameid})\n**디스코드 초대링크:** [**여기**를 눌러 이동하세요.](https://discord.gg/{discordlink})\n**정품 인증 코드: **``{key}``\n\n**(정품 인증 키는 한 키당 한 게임에서 사용이 가능하며, 추가 발급은 문의티켓을 개설해주시면 도와드리겠습니다.)**\n**(정품 인증 키는 정품 인증 조회때도 사용되오니 키를 분실하지 않도록 각별히 주의하시기 바랍니다.)**", color=0x59ff85))
                else:
                    await interaction.response.send_message(embed=disnake.Embed(title="**<:X_:1141002622896185426> | 오류 발생**", description='게임 아이디가 올바르지 않습니다.', color=0xff4040))
            else:
                await interaction.response.send_message(embed=disnake.Embed(title="**<:X_:1141002622896185426> | 오류 발생**", description='올바르지 않은 디스코드 링크입니다.', color=0xff4040))
        else:
            await interaction.response.send_message(embed=disnake.Embed(title="**<:X_:1141002622896185426> | 오류 발생**", description='이 제품 키를 사용하여 **일렉시티** 제품을 정품 인증할수 없습니다.', color=0xff4040), ephemeral=False)



@bot.slash_command(name='정품조회', description='라이선스 조회 명령어')
async def 정품조회(
    interaction: disnake.ApplicationCommandInteraction,
    key: str,
    modelname: str = commands.Param(choices=["ElecCity"])
    ):
    if modelname == "ElecCity":
        conn = sqlite3.connect('eleccity.db')
        cursor = conn.cursor()
        config = load_config()
        code = key
        found = False
        for data in config['eleccity']:
            if data.get("licensecode") == key:
                found = True
                registerer = data.get("registerer")
                licensecode = data.get("licensecode")
                gameid = data.get("gameid")
                discordcode = data.get("discordlink")
                discordlink = "https://discord.gg/" + discordcode
                licensed = data.get("licensed")
                rbgmlink = f"https://www.roblox.com/ko/games/{gameid}/"
                if licensed == True:
                    await interaction.response.send_message(
                        embed=disnake.Embed(
                            title="**<:CHECK:1141002471297253538> | 정품인증 조회 완료**",
                            description=(
                                f">>> 아래의 게임에서 **일렉시티** 제품이 정품 인증되어있습니다. \n\n"
                                f"**등록인: <@{registerer}>**\n"
                                f"**게임링크:** [**여기**를 눌러 이동하세요.]({rbgmlink})\n"
                                f"**디스코드 초대링크:** [**여기**를 눌러 이동하세요.]({discordlink})\n"
                                f"**조회 ID:** ``{key}``\n"
                                f"**승인여부:** ``{licensed}``"
                            ),
                            color=0x59ff85
                            )
                        )
                elif licensed == False:
                    await interaction.response.send_message(
                        embed=disnake.Embed(
                            title="**<:CHECK:1141002471297253538> | 정품인증 조회 완료**",
                            description=(
                                f">>> 아래의 게임에서 **일렉시티** 제품이 정품 인증되어있지 않습니다. \n\n"
                                f"**등록인: <@{registerer}>**\n"
                                f"**게임링크:** [**여기**를 눌러 이동하세요.]({rbgmlink})\n"
                                f"**디스코드 초대링크:** [**여기**를 눌러 이동하세요.]({discordlink})\n"
                                f"**조회 ID:** ``{key}``\n"
                                f"**승인여부:** ``{licensed}``"
                            ),
                            color=0xff4040
                            )
                        )
            else:
                pass
        if not found:  # 루프가 끝날 때까지 키가 발견되지 않음
            await interaction.response.send_message(
                embed=disnake.Embed(
                    title="**<:X_:1141002622896185426> | 조회 실패**",
                    description=(
                        f">>> 입력하신 ID ``{key}``에 대한 정품 인증 정보를 찾을 수 없습니다. \n"
                        "입력한 ID가 정확한지 확인하시고 다시 시도해주세요."
                    ),
                    color=0xff4040
                )
                )
        else:
            pass
    
        
@bot.slash_command(name='정품해제', description='정품 해제 명령어')
async def 정품해제(
    interaction:disnake.ApplicationCommandInteraction,
    key: str,
    modelname: str = commands.Param(choices=["ElecCity"])
):
    if interaction.author.id == int(978910234166820864):
        if modelname == "ElecCity":
            config = load_config()
            code = key
            found = False
            for data in config['eleccity']:
                if data.get("licensecode") == key:
                    found = True
                    found = True
                    registerer = data.get("registerer")
                    licensecode = data.get("licensecode")
                    gameid = data.get("gameid")
                    discordcode = data.get("discordlink")
                    discordlink = "https://discord.gg/" + discordcode
                    licensed = data.get("licensed")
                    rbgmlink = f"https://www.roblox.com/ko/games/{gameid}/"

                    data['licensed'] = False

                    
                    await interaction.response.send_message(
                        embed=disnake.Embed(
                            title="**<:CHECK:1141002471297253538> | 정품인증 해제 성공**",
                            description=(
                                f">>> 해당 키로 인증된 게임의 정품을 인증을 해제하였습니다.\n아래는 정품인증 정보입니다. \n\n"
                                f"**등록인: <@{registerer}>**\n"
                                f"**게임링크:** [**여기**를 눌러 이동하세요.]({rbgmlink})\n"
                                f"**디스코드 초대링크:** [**여기**를 눌러 이동하세요.]({discordlink})\n"
                                f"**조회 ID:** ``{key}``\n"
                                f"**승인여부:** ``False``"
                            ),
                            color=0x59ff85
                            )
                        )
            if not found:
                await interaction.response.send_message(
                    embed=disnake.Embed(
                        title="**<:X_:1141002622896185426> | 정품인증 해제 실패**",
                        description=(
                            f">>> 해당 키로 인증된 게임의 정품 인증 정보를 찾을수 없습니다.\n아래는 정품인증 정보입니다. \n\n"
                            f"**정품인증 해제 시도 제품키:** ``{key}``"
                        ),
                            color=0x59ff85
                            )
                        )
    else:
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='권한이 없습니다.', color=0xff4040), ephemeral=False)


@bot.slash_command(name='정품복구', description='해제된 정품인증 복구 명령어')
async def 정품해제(
    interaction:disnake.ApplicationCommandInteraction,
    key: str,
    modelname: str = commands.Param(choices=["ElecCity"])
):
    if interaction.author.id == int(978910234166820864):
        if modelname == "ElecCity":
            config = load_config()
            code = key
            found = False
            for data in config['eleccity']:
                if data.get("licensecode") == key:
                    found = True
                    found = True
                    registerer = data.get("registerer")
                    licensecode = data.get("licensecode")
                    gameid = data.get("gameid")
                    discordcode = data.get("discordlink")
                    discordlink = "https://discord.gg/" + discordcode
                    licensed = data.get("licensed")
                    rbgmlink = f"https://www.roblox.com/ko/games/{gameid}/"

                    data['licensed'] = True
                    save_config(config)
                    await interaction.response.send_message(
                        embed=disnake.Embed(
                            title="**<:CHECK:1141002471297253538> | 정품인증 복구 완료**",
                            description=(
                                f">>> 해당 키로 인증된 게임의 해제된 정품 인증을 복구하였습니다.\n아래는 정품인증 정보입니다. \n\n"
                                f"**등록인: <@{registerer}>**\n"
                                f"**게임링크:** [**여기**를 눌러 이동하세요.]({rbgmlink})\n"
                                f"**디스코드 초대링크:** [**여기**를 눌러 이동하세요.]({discordlink})\n"
                                f"**조회 ID:** ``{key}``\n"
                                f"**승인여부:** ``True``"
                            ),
                            color=0x59ff85
                            )
                        )
            if not found:
                await interaction.response.send_message(
                    embed=disnake.Embed(
                        title="**<:X_:1141002622896185426> | 정품인증 복구 실패**",
                        description=(
                            f">>> 해당 키로 인증된 게임의 정품 인증 정보를 찾을수 없습니다.\n아래는 정품인증 정보입니다. \n\n"
                            f"**정품인증 해제 시도 제품키:** ``{key}``"
                        ),
                            color=0xff4040
                            )
                        )    
    else:
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='권한이 없습니다.', color=0xff4040), ephemeral=False)



@bot.slash_command(name='db갱신', description='DB를 갱신합니다.')
async def db갱신(
    interaction: disnake.ApplicationCommandInteraction    
):
    result = UpdateConfig(folderpath=fdpath, commitmsg="DB갱신")

    if result:
        await interaction.response.send_message(
            embed=disnake.Embed(
                title="**<:CHECK:1141002471297253538> | 갱신 성공**",
                description=(
                    f">>> 정품인증 DB 갱신에 성공하였습니다."
                ),
                color=0x59ff85
            )
        )   
    else:
        await interaction.response.send_message(
            embed=disnake.Embed(
                title="**<:X_:1141002622896185426> | 갱신 실패**",
                description=(
                    f">>> 정품인증 DB 갱신에 실패하였습니다."
                ),
                color=0xff4040
            )
        )

@bot.slash_command(name='db강제갱신', description='DB를 강제로 갱신합니다.')
async def db강제갱신(
    interaction: disnake.ApplicationCommandInteraction    
):
    await interaction.response.defer()
    result = UpdateConfigWithForce(folderpath=fdpath, commitmsg="DB갱신")

    if result:
        await interaction.edit_original_response(
            embed=disnake.Embed(
                title="**<:CHECK:1141002471297253538> | 갱신 성공**",
                description=(
                    f">>> 정품인증 DB 갱신에 성공하였습니다."
                ),
                color=0x59ff85
            )
        )   
    else:
        await interaction.edit_original_response(
            embed=disnake.Embed(
                title="**<:X_:1141002622896185426> | 갱신 실패**",
                description=(
                    f">>> 정품인증 DB 갱신에 실패하였습니다."
                ),
                color=0xff4040
            )
        )







@제품키.sub_command(name='제거', description='라이선스 제거 명령어')
async def 제거(
    interaction: disnake.ApplicationCommandInteraction,
    count: int,
    modelname: str = commands.Param(choices=["ElecCity"])
):
    if interaction.author.id == int(978910234166820864):
        if count == None:
            await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='라이선스 개수를 입력하세요.', color=0xff4040), ephemeral=False)
        else:
            if modelname == "ElecCity":
                conn = sqlite3.connect('eleccity.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM licenses LIMIT ?', count)
                conn.commit()
                conn.close()
                await interaction.response.send_message(embed=disnake.Embed(title="**<:CHECK:1141002471297253538> | 라이선스 제거 성공**", description=f"아직 등록되지 않은 {modelname} 제품의 라이선스 {count}개를 성공적으로 데이터베이스에서 제거시켰어요."))
    else:
        await interaction.response.send_message(embed=disnake.Embed(title="```오류!```", description='권한이 없습니다.', color=0xff4040), ephemeral=False)
    






















@bot.event
async def on_ready():
    activity = disnake.Game(name="정품인증 서비스")
    await bot.change_presence(status=disnake.Status.idle, activity=activity)
    print("Bot is ready!")

bot.run(token)



