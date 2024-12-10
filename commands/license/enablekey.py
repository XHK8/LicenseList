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
    @bot.slash_command(name='정품복구', description='해제된 정품인증 복구 명령어')
    async def 정품복구(
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