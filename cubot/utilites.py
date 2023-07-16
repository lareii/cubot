from datetime import datetime
from nextcord import Embed

def log(level, message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(time, level, message)

def embed_builder(
        title="", 
        desc="Hello from utilities.embed_builder", 
        footer="", 
        fields=[], 
        thumb=""
    ):
    embed = Embed()
    embed.title = title
    embed.description = desc
    embed.color = 0
    embed.set_footer(text=footer)
    embed.set_thumbnail(url=thumb)

    if fields:
        for field in fields:
            name, value, inline = field.values()
            embed.add_field(name=name, value=value, inline=inline)

    return embed