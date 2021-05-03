import unittest
import message_generator as mg


class TestMessageGenerator(unittest.TestCase):
    def test_recruiting_prod(self):
        "本番モードで募集"
        content, reaction = mg.make_command_message(
            False, '<@123>', '/atumaru 募集します')
        expected = """@everyone 募集します
参加したい人は👍リアクションを付けてください。
起案者 <@123> は🔑と🗑リアクションで削除出来ます。"""
        self.assertEqual(content, expected)
        self.assertTrue(reaction)

    def test_help_prod(self):
        "本番モードでヘルプ"
        content, reaction = mg.make_command_message(
            False, '<@123>', '/atumaru')
        self.assertEqual(content, mg.HELP_MESSAGE)
        self.assertFalse(reaction)

    def test_recruiting_dev(self):
        "テストモードで募集"
        content, reaction = mg.make_command_message(
            True, '<@123>', '/atumaru_test 募集します')
        expected = """【テスト】@everyone 募集します
参加したい人は👍リアクションを付けてください。
起案者 <@123> は🔑と🗑リアクションで削除出来ます。"""
        self.assertEqual(content, expected)
        self.assertTrue(reaction)

    def test_help_dev(self):
        "テストモードでヘルプ"
        content, reaction = mg.make_command_message(
            True, '<@123>', '/atumaru_test')
        self.assertEqual(content, mg.HELP_MESSAGE)
        self.assertFalse(reaction)

    def test_not_command(self):
        "コマンドでないケース"
        content, reaction = mg.make_command_message(
            True, '<@123>', '/not_command')
        self.assertEqual(content, None)
        self.assertFalse(reaction)

    def test_reaction_to_help(self):
        "ヘルプへのリアクションケース"
        content = "使い方\n```"
        edited = mg.make_reaction_update_message(False, content, [], [], [])
        self.assertEqual(edited, None)

    def test_reaction_to_dev_in_prod(self):
        "本番モードで【テスト】とついているメッセージにリアクション"
        content = "【テスト】@everyone 募集文"
        edited = mg.make_reaction_update_message(False, content, [], [], [])
        self.assertEqual(edited, None)

    def test_reaction_to_prod_in_dev(self):
        "テストモードで【テスト】とついていないメッセージにリアクション"
        content = "@everyone 募集文"
        edited = mg.make_reaction_update_message(True, content, [], [], [])
        self.assertEqual(edited, None)

    def test_reaction(self):
        "リアクションに反応するケース"
        content = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(1人)
<@1234>
"""
        edited = mg.make_reaction_update_message(
            False, content, ["<@1234>", "<@5678>"], [], [])
        expected = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(2人)
<@1234>
<@5678>
"""
        self.assertEqual(edited, expected)

    def test_delete(self):
        "削除機能をテストする"
        content = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(1人)
<@1234>
"""
        # 起案者と同じ人が🔑と🗑リアクションを付けた
        edited = mg.make_reaction_update_message(
            False, content, ["<@1234>"], ["<@999>"], ["<@999>"])
        self.assertEqual(edited, "")

    def test_other_can_not_delete(self):
        "起案者では無い人は削除出来ない"
        content = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(1人)
<@1234>
"""
        # 起案者と同じ人が🔑と🗑リアクションを付けた
        edited = mg.make_reaction_update_message(
            False, content, ["<@1234>"], ["<@888>"], ["<@888>"])
        # 編集後も変化無し
        self.assertEqual(edited, content)

    def test_sep(self):
        "SEPモードの確認"
        content = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(1人)
<@1>
<@2>
<@3>
<@4>
"""
        edited = mg.make_reaction_update_message(
            False, content, ["<@1>", "<@2>", "<@3>", "<@4>", "<@5>"],
            [], [],
            sep_flag=True)
        expected = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(5人)
<@1>
<@2>
<@3>
<@4>
<@5>

対戦表
1戦目 🔴 <@2> <@3> 🟢 <@4> <@5> 📹 <@1>
2戦目 🔴 <@1> <@4> 🟢 <@3> <@5> 📹 <@2>
3戦目 🔴 <@1> <@5> 🟢 <@2> <@4> 📹 <@3>
4戦目 🔴 <@1> <@3> 🟢 <@2> <@5> 📹 <@4>
5戦目 🔴 <@1> <@2> 🟢 <@3> <@4> 📹 <@5>
"""
        self.assertEqual(edited, expected)

    def test_sep_disabled(self):
        "SEPモード無効化ケース"
        content = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(1人)
<@1>
<@2>
<@3>
<@4>
"""
        edited = mg.make_reaction_update_message(
            False, content, ["<@1>", "<@2>", "<@3>", "<@4>", "<@5>"], [], [],
            sep_flag=False)
        expected = """@everyone 募集文
参加したい人は👍リアクションを付けてください。
起案者 <@999> は🔑と🗑リアクションで削除出来ます。

現在参加希望者(5人)
<@1>
<@2>
<@3>
<@4>
<@5>
"""
        self.assertEqual(edited, expected)

    def test_get_owner_mention(self):
        "起案者が誰かを得る"
        owner_mention = mg.get_owner_mention("起案者 <@999> は🔑と🗑リアクションで削除出来ます。")
        self.assertEqual(owner_mention, "<@999>")


if __name__ == '__main__':
    unittest.main()
