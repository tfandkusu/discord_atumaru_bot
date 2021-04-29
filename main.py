import os
import discord
import message_generator as mg

ATUMARU_BOT_ENV_DEV = "dev"
ATUMARU_BOT_ENV_PROD = "prod"
# 環境を確認
ATUMARU_BOT_ENV = os.environ['ATUMARU_BOT_ENV']
if ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_DEV and ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_PROD:
    raise "ATUMARU_BOT_ENV must be 'dev' or 'prod'"


def is_test_mode():
    "テストモードならばTrueを返却する"
    return ATUMARU_BOT_ENV == ATUMARU_BOT_ENV_DEV


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
    # 投稿文を作成する
    body, reaction_flag = mg.make_command_message(
        test_flag=is_test_mode(),
        content=content)
    # 投稿文があれば投稿する
    if body != None:
        message = await message.channel.send(body)
        # リアクションを必要に応じて付ける
        if reaction_flag:
            await message.add_reaction('👍')


async def on_reaction_update(reaction, user):
    "リアクションが追加または削除されたときに呼ばれる"
    message = reaction.message
    # Botが書いたメッセージに対して
    if message.author != client.user:
        return
    # 👍リアクションの時は
    if reaction.emoji != '👍':
        return
    # メンション一覧
    user_mentions = []
    async for user in reaction.users():
        if user != client.user:
            user_mentions.append(user.mention)
    # 編集後メッセージ作成
    edited = mg.make_reaction_update_message(
        test_flag=is_test_mode(),
        content=message.content,
        user_mentions=user_mentions)
    # メッセージを編集する
    if edited != None:
        await message.edit(content=edited)


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
