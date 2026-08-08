from discord.ext import commands

bot = commands.Bot(command_prefix="!")

def is_guild_owner():
    async def predicate(ctx):
        return ctx.author.id == ctx.guild.owner_id
    return commands.check(predicate)