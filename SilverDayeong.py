import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.op.gg/summoner/userName=화면고정망나니"
res = requests.get(url)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")


tier_rank = soup.find("div",{"class":"TierRank"})
tier = re.sub('\d', '', tier_rank.get_text())
tiern = re.sub('\D', '', tier_rank.get_text())

ktier = ("아" if tier == "Iron "
            else "브" if tier == "Bronze "
            else "실" if  tier == "Silver "
            else "error")
ktier = ktier + tiern

lp = soup.find("span",{"class":"LeaguePoints"})
lp = re.sub("	|\n","",lp.get_text())

recent_status_total = soup.find("span",{"class":"total"})
recent_status_win = recent_status_total.find_next_sibling()
recent_status_lose = recent_status_win.find_next_sibling()

wins = re.sub('\D','',soup.find("span",{"class":"wins"}).get_text())
losses = re.sub('\D','',soup.find("span",{"class":"losses"}).get_text())
현재티어 = f"현재 티어 : {tier_rank.get_text()} {lp}"
최근전적 = f"최근 전적 : {recent_status_total.get_text()}전 {recent_status_win.get_text()}승 {recent_status_lose.get_text()}패 (승률 {round(100*(int(recent_status_win.get_text())/int(recent_status_total.get_text())))}%)"
놀리기 = f"{int(wins)+int(losses)}판 {ktier}딱 ㅋㅋ"

status=soup.find_all("div",attrs={"class":"GameResult"})
for i in range(len(status)) :
    status[i] = re.sub('\n|\t','',status[i].get_text())
status.append(0)

i=0
lr = 1
while status[i]==status[i+1] :
    lr+=1
    i+=1
if status[0] == 'Victory' :
    wlr = '연승'
else :
    wlr = '연패'
연승연패 = str(lr)+wlr




app = commands.Bot(command_prefix='!')
 
@app.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(app.user.name)
    print('connection was succesful')
    await app.change_presence(status=discord.Status.online, activity=None)
     
@app.event
async def on_message(message) :
    if message.content == "!안녕" :
        await message.channel.send("hi")
    elif message.content == "!금다형" :
        await message.channel.send(놀리기)
    elif message.content == "!금다형 최근전적":
        await message.channel.send(최근전적)
        if lr > 1 :
            if wlr == "연승" :
                await message.channel.send(f"{연승연패}중... 이제 질 타이밍 ㄹㅇㅋㅋ")
            else :
                await message.channel.send(f"금다형 현재 {연승연패}중 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ 쭉 흐름타고 브론즈까지 가보자")
    elif message.content == "!금다형 티어":
        await message.channel.send(현재티어)   

app.run('토큰은 비밀')


