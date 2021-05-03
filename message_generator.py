"メッセージ作成"
import sep

TEST_TAG = "【テスト】"
BODY_TEXT = "参加したい人は👍リアクションを付けてください。"
HELP_HEAD = "使い方"
HELP_MESSAGE = """
使い方
```
/atumaru 募集文
```
"""
COUNT_TEXT = "現在参加希望者(%d人)\n"


def make_command_message(test_flag, content):
    """
    ユーザの投稿メッセージに対して、Botが投稿するメッセージと👍リアクションフラグを返却する。
    Botが投稿するメッセージがないときは(None, False)を返却する。
    """

    # コマンド名は本番とテストで違う
    if test_flag:
        command = '/atumaru_test'
    else:
        command = '/atumaru'

    # コマンドに対応したメッセージ
    if content.startswith(command + ' '):
        # 募集文掲載
        recruiting = content[(len(command) + 1):]
        # @everyoneを付ける
        recruiting = '@everyone ' + recruiting
        # テストモードの時は【テスト】を追加
        if test_flag:
            recruiting = TEST_TAG + recruiting
        body = "%s\n%s" % (recruiting, BODY_TEXT)
        return body, True
    elif content == command:
        # ヘルプ表示
        body = HELP_MESSAGE
        return body, False
    else:
        return None, False


def make_reaction_update_message(test_flag, content, user_mentions,
                                 sep_flag=False):
    """
    Botの投稿メッセージに対するリアクションに反応する
    contentは現在投稿メッセージ。user_mentionsは現在リアクションを付けたユーザのmention文字列一覧。
    Bot自身のそれは除く。
    返却は編集後のメッセージ。Noneの時はなにもしない。
    sep_flagがTrueで5人いるときは、2vs2のマッチング表を出力する。
    """
    # ヘルプ表示ではなく
    if content.startswith(HELP_HEAD):
        return None
    # 【テスト】と付いているメッセージに対して
    if content.startswith(TEST_TAG):
        # 本番環境
        if test_flag == False:
            return None
    # 【テスト】と付いてないメッセージに対して
    if content.startswith(TEST_TAG) == False:
        # 本番環境で無い
        if test_flag == True:
            return None
    # 編集後のメッセージ文字列を生成して
    lines = content.splitlines()
    edited = "%s\n%s" % (lines[0], lines[1])
    if len(user_mentions) >= 1:
        edited += "\n\n"
        # 現在参加希望者(N人)
        edited += COUNT_TEXT % len(user_mentions)
        # 参加者一覧
        for mention in user_mentions:
            edited += "%s\n" % mention
    if sep_flag and len(user_mentions) == 5:
        # SEP向けマッチング表出力
        edited += sep.make_matching(user_mentions)
    return edited
