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

    def test_failed(self):
        "わざと失敗するテスト入れる"
        self.assertFalse(true)


if __name__ == '__main__':
    unittest.main()
