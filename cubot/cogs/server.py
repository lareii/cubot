from nextcord import ButtonStyle, Interaction, slash_command
from nextcord.ext import commands, application_checks
from nextcord.ui import View, Button, button
from cooldowns import SlashBucket, cooldown
from os import getenv, startfile
from asyncio import sleep
from subprocess import run

from ..utilites import log

class Buttons(View):
    def __init__(self):
        super().__init__()
        self.value = False

    @button(label="Accept", style=ButtonStyle.green)
    async def accept(self, button: Button, interaction: Interaction):
        await interaction.send("Process has been accepted, server will reboot in 5 seconds.", ephemeral=True)
        self.value = True
        self.stop()

    @button(label="Decline", style=ButtonStyle.red)
    async def decline(self, button: Button, interaction: Interaction):
        await interaction.send("Process has been denied.", ephemeral=True)
        self.stop()

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Reboots the game server.", guild_ids=[int(getenv("GUILD"))])
    @application_checks.has_role(int(getenv("REBOOT")))
    @cooldown(1, 60, bucket=SlashBucket.guild)
    async def reboot(self, interaction: Interaction):
        buttons = Buttons()

        await interaction.send("The server will reboot, do you accept that?", view=buttons, ephemeral=True)
        await buttons.wait()

        if buttons.value:
            await interaction.delete_original_message()

            try:
                server_path = getenv("SERVER")
                server_name = server_path.split("\\")[-1]

                resp = run(f'taskkill /f /im "{server_name}"', capture_output=True)
                if not resp.stdout:
                    log("ERROR", str(resp.stderr).replace("ERROR: ", ""))
                
                await sleep(5)
                startfile(server_path)

                await interaction.send("Server is back online!", ephemeral=True)

                log("INFO", f"Server restarted by {interaction.user.name}")
            
            except Exception:
                await interaction.send("An error occurred.", ephemeral=True)

def setup(bot):
    bot.add_cog(Server(bot))