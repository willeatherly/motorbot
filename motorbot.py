#by Will Eatherly
#I'm sorry, in advance

#import PonyORM for postgres
from pony.orm import *
import validators
#import discord.py and supporting packages
import discord
from discord.ext import commands

#set up the class for bikes, probably
db = Database()
class Bikes(db.Entity):
    __table_name__ = 'bikes'
    discordid = PrimaryKey(str)
    bike = Required(str)
    secretfield = Optional(str)

#setup the bot
intents= discord.Intents.default()
intents.members = True
intents.message_content = True
description = 'A bot designed to track user\'s cars and motorcycles! Type \"!usage" for how to add your information!'
bot = commands.Bot(command_prefix='!', description=description, intents=intents )

class ChannelOrMemberConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        
        member_converter = commands.MemberConverter()
        try:
            member = await member_converter.convert(ctx, argument)
        except commands.MemberNotFound:
            pass
        else:
            return member

        # Do the same for TextChannel...
        textchannel_converter = commands.TextChannelConverter()
        try:
            channel = await textchannel_converter.convert(ctx, argument)
        except commands.ChannelNotFound:
            pass
        else:
            return channel

        raise commands.BadArgument(f'No Member or TextChannel could be converted from "{argument}"')

@bot.command()
async def amalive(ctx:commands.Context):
    await ctx.send(f'alive')

@db_session
def readbikes(userid):
    try:
        bikeuser = Bikes[userid]
    
    except:
        return
    
    bikelist = bikeuser.bike
    return bikelist

@bot.command()
async def bikes(ctx:commands.Context, user: discord.User=None):
    userid = 0

    if user is None:
        userid = ctx.author.id
        userobj = ctx.author
    else: 
        userid = user.id
        userobj = user
    
    bikelist = readbikes(str(userid))
    #print(bikelist)
    url = False
    link = ""
    printing = ""
    if validators.url(bikelist):
        link = bikelist
        url = True
    for x in bikelist:
        if x == "\n":
            url = True
            link = ""
            init = bikelist.split('\n')
            printing = ""
            constructing = ""
            if validators.url(init[-1]):
                link = link + init[-1]
            
                init = init[:-1]
                for x in init:
                    constructing += x + "\n"

                printing = constructing[:-1]
            
            else:
                printing += bikelist
    
    if not url:
        printing = bikelist

    embed=discord.Embed(title=printing)
    embed.set_author(name=userobj.display_name+"\'s bikes", icon_url=userobj.display_avatar.url)
    embed.set_thumbnail(url=link)
    await ctx.send(embed=embed)
    #await ctx.send(bikelist)
    


@db_session
def newbiker(user,newbikes):
    try:
        Bikes[user].bike = newbikes
        return "old"
    except:
        newbiker = Bikes(discordid = user, bike = newbikes, secretfield = "")
        return "new"

@bot.command()
async def setbikes(ctx:commands.Context, *, newbikes:str):
    user = ctx.author
    result = newbiker(str(user.id), newbikes)
    if result == "old":
        await ctx.send(f"Updated Bikes for " + ctx.author.display_name)
    else:
        await ctx.send(f"New user added to the bike database!")
    
    bikelist = readbikes(str(user.id))
    #print(bikelist)
    url = False
    link = ""
    printing = ""
    if validators.url(bikelist):
        link = bikelist
        url = True
    for x in bikelist:
        if x == "\n":
            url = True
            link = ""
            init = bikelist.split('\n')
            printing = ""
            constructing = ""
            if validators.url(init[-1]):
                link = link + init[-1]
            
                init = init[:-1]
                for x in init:
                    constructing += x + "\n"

                printing = constructing[:-1]
            
            else:
                printing += bikelist
    
    if not url:
        printing = bikelist

    embed=discord.Embed(title=printing)
    embed.set_author(name=user.display_name+"\'s bikes", icon_url=user.display_avatar.url)
    embed.set_thumbnail(url=link)
    await ctx.send(embed=embed)

    #embed=discord.Embed(title=readbikes(str(user.id)))
    #embed.set_author(name=user.display_name+"\'s bikes", icon_url=user.display_avatar.url)
    #await ctx.send(embed=embed)
    
