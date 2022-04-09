"SEP専用機能"


def make_matching(user_mentions):
    """
    5人のときの2vs2マッチング表文字列を返却する。
    user_mentionsがその5人のメンション一覧。
    """
    m = [
        [2, 3, 4, 5, 1],
        [1, 4, 3, 5, 2],
        [1, 5, 2, 4, 3],
        [1, 3, 2, 5, 4],
        [1, 2, 3, 4, 5],
    ]
    us = [None] + user_mentions
    text = "\n対戦表\n"
    for i in range(0, 5):
        text += "%d戦目 🔴 %s %s 🟢 %s %s 📹 %s\n" % (
            i + 1,
            us[m[i][0]],
            us[m[i][1]],
            us[m[i][2]],
            us[m[i][3]],
            us[m[i][4]],
        )
    return text
