import unittest
import message_generator as mg


class TestMessageGenerator(unittest.TestCase):
    def test_recruiting_prod(self):
        "本番モードで募集"
        content, reaction = mg.make_command_message(False, '/atumaru 募集します')
        self.assertEqual(content,
                         "募集します\n参加したい人は👍リアクションを付けてください。")
        self.assertTrue(reaction)

    def test_help_prod(self):
        "本番モードでヘルプ"
        content, reaction = mg.make_command_message(False, '/atumaru')
        self.assertEqual(content, mg.HELP_MESSAGE)
        self.assertFalse(reaction)

    def test_recruiting_dev(self):
        "テストモードで募集"
        content, reaction = mg.make_command_message(
            True, '/atumaru_test 募集します')
        self.assertEqual(content,
                         "【テスト】募集します\n参加したい人は👍リアクションを付けてください。")
        self.assertTrue(reaction)

    def test_help_dev(self):
        "テストモードでヘルプ"
        content, reaction = mg.make_command_message(True, '/atumaru_test')
        self.assertEqual(content, mg.HELP_MESSAGE)
        self.assertFalse(reaction)

    def test_not_command(self):
        "コマンドでないケース"
        content, reaction = mg.make_command_message(True, '/not_command')
        self.assertEqual(content, None)
        self.assertFalse(reaction)

    def test_reaction_to_help(self):
        "ヘルプへのリアクションケース"
        content = "使い方\n```"
        edited = mg.make_reaction_update_message(False, content, [])
        self.assertEqual(edited, None)

    def test_reaction_to_dev_in_prod(self):
        "本番モードで【テスト】とついているメッセージにリアクション"
        content = "【テスト】募集文"
        edited = mg.make_reaction_update_message(False, content, [])
        self.assertEqual(edited, None)

    def test_reaction_to_prod_in_dev(self):
        "テストモードで【テスト】とついていないメッセージにリアクション"
        content = "募集文"
        edited = mg.make_reaction_update_message(True, content, [])
        self.assertEqual(edited, None)

    def test_reaction(self):
        "リアクションに反応するケース"
        content = "募集文\n参加したい人は👍リアクションを付けてください。"
        edited = mg.make_reaction_update_message(
            False, content, ["<@1234>", "<@5678>"])
        expected = """募集文
参加したい人は👍リアクションを付けてください。

現在参加希望者(2人)
<@1234>
<@5678>
"""
        self.assertEqual(edited, expected)

    def test_sep(self):
        "SEPモードの確認"
        content = "募集文\n参加したい人は👍リアクションを付けてください。"
        edited = mg.make_reaction_update_message(
            False, content, ["<@1>", "<@2>", "<@3>", "<@4>", "<@5>"],
            sep_flag=True)
        expected = """募集文
参加したい人は👍リアクションを付けてください。

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
        content = "募集文\n参加したい人は👍リアクションを付けてください。"
        edited = mg.make_reaction_update_message(
            False, content, ["<@1>", "<@2>", "<@3>", "<@4>", "<@5>"],
            sep_flag=False)
        expected = """募集文
参加したい人は👍リアクションを付けてください。

現在参加希望者(5人)
<@1>
<@2>
<@3>
<@4>
<@5>
"""
        self.assertEqual(edited, expected)


if __name__ == '__main__':
    unittest.main()
