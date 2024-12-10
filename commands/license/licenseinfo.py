import disnake, asyncio, json, random, sqlite3, os, httpx, requests
from disnake.ext import commands
from datetime import datetime, timedelta
from enum import Enum
intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
import subprocess

def  load_config():
    with open('config.json', 'r', encoding="utf-8") as file:
        return json.load(file)

def  save_config(data):
    with open('config.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def setup(bot):
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

