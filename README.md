# 集まるBot

Discordで参加者を募集するBot。ワンクリックで募集案件への応募が可能。

<img src="https://user-images.githubusercontent.com/16898831/117563187-259a5900-b0df-11eb-99bf-875b90311afd.gif">

## 実行方法

### 環境変数の設定

| 環境変数 | 説明 |
| --- | --- |
| ATUMARU_BOT_ENV | prod: 本番モード。コマンド名は/atumaru。dev:テストモード。コマンド名は/atumaru_test |
| DISCORD_TOKEN | Discordのトークン |

### ローカル

```sh
poetry install
poetry run python main.py
```

### docker

```sh
docker-compose build
docker-compose run discord_atumaru_bot poetry run python main.py
```

## 使用技術


- Python
- [discord.py](https://discordpy.readthedocs.io/ja/latest/index.html)
- [Poetry](https://python-poetry.org/)
- [GitHub Actions](https://docs.github.com/ja/actions)
- Docker
- [Google Compute Engine](https://cloud.google.com/compute/?hl=ja)
- [Google Artifact Registory](https://cloud.google.com/artifact-registry?hl=ja)

## デプロイについて

[Google Cloud Platform](https://cloud.google.com/free/?hl=ja)の無料枠で100人規模のサーバでの動作を確認しています。

## 謝辞

[SEP](https://hageyuto.com/2679-2/)の代表および皆様に導入と動作確認へのご協力を頂きました。ありがとうございます。

