# AOE_Shirts-telegrambot

A stateful Telegram bot to interact with the [AOE_Shirts-api](https://github.com/VincentSchmid/AOE_Shirts-api).
Currently, only supports the full_pipeline request.

## Setting up a bot
Talk to the [Botfather](https://telegram.me/BotFather) first to create your bot.  
There is a command list and a bot description can be specified there as well.

## Installation
Use the provided Makefile to deploy locally or on gcloud. 
To use the `Makefile` a file called `params.mk` is required containing make variables. The file content should look like this:  

```Makefile
export SHIRT_POROCESSING_ADDRESS := <url_to_AOE_Shirts-api>
export TELEGRAM_TOKEN := <bot-token>
export GCLOUD_PROJECT_ID := <project-id>
export CONTAINER_NAME := <container-name>
export LOCAL_PORT := <local-port>
export CONFIG_FILE := config.yaml
export USERNAME := <dockerhub-username>
``` 
The make command will build the container image:  

```bash
make
``` 
Alternatively, you can use:
```bash
docker build -t shirt_bot .
```

The Makefile contains an automated deployment to Gcloud using Cloud Run. This will also link the Telegram bot, to the deployed instance:
```bash
make deploy-gcloud
```

To manually link a bot to a deployed service, use this command:
```bash
curl "https://api.telegram.org/bot${TELEGRAM_TOKEN}/setWebhook?url=${SERVICE_URL}"
```

Run the tests:
```bash
make test
```

## Usage
Once linked send `/start` to the Telegram bot.

## License
[MIT](https://choosealicense.com/licenses/mit/)