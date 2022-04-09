import os
import discord
import message_generator as mg
import asyncio
import time

ATUMARU_BOT_ENV_DEV = "dev"
ATUMARU_BOT_ENV_PROD = "prod"
# 環境を確認
ATUMARU_BOT_ENV = os.environ["ATUMARU_BOT_ENV"]
if ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_DEV and ATUMARU_BOT_ENV != ATUMARU_BOT_ENV_PROD:
    raise "ATUMARU_BOT_ENV must be 'dev' or 'prod'"
ATUMARU_BOT_SEP = os.environ.get('ATUMARU_BOT_SEP')


def is_test_mode():
    "テストモードならばTrueを返却する"
    return ATUMARU_BOT_ENV == ATUMARU_BOT_ENV_DEV


def is_sep():
    "SEP向けならばTrueを返却する"
    return ATUMARU_BOT_SEP is not None


class BotTask:
    "ネットワーク接続が切れたときの再接続対応クラス"

    def __init__(self):
        # 再接続を行った回数
        self.retry_count = 0

    def start_with_retry(self):
        "再接続対応でBotを開始する"
        while True:
            try:
                # Botを開始する
                self._start()
                # 正常終了の時はスクリプトを終了する
                break
            except Exception as e:
                self.retry_count += 1
                print(e)
                # エラーが発生したときは
                print("retry %d" % self.retry_count)
                # 2のリトライ回数乗×5秒待つ
                interval = 5 * 2**self.retry_count
                print("interval %d" % interval)
                # 待ち時間が4時間超えたら、スクリプトを終了する
                if interval >= 4 * 60 * 60:
                    break
                time.sleep(interval)

    def _start(self):
        # クライアントを作成
        client = self._make_client()
        # 環境変数からトークンを得る
        token = os.environ["DISCORD_TOKEN"]
        # Botを実行
        client.run(token, reconnect=False)

    def _make_client(self):
        "Discordのクライアントを作成する"
        # リアクション削除の取得に必要
        intents = discord.Intents.default()
        intents.members = True
        # Clientクラス内部で作られるイベントループは1スレッド1つ。
        # そしてエラーになると、それが閉じられるので、毎回新しく作成する
        loop = asyncio.new_event_loop()
        # それをクライアント作成時に渡す
        client = discord.Client(intents=intents, loop=loop)

        @client.event
        async def on_ready():
            # 接続出来たのでretry_countを戻す
            self.retry_count = 0
            print("We have logged in as {0.user}".format(client))

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
                content=content,
            )
            # 投稿文があれば投稿する
            if body != None:
                message = await message.channel.send(body)
                # リアクションを必要に応じて付ける
                if reaction_flag:
                    await message.add_reaction("👍")
                    await message.add_reaction("🗑")
                    await message.add_reaction("🆗")

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
                        if reaction.emoji == "👍":
                            user_mentions.append(user.mention)
                        elif reaction.emoji == "🗑":
                            trash_user_mentions.append(user.mention)
                        elif reaction.emoji == "🆗":
                            ok_user_mentions.append(user.mention)
            # 編集後メッセージ作成
            edited = mg.make_reaction_update_message(
                test_flag=is_test_mode(),
                content=message.content,
                user_mentions=user_mentions,
                trash_user_mentions=trash_user_mentions,
                ok_user_mentions=ok_user_mentions,
                sep_flag=is_sep(),
            )
            if edited == "":
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

        return client


task = BotTask()
task.start_with_retry()
