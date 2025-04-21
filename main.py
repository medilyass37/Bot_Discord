import discord 
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord import Member
from discord.ext.commands import has_permissions, BotMissingPermissions
import os
from dotenv import load_dotenv
import json
from os import getenv

load_dotenv() # Chargement des variables d'environnement

welcome_channel_id = int(getenv('WELCOME_CHANNEL_ID'))

# Chargement des mots bannis
with open('banned_words.json', 'r', encoding='utf-8') as f:
    banned_data = json.load(f)
    specific_words = banned_data["words"]

intents =  discord.Intents.default() #Initialise les intents par défaut
intents.message_content = True #Permet au BOT de lire le contenu du msg
intents.members = True

client = commands.Bot(command_prefix = '!', intents=intents)
#Instance de commands.Bot nommée client
#Toutes les commandes du BOT commencent par !
#intents=intents passe les intents définis précédemment à l'instance du bot.

@client.event 
async def on_ready():
    print("The BOT is now ready for use!") #print s'affiche au terminal
    print("-----------------------")

    
@client.command()
async def hello(ctx):
    await ctx.send("Hello! I am the Discord BOT.") #send s'affiche dans conversation discord

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye my friend. Have a good day !")

@client.event 
async def on_member_join(member):
    channel = client.get_channel(welcome_channel_id)
    await channel.send("Hello new member, you're welcome !")
    
@client.event 
async def on_member_remove(member):
    channel = client.get_channel(welcome_channel_id)
    await channel.send("One member has left the group, Goodbye !")

@client.command(pass_context = True) #une commande qu'on peut appeler dans Discord.
async def join(ctx):
    if (ctx.author.voice): #si l'auteur de la commande est dans voice channel
        channel = ctx.message.author.voice.channel #Si l'auteur est dans voice channel, récupère ce canal et le stocke dans var channel
        voice = await channel.connect() #connecte le bot au voice channel récupéré
        source = FFmpegPCMAudio('AUDIO.wav')
        player = voice.play(source)

    else: #si l'auteur de la commande n'est pas dans voice channel
        await ctx.send("You're not in a voice channel, you must be in avoice channel to run this command")

@client.command(pass_context = True) #si on tape la commande !leave
async def leave(ctx): 
    if (ctx.voice_client): #if the bot is in a voice channel
        await ctx.guild.voice_client.disconnect() #go to your guild (server) -> voice channel dwhere the bot is et deconnecte le
        await ctx.send("I left the voice channel")
    else: #if he's not in a voice channel
        await ctx.send("I am not in a voice channel")

@client.command(pass_context = True) #si on tape la commande !pause
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing(): #the bot is playing an audio file
        voice.pause()
    else:
        await ctx.send("There is no audio playing in the voice channel")

@client.command(pass_context = True) #si on tape la commande !resume
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused(): #the bot's audio is paused
        voice.resume()
    else:
        await ctx.send("At the moment, no song is paused!")
    
@client.command(pass_context = True) #si on tape la commande !stop
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

@client.command(pass_context = True) #si on tape la commande !play
async def play(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source)


'''@client.event
async def on_message(message):
    if any(word in message.content.lower() for word in specific_words): # .lower pour eviter prob de casse
        await message.delete()
        await message.channel.send("Don't send that again!")
    await client.process_commands(message)  # Permet aux autres commandes de fonctionner. fach madrthach mab9awch kikhedmo les autres commandes
    '''

'''@client.event
async def on_message(message):    
    mots = message.content.split()
    for element in mots:
        if element.lower() in specific_words:
            await message.delete()
            await message.channel.send("The message you sent was deleted! Don't send that again!")
            break
    await client.process_commands(message)'''
    
@client.event
async def on_message(message):    
    if message.author == client.user:
        return
        
    mots = message.content.split()
    for element in mots:
        if element.lower() in specific_words:
            await message.delete()
            warning_msg = banned_data["responses"]["warning"]
            await message.channel.send(f"{message.author.mention} {warning_msg}")
            break
    await client.process_commands(message)


@client.command()
@has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has been kicked')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to kick people!")

'''
@client.command()
@has_permissions(ban_members = True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'User {member} has been banned')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to ban people!")
'''

@client.command()
async def wydad(ctx):
    embed = discord.Embed(title="WYDAD", url="https://fr.wikipedia.org/wiki/Wydad_Athletic_Club_(football)", description="Dima WYDAD!", color=0xff0000)
    embed.set_author(name=ctx.author.display_name, url="https://www.linkedin.com/in/mohamed-ilyass-salim-el-qalb-92ab19247/?originalSubdomain=ma", icon_url=ctx.author.display_avatar.url)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/fr/9/96/Logo_Wydad_Athletic_Club.png")
    embed.add_field(name="RCA", value="Rival de Casa", inline=True) #koun drt false ghyrj3o lster
    embed.add_field(name="FAR", value="Rival de Rabat", inline=True)
    embed.set_footer(text="Respectez les adversaires")
    await ctx.send(embed=embed)

@client.command()
async def barca(ctx):
    embed = discord.Embed(title="BARCA", url="https://www.fcbarcelona.fr/fr/club/identite/ecusson", description="Visca BARCA!", color=0x335bff)
    embed.set_author(name=ctx.author.display_name, url="https://www.linkedin.com/in/mohamed-ilyass-salim-el-qalb-92ab19247/?originalSubdomain=ma", icon_url=ctx.author.display_avatar.url)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/fr/thumb/a/a1/Logo_FC_Barcelona.svg/1200px-Logo_FC_Barcelona.svg.png")
    embed.add_field(name="Real", value="Grand rival", inline=True) 
    embed.add_field(name="Seville", value="Compétiteur", inline=True)
    embed.set_footer(text="Le fair-play avant tout")
    await ctx.send(embed=embed)

client.run(os.getenv('DISCORD_TOKEN'))
#demarre le bot et le connecte au jeton token entre ()