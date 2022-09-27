from typing import List, Mapping, Optional
from unicodedata import category
import discord
from discord.ext import commands
from interpreter import CommandParser

# CODE = "```"
# BOLD = "**"

# class AlgebraBot(discord.Client):
#     async def on_ready(self):
#         await self.get_channel(1022997133516877865).send(BOLD + "AlgebraBot est connecté au serveur !\npréfixe: " + CommandParser.prefix + BOLD)
#         print("le bot est prêt")

#     async def on_message(self, message:discord.Message):
#         s: str = message.content

#         if(not s.startswith(CommandParser.prefix)):
#             return

#         comm = s.removeprefix(CommandParser.prefix)
#         await self.interpret(self.get_channel(1022997133516877865), comm)

#     async def interpret(self, channel:discord.TextChannel, comm: str):
#         async with channel.typing():
#             parser = CommandParser()
#             rep = parser.parseCommand(comm)
#             await channel.send(embed=rep.build())

DEFAULTCOLOR = discord.Color.dark_blue()
ERRORCOLOR = discord.Color.dark_orange()

f = open("bot/secret.txt", encoding="utf-8")

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping:Mapping[Optional[commands.Cog], List[commands.Command]]):
        embed = discord.Embed(title="List of available commands :", colour=DEFAULTCOLOR, type='rich')
        for cog, cmds in mapping.items():  # get the cog and its commands
            embed.add_field(name=("No category" if cog is None else cog.qualified_name), value=f'{len(cmds)} commands')

        channel:discord.abc.MessageableChannel = self.get_destination()  # this method is inherited from `HelpCommand`, and gets the channel in context
        await channel.send(embed=embed)
    
bot = commands.Bot("/", help_command=CustomHelpCommand())
bot.intents.all()

@bot.event
async def on_ready():
    print("bot is ready !")


@bot.slash_command(name="cloud_add", help="this should be the response of the help command", brief="add a file to cloud", description="add a file to cloud specifying the visibility")
async def cloud_add(ctx:commands.Context, visibility:str, file: discord.Attachment):
    await ctx.respond("File" + file.filename + " added to "+("shared" if visibility == "shared" else "personnal")+" cloud.")

bot.run(f.read())
