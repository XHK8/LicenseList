import disnake, asyncio, json, random, sqlite3, os, httpx, requests
from disnake.ext import commands
from datetime import datetime, timedelta
from enum import Enum
intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
import subprocess


def getInviteCode(invite_code):
    if "discord.gg" not in invite_code:
        return invite_code
    if "discord.gg" in invite_code:
        invite = invite_code.split("discord.gg/")[1]
        return invite
    if "https://discord.gg" in invite_code:
        invite = invite_code.split("https://discord.gg/")[1]
        return invite

def setup(bot):
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
