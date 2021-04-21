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

※ discord-atumaru-bot文字列は固有の環境のものなので適時置き換えてください。

```sh
docker-compose build
docker tag discord_atumaru_bot_discord_atumaru_bot:latest us-central1-docker.pkg.dev/discord-atumaru-bot/discord-atumaru-bot/image:latest
docker push us-central1-docker.pkg.dev/discord-atumaru-bot/discord-atumaru-bot/image:latest
```

Compute Engineのコンテナを更新してインスタンスを再起動。

```sh
 gcloud compute instances update-container discord-atumaru-bot --container-image=us-central1-docker.pkg.dev/discord-atumaru-bot/discord-atumaru-bot/image:latest
 ```
