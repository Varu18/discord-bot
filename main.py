
import os
import discord
from dotenv import load_dotenv

load_dotenv()


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if (message.channel.id == 1545374003173130312 and message.content.startswith('salut')):
            await message.channel.send(f'Salutare acolo {message.author}!')
    
    async def on_member_join(self, member):
        channel = self.get_channel(1545395912086519889)

        if channel:
            await channel.send(f"👋 Bine ai venit, {member.mention}!")

    async def on_member_remove(self, member):
        channel = self.get_channel(1545395912086519889)

        if channel:
            await channel.send(f"😢 {member.name} a părăsit serverul.")
    


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = Client(intents=intents)
client.run(os.getenv('DISCORD_TOKEN')) 