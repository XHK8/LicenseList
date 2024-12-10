import disnake, asyncio, json, random, sqlite3, os, httpx, requests
from disnake.ext import commands
from datetime import datetime, timedelta
from enum import Enum
intents = disnake.Intents.default()
intents.message_content = True  # 메시지 내용 인텐트 활성화
import subprocess

fdpath = os.getcwd()

def UpdateConfigWithForce(folderpath, commitmsg):
    try:
        # git add 실행
        subprocess.run(['git', '-C', folderpath, 'add', '.'], check=True)
        
        # git commit 실행, 출력 캡처
        commit_result = subprocess.run(
            ['git', '-C', folderpath, 'commit', '-m', commitmsg],
            check=False,  # 오류를 발생시키지 않도록 설정
            capture_output=True,  # 출력 캡처
            text=True  # 문자열 형식으로 출력 처리
        )
        
        # 'nothing to commit' 메시지 확인
        if "nothing to commit, working tree clean" in commit_result.stdout.lower():
            return "NOTHING_TO_COMMIT"
        
        # git push 실행
        subprocess.run(['git', '-C', folderpath, 'push', '-u', 'origin', 'main', '--force'], check=True)
        return "SUCCESS"
    except subprocess.CalledProcessError:
        return "FAILURE"

def  load_config():
    with open('config.json', 'r', encoding="utf-8") as file:
        return json.load(file)

def  save_config(data):
    with open('config.json', 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def setup(bot):
    @bot.slash_command(name='db갱신', description='DB를 강제로 갱신합니다.')
    async def db갱신(interaction: disnake.ApplicationCommandInteraction):
        await interaction.response.defer()
        result = UpdateConfigWithForce(folderpath=fdpath, commitmsg="DB갱신")
        if result == "SUCCESS":
            embed = disnake.Embed(
                title="**<:CHECK:1141002471297253538> | 갱신 성공**",
                description=">>> 정품인증 DB 갱신에 성공하였습니다.",
                color=0x59ff85
            )
        elif result == "NOTHING_TO_COMMIT":
            embed = disnake.Embed(
                title="**<:Caution:1144625795059433543> | 갱신 불필요**",
                description=">>> 변경된 내용이 없어 갱신이 필요하지 않습니다.",
                color=0xFFBE57
            )
        else:  # FAILURE
            embed = disnake.Embed(
                title="**<:X_:1141002622896185426> | 갱신 실패**",
                description=">>> 정품인증 DB 갱신에 실패하였습니다.",
                color=0xff4040
            )
        await interaction.edit_original_response(embed=embed)