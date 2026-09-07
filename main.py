import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()


GUILD_ID = discord.Object(id=1545374002099527752)
MODERATOR_ROLE_ID = 1546574166126497884
warnings = {}


class Client(commands.Bot):

    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)
        print("Slash commands synced!")

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if (
            message.channel.id == 1545374003173130312
            and message.content.startswith('salut')
        ):
            await message.channel.send(
                f'Salutare acolo {message.author}!'
            )

    async def on_member_join(self, member):
        channel = self.get_channel(1545395912086519889)

        if channel:
            await channel.send(
                f"👋 Bine ai venit, {member.mention}!"
            )

    async def on_member_remove(self, member):
        channel = self.get_channel(1545395912086519889)

        if channel:
            await channel.send(
                f"😢 {member.name} a părăsit serverul."
            )


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(
    command_prefix='!',
    intents=intents
)


@client.tree.command(
    name='salut',
    description='Salută botul'
)
async def salut(interaction: discord.Interaction):
    await interaction.response.send_message(
        'Salut! Ce mai faci?'
    )


@client.tree.command(
    name='ping',
    description='Verifică latența botului'
)
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)

    await interaction.response.send_message(
        f'🏓 Pong! {latency}ms'
    )


@client.tree.command(
    name='clear',
    description='Șterge un număr specificat de mesaje'
)
@app_commands.describe(
    num_messages='Numărul de mesaje de șters'
)
@app_commands.checks.has_permissions(
    manage_messages=True
)
async def clear(
    interaction: discord.Interaction,
    num_messages: int
):
    if num_messages < 1:
        await interaction.response.send_message(
            '❌ Trebuie să specifici un număr mai mare de 0.',
            ephemeral=True
        )
        return

    deleted = await interaction.channel.purge(
        limit=num_messages
    )

    await interaction.response.send_message(
        f'✅ Am șters {len(deleted)} mesaje.',
        ephemeral=True
    )


@clear.error
async def clear_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            '❌ Nu ai permisiunea să ștergi mesaje.',
            ephemeral=True
        )



@client.tree.command(
    name='kick',
    description='Dă afară un membru de pe server'
)
@app_commands.describe(
    user='Membrul care va fi dat afară',
    reason='Motivul pentru kick'
)
async def kick(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: str = 'Nu a fost specificat'
):
    moderator_role = interaction.guild.get_role(MODERATOR_ROLE_ID)

    if moderator_role not in interaction.user.roles:
        await interaction.response.send_message(
            '❌ Nu ai rolul necesar pentru această comandă.',
            ephemeral=True
        )
        return

    await user.kick(reason=reason)

    await interaction.response.send_message(
        f'👢 {user.mention} a fost dat afară de pe server.\n'
        f'Motiv: {reason}'
    )


@kick.error
async def kick_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            '❌ Ai nevoie de rolul 🔨 Moderator pentru această comandă.',
            ephemeral=True
        )




@client.tree.command(
    name='warn',
    description='Avertizează un membru'
)
@app_commands.describe(
    user='Membrul care primește warning',
    reason='Motivul warningului'
)
async def warn(
    interaction: discord.Interaction,
    user: discord.Member,
    reason: str = 'Nu a fost specificat'
):
    moderator_role = interaction.guild.get_role(MODERATOR_ROLE_ID)

    if moderator_role not in interaction.user.roles:
        await interaction.response.send_message(
            '❌ Nu ai rolul necesar pentru această comandă.',
            ephemeral=True
        )
        return

    user_id = user.id

    if user_id not in warnings:
     warnings[user_id] = []

    warnings[user_id].append(reason)

    warning_count = len(warnings[user_id])

    if warning_count >= 3:
        await user.kick(reason=f'3 warnings. Ultimul motiv: {reason}')

        del warnings[user_id]

        await interaction.response.send_message(
            f'👢 {user.mention} a primit al 3-lea warning și a fost dat afară.\n'
            f'Ultimul motiv: {reason}'
        )

        return

    await interaction.response.send_message(
        f'⚠️ {user.mention} a primit un warning.\n'
        f'Motiv: {reason}\n'
        f'Warnings: {warning_count}/3'
    )


@client.tree.command(
    name='warnings',
    description='Vezi warningurile unui membru'
)
@app_commands.describe(
    user='Membrul ale cărui warninguri vrei să le vezi'
)
async def warnings_command(
    interaction: discord.Interaction,
    user: discord.Member
):
    moderator_role = interaction.guild.get_role(MODERATOR_ROLE_ID)

    if moderator_role not in interaction.user.roles:
        await interaction.response.send_message(
            '❌ Nu ai rolul necesar pentru această comandă.',
            ephemeral=True
        )
        return

    user_warnings = warnings.get(user.id, [])

    if not user_warnings:
        await interaction.response.send_message(
            f'✅ {user.mention} nu are niciun warning.',
            ephemeral=True
        )
        return

    warning_list = '\n'.join(
        f'{index}. {reason}'
        for index, reason in enumerate(user_warnings, start=1)
    )

    await interaction.response.send_message(
        f'⚠️ Warnings pentru {user.mention}\n\n'
        f'{warning_list}\n\n'
        f'Total: {len(user_warnings)}/3'
    )







client.run(os.getenv('DISCORD_TOKEN'))