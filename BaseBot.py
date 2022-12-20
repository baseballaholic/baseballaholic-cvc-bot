import json
import requests
from discord.ext import commands
from discord import app_commands
import os
bot = commands.Bot(command_prefix= "$", intents = discord.Intents.all())

# TODOS
# Learn how to do leaderboards
# Improve literally everything if possible

TOKEN = 'ODgxMDA5MjM4OTEzMjA0MjY2.GrBjF9.VGi-9Qo3-leiw6Y9uQl_NHObkleSQA9-_mYPlw'
stats = " "
ign = " "
uuid = " "
oneTimeList = " "
@bot.event
async def on_ready():
    activity = discord.Game(name="Cozy Ranked!")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('We have logged in as {0.user}'.format(bot))
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

async def statshelper(ctx, *, message):
    global stats, ign, uuid, oneTimeList
    try:
        #If they're using a command, grab the username, UUID, and API of that player
        player = message
        uuid = get_uuid(player)
        stats = get_API(uuid)
        #Grab their current username with correct caps
        ign = stats["player"]["displayname"]
        #Create an array and fill it with that player's one time Achievements
        oneTimeList = []
        for i in stats["player"]["achievementsOneTime"]:
            oneTimeList.append(i)
        return True
    except:
        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name="Error", value="Invalid Username/Command")
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)
        return False

#Command to check a player's defusal stats
@bot.tree.command(name="defusal", description="Check a player's defusal stats")
@app_commands.describe(username="Username")
async def defusal(ctx, username: str):
    # THE ORDER OF THE ARRAY: KILLS, DEATHS, WINS, BOMBS PLANTED, BOMBS DEFUSED
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # THE ORDER OF THE ARRAY: KILLS, DEATHS, WINS, BOMBS PLANTED, BOMBS DEFUSED
        defusal_stats = get_cvc_defusal_stats(stats)
        (defusal_kills, defusal_deaths, defusal_wins, bomb_plants, bomb_defused) = defusal_stats

        if defusal_deaths > 0:
            #Calculate the kdr of the player
            defusal_kdr = round(defusal_kills / defusal_deaths, 3)
        else: defusal_kdr = 0

        #Format everything because we don't know the size of the number
        defusal_kills = "{:,}".format(defusal_kills)
        defusal_deaths = "{:,}".format(defusal_deaths)
        bomb_plants = "{:,}".format(bomb_plants)
        bomb_defused = "{:,}".format(bomb_defused)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Defusal Stats:", value=f"Kills: {defusal_kills}\nDeaths: {defusal_deaths}\n"
                                                              f"KDR: {defusal_kdr}\nWins: {defusal_wins}\n"
                                                              f"Bombs Planted: {bomb_plants}\nBombs Defused: {bomb_defused}")
        #Displays the face of their minecraft skin in the top right of the embed (does this with every command where a player is involved)
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

