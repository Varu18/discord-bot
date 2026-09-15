import datetime
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from database import add_warning, get_warnings, remove_warning

load_dotenv()


GUILD_ID = discord.Object(id=1545374002099527752)
MODERATOR_ROLE_ID = 1546574166126497884


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

    await interaction.response.defer(
        ephemeral=True
    )

    deleted = await interaction.channel.purge(
        limit=num_messages
    )

    embed = discord.Embed(
        title='🧹 Messages Cleared',
        description=f'Am șters {len(deleted)} mesaje din acest canal.',
        color=discord.Color.purple()
    )

    embed.set_footer(
        text=f'Cleared by {interaction.user.display_name}'
    )

    await interaction.edit_original_response(
        embed=embed
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

    embed = discord.Embed(
        title='👢 Member Kicked',
        description=f'{user.mention} a fost dat afară de pe server.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name='User',
        value=user.mention,
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Kicked by {interaction.user.display_name}'
    )

    await interaction.response.send_message(embed=embed)

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
    name='ban',
    description='Banează un membru de pe server'
)
@app_commands.describe(
    user='Membrul care va fi banat',
    reason='Motivul pentru ban'
)
async def ban(
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

    await user.ban(reason=reason)

    embed = discord.Embed(
        title='🔨 Member Banned',
        description=f'{user.mention} a fost banat de pe server.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name='User',
        value=user.mention,
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Banned by {interaction.user.display_name}'
    )

    await interaction.response.send_message(embed=embed)



@client.tree.command(
    name='unban',
    description='Debanează un utilizator de pe server'
)
@app_commands.describe(
    user_id='ID-ul utilizatorului care va fi debanat',
    reason='Motivul pentru unban'
)
async def unban(
    interaction: discord.Interaction,
    user_id: str,
    reason: str = 'Nu a fost specificat'
):
    moderator_role = interaction.guild.get_role(MODERATOR_ROLE_ID)

    if moderator_role not in interaction.user.roles:
        await interaction.response.send_message(
            '❌ Nu ai rolul necesar pentru această comandă.',
            ephemeral=True
        )
        return

    try:
        user = await client.fetch_user(int(user_id))
        await interaction.guild.unban(user, reason=reason)

    except ValueError:
        await interaction.response.send_message(
            '❌ ID-ul utilizatorului nu este valid.',
            ephemeral=True
        )
        return

    except discord.NotFound:
        await interaction.response.send_message(
            '❌ Acest utilizator nu este banat sau nu a fost găsit.',
            ephemeral=True
        )
        return

    embed = discord.Embed(
        title='🔓 Member Unbanned',
        description=f'{user.mention} a fost debanat de pe server.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(
        url=user.display_avatar.url
    )

    embed.add_field(
        name='User',
        value=f'{user.mention}\n`{user.id}`',
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Unbanned by {interaction.user.display_name}'
    )

    await interaction.response.send_message(
        embed=embed
    )



@client.tree.command(
    name='mute',
    description='Aplică un mute temporar unui membru'
)
@app_commands.describe(
    user='Membru care va primi mute',
    duration='Durata mute-ului în minute',
    reason='Motivul mute-ului'
)
async def mute(
    interaction: discord.Interaction,
    user: discord.Member,
    duration: int,
    reason: str = 'Nu a fost specificat'
):
    moderator_role = interaction.guild.get_role(MODERATOR_ROLE_ID)

    if moderator_role not in interaction.user.roles:
        await interaction.response.send_message(
            '❌ Nu ai rolul necesar pentru această comandă.',
            ephemeral=True
        )
        return

    if duration < 1:
        await interaction.response.send_message(
            '❌ Durata mute-ului trebuie să fie de cel puțin 1 minut.',
            ephemeral=True
        )
        return

    if duration > 40320:
        await interaction.response.send_message(
            '❌ Durata mute-ului nu poate depăși 28 de zile (40320 minute).',
            ephemeral=True
        )
        return

    if user.guild_permissions.administrator:
        await interaction.response.send_message(
            '❌ Nu poți aplica mute unui administrator.',
            ephemeral=True
        )
        return
    
    await interaction.response.defer(
        ephemeral=True
    )   

    timeout_duration = datetime.timedelta(
        minutes=duration
        )


    await user.timeout(
        timeout_duration,
        reason=reason
    )

    embed = discord.Embed(
        title='🔇 Member Muted',
        description=f'{user.mention} a primit mute pentru {duration} minute.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name='User',
        value=user.mention,
        inline=True
    )

    embed.add_field(
        name='Duration',
        value=f'{duration} minute',
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Muted by {interaction.user.display_name}'
    )

    await interaction.edit_original_response(
        embed=embed
        )



@client.tree.command(
    name='unmute',
    description='Elimină mute-ul unui membru'
)
@app_commands.describe(
     user='Membrul căruia îi va fi eliminat mute-ul',
    reason='Motivul pentru eliminarea mute-ului'
)
async def unmute(
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

    await interaction.response.defer(
        ephemeral=True
    )

    await user.timeout(
        None,
        reason=reason
    )

    embed = discord.Embed(
        title='🔊 Member Unmuted',
        description=f'Mute-ul lui {user.mention} a fost eliminat.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(
        url=user.display_avatar.url
    )

    embed.add_field(
        name='User',
        value=user.mention,
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Unmuted by {interaction.user.display_name}'
    )

    await interaction.edit_original_response(
        embed=embed
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

    add_warning(user.id, reason)

    user_warnings = get_warnings(user.id)
    warning_count = len(user_warnings)


    if warning_count >= 3:
        await user.kick(
        reason=f'3 warnings. Ultimul motiv: {reason}'
    )

        embed = discord.Embed(
        title='👢 Member Kicked',
        description=f'{user.mention} a primit al 3-lea warning și a fost dat afară.',
        color=discord.Color.purple()
    )

        embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

        embed.set_footer(
        text=f'Action by {interaction.user.display_name}'
    )

        await interaction.response.send_message(embed=embed)
        return





    embed = discord.Embed(
    title='⚠️ Member Warned',
    description=f'{user.mention} a primit un warning.',
    color=discord.Color.purple()
)

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
    name='User',
    value=user.mention,
    inline=True
)

    embed.add_field(
        name='Warnings',
        value=f'{warning_count}/3',
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Warned by {interaction.user.display_name}'
    )

    await interaction.response.send_message(embed=embed)


@client.tree.command(
    name='unwarn',
    description='Elimină un warning unui membru'
)
@app_commands.describe(
    user='Membrul căruia îi va fi eliminat warning-ul',
    reason='Motivul pentru eliminarea warning-ului'
)
async def unwarn(
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

    removed = remove_warning(user.id)

    if removed == 0:
        await interaction.response.send_message(
            f'❌ {user.mention} nu are warninguri de eliminat.',
            ephemeral=True
        )
        return

    user_warnings = get_warnings(user.id)
    warning_count = len(user_warnings)

    embed = discord.Embed(
        title='✅ Warning Removed',
        description=f'Un warning a fost eliminat pentru {user.mention}.',
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=user.display_avatar.url)

    embed.add_field(
        name='User',
        value=user.mention,
        inline=True
    )

    embed.add_field(
        name='Warnings',
        value=f'{warning_count}/3',
        inline=True
    )

    embed.add_field(
        name='Reason',
        value=reason,
        inline=False
    )

    embed.set_footer(
        text=f'Unwarned by {interaction.user.display_name}'
    )

    await interaction.response.send_message(embed=embed)


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

    user_warnings = get_warnings(user.id)

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



@client.tree.command(
        name='help',
        description='Afișează lista de comenzi disponibile'
    )
async def help_command(
        interaction: discord.Interaction
    ):
        embed = discord.Embed(
            title='📜 VRU Bot - Help',
            description='Lista comenzilor disponibile:',
            color=discord.Color.purple()
        )

        embed.add_field(
            name='🔧 General',
            value=(
            '`/salut` - Salută botul\n'
            '`/ping` - Verifică latența botului\n'
            '`/help` - Afișează acest meniu'
            ),
            inline=False
        )

        embed.add_field(
            name='🛡️ Moderation',
             value=(
            '`/clear` - Șterge mesaje\n'
            '`/kick` - Dă afară un membru\n'
            '`/warn` - Avertizează un membru\n'
            '`/warnings` - Vezi warningurile unui membru\n'
            '`/ban` - Banează un membru de pe server\n'
            '`/unban` - Debanează un membru de pe server\n'
            '`/mute` - Dai mute unui membru pentru un anumit timp\n'
            '`/unmute` - Elimină mute-ul unui membru\n'
            ),
            inline=False
        )

        embed.set_footer(
            text=f'Requested by {interaction.user.display_name}'
        )

        await interaction.response.send_message(
            embed=embed)




client.run(os.getenv('DISCORD_TOKEN'))