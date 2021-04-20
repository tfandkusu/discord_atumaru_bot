# discord_atumaru_bot
Discordで特定の人数を募集するBot

## 実行方法

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

## デプロイ方法

Artifact Registryに保存

```sh
docker-compose build
docker tag discord_atumaru_bot_discord_atumaru_bot:latest us-central1-docker.pkg.dev/discord-atumaru-bot/discord-atumaru-bot/image:latest
docker push us-central1-docker.pkg.dev/discord-atumaru-bot/discord-atumaru-bot/image:latest
```

## アップデート方法

まだ試していないが、こちらの方法でできそう。

https://cloud.google.com/sdk/gcloud/reference/compute/instances/update-container?hl=ja