#cars section
@db_session
def newdriver(user,newbikes):
    try:
        Bikes[user].secretfield = newbikes
        return "old"
    except:
        newbiker = Bikes(discordid = user, bike = "None", secretfield = newbikes)
        return "new"

@db_session
def readcars(userid):
    try:
        bikeuser = Bikes[userid]
    
    except:
        return
    
    bikelist = bikeuser.secretfield
    return bikelist

@bot.command()
async def setcars(ctx:commands.Context, *, newbikes:str):
    user = ctx.author
    result = newdriver(str(user.id), newbikes)
    if result == "old":
        await ctx.send(f"Updated Cars for " + ctx.author.display_name)
    else:
        await ctx.send(f"New user added to the car database!")
    bikelist = readcars(str(user.id))
    url = False
    link = ""
    printing = ""
    if validators.url(bikelist):
        link = bikelist
        url = True

    for x in bikelist:
        if x == "\n":
            url = True
            link = ""
            init = bikelist.split('\n')
            printing = ""
            constructing = ""
            if validators.url(init[-1]):
                link = link + init[-1]
            
                init = init[:-1]
                for x in init:
                    constructing += x + "\n"

                printing = constructing[:-1]
            
            else:
                printing += bikelist
    
    if not url:
        printing = bikelist

    embed=discord.Embed(title=printing)
    embed.set_author(name=user.display_name+"\'s cars", icon_url=user.display_avatar.url)
    embed.set_thumbnail(url=link)
    await ctx.send(embed=embed)
    
    #embed=discord.Embed(title=readcars(str(user.id)))
    #embed.set_author(name=user.display_name+"\'s cars", icon_url=user.display_avatar.url)
    #await ctx.send(embed=embed)

@bot.command()
async def cars(ctx:commands.Context, user: discord.User=None):
    userid = 0

    if user is None:
        userid = ctx.author.id
        userobj = ctx.author
    else: 
        userid = user.id
        userobj = user
    
    bikelist = readcars(str(userid))
    #print(bikelist)
    url = False
    link = ""
    printing = ""
    if validators.url(bikelist):
        link = bikelist
        url = True

    for x in bikelist:
        if x == "\n":
            url = True
            link = ""
            init = bikelist.split('\n')
            printing = ""
            constructing = ""
            if validators.url(init[-1]):
                link = link + init[-1]
            
                init = init[:-1]
                for x in init:
                    constructing += x + "\n"

                printing = constructing[:-1]
            
            else:
                printing += bikelist
    
    if not url:
        printing = bikelist

    embed=discord.Embed(title=printing)
    embed.set_author(name=userobj.display_name+"\'s cars", icon_url=userobj.display_avatar.url)
    embed.set_thumbnail(url=link)
    await ctx.send(embed=embed)

@bot.command()
async def usage(ctx:commands.Context):
    await ctx.send(f"The bot is pretty straightforward, but has some rules you need to follow.\n\nTo add your bike, use the `!setbikes` command, and for cars, use the `!setcars` command.\n\nTo view your cars or bikes, use the `!cars` or `!bikes` command. This also works if you tag a user.\nex: ```!cars @discorduser``` ```!bikes @discorduser```\n\nIf you want to add an image, create a newline at the end of the command and paste a link to the image. Some image providers don't work, so the best way to do this is paste an image in Discord, and use the link generated from the paste (right click and select \"copy link\")\n\nHere's an example with multiple vehicles and an image:\n```!setcars 2002 Honda Civic\n2005 Honda S2000\nhttps://example.com/abc.jpg``` ```!setbikes 2020 Kawasaki Ninja 650\n2005 Suzuki GSX-R 1000\nhttps://example.com/abc.gif``` \n**NOTE, IMAGE MUST BE A JPG OR GIF FILE**")

def main():
    db.bind(provider='postgres',user='postgres',password='user',database='postgres')
    db.generate_mapping(create_tables=False)
    bot.run('key')

main()
 
