import discord
from discord.ext import commands

import helpers.ioi as ioi
import nice


class ProblemView(discord.ui.View):
    def __init__(self, timeout=120):
        super().__init__()
        self.choice = None
        self.timed_out = False
        
    async def on_timeout(self):
        self.timed_out = True  # used to check if timeout occurred

    @discord.ui.button(label="accept", style=discord.ButtonStyle.primary)
    async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "accept"
        await interaction.response.edit_message(content="good luck!", view=None)
        self.stop()

    @discord.ui.button(label="reroll", style=discord.ButtonStyle.secondary)
    async def reroll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "reroll"
        await interaction.response.defer()
        self.stop()

    @discord.ui.button(label="reject", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.choice = "reject"
        await interaction.response.edit_message(content="cancelled challenge", view=None, embed=None)
        self.stop()


class IOICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(brief="Get a new IOI problem.")
    async def ioichal(self, ctx):
        if ctx.message.author == self.bot.user: return

        message = await ctx.send(content="getting problem...\n")
        usercode = ctx.author.id
        taken = False
        firstPass = True

        while not taken:
            print("looped")

            if not firstPass: await message.edit(content="getting another problem...\n", embed = None, view = None)

            problem = ioi.challenge(usercode)
            
            print("generated problem!")
            
            problemDisplay = problem[0].disp()
            problemStats = problem[0].getStats()
            problemLinks = problem[0].getLinks()

            print(problemDisplay, problemStats, problemLinks, sep='\n')

            toSendEmbed = discord.Embed(title=problemDisplay, color=nice.randomRGB(255 * 0.25, 255))
            toSendEmbed.set_footer(text=f"challenging {ctx.author.name}, who has pool of {problem[1]} problems.")
            toSendEmbed.add_field(name="problem statistics",
                                  value=problemStats,
                                  inline=False)
            toSendEmbed.add_field(name="problem links (untested, might be broken)",
                                  value=problemLinks,
                                  inline=False)

            view = ProblemView(timeout=120)
            await message.edit(content="accept challenge?", embed=toSendEmbed, view=view)
            await view.wait()
            
            if view.timed_out:
                await message.edit(content="challenge timed out due to inactivity.", embed=None, view=None)
                return

            if view.choice == "accept":
                ioi.pendProblem(usercode, problem[0])
                taken = True
            elif view.choice == "reject":
                return
            elif view.choice == "reroll":
                firstPass = False
                continue
            
async def setup(bot):
    await bot.add_cog(IOICommands(bot))