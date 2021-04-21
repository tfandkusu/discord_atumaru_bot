import os
import discord

BODY_TEXT = "参加したい人は👍リアクションを付けてください。"
COUNT_TEXT = "現在参加希望者(%d人)\n"
HELP_HEAD = "使い方"
HELP_MESSAGE = """
使い方
```
/atumaru 募集文
```
"""

# リアクション削除の取得に必要
intents = discord.Intents.default()
intents.members = True
# クライアントを作成
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    "メッセージが追加されたときに呼ばれる"
    if message.author == client.user:
        return
    # メッセージは前後の空白が自動で除去される
    content = message.content
    if content.startswith('/atumaru '):
        # 募集文掲載
        recruiting = content[8:]
        body = "%s\n%s" % (recruiting, BODY_TEXT)
        await message.channel.send(body)
    elif content == '/atumaru':
        # ヘルプ表示
        body = HELP_MESSAGE
        await message.channel.send(body)


async def on_reaction_update(reaction, user):
    "リアクションが追加または削除されたときに呼ばれる"
    message = reaction.message
    # Botが書いたメッセージに対して
    if message.author != client.user:
        return
    # ヘルプ表示ではなく
    if message.content.startswith(HELP_HEAD):
        return
    # 👍リアクションの時は
    if reaction.emoji != '👍':
        return
    # 編集後のメッセージ文字列を生成して
    lines = message.content.splitlines()
    content = "%s\n%s" % (lines[0], lines[1])
    if reaction.count >= 1:
        content += "\n\n"
        content += COUNT_TEXT % reaction.count
        async for user in reaction.users():
            content += "%s\n" % user.mention
    # メッセージを編集する
    await message.edit(content=content)


@client.event
async def on_reaction_add(reaction, user):
    "リアクションが追加されたときに呼ばれる"
    await on_reaction_update(reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    "リアクションが削除されたときに呼ばれる"
    await on_reaction_update(reaction, user)


# 環境変数からトークンを得る
token = os.environ['DISCORD_TOKEN']
# 実行する
client.run(token)
