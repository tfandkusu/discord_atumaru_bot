import os
import discord
from retrying import retry
import message_generator as mg

ATUMARU_BOT_ENV_DEV = "dev"
ATUMARU_BOT_ENV_PROD = "prod"
# 環境を確認
ATUMARU_BOT_ENV = os.environ['ATUMARU_BOT_ENV']
if ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_DEV and ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_PROD:
    raise "ATUMARU_BOT_ENV must be 'dev' or 'prod'"
ATUMARU_BOT_SEP = os.environ.get('ATUMARU_BOT_SEP')


def is_test_mode():
    "テストモードならばTrueを返却する"
    return ATUMARU_BOT_ENV == ATUMARU_BOT_ENV_DEV


def is_sep():
    "SEP向けならばTrueを返却する"
    return ATUMARU_BOT_SEP is not None


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
        auther_menthon=message.author.mention,
        test_flag=is_test_mode(),
        content=content)
    # 投稿文があれば投稿する
    if body != None:
        message = await message.channel.send(body)
        # リアクションを必要に応じて付ける
        if reaction_flag:
            await message.add_reaction('👍')
            await message.add_reaction('🗑')
            await message.add_reaction('🆗')


async def on_reaction_update(reaction, user):
    "リアクションが追加または削除されたときに呼ばれる"
    message = reaction.message
    # Botが書いたメッセージに対して
    if message.author != client.user:
        return
    # 👍付けた人のメンション一覧
    user_mentions = []
    # 🗑付けた人のメンション一覧
    trash_user_mentions = []
    # 🆗付けた人のメンション一覧
    ok_user_mentions = []
    # メッセージについているリアクションをすべて取得
    for reaction in message.reactions:
        # リアクションのユーザ一覧
        async for user in reaction.users():
            if user != client.user:
                # Bot以外
                if reaction.emoji == '👍':
                    user_mentions.append(user.mention)
                elif reaction.emoji == '🗑':
                    trash_user_mentions.append(user.mention)
                elif reaction.emoji == '🆗':
                    ok_user_mentions.append(user.mention)
    # 編集後メッセージ作成
    edited = mg.make_reaction_update_message(
        test_flag=is_test_mode(),
        content=message.content,
        user_mentions=user_mentions,
        trash_user_mentions=trash_user_mentions,
        ok_user_mentions=ok_user_mentions,
        sep_flag=is_sep())
    if edited == '':
        # 削除する
        await message.delete()
    elif edited != None:
        # メッセージを編集する
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


def on_exception(e):
    print(e)
    return True


class BotTask:

    def __init__(self):
        # start関数が呼ばれた回数
        self.start_count = 0

    # 合計4時間待つ
    # 最初は10秒待つ。失敗したらインターバルを2倍にする。
    # 合計4時間が経ってしまったら、例外を再度raiseする
    # 毎回の例外は標準出力する
    @retry(stop_max_delay=4*60*60*1000, wait_exponential_multiplier=5000,
           wrap_exception=True, retry_on_exception=on_exception)
    def start(self):
        print("start %d" % self.start_count)
        self.start_count += 1
        client.run(token, reconnect=False)


task = BotTask()
task.start()
