from nextcord import Intents, Status, Game, Interaction
from nextcord.ext import commands, application_checks
from cooldowns import CallableOnCooldown
from os import getenv

from .utilites import log

class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            help_command=None,
            command_prefix=getenv("PREFIX"),
            intents=intents,
            activity=Game(getenv("ACTIVITY")),
            status=Status.idle,
        )

    async def on_ready(self):
        GUILD = self.get_guild(int(getenv("GUILD")))

        log("INIT", f"The bot logged in as {self.user} and ready to serve {GUILD.member_count} members in the {GUILD.name}.")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            ctx.send("Cubot now supports slash commands. Try typing /info.")

    async def on_application_command_error(self, interaction: Interaction, error):
        error = getattr(error, 'original', error)
        
        if isinstance(error, CallableOnCooldown):
            await interaction.send(error)
        if isinstance(error, application_checks.errors.ApplicationMissingRole):
            await interaction.send('Missing required permission(s).')
        if isinstance(error, application_checks.errors.ApplicationNotOwner):
            await interaction.send('Missing required permission(s).')
        else:
            log("ERROR", error)