import discord

def default_embed(title: str = "", message: str = ""):
    embed = discord.Embed(title=title, description=message, color=0xA68BD3)
    return embed


def error_embed(title: str = "", message: str = ""):
    embed = discord.Embed(title=title, description=message, color=0xFC5165)
    return embed

def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]