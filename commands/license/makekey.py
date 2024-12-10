import disnake, asyncio, json, random, sqlite3, os, httpx, requests
from disnake.ext import commands
from datetime import datetime, timedelta
from enum import Enum
intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
import subprocess

def setup(bot):
    @bot.slash_command(name='제품키', description='라이선스 관리 명령어입니다.')
    async def 제품키(interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.send_message(embed=disnake.Embed(title="**<:X_:1141002622896185426> | 오류 발생**", description='하위 명령어를 입력해주세요!', color=0xff4040), ephemeral=False)


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
