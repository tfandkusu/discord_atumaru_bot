import os
import discord

BODY_TEXT = "参加したい人は👍リアクションを付けてください。"
COUNT_TEXT = "現在参加希望者(%d人)"

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    content = message.content
    if content.startswith('/atumaru '):
        recruiting = content[8:].strip()
        # TODO 本文空白ケース
        body = "%s\n%s" % (recruiting, BODY_TEXT)
        await message.channel.send(body)

client.run(os.environ['DISCORD_TOKEN'])