#Command to check a player's tdm stats
@bot.tree.command(name="tdm", description="Check a player's TDM stats")
@app_commands.describe(username="Username")
async def tdm(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # THE ORDER OF THE ARRAY: KILLS, DEATHS, WINS
        tdm_stats = get_cvc_tdm_stats(stats)
        (tdm_kills, tdm_deaths, tdm_wins) = tdm_stats
        if tdm_deaths > 0:
            tdm_kdr = round(tdm_kills / tdm_deaths, 3)
        else: tdm_kdr = 0
        tdm_kills = "{:,}".format(tdm_kills)
        tdm_deaths = "{:,}".format(tdm_deaths)
        tdm_wins = "{:,}".format(tdm_wins)
        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s TDM Stats:", value=f"Kills: {tdm_kills}\nDeaths: {tdm_deaths}\n"
                                                          f"KDR: {tdm_kdr}\nWins: {tdm_wins}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

#Command to check a player's gun game stats
@bot.tree.command(name="gungame", description="Check a player's Gun Game stats")
@app_commands.describe(username="Username")
async def gungame(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # THE ORDER OF THE ARRAY: WINS, KILLS, DEATHS, GAMES PLAYED, FASTEST, CARE, ARMOR, SPEED
        gg_stats = get_cvc_gun_game_stats(stats)
        (gg_wins, gg_kills, gg_deaths, gg_gp, gg_fastest, gg_care, gg_armor, gg_speed) = gg_stats
        if gg_deaths > 0:
            gg_kdr = round(gg_kills / gg_deaths, 3)
        else: gg_kdr = 0
        gg_kills = "{:,}".format(gg_kills)
        gg_deaths = "{:,}".format(gg_deaths)
        gg_wins = "{:,}".format(gg_wins)
        gg_gp = "{:,}".format(gg_gp)
        gg_care = "{:,}".format(gg_care)
        gg_armor = "{:,}".format(gg_armor)
        gg_speed = "{:,}".format(gg_speed)
        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Gun Game Stats:", value=f"Wins: {gg_wins}\nKills: {gg_kills}\n"
                                                               f"Deaths: {gg_deaths}\nKDR: {gg_kdr}\n"
                                                               f"Fastest Time: {gg_fastest}s\n"
                                                               f"Games Played: {gg_gp}\nCare Packages: {gg_care}\n"
                                                               f"Armor Powerups: {gg_armor}\nSpeed Powerups: {gg_speed}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

#Grabs a player's individual map wins and displays them
@bot.tree.command(name="mapwins", description="Check a player's overall map wins")
@app_commands.describe(username="Username")
async def mapwins(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        map_wins = get_cvc_map_wins(stats)
        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Map Wins:", value=f"Alleyway: {map_wins[0]}\n"
                                                         f"Atomic: {map_wins[1]}\nBazaar: {map_wins[2]}\n"
                                                         f"Carrier: {map_wins[3]}\nDerailed: {map_wins[4]}\n"
                                                         f"Junction: {map_wins[5]}\nMelon Factory: {map_wins[6]}\n"
                                                         f"Overgrown: {map_wins[7]}\nReserve: {map_wins[8]}\n"
                                                         f"Sandstorm: {map_wins[9]}\nTemple: {map_wins[10]}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

#Checks a player's combined stats in cvc
@bot.tree.command(name="overall", description="Check a player's overall CvC stats")
@app_commands.describe(username="Username")
async def overall(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # THE ORDER OF THE ARRAY: KILLS, DEATHS, KDR, WINS, GRENADE KILLS, SHOTS FIRED, HS, HS%, COINS)
        overall_stats = get_cvc_overall_stats(stats)
        (overall_kills, overall_deaths, overall_kdr, overall_wins, overall_grenade_kills, overall_shots_fired, overall_headshot_kills,
        overall_headshot_kills_percentage, overall_coins) = overall_stats
        overall_kills = "{:,}".format(overall_kills)
        overall_deaths = "{:,}".format(overall_deaths)
        overall_wins = "{:,}".format(overall_wins)
        overall_grenade_kills = "{:,}".format(overall_grenade_kills)
        overall_shots_fired = "{:,}".format(overall_shots_fired)
        overall_headshot_kills = "{:,}".format(overall_headshot_kills)
        overall_coins = "{:,}".format(overall_coins)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Overall CvC Stats", value=f'Coins: {overall_coins}\n'
                                                                 f'Kills: {overall_kills}\n'
                                                                 f'Deaths: {overall_deaths}\n'
                                                                 f'KDR: {overall_kdr}\n'
                                                                 f'Wins: {overall_wins}\n'
                                                                 f'Headshot Kills: {overall_headshot_kills}\n'
                                                                 f'Headshot Percentage: {overall_headshot_kills_percentage}%\n'
                                                                 f'Shots Fired: {overall_shots_fired}\n'
                                                                 f'Grenade Kills: {overall_grenade_kills}')
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

#Displays the help message
@bot.tree.command(name="cvchelp", description="Displays the help message")
async def cvchelp(ctx):
    embed = discord.Embed(
        title="How to use BaseBot!",
        color=discord.Color.blurple()
    )
    embed.set_thumbnail(url='https://hypixel.net/styles/hypixel-v2/images/game-icons/CVC-64.png')
    embed.add_field(name='General Commands', value='/**help** --> Displays the page you are currently reading\n'
                                                      '/**overall** (name) --> Displays the Overall stats of a player\n'
                                                      '/**tdm** (name) --> Displays the TDM stats of a player\n'
                                                      '/**defusal** (name) --> Displays the Defusal stats of a player\n'
                                                      '/**gungame** (name) --> Displays the Gun Game stats of a player\n'
                                                      '/**mapwins** (name) --> Displays the Map Win stats of a player\n'
                                                      '/**skinsprogress** (name) --> Displays the Skin Progress of a player\n'
                                                      '/**cvctourney1** (name) --> Displays the 1st Hypixel Official CvC Tourney stats of a player\n'
                                                      '/**cvctourney2** (name) --> Displays the 2nd Hypixel Official CvC Tourney stats of a player',
                   inline=False)
    embed.add_field(name='Gun Specific Commands:', value=
                                                      '**Note**: Gun stats have only started tracking with the 2020 update\n'
                                                      '/**pistol** (name) --> Displays the pistol stats of a player\n'
                                                      '/**hk** (name) --> Displays the handgun stats of a player\n'
                                                      '/**deagle** (name) --> Displays the Deagle stats of a player\n'
                                                      '/**sniper** (name) --> Displays the Sniper stats of a player\n'
                                                      '/**p90** (name) --> Displays the P90 stats of a player\n'
                                                      '/**mp5** (name) --> Displays the MP5 stats of a player\n'
                                                      '/**ak** (name) --> Displays the AK stats of a player\n'
                                                      '/**m4** (name) --> Displays the M4 stats of a player\n'
                                                      '/**aug** (name) --> Displays the AUG stats of a player\n'
                                                      '/**shotgun** (name) --> Displays the Shotgun stats of a player\n'
                                                      '/**auto shotgun** (name) --> Displays the Auto Shotgun stats of a player\n')
    embed.set_footer(text="BaseBot by baseballaholic",
                     icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')

    await ctx.response.send_message(embed=embed)

#Displays how close a player is to unlocking all the obtainable gun skins
@bot.tree.command(name="skinsprogress", description="Check a player's CvC skins progress")
@app_commands.describe(username="Username")
async def skinsprogress(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid, oneTimeList
        skin_progress = get_cvc_skins_progress(stats, oneTimeList)
        (pistol_kills, handgun_kills, carbine_kills, scoped_rifle_kills, shotgun_kills, auto_shotgun_kills, magnum_skin, p90_skin,
        mp5_skin, rifle_skin) = skin_progress
        #Requirement: 100 Pistol Headshot Kills
        if pistol_kills > 100:
            pistol_kills = "Unlocked"
        else:
            pistol_kills = (f"{pistol_kills}/100 Pistol Kills")
        #Requirement: 1500 HK Headshot kills
        if handgun_kills > 1500:
            handgun_kills = "Unlocked"
        else:
            handgun_kills = "{:,}".format(handgun_kills)
            handgun_kills = (f"{handgun_kills}/1,500 Handgun Headshot Kills")
        #Requirement: 5000 M4 Kills
        if carbine_kills > 5000:
            carbine_kills = "Unlocked"
        else:
            carbine_kills = "{:,}".format(carbine_kills)
            carbine_kills = (f"{carbine_kills}/5,000 Carbine Kills")
        #Requirement: 2500 AUG Headshot Kills
        if scoped_rifle_kills > 2500:
            scoped_rifle_kills = "Unlocked"
        else:
            scoped_rifle_kills = "{:,}".format(scoped_rifle_kills)
            scoped_rifle_kills = (f"{scoped_rifle_kills}/2,500 Scoped Rifle Headshot Kills")
        #Requirement: 250 Shotgun Headshot Kills
        if shotgun_kills > 200:
            shotgun_kills = "Unlocked"
        else:
            shotgun_kills = "{:,}".format(shotgun_kills)
            shotgun_kills = (f"{shotgun_kills}/250 Shotgun Headshot Kills")
        #Requirement: 7500 Auto Shotty Kills (cringe)
        if auto_shotgun_kills > 7500:
            auto_shotgun_kills = "Unlocked"
        else:
            auto_shotgun_kills = "{:,}".format(auto_shotgun_kills)
            auto_shotgun_kills = (f"{auto_shotgun_kills}/7,500 Auto Shotgun Kills")
        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s CvC Skin Progress", value=f"Pistol       - {pistol_kills}\nHandgun      - {handgun_kills}\n"
                                                                 f"Magnum       - {magnum_skin}\nBullpup      - {p90_skin}\n"
                                                                 f"SMG          - {mp5_skin}\nRifle        - {rifle_skin}\n"
                                                                 f"Carbine      - {carbine_kills}\nScoped Rifle - {scoped_rifle_kills}\n"
                                                                 f"Shotgun      - {shotgun_kills}\nAuto Shotgun - {auto_shotgun_kills}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="pistol", description="Check a player's pistol stats")
@app_commands.describe(username="Username")
async def pistol(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        #ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, KILLS, HEADSHOT, SKIN, CLIP
        pistol_stats = get_cvc_pistol_stats(stats)
        (pistol_damage_increase, pistol_recoil_reduction, pistol_reload_speed_reduction, pistol_kills, pistol_headshots,
        pistol_skin, pistol_ammo_clip) = pistol_stats
        if pistol_headshots > 0: pistol_headshot_ratio = round((pistol_headshots/pistol_kills)*100, 2)
        else: pistol_headshot_ratio = 0
        pistol_kills = "{:,}".format(pistol_kills)
        pistol_headshots = "{:,}".format(pistol_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Pistol Stats", value=f"Damage Increase: {pistol_damage_increase}/9\n"
                                                            f"Recoil Reduction: {pistol_recoil_reduction}/9\n"
                                                            f"Reload Speed Reduction: {pistol_reload_speed_reduction}/9\n"
                                                            f"Kills: {pistol_kills}\n"
                                                            f"Headshot Kills: {pistol_headshots}\n"
                                                            f"Headshot Kill Ratio: {pistol_headshot_ratio}%\n"
                                                            f"Ammo Clip Upgrade: {pistol_ammo_clip}")
        embed.set_image(url=pistol_skin)
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="hk", description="Check a player's HK stats")
@app_commands.describe(username="Username")
async def hk(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        #ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        handgun_stats = get_cvc_handgun_stats(stats)
        handgun_kills = handgun_stats[4]
        handgun_headshots = handgun_stats[5]
        if handgun_headshots > 0: handgun_headshot_ratio = round((handgun_headshots / handgun_kills)*100, 2)
        else: handgun_headshot_ratio = 0
        handgun_kills = "{:,}".format(handgun_kills)
        handgun_headshots = "{:,}".format(handgun_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Handgun Stats", value=f"Damage Increase: {handgun_stats[0]}/9\n"
                                                            f"Recoil Reduction: {handgun_stats[1]}/9\n"
                                                            f"Reload Speed Reduction: {handgun_stats[2]}/9\n"
                                                            f"Cost Reduction: {handgun_stats[3]}/9\n"
                                                            f"Kills: {handgun_kills}\n"
                                                            f"Headshot Kills: {handgun_headshots}\n"
                                                            f"Headshot Kill Ratio: {handgun_headshot_ratio}%\n"
                                                            f"Ammo Clip Upgrade: {handgun_stats[7]}")
        embed.set_image(url=handgun_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="deagle", description="Check a player's Deagle stats")
@app_commands.describe(username="Username")
async def deagle(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        magnum_stats = get_cvc_magnum_stats(stats)
        magnum_kills = magnum_stats[4]
        magnum_headshots = magnum_stats[5]
        if magnum_headshots > 0:
            magnum_headshot_ratio = round((magnum_headshots / magnum_kills) * 100, 2)
        else:
            magnum_headshot_ratio = 0
        magnum_kills = "{:,}".format(magnum_kills)
        magnum_headshots = "{:,}".format(magnum_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Magnum Stats", value=f"Damage Increase: {magnum_stats[0]}/9\n"
                                                             f"Recoil Reduction: {magnum_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {magnum_stats[2]}/9\n"
                                                             f"Cost Reduction: {magnum_stats[3]}/9\n"
                                                             f"Kills: {magnum_kills}\n"
                                                             f"Headshot Kills: {magnum_headshots}\n"
                                                             f"Headshot Kill Ratio: {magnum_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {magnum_stats[7]}")
        embed.set_image(url=magnum_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="sniper", description="Check a player's Sniper stats")
@app_commands.describe(username="Username")
async def sniper(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, CHARGE, RELOAD, COST, KILLS, HEADSHOT, CLIP
        sniper_stats = get_cvc_sniper_stats(stats)
        sniper_kills = sniper_stats[4]
        sniper_headshots = sniper_stats[5]
        if sniper_headshots > 0:
            sniper_headshot_ratio = round((sniper_headshots / sniper_kills) * 100, 2)
        else:
            sniper_headshot_ratio = 0
        sniper_kills = "{:,}".format(sniper_kills)
        sniper_headshots = "{:,}".format(sniper_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Sniper Stats", value=f"Damage Increase: {sniper_stats[0]}/9\n"
                                                            f"Charge Speed Reduction: {sniper_stats[1]}/9\n"
                                                            f"Reload Speed Reduction: {sniper_stats[2]}/9\n"
                                                            f"Cost Reduction: {sniper_stats[3]}/9\n"
                                                            f"Kills: {sniper_kills}\n"
                                                            f"Headshot Kills: {sniper_headshots}\n"
                                                            f"Headshot Kill Ratio: {sniper_headshot_ratio}%\n"
                                                            f"Ammo Clip Upgrade: {sniper_stats[6]}")
        embed.set_image(url=SNIPER)
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="p90", description="Check a player's P90 stats")
@app_commands.describe(username="Username")
async def p90(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        bullpup_stats = get_cvc_bullpup_stats(stats)
        bullpup_kills = bullpup_stats[4]
        bullpup_headshots = bullpup_stats[5]
        if bullpup_headshots > 0:
            bullpup_headshot_ratio = round((bullpup_headshots / bullpup_kills) * 100, 2)
        else:
            bullpup_headshot_ratio = 0
        bullpup_kills = "{:,}".format(bullpup_kills)
        bullpup_headshots = "{:,}".format(bullpup_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Bullpup Stats", value=f"Damage Increase: {bullpup_stats[0]}/9\n"
                                                             f"Recoil Reduction: {bullpup_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {bullpup_stats[2]}/9\n"
                                                             f"Cost Reduction: {bullpup_stats[3]}/9\n"
                                                             f"Kills: {bullpup_kills}\n"
                                                             f"Headshot Kills: {bullpup_headshots}\n"
                                                             f"Headshot Kill Ratio: {bullpup_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {bullpup_stats[7]}")
        embed.set_image(url=bullpup_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="mp5", description="Check a player's MP5 stats")
@app_commands.describe(username="Username")
async def mp5(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        smg_stats = get_cvc_smg_stats(stats)
        smg_kills = smg_stats[4]
        smg_headshots = smg_stats[5]
        if smg_headshots > 0:
            smg_headshot_ratio = round((smg_headshots / smg_kills) * 100, 2)
        else:
            smg_headshot_ratio = 0
        smg_kills = "{:,}".format(smg_kills)
        smg_headshots = "{:,}".format(smg_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s SMG Stats", value=f"Damage Increase: {smg_stats[0]}/9\n"
                                                             f"Recoil Reduction: {smg_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {smg_stats[2]}/9\n"
                                                             f"Cost Reduction: {smg_stats[3]}/9\n"
                                                             f"Kills: {smg_kills}\n"
                                                             f"Headshot Kills: {smg_headshots}\n"
                                                             f"Headshot Kill Ratio: {smg_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {smg_stats[7]}")
        embed.set_image(url=smg_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="ak", description="Check a player's AK-47 stats")
@app_commands.describe(username="Username")
async def ak(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        rifle_stats = get_cvc_rifle_stats(stats)
        rifle_kills = rifle_stats[4]
        rifle_headshots = rifle_stats[5]
        if rifle_headshots > 0:
            rifle_headshot_ratio = round((rifle_headshots / rifle_kills) * 100, 2)
        else:
            rifle_headshot_ratio = 0
        rifle_kills = "{:,}".format(rifle_kills)
        rifle_headshots = "{:,}".format(rifle_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Rifle Stats", value=f"Damage Increase: {rifle_stats[0]}/9\n"
                                                             f"Recoil Reduction: {rifle_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {rifle_stats[2]}/9\n"
                                                             f"Cost Reduction: {rifle_stats[3]}/9\n"
                                                             f"Kills: {rifle_kills}\n"
                                                             f"Headshot Kills: {rifle_headshots}\n"
                                                             f"Headshot Kill Ratio: {rifle_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {rifle_stats[7]}")
        embed.set_image(url=rifle_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="m4", description="Check a M4 pistol stats")
@app_commands.describe(username="Username")
async def m4(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        carbine_stats = get_cvc_carbine_stats(stats)
        carbine_kills = carbine_stats[4]
        carbine_headshots = carbine_stats[5]
        if carbine_headshots > 0:
            carbine_headshot_ratio = round((carbine_headshots / carbine_kills) * 100, 2)
        else:
            carbine_headshot_ratio = 0
        carbine_kills = "{:,}".format(carbine_kills)
        carbine_headshots = "{:,}".format(carbine_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Carbine Stats", value=f"Damage Increase: {carbine_stats[0]}/9\n"
                                                             f"Recoil Reduction: {carbine_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {carbine_stats[2]}/9\n"
                                                             f"Cost Reduction: {carbine_stats[3]}/9\n"
                                                             f"Kills: {carbine_kills}\n"
                                                             f"Headshot Kills: {carbine_headshots}\n"
                                                             f"Headshot Kill Ratio: {carbine_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {carbine_stats[7]}")
        embed.set_image(url=carbine_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="aug", description="Check a player's AUG stats")
@app_commands.describe(username="Username")
async def aug(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        scoped_rifle_stats = get_cvc_scoped_rifle_stats(stats)
        scoped_rifle_kills = scoped_rifle_stats[4]
        scoped_rifle_headshots = scoped_rifle_stats[5]
        if scoped_rifle_headshots > 0:
            scoped_rifle_headshot_ratio = round((scoped_rifle_headshots / scoped_rifle_kills) * 100, 2)
        else:
            scoped_rifle_headshot_ratio = 0
        scoped_rifle_kills = "{:,}".format(scoped_rifle_kills)
        scoped_rifle_headshots = "{:,}".format(scoped_rifle_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Aug Stats", value=f"Damage Increase: {scoped_rifle_stats[0]}/9\n"
                                                             f"Recoil Reduction: {scoped_rifle_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {scoped_rifle_stats[2]}/9\n"
                                                             f"Cost Reduction: {scoped_rifle_stats[3]}/9\n"
                                                             f"Kills: {scoped_rifle_kills}\n"
                                                             f"Headshot Kills: {scoped_rifle_headshots}\n"
                                                             f"Headshot Kill Ratio: {scoped_rifle_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {scoped_rifle_stats[7]}")
        embed.set_image(url=scoped_rifle_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="shotgun", description="Check a player's pistol stats")
@app_commands.describe(username="Username")
async def shotgun(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        shotgun_stats = get_cvc_shotgun_stats(stats)
        shotgun_kills = shotgun_stats[4]
        shotgun_headshots = shotgun_stats[5]
        if shotgun_headshots > 0:
            shotgun_headshot_ratio = round((shotgun_headshots / shotgun_kills) * 100, 2)
        else:
            shotgun_headshot_ratio = 0
        shotgun_kills = "{:,}".format(shotgun_kills)
        shotgun_headshots = "{:,}".format(shotgun_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Shotgun Stats", value=f"Damage Increase: {shotgun_stats[0]}/9\n"
                                                             f"Recoil Reduction: {shotgun_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {shotgun_stats[2]}/9\n"
                                                             f"Cost Reduction: {shotgun_stats[3]}/9\n"
                                                             f"Kills: {shotgun_kills}\n"
                                                             f"Headshot Kills: {shotgun_headshots}\n"
                                                             f"Headshot Kill Ratio: {shotgun_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {shotgun_stats[7]}")
        embed.set_image(url=shotgun_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="autoshotgun", description="Check a player's Auto Shotgun stats")
@app_commands.describe(username="Username")
async def autoshotgun(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        # ARRAY ORDER IS DAMAGE, RECOIL, RELOAD, COST, KILLS, HEADSHOT, SKIN, CLIP
        auto_shotgun_stats = get_cvc_auto_shotgun_stats(stats)
        auto_shotgun_kills = auto_shotgun_stats[4]
        auto_shotgun_headshots = auto_shotgun_stats[5]
        if auto_shotgun_headshots > 0:
            auto_shotgun_headshot_ratio = round((auto_shotgun_headshots / auto_shotgun_kills) * 100, 2)
        else:
            auto_shotgun_headshot_ratio = 0
        auto_shotgun_kills = "{:,}".format(auto_shotgun_kills)
        auto_shotgun_headshots = "{:,}".format(auto_shotgun_headshots)

        embed = discord.Embed(
            color=discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s Auto Shotgun Stats", value=f"Damage Increase: {auto_shotgun_stats[0]}/9\n"
                                                             f"Recoil Reduction: {auto_shotgun_stats[1]}/9\n"
                                                             f"Reload Speed Reduction: {auto_shotgun_stats[2]}/9\n"
                                                             f"Cost Reduction: {auto_shotgun_stats[3]}/9\n"
                                                             f"Kills: {auto_shotgun_kills}\n"
                                                             f"Headshot Kills: {auto_shotgun_headshots}\n"
                                                             f"Headshot Kill Ratio: {auto_shotgun_headshot_ratio}%\n"
                                                             f"Ammo Clip Upgrade: {auto_shotgun_stats[7]}")
        embed.set_image(url=auto_shotgun_stats[6])
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="cvctourney1", description="Check a player's Hypixel CvC Tourney 1 stats")
@app_commands.describe(username="Username")
async def cvctourney1(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        #ARRAY ORDER IS WINS, GAMES PLAYED, KILLS, DEATHS, HEADSHOT KILLS, SHOTS FIRED, BOMBS PLANTED, BOMBS DEFUSED, GRENADE KILLS
        tourney_zero = get_cvc_tourney_zero_stats(stats)
        if tourney_zero[3] > 0:
            tourney_kd = round(tourney_zero[2]/tourney_zero[3], 2)
        else: tourney_kd = 0
        if tourney_zero[1] > 0:
            tourney_wl = round(tourney_zero[0]/tourney_zero[1]*100, 2)
        else: tourney_wl = 0
        if tourney_zero[2] > 0:
            tourney_hs = round(tourney_zero[4]/tourney_zero[2]*100, 2)
        else: tourney_hs = 0
        embed = discord.Embed(
            color = discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s 1st CvC Tourney Stats:", value=f"Games Played: {tourney_zero[1]}\n"
                                                                      f"Wins: {tourney_zero[0]}\nWin/Loss: {tourney_wl}%\n"
                                                                      f"Kills: {tourney_zero[2]}\nDeaths: {tourney_zero[3]}\n"
                                                                      f"KDR: {tourney_kd}\nHeadshot Kills: {tourney_zero[4]}\n"
                                                                      f"Headshot Percentage: {tourney_hs}%\nShots Fired: {tourney_zero[5]}\n"
                                                                      f"Bombs Planted: {tourney_zero[6]}\n"
                                                                      f"Bombs Defused: {tourney_zero[7]}\nGrenade Kills: {tourney_zero[8]}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)

@bot.tree.command(name="cvctourney2", description="Check a player's Hypixel CvC Tourney 2 stats")
@app_commands.describe(username="Username")
async def cvctourney2(ctx, username: str):
    result = await statshelper(ctx, message=username)
    if result is True:
        global stats, ign, uuid
        #ARRAY ORDER IS WINS, GAMES PLAYED, KILLS, DEATHS, HEADSHOT KILLS, SHOTS FIRED, BOMBS PLANTED, BOMBS DEFUSED, GRENADE KILLS
        tourney_one = get_cvc_tourney_one_stats(stats)
        if tourney_one[3] > 0:
            tourney_kd = round(tourney_one[2]/tourney_one[3], 2)
        else: tourney_kd = 0
        if tourney_one[1] > 0:
            tourney_wl = round(tourney_one[0]/tourney_one[1]*100, 2)
        else: tourney_wl = 0
        if tourney_one[2] > 0:
            tourney_hs = round(tourney_one[4]/tourney_one[2]*100, 2)
        else: tourney_hs = 0
        embed = discord.Embed(
            color = discord.Color.blurple()
        )
        embed.add_field(name=f"{ign}'s 2nd CvC Tourney Stats:", value=f"Games Played: {tourney_one[1]}\n"
                                                                      f"Wins: {tourney_one[0]}\nWin/Loss: {tourney_wl}%\n"
                                                                      f"Kills: {tourney_one[2]}\nDeaths: {tourney_one[3]}\n"
                                                                      f"KDR: {tourney_kd}\nHeadshot Kills: {tourney_one[4]}\n"
                                                                      f"Headshot Percentage: {tourney_hs}%\nShots Fired: {tourney_one[5]}\n"
                                                                      f"Bombs Planted: {tourney_one[6]}\n"
                                                                      f"Bombs Defused: {tourney_one[7]}\nGrenade Kills: {tourney_one[8]}")
        embed.set_thumbnail(url=f'https://crafatar.com/avatars/{uuid}')
        embed.set_footer(text="BaseBot by baseballaholic",
                         icon_url='https://cdn.discordapp.com/attachments/881008770224898200/887185034551902218/Fake_Forums_Avatar.png')
        await ctx.response.send_message(embed=embed)
        

def getinfo(call):
    r = requests.get(call)
    return r.json()


def get_uuid(player):
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}")
    try:
        uuid = json.loads(response.text)['id']
        return uuid
    except:
        return 'ERROR'


def get_API(player):
    data = getinfo(f"https://api.hypixel.net/player?key={API_KEY}&uuid={player}")
    return data


API_KEY = "deb9e086-d418-42f8-9de5-03676d1f98d9"


# uuid_link = f"https://api.hypixel.net/player?key={API_KEY}&uuid={uuid}"
# API QUICK ACCESS: https://api.hypixel.net/player?key=deb9e086-d418-42f8-9de5-03676d1f98d9&uuid=14552d0d4cb949b59d4f7d1875b0ad94

# data = getinfo(uuid_link)

# THIS FUNCTION IS FOR CVC COINS
def get_cvc_coins(data):
    cvc_coins = data["player"]["stats"]["MCGO"]["coins"]
    return cvc_coins


# ALL CODE BELOW HERE IS FOR THE CVC DEFUSAL STATS
def get_cvc_defusal_stats(data):
    try: cvc_defusal_kills = data["player"]["stats"]["MCGO"]["kills"]
    except: cvc_defusal_kills = 0
    try: cvc_defusal_deaths = data["player"]["stats"]["MCGO"]["deaths"]
    except: cvc_defusal_deaths = 0
    try: cvc_bomb_plants = data["player"]["stats"]["MCGO"]["bombs_planted"]
    except: cvc_bomb_plants = 0
    try: cvc_bomb_defused = data["player"]["stats"]["MCGO"]["bombs_defused"]
    except: cvc_bomb_defused = 0
    try: cvc_defusal_wins = data["player"]["stats"]["MCGO"]["game_wins"]
    except: cvc_defusal_wins = 0
    return (cvc_defusal_kills, cvc_defusal_deaths, cvc_defusal_wins, cvc_bomb_plants, cvc_bomb_defused)


# ALL CODE BELOW HERE IS FOR CVC TDM STATS
def get_cvc_tdm_stats(data):
    try: cvc_tdm_kills = data["player"]["stats"]["MCGO"]["kills_deathmatch"]
    except: cvc_tdm_kills = 0
    try: cvc_tdm_deaths = data["player"]["stats"]["MCGO"]["deaths_deathmatch"]
    except: cvc_tdm_deaths = 0
    try: cvc_tdm_wins = data["player"]["stats"]["MCGO"]["game_wins_deathmatch"]
    except: cvc_tdm_wins = 0
    return (cvc_tdm_kills, cvc_tdm_deaths, cvc_tdm_wins)


# ALL CODE BELOW HERE IS FOR MAP WINS
def get_cvc_map_wins(data):
    try: cvc_alleyway_wins = data["player"]["stats"]["MCGO"]["game_wins_alleyway"]
    except: cvc_alleyway_wins = 0
    try: cvc_atomic_wins = data["player"]["stats"]["MCGO"]["game_wins_atomic"]
    except: cvc_atomic_wins = 0
    try: cvc_bazaar_wins = data["player"]["stats"]["MCGO"]["game_wins_bazaar"]
    except: cvc_bazaar_wins = 0
    try: cvc_carrier_wins = data["player"]["stats"]["MCGO"]["game_wins_carrier"]
    except: cvc_carrier_wins = 0
    try: cvc_derailed_wins = data["player"]["stats"]["MCGO"]["game_wins_derailed"]
    except: cvc_derailed_wins = 0
    try: cvc_junction_wins = data["player"]["stats"]["MCGO"]["game_wins_junction"]
    except: cvc_junction_wins = 0
    try: cvc_melon_factory_wins = data["player"]["stats"]["MCGO"]["game_wins_melon factory"]
    except: cvc_melon_factory_wins = 0
    try: cvc_overgrown_wins = data["player"]["stats"]["MCGO"]["game_wins_overgrown"]
    except: cvc_overgrown_wins = 0
    try: cvc_reserve_wins = data["player"]["stats"]["MCGO"]["game_wins_reserve"]
    except: cvc_reserve_wins = 0
    try: cvc_sandstorm_wins = data["player"]["stats"]["MCGO"]["game_wins_sandstorm"]
    except: cvc_sandstorm_wins = 0
    try: cvc_temple_wins = data["player"]["stats"]["MCGO"]["game_wins_temple"]
    except: cvc_temple_wins = 0
    return (cvc_alleyway_wins, cvc_atomic_wins, cvc_bazaar_wins, cvc_carrier_wins, cvc_derailed_wins,
            cvc_junction_wins, cvc_melon_factory_wins, cvc_overgrown_wins, cvc_reserve_wins,
            cvc_sandstorm_wins, cvc_temple_wins)


# ALL CODE BELOW HERE IS FOR CVC OVERALL STATS
def get_cvc_overall_stats(data):
    # THE ORDER OF THE DEFUSAL ARRAY: KILLS, DEATHS, WINS, BOMBS PLANTED, BOMBS DEFUSED
    # THE ORDER OF THE TDM ARRAY: KILLS, DEATHS, WINS
    # THE ORDER OF THE GG ARRAY: WINS, KILLS, DEATHS, GAMES PLAYES, FASTEST, CARE, ARMOR, SPEED
    cvc_defusal_stats = get_cvc_defusal_stats(data)
    cvc_tdm_stats = get_cvc_tdm_stats(data)
    cvc_gg_stats = get_cvc_gun_game_stats(data)
    cvc_overall_kills = cvc_defusal_stats[0] + cvc_tdm_stats[0] + cvc_gg_stats[1]
    cvc_overall_deaths = cvc_defusal_stats[1] + cvc_tdm_stats[1] + cvc_gg_stats[2]
    if cvc_overall_deaths > 0:
        cvc_overall_kdr = round(cvc_overall_kills / cvc_overall_deaths, 3)
    else: cvc_overall_kdr = 0
    cvc_overall_wins = cvc_defusal_stats[2] + cvc_tdm_stats[2] + cvc_gg_stats[0]
    try: cvc_grenade_kills = data["player"]["stats"]["MCGO"]["grenade_kills"]
    except: cvc_grenade_kills = 0
    try: cvc_shots_fired = data["player"]["stats"]["MCGO"]["shots_fired"]
    except: cvc_shots_fired = 0
    try: cvc_headshot_kills = data["player"]["stats"]["MCGO"]["headshot_kills"]
    except: cvc_headshot_kills = 0
    if cvc_overall_kills > 0:
        cvc_headshot_percent = round(((cvc_headshot_kills / cvc_overall_kills) * 100), 2)
    else: cvc_headshot_percent = 0
    try: cvc_coins = get_cvc_coins(data)
    except: cvc_coins = 0
    return (
        cvc_overall_kills, cvc_overall_deaths, cvc_overall_kdr, cvc_overall_wins, cvc_grenade_kills, cvc_shots_fired,
        cvc_headshot_kills, cvc_headshot_percent, cvc_coins)

# ALL CODE BELOW HERE IS FOR CVC SKINS PROGRESS
def get_cvc_skins_progress(data, oneTimeList):
    try: cvc_pistol_kills = data["player"]["stats"]["MCGO"]["pistolKills"]
    except: cvc_pistol_kills = 0
    try: cvc_handgun_kills = data["player"]["stats"]["MCGO"]["handgunKills"]
    except: cvc_handgun_kills = 0
    cvc_magnum_skin = "copsandcrims_golden_deagle"
    if cvc_magnum_skin in oneTimeList:
        cvc_magnum_skin = "Unlocked"
    else: cvc_magnum_skin = "Locked"
    cvc_bullpup_skin = "copsandcrims_p90_streak"
    if cvc_bullpup_skin in oneTimeList:
        cvc_bullpup_skin = "Unlocked"
    else: cvc_bullpup_skin = "Locked"
    cvc_smg_skin = "copsandcrims_mp5_streak"
    if cvc_smg_skin in oneTimeList:
        cvc_smg_skin = "Unlocked"
    else: cvc_smg_skin = "Locked"
    cvc_rifle_skin ="copsandcrims_wrecking_machine"
    if cvc_rifle_skin in oneTimeList:
        cvc_rifle_skin = "Unlocked"
    else: cvc_rifle_skin = "Locked"
    try: cvc_carbine_kills = data["player"]["stats"]["MCGO"]["carbineKills"]
    except: cvc_carbine_kills = 0
    try: cvc_scoped_rifle_headshot_kills = data["player"]["stats"]["MCGO"]["scopedRifleHeadshots"]
    except: cvc_scoped_rifle_headshot_kills = 0
    try: cvc_shotgun_headshot_kills = data["player"]["stats"]["MCGO"]["shotgunHeadshots"]
    except: cvc_shotgun_headshot_kills = 0
    try: cvc_auto_shotgun_kills = data["player"]["stats"]["MCGO"]["autoShotgunKills"]
    except: cvc_auto_shotgun_kills = 0
    return (cvc_pistol_kills, cvc_handgun_kills, cvc_carbine_kills, cvc_scoped_rifle_headshot_kills,
            cvc_shotgun_headshot_kills, cvc_auto_shotgun_kills, cvc_magnum_skin, cvc_bullpup_skin, cvc_smg_skin,
            cvc_rifle_skin)

# All these functions below are identical, grab a stat, check what skin they use, check if they have ammo clip upgrade, and return the stats
# ALL CODE BELOW HERE IS FOR CVC pistol STATS
def get_cvc_pistol_stats(data):
    try: cvc_pistol_damage = data["player"]["stats"]["MCGO"]["pistol_damage_increase"]
    except: cvc_pistol_damage = 0
    try: cvc_pistol_recoil = data["player"]["stats"]["MCGO"]["pistol_recoil_reduction"]
    except: cvc_pistol_recoil = 0
    try: cvc_pistol_reload = data["player"]["stats"]["MCGO"]["pistol_reload_speed_reduction"]
    except: cvc_pistol_reload = 0
    try: cvc_pistol_kills = data["player"]["stats"]["MCGO"]["pistolKills"]
    except: cvc_pistol_kills = 0
    try: cvc_pistol_headshots = data["player"]["stats"]["MCGO"]["pistolHeadshots"]
    except: cvc_pistol_headshots = 0
    try: cvc_pistol_skin = data["player"]["stats"]["MCGO"]["selectedpistolDev"]
    except: cvc_pistol_skin = USP
    print(cvc_pistol_skin)
    if cvc_pistol_skin == 'USP_WHISPER_PLUS':
        cvc_pistol_skin = USP_WHISPER
    elif cvc_pistol_skin == 'USP_WHISPER':
        cvc_pistol_skin = USP_WHISPER
    elif cvc_pistol_skin == 'USP_PLUS':
        cvc_pistol_skin = USP
    elif cvc_pistol_skin == 'USP':
        cvc_pistol_skin = USP
    cvc_pistol_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "pistol_clip" in cvc_pistol_clip:
        cvc_pistol_clip = ":white_check_mark:"
    else:
        cvc_pistol_clip = ":negative_squared_cross_mark:"
    return (cvc_pistol_damage, cvc_pistol_recoil, cvc_pistol_reload, cvc_pistol_kills, cvc_pistol_headshots, cvc_pistol_skin, cvc_pistol_clip)

# ALL CODE BELOW HERE IS FOR CVC pistol STATS
def get_cvc_handgun_stats(data):
    try: cvc_handgun_damage = data["player"]["stats"]["MCGO"]["handgun_damage_increase"]
    except: cvc_handgun_damage = 0
    try: cvc_handgun_recoil = data["player"]["stats"]["MCGO"]["handgun_recoil_reduction"]
    except: cvc_handgun_recoil = 0
    try: cvc_handgun_reload = data["player"]["stats"]["MCGO"]["handgun_reload_speed_reduction"]
    except: cvc_handgun_reload = 0
    try: cvc_handgun_cost = data["player"]["stats"]["MCGO"]["handgun_cost_reduction"]
    except: cvc_handgun_cost = 0
    try: cvc_handgun_kills = data["player"]["stats"]["MCGO"]["handgunKills"]
    except: cvc_handgun_kills = 0
    try: cvc_handgun_headshots = data["player"]["stats"]["MCGO"]["handgunHeadshots"]
    except: cvc_handgun_headshots = 0
    try: cvc_handgun_skin = data["player"]["stats"]["MCGO"]["selectedHandgunDev"]
    except: cvc_handgun_skin = HK45
    if cvc_handgun_skin == 'HK45_MOUNTAINOUS_PLUS':
        cvc_handgun_skin = HK45_MOUNTAINOUS
    elif cvc_handgun_skin == 'HK45_MOUNTAINOUS':
        cvc_handgun_skin = HK45_MOUNTAINOUS
    elif cvc_handgun_skin == 'HK45_PLUS':
        cvc_handgun_skin = HK45
    elif cvc_handgun_skin == 'HK45':
        cvc_handgun_skin = HK45
    cvc_handgun_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "handgun_clip" in cvc_handgun_clip:
        cvc_handgun_clip = ":white_check_mark:"
    else:
        cvc_handgun_clip = ":negative_squared_cross_mark:"
    return (cvc_handgun_damage, cvc_handgun_recoil, cvc_handgun_reload, cvc_handgun_cost, cvc_handgun_kills,
            cvc_handgun_headshots, cvc_handgun_skin, cvc_handgun_clip)

# ALL CODE BELOW HERE IS FOR CVC DEAGLE STATS
def get_cvc_magnum_stats(data):
    try: cvc_magnum_damage = data["player"]["stats"]["MCGO"]["magnum_damage_increase"]
    except: cvc_magnum_damage = 0
    try: cvc_magnum_recoil = data["player"]["stats"]["MCGO"]["magnum_recoil_reduction"]
    except: cvc_magnum_recoil = 0
    try: cvc_magnum_reload = data["player"]["stats"]["MCGO"]["magnum_reload_speed_reduction"]
    except: cvc_magnum_reload = 0
    try: cvc_magnum_cost = data["player"]["stats"]["MCGO"]["magnum_cost_reduction"]
    except: cvc_magnum_cost = 0
    try: cvc_magnum_kills = data["player"]["stats"]["MCGO"]["magnumKills"]
    except: cvc_magnum_kills = 0
    try: cvc_magnum_headshots = data["player"]["stats"]["MCGO"]["magnumHeadshots"]
    except: cvc_magnum_headshots = 0
    try: cvc_magnum_skin = data["player"]["stats"]["MCGO"]["selectedMagnumDev"]
    except: cvc_magnum_skin = DESERT_EAGLE
    if cvc_magnum_skin == 'GOLDEN_DEAGLE_PLUS':
        cvc_magnum_skin = GOLDEN_DEAGLE
    elif cvc_magnum_skin == 'GOLDEN_DEAGLE':
        cvc_magnum_skin = GOLDEN_DEAGLE
    elif cvc_magnum_skin == 'DESERT_EAGLE_PLUS':
        cvc_magnum_skin = DESERT_EAGLE
    elif cvc_magnum_skin == 'DESERT_EAGLE':
        cvc_magnum_skin = DESERT_EAGLE
    cvc_magnum_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "magnum_clip" in cvc_magnum_clip:
        cvc_magnum_clip = ":white_check_mark:"
    else:
        cvc_magnum_clip = ":negative_squared_cross_mark:"
    return (cvc_magnum_damage, cvc_magnum_recoil, cvc_magnum_reload, cvc_magnum_cost, cvc_magnum_kills,
            cvc_magnum_headshots, cvc_magnum_skin, cvc_magnum_clip)

# ALL CODE BELOW HERE IS FOR CVC SNIPER STATS
def get_cvc_sniper_stats(data):
    try: cvc_sniper_damage = data["player"]["stats"]["MCGO"]["sniper_damage_increase"]
    except: cvc_sniper_damage = 0
    try: cvc_sniper_charge = data["player"]["stats"]["MCGO"]["sniper_charge_bonus"]
    except: cvc_sniper_charge = 0
    try: cvc_sniper_reload = data["player"]["stats"]["MCGO"]["sniper_reload_speed_reduction"]
    except: cvc_sniper_reload = 0
    try: cvc_sniper_cost = data["player"]["stats"]["MCGO"]["sniper_cost_reduction"]
    except: cvc_sniper_cost = 0
    try: cvc_sniper_kills = data["player"]["stats"]["MCGO"]["sniperKills"]
    except: cvc_sniper_kills = 0
    try: cvc_sniper_headshots = data["player"]["stats"]["MCGO"]["sniperHeadshots"]
    except: cvc_sniper_headshots = 0
    cvc_sniper_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "sniper_clip" in cvc_sniper_clip:
        cvc_sniper_clip = ":white_check_mark:"
    else:
        cvc_sniper_clip = ":negative_squared_cross_mark:"
    return (cvc_sniper_damage, cvc_sniper_charge, cvc_sniper_reload, cvc_sniper_cost, cvc_sniper_kills, cvc_sniper_headshots, cvc_sniper_clip)

# ALL CODE BELOW HERE IS FOR CVC P90 STATS
def get_cvc_bullpup_stats(data):
    try: cvc_bullpup_damage = data["player"]["stats"]["MCGO"]["bullpup_damage_increase"]
    except: cvc_bullpup_damage = 0
    try: cvc_bullpup_recoil = data["player"]["stats"]["MCGO"]["bullpup_recoil_reduction"]
    except: cvc_bullpup_recoil = 0
    try: cvc_bullpup_reload = data["player"]["stats"]["MCGO"]["bullpup_reload_speed_reduction"]
    except: cvc_bullpup_reload = 0
    try: cvc_bullpup_cost = data["player"]["stats"]["MCGO"]["bullpup_cost_reduction"]
    except: cvc_bullpup_cost = 0
    try: cvc_bullpup_kills = data["player"]["stats"]["MCGO"]["bullpupKills"]
    except: cvc_bullpup_kills = 0
    try: cvc_bullpup_headshots = data["player"]["stats"]["MCGO"]["bullpupHeadshots"]
    except: cvc_bullpup_headshots = 0
    try: cvc_bullpup_skin = data["player"]["stats"]["MCGO"]["selectedBullpupDev"]
    except: cvc_bullpup_skin = P90
    if cvc_bullpup_skin == 'P90_VIBRANT_PLUS':
        cvc_bullpup_skin = P90_VIBRANT
    elif cvc_bullpup_skin == 'P90_VIBRANT':
        cvc_bullpup_skin = P90_VIBRANT
    elif cvc_bullpup_skin == 'P90_PLUS':
        cvc_bullpup_skin = P90
    elif cvc_bullpup_skin == 'P90':
        cvc_bullpup_skin = P90
    cvc_bullpup_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "bullpup_clip" in cvc_bullpup_clip:
        cvc_bullpup_clip = ":white_check_mark:"
    else:
        cvc_bullpup_clip = ":negative_squared_cross_mark:"
    return (cvc_bullpup_damage, cvc_bullpup_recoil, cvc_bullpup_reload, cvc_bullpup_cost, cvc_bullpup_kills,
            cvc_bullpup_headshots, cvc_bullpup_skin, cvc_bullpup_clip)

# ALL CODE BELOW HERE IS FOR CVC SMG STATS
def get_cvc_smg_stats(data):
    try: cvc_smg_damage = data["player"]["stats"]["MCGO"]["smg_damage_increase"]
    except: cvc_smg_damage = 0
    try: cvc_smg_recoil = data["player"]["stats"]["MCGO"]["smg_recoil_reduction"]
    except: cvc_smg_recoil = 0
    try: cvc_smg_reload = data["player"]["stats"]["MCGO"]["smg_reload_speed_reduction"]
    except: cvc_smg_reload = 0
    try: cvc_smg_cost = data["player"]["stats"]["MCGO"]["smg_cost_reduction"]
    except: cvc_smg_cost = 0
    try: cvc_smg_kills = data["player"]["stats"]["MCGO"]["smgKills"]
    except: cvc_smg_kills = 0
    try: cvc_smg_headshots = data["player"]["stats"]["MCGO"]["smgHeadshots"]
    except: cvc_smg_headshots = 0
    try: cvc_smg_skin = data["player"]["stats"]["MCGO"]["selectedSmgDev"]
    except: cvc_smg_skin = MP5
    if cvc_smg_skin == 'MP5_CYBERPUNK_PLUS':
        cvc_smg_skin = MP5_CYBERPUNK
    elif cvc_smg_skin == 'MP5_CYBERPUNK':
        cvc_smg_skin = MP5_CYBERPUNK
    elif cvc_smg_skin == 'MP5_PLUS':
        cvc_smg_skin = MP5
    elif cvc_smg_skin == 'MP5':
        cvc_smg_skin = MP5
    cvc_smg_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "smg_clip" in cvc_smg_clip:
        cvc_smg_clip = ":white_check_mark:"
    else:
        cvc_smg_clip = ":negative_squared_cross_mark:"
    return (cvc_smg_damage, cvc_smg_recoil, cvc_smg_reload, cvc_smg_cost, cvc_smg_kills, cvc_smg_headshots, cvc_smg_skin, cvc_smg_clip)

# ALL CODE BELOW HERE IS FOR CVC RIFLE STATS
def get_cvc_rifle_stats(data):
    try: cvc_rifle_damage = data["player"]["stats"]["MCGO"]["rifle_damage_increase"]
    except: cvc_rifle_damage = 0
    try: cvc_rifle_recoil = data["player"]["stats"]["MCGO"]["rifle_recoil_reduction"]
    except: cvc_rifle_recoil = 0
    try: cvc_rifle_reload = data["player"]["stats"]["MCGO"]["rifle_reload_speed_reduction"]
    except: cvc_rifle_reload = 0
    try: cvc_rifle_cost = data["player"]["stats"]["MCGO"]["rifle_cost_reduction"]
    except: cvc_rifle_cost = 0
    try: cvc_rifle_kills = data["player"]["stats"]["MCGO"]["rifleKills"]
    except: cvc_rifle_kills = 0
    try: cvc_rifle_headshots = data["player"]["stats"]["MCGO"]["rifleHeadshots"]
    except: cvc_rifle_headshots = 0
    try: cvc_rifle_skin = data["player"]["stats"]["MCGO"]["selectedRifleDev"]
    except: cvc_rifle_skin = AK_47
    if cvc_rifle_skin == 'AK_47_VIOLET_PLUS':
        cvc_rifle_skin = AK_47_VIOLET
    elif cvc_rifle_skin == 'AK_47_VIOLET':
        cvc_rifle_skin = AK_47_VIOLET
    elif cvc_rifle_skin == 'AK_47_PLUS':
        cvc_rifle_skin = AK_47
    elif cvc_rifle_skin == 'AK_47':
        cvc_rifle_skin = AK_47
    cvc_rifle_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "rifle_clip" in cvc_rifle_clip:
        cvc_rifle_clip = ":white_check_mark:"
    else:
        cvc_rifle_clip = ":negative_squared_cross_mark:"
    return (cvc_rifle_damage, cvc_rifle_recoil, cvc_rifle_reload, cvc_rifle_cost, cvc_rifle_kills,
            cvc_rifle_headshots, cvc_rifle_skin, cvc_rifle_clip)

# ALL CODE BELOW HERE IS FOR CVC CARBINE STATS
def get_cvc_carbine_stats(data):
    try: cvc_carbine_damage = data["player"]["stats"]["MCGO"]["carbine_damage_increase"]
    except: cvc_carbine_damage = 0
    try: cvc_carbine_recoil = data["player"]["stats"]["MCGO"]["carbine_recoil_reduction"]
    except: cvc_carbine_recoil = 0
    try: cvc_carbine_reload = data["player"]["stats"]["MCGO"]["carbine_reload_speed_reduction"]
    except: cvc_carbine_reload = 0
    try: cvc_carbine_cost = data["player"]["stats"]["MCGO"]["carbine_cost_reduction"]
    except: cvc_carbine_cost = 0
    try: cvc_carbine_kills = data["player"]["stats"]["MCGO"]["carbineKills"]
    except: cvc_carbine_kills = 0
    try: cvc_carbine_headshots = data["player"]["stats"]["MCGO"]["carbineHeadshots"]
    except: cvc_carbine_headshots = 0
    try: cvc_carbine_skin = data["player"]["stats"]["MCGO"]["selectedCarbineDev"]
    except: cvc_carbine_skin = M4
    if cvc_carbine_skin == 'M4_AQUATIC_PLUS':
        cvc_carbine_skin = M4_AQUATIC
    elif cvc_carbine_skin == 'M4_AQUATIC':
        cvc_carbine_skin = M4_AQUATIC
    elif cvc_carbine_skin == 'M4_PLUS':
        cvc_carbine_skin = M4
    elif cvc_carbine_skin == 'M4':
        cvc_carbine_skin = M4
    cvc_carbine_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "carbine_clip" in cvc_carbine_clip:
        cvc_carbine_clip = ":white_check_mark:"
    else:
        cvc_carbine_clip = ":negative_squared_cross_mark:"
    return (cvc_carbine_damage, cvc_carbine_recoil, cvc_carbine_reload, cvc_carbine_cost, cvc_carbine_kills,
            cvc_carbine_headshots, cvc_carbine_skin, cvc_carbine_clip)

# ALL CODE BELOW HERE IS FOR CVC SCOPED RIFLE STATS
def get_cvc_scoped_rifle_stats(data):
    try: cvc_scoped_rifle_damage = data["player"]["stats"]["MCGO"]["scoped_rifle_damage_increase"]
    except: cvc_scoped_rifle_damage = 0
    try: cvc_scoped_rifle_recoil = data["player"]["stats"]["MCGO"]["scoped_rifle_recoil_reduction"]
    except: cvc_scoped_rifle_recoil = 0
    try: cvc_scoped_rifle_reload = data["player"]["stats"]["MCGO"]["scoped_rifle_reload_speed_reduction"]
    except: cvc_scoped_rifle_reload = 0
    try: cvc_scoped_rifle_cost = data["player"]["stats"]["MCGO"]["scoped_rifle_cost_reduction"]
    except: cvc_scoped_rifle_cost = 0
    try: cvc_scoped_rifle_kills = data["player"]["stats"]["MCGO"]["scopedRifleKills"]
    except: cvc_scoped_rifle_kills = 0
    try: cvc_scoped_rifle_headshots = data["player"]["stats"]["MCGO"]["scopedRifleHeadshots"]
    except: cvc_scoped_rifle_headshots = 0
    try: cvc_scoped_rifle_skin = data["player"]["stats"]["MCGO"]["selectedScopedRifleDev"]
    except: cvc_scoped_rifle_skin = STEYR_AUG
    if cvc_scoped_rifle_skin == 'STEYR_AUG_VOLCANIC_PLUS':
        cvc_scoped_rifle_skin = STEYR_AUG_VOLCANIC
    elif cvc_scoped_rifle_skin == 'STEYR_AUG_VOLCANIC':
        cvc_scoped_rifle_skin = STEYR_AUG_VOLCANIC
    elif cvc_scoped_rifle_skin == 'STEYR_AUG_PLUS':
        cvc_scoped_rifle_skin = STEYR_AUG
    elif cvc_scoped_rifle_skin == 'STEYR_AUG':
        cvc_scoped_rifle_skin = STEYR_AUG
    cvc_scoped_rifle_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "scoped_rifle_clip" in cvc_scoped_rifle_clip:
        cvc_scoped_rifle_clip = ":white_check_mark:"
    else:
        cvc_scoped_rifle_clip = ":negative_squared_cross_mark:"
    return (cvc_scoped_rifle_damage, cvc_scoped_rifle_recoil, cvc_scoped_rifle_reload, cvc_scoped_rifle_cost,
            cvc_scoped_rifle_kills, cvc_scoped_rifle_headshots, cvc_scoped_rifle_skin, cvc_scoped_rifle_clip)

# ALL CODE BELOW HERE IS FOR CVC SHOTGUN STATS
def get_cvc_shotgun_stats(data):
    try: cvc_shotgun_damage = data["player"]["stats"]["MCGO"]["shotgun_damage_increase"]
    except: cvc_shotgun_damage = 0
    try: cvc_shotgun_recoil = data["player"]["stats"]["MCGO"]["shotgun_recoil_reduction"]
    except: cvc_shotgun_recoil = 0
    try: cvc_shotgun_reload = data["player"]["stats"]["MCGO"]["shotgun_reload_speed_reduction"]
    except: cvc_shotgun_reload = 0
    try: cvc_shotgun_cost = data["player"]["stats"]["MCGO"]["shotgun_cost_reduction"]
    except: cvc_shotgun_cost = 0
    try: cvc_shotgun_kills = data["player"]["stats"]["MCGO"]["shotgunKills"]
    except: cvc_shotgun_kills = 0
    try: cvc_shotgun_headshots = data["player"]["stats"]["MCGO"]["shotgunHeadshots"]
    except: cvc_shotgun_headshots = 0
    try: cvc_shotgun_skin = data["player"]["stats"]["MCGO"]["selectedShotgunDev"]
    except: cvc_shotgun_skin = PUMP_ACTION
    if cvc_shotgun_skin == 'BASALT_SHOTGUN_PLUS':
        cvc_shotgun_skin = BASALT_SHOTGUN
    elif cvc_shotgun_skin == 'BASALT_SHOTGUN':
        cvc_shotgun_skin = BASALT_SHOTGUN
    elif cvc_shotgun_skin == 'PUMP_ACTION_PLUS':
        cvc_shotgun_skin = PUMP_ACTION
    elif cvc_shotgun_skin == 'PUMP_ACTION':
        cvc_shotgun_skin = PUMP_ACTION
    cvc_shotgun_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "shotgun_clip" in cvc_shotgun_clip:
        cvc_shotgun_clip = ":white_check_mark:"
    else:
        cvc_shotgun_clip = ":negative_squared_cross_mark:"
    return (cvc_shotgun_damage, cvc_shotgun_recoil, cvc_shotgun_reload, cvc_shotgun_cost, cvc_shotgun_kills,
            cvc_shotgun_headshots, cvc_shotgun_skin, cvc_shotgun_clip)

# ALL CODE BELOW HERE IS FOR CVC AUTO SHOTGUN STATS
def get_cvc_auto_shotgun_stats(data):
    try: cvc_auto_shotgun_damage = data["player"]["stats"]["MCGO"]["auto_shotgun_damage_increase"]
    except: cvc_auto_shotgun_damage = 0
    try: cvc_auto_shotgun_recoil = data["player"]["stats"]["MCGO"]["auto_shotgun_recoil_reduction"]
    except: cvc_auto_shotgun_recoil = 0
    try: cvc_auto_shotgun_reload = data["player"]["stats"]["MCGO"]["auto_shotgun_reload_speed_reduction"]
    except: cvc_auto_shotgun_reload = 0
    try: cvc_auto_shotgun_cost = data["player"]["stats"]["MCGO"]["auto_shotgun_cost_reduction"]
    except: cvc_auto_shotgun_cost = 0
    try: cvc_auto_shotgun_kills = data["player"]["stats"]["MCGO"]["autoShotgunKills"]
    except: cvc_auto_shotgun_kills = 0
    try: cvc_auto_shotgun_headshots = data["player"]["stats"]["MCGO"]["autoShotgunHeadshots"]
    except: cvc_auto_shotgun_headshots = 0
    try: cvc_auto_shotgun_skin = data["player"]["stats"]["MCGO"]["selectedAutoShotgunDev"]
    except: cvc_auto_shotgun_skin = SPAS_12
    if cvc_auto_shotgun_skin == 'SPAS_12_URBAN_PLUS':
        cvc_auto_shotgun_skin = SPAS_12_URBAN
    elif cvc_auto_shotgun_skin == 'SPAS_12_URBAN':
        cvc_auto_shotgun_skin = SPAS_12_URBAN
    elif cvc_auto_shotgun_skin == 'SPAS_12_PLUS':
        cvc_auto_shotgun_skin = SPAS_12
    elif cvc_auto_shotgun_skin == 'SPAS_12':
        cvc_auto_shotgun_skin = SPAS_12
    cvc_auto_shotgun_clip = data["player"]["stats"]["MCGO"]["packages"]
    if "auto_shotgun_clip" in cvc_auto_shotgun_clip:
        cvc_auto_shotgun_clip = ":white_check_mark:"
    else: cvc_auto_shotgun_clip = ":negative_squared_cross_mark:"
    return (cvc_auto_shotgun_damage, cvc_auto_shotgun_recoil, cvc_auto_shotgun_reload, cvc_auto_shotgun_cost, cvc_auto_shotgun_kills,
            cvc_auto_shotgun_headshots, cvc_auto_shotgun_skin, cvc_auto_shotgun_clip)

def get_cvc_tourney_zero_stats(data):
    try: cvc_tourney_zero_wins = data["player"]["stats"]["MCGO"]["game_wins_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_wins = 0
    try: cvc_tourney_zero_games_played = data["player"]["stats"]["MCGO"]["game_plays_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_games_played = 0
    try: cvc_tourney_zero_kills = data["player"]["stats"]["MCGO"]["kills_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_kills = 0
    try: cvc_tourney_zero_deaths = data["player"]["stats"]["MCGO"]["deaths_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_deaths = 0
    try: cvc_tourney_zero_headshot_kills = data["player"]["stats"]["MCGO"]["headshot_kills_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_headshot_kills = 0
    try: cvc_tourney_zero_shots_fired = data["player"]["stats"]["MCGO"]["shots_fired_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_shots_fired = 0
    try: cvc_tourney_zero_bombs_planted = data["player"]["stats"]["MCGO"]["bombs_planted_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_bombs_planted = 0
    try: cvc_tourney_zero_bombs_defused = data["player"]["stats"]["MCGO"]["bombs_defused_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_bombs_defused = 0
    try: cvc_tourney_zero_grenade_kills = data["player"]["stats"]["MCGO"]["grenade_kills_tourney_mcgo_defusal_0"]
    except: cvc_tourney_zero_grenade_kills = 0
    return(cvc_tourney_zero_wins, cvc_tourney_zero_games_played, cvc_tourney_zero_kills, cvc_tourney_zero_deaths,
           cvc_tourney_zero_headshot_kills, cvc_tourney_zero_shots_fired, cvc_tourney_zero_bombs_planted,
           cvc_tourney_zero_bombs_defused, cvc_tourney_zero_grenade_kills)

def get_cvc_tourney_one_stats(data):
    try: cvc_tourney_one_wins = data["player"]["stats"]["MCGO"]["game_wins_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_wins = 0
    try: cvc_tourney_one_games_played = data["player"]["stats"]["MCGO"]["game_plays_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_games_played = 0
    try: cvc_tourney_one_kills = data["player"]["stats"]["MCGO"]["kills_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_kills = 0
    try: cvc_tourney_one_deaths = data["player"]["stats"]["MCGO"]["deaths_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_deaths = 0
    try: cvc_tourney_one_headshot_kills = data["player"]["stats"]["MCGO"]["headshot_kills_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_headshot_kills = 0
    try: cvc_tourney_one_shots_fired = data["player"]["stats"]["MCGO"]["shots_fired_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_shots_fired = 0
    try: cvc_tourney_one_bombs_planted = data["player"]["stats"]["MCGO"]["bombs_planted_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_bombs_planted = 0
    try: cvc_tourney_one_bombs_defused = data["player"]["stats"]["MCGO"]["bombs_defused_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_bombs_defused = 0
    try: cvc_tourney_one_grenade_kills = data["player"]["stats"]["MCGO"]["grenade_kills_tourney_mcgo_defusal_1"]
    except: cvc_tourney_one_grenade_kills = 0
    return(cvc_tourney_one_wins, cvc_tourney_one_games_played, cvc_tourney_one_kills, cvc_tourney_one_deaths,
           cvc_tourney_one_headshot_kills, cvc_tourney_one_shots_fired, cvc_tourney_one_bombs_planted,
           cvc_tourney_one_bombs_defused, cvc_tourney_one_grenade_kills)

def get_cvc_gun_game_stats(data):
    try: cvc_gun_game_wins = data["player"]["stats"]["MCGO"]["game_wins_gungame"]
    except: cvc_gun_game_wins = 0
    try: cvc_gun_game_kills = data["player"]["stats"]["MCGO"]["kills_gungame"]
    except: cvc_gun_game_kills = 0
    try: cvc_gun_game_deaths = data["player"]["stats"]["MCGO"]["deaths_gungame"]
    except: cvc_gun_game_deaths = 0
    try: cvc_gun_game_played = data["player"]["stats"]["MCGO"]["game_plays_gungame"]
    except: cvc_gun_game_played = 0
    #Returns a very large number
    try: cvc_gun_game_fastest = data["player"]["stats"]["MCGO"]["fastest_win_gungame"]
    except: cvc_gun_game_fastest = "N/A"
    if cvc_gun_game_fastest != "N/A":
        cvc_gun_game_fastest = cvc_gun_game_fastest/1000
    try: cvc_gun_game_care_packages = data["player"]["stats"]["MCGO"]["care_packages_collected_gungame"]
    except: cvc_gun_game_care_packages = 0
    try: cvc_gun_game_armor = data["player"]["stats"]["MCGO"]["armor_packs_collected_gungame"]
    except: cvc_gun_game_armor = 0
    try: cvc_gun_game_speed = data["player"]["stats"]["MCGO"]["speed_boosts_collected_gungame"]
    except: cvc_gun_game_speed = 0
    return(cvc_gun_game_wins, cvc_gun_game_kills, cvc_gun_game_deaths, cvc_gun_game_played, cvc_gun_game_fastest
           , cvc_gun_game_care_packages, cvc_gun_game_armor, cvc_gun_game_speed)



#These links go to tiny png of the gun skins so we can display what gun skin the user has equipped

USP = 'https://cdn.discordapp.com/attachments/881008770224898200/1046704345342812320/wood_pickaxe.png'
USP_WHISPER = 'https://cdn.discordapp.com/attachments/881008770224898200/887211934754156544/iron_pickaxe.png'
HK45 = 'https://cdn.discordapp.com/attachments/881008770224898200/887220692473483294/stone_pickaxe.png'
HK45_MOUNTAINOUS = 'https://cdn.discordapp.com/attachments/881008770224898200/887220500592484382/wood_shovel.png'
DESERT_EAGLE = "https://cdn.discordapp.com/attachments/881008770224898200/887516035631153152/gold_pickaxe.png"
GOLDEN_DEAGLE = "https://cdn.discordapp.com/attachments/881008770224898200/887515511682900038/diamond_pickaxe.png"
SNIPER = "https://cdn.discordapp.com/attachments/881008770224898200/887549026126405662/bow_standby.png"
P90 = "https://cdn.discordapp.com/attachments/881008770224898200/887551808099188816/gold_shovel.png"
P90_VIBRANT = "https://cdn.discordapp.com/attachments/881008770224898200/887551839036379197/iron_hoe.png"
MP5 = "https://cdn.discordapp.com/attachments/881008770224898200/887554250861871174/stone_shovel.png"
MP5_CYBERPUNK = 'https://cdn.discordapp.com/attachments/881008770224898200/887554224399982602/iron_shovel.png'
AK_47 = 'https://cdn.discordapp.com/attachments/881008770224898200/887555644574531605/stone_hoe.png'
AK_47_VIOLET = 'https://cdn.discordapp.com/attachments/881008770224898200/887555666452049991/diamond_hoe.png'
M4 = 'https://cdn.discordapp.com/attachments/881008770224898200/887557925311229992/iron_axe.png'
M4_AQUATIC = 'https://cdn.discordapp.com/attachments/881008770224898200/887557957338951720/diamond_axe.png'
STEYR_AUG = 'https://cdn.discordapp.com/attachments/881008770224898200/887560689445638174/gold_axe.png'
STEYR_AUG_VOLCANIC = 'https://cdn.discordapp.com/attachments/881008770224898200/887560712682098708/gold_hoe.png'
PUMP_ACTION = 'https://cdn.discordapp.com/attachments/881008770224898200/887562676421668884/diamond_shovel.png'
BASALT_SHOTGUN = 'https://cdn.discordapp.com/attachments/881008770224898200/887562731954274325/wood_hoe.png'
SPAS_12 = 'https://cdn.discordapp.com/attachments/881008770224898200/887565004231036948/wood_axe.png'
SPAS_12_URBAN = 'https://cdn.discordapp.com/attachments/881008770224898200/887565027928846397/stone_axe.png'

bot.run(TOKEN)
