import discord
from discord.enums import Status
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re


def set(nickname):

    url = "https://www.op.gg/summoner/userName="+ nickname
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    global 놀리기, 최근전적, 연승연패, 현재티어, lr, wlr, kstatus

    tier_rank = soup.find("div",{"class":"TierRank"})
    tier = re.sub('\d', '', tier_rank.get_text())
    tiern = re.sub('\D', '', tier_rank.get_text())

    ktier = ("아" if tier == "Iron "
                else "브" if tier == "Bronze "
                else "실" if tier == "Silver "
                else "골" if tier == "Gold "
                else "플" if tier == "Platinum "
                else "다" if tier == "Diamond "
                else "마" if tier == "Master"
                else "그마" if tier == "Grandmaster"
                else "챌" if tier == "Challenger"
                else "error")
    ktier = ktier + tiern

    lp = soup.find("span",{"class":"LeaguePoints"})
    lp = re.sub("	|\n","",lp.get_text())

    recent_status_total = soup.find("span",{"class":"total"})
    recent_status_win = recent_status_total.find_next_sibling()
    recent_status_lose = recent_status_win.find_next_sibling()

    wins = re.sub('\D','',soup.find("span",{"class":"wins"}).get_text())
    losses = re.sub('\D','',soup.find("span",{"class":"losses"}).get_text())
    현재티어 = f"현재 티어 : {tier_rank.get_text()} | {lp}"
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

    kstatus = re.sub('Victory','O ',str(status[0:20]))
    kstatus = re.sub('Defeat','X ',kstatus)
    kstatus = re.sub("\[|\]|\,|'","",kstatus)




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
    else :
        if message.content.startswith("!최근전적"):
            try :
                set(message.content[6:])
                mes = 최근전적+"\n"+kstatus+"\n"
                if lr > 1 :
                    if wlr == "연승" :
                        mes += f"{연승연패}중... 이제 질 타이밍 ㄹㅇㅋㅋ"
                    else :
                        mes += f"{message.content[6:]} 현재 {연승연패}중 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ 쭉 흐름타고 아이언까지 가보자"
                await message.channel.send(mes)
            except :
                await message.channel.send("그런 계정 없는데 닉네임 다시 확인 ㄱㄱ")
        elif message.content.startswith("!티어"):
            try :
                set(message.content[4:])
                await message.channel.send(현재티어+"\n"+놀리기)  
            except :
                await message.channel.send("그런 계정 없는데 닉네임 다시 확인 ㄱㄱ")

        elif message.content == "!help" :
            await message.channel.send("""**명령어리스트**    
            - !안녕
            - !티어 [닉네임]
            - !최근전적 [닉네임]
            - !help""")  

app.run('')


