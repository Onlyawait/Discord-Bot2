import discord 
from discord.ext import commands
from discord.ui import Select , View
import requests
from discord.ext.commands import has_permissions, guild_only
import os
import asyncio
import random
bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
counter = 0
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("[x] Successfully Login", bot.user)
    print("[x] Ready")
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("Made By Await/IG: _824"))

@bot.tree.command(name="anime")
async def _animeinfo(ctx: discord.Interaction, name: str):
    channel_id = 775731171782295592  # replace with your channel ID
    if ctx.channel_id == channel_id:
        data = GetAnimeName(name)
        options = []
        for i, r in enumerate(data):
            options.append(discord.SelectOption(label=r))
        g = Select(options=options, placeholder="choose which anime,")
        async def my_callback(send: discord.Interaction):
            try:
                await send.response.edit_message(content="I'll try to garb the info for you", view=None)
                embed = await GetAnimeInfo(g.values[0])
                await send.followup.send(embed=embed)
            except Exception as e:
                await send.followup.send(content=f"hentai is big No No {ctx.user.mention}", ephemeral=True)
        view = View()
        view.add_item(g)
        g.callback = my_callback
        await ctx.response.send_message(view=view , ephemeral=True)
    else:
        await ctx.response.send_message(f"u can only use this command in: <#{channel_id}>", ephemeral=True)    

async def GetAnimeInfo(AnimeName: str):
    url = "https://api.myanimelist.net/v3/search"
    params = {
    "fields": "anime{alternative_titles,media_type,genres,num_episodes,status,start_date,end_date,average_episode_duration,synopsis,mean,rank,popularity,num_list_users,num_favorites,num_scoring_users,start_season,broadcast,my_list_status{start_date,finish_date},favorites_info,nsfw,created_at,updated_at},manga{id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,num_volumes,num_chapters,favorites_info,my_list_status{start_date,finish_date,tags,priority,num_times_reread,reread_value},authors{first_name,last_name},serialization{name}}",
    "limit": "50",
    "offset": "0",
    "q": AnimeName,
    "type": "anime"
    }
    headers = {
        "Accept": "application/json",
        "User-Agent": "MAL (ios, 197)",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Mal-Client-Id": "6591a087c62b3e94d769cd8e35ffe909",
        "Cache-Control": "public, max-age=60"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()["data"]
    x = -1
    for i in data:
        x+=1
        r = str(data[x]["node"]["anime"]["title"]).lower()
        # print(r)
        if r == AnimeName.lower():
            getinfo = data[x]["node"]["anime"]
            AnimeImageUrl = getinfo['main_picture']['medium']
            Rating = getinfo['mean']
            media_type = getinfo['media_type']
            status = getinfo['status']
            year = getinfo['start_season']['year']
            season = getinfo['start_season']['season']
            embed = discord.Embed(
            title=AnimeName,
            color=0x000000
            )
            user_id = 602929951519408133  # Replace with the actual user ID
            user = await bot.fetch_user(user_id)
            # embed.set_author(name=title, icon_url=AnimeImageUrl)
            embed.set_footer(text="by await : IG _824",
                            icon_url=user.avatar.url)
            if status == "finished_airing":
                num_episodes = getinfo['num_episodes']
                embed.add_field(name='episodes', value=num_episodes, inline=True)
            elif status == "currently_airing":
                broadcast = getinfo['broadcast']
                day_of_the_week = broadcast['day_of_the_week']
                start_time = broadcast['start_time']
                embed.add_field(name='broadcast', value=f"{day_of_the_week}:{start_time}", inline=True) 
            embed.add_field(name='score', value=Rating, inline=True)
            embed.add_field(name='season', value=season, inline=True)
            embed.add_field(name='year', value=year, inline=True)
            embed.add_field(name='type', value=media_type, inline=True)
            embed.add_field(name='status', value=str(status).replace("_"," "), inline=True)
            embed.set_thumbnail(url=AnimeImageUrl)
            return embed
def GetAnimeName(Animename: str):
    response = requests.get(f"https://myanimelist.net/search/prefix.json?type=anime&keyword={Animename}&v=1")
    data = response.json()["categories"]
    names = []  # List to hold all anime names
    for category in data:
        for item in category["items"]:
            name = item["name"]
            names.append(name)  # Add each name to the list
    return names
def check_database(AnimeName, NumberOfEpisode):
    with open('Json.txt', 'r', encoding='utf-8') as file:
        read_from_txt = file.read()
        if f'"anime_name":"{AnimeName}","episode_name":"{NumberOfEpisode}",' in read_from_txt:
            return False
    return True
async def write_data_json(AnimeName, AnimeEpisode, drive_url, mega_url):
    data = ""
    with open('Json.txt', 'r', encoding='utf-8') as file:
        read_from_txt = file.readlines()

    for line in read_from_txt:
        gg = f',{{"anime_name":"{AnimeName}","episode_name":"{AnimeEpisode}","video_url_drive":"{drive_url}","video_url_mega":"{mega_url}"}},]'
        data = line.replace(",]", gg)

    os.remove('Json.txt')

    with open('Json.txt', 'a', encoding='utf-8') as file:
         file.write(data)

@_animeinfo.error
async def select_error(ctx: discord.Interaction, error):
    await ctx.response.send_message("no anime found try again.", ephemeral=True)

# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
#     
bot.run("MTEzMDI1NTk4MTYzMzM0NzY2NQ.GY-Mcp.IewKbIIXvdTG6-mkqtHZirDNu7LF8LvgKaV0PA")



