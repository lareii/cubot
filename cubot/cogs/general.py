from nextcord import slash_command, __version__, Interaction
from nextcord.ext import commands
from datetime import timedelta
from time import time
from os import getenv

from ..utilites import embed_builder

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time()

    @slash_command(description="Displays information about the bot.")
    # guild_ids=[int(getenv("GUILD"))]
    async def info(self, interaction: Interaction):
        current_time = time()
        difference = int(round(current_time - self.start_time))
        uptime = str(timedelta(seconds=difference))

        embed = embed_builder(
            title=f"About {self.bot.user.name}",
            desc=f"**✨ Change Log**\n• Cubot v3.0 released.",
            fields=[
                {"name": ":1234: Bot version", "value": "v3.0", "inline": False},
                {"name": ":stopwatch: Bot latency", "value": str(round(self.bot.latency * 1000)), "inline": False},
                {"name": ":clock10: Bot uptime", "value": uptime, "inline": False},
                {"name": ":robot: Bot library", "value": f"nextcord=={__version__}", "inline": False},
            ],
            thumb=self.bot.user.avatar
        )

        await interaction.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if f"<@{self.bot.user.id}>" == message.content:
            await message.add_reaction("👀")

        if message.channel in self.bot.get_channel(int(getenv("SUGGESTIONS"))).threads:
            first_message = (await message.channel.history(limit=1, oldest_first=True).flatten())[0]
            await first_message.add_reaction("⬆️")

def setup(bot):
    bot.add_cog(General(bot))
