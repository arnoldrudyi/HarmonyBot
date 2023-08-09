# Harmony Bot

> **Disclaimer**: downloading copyright songs may be illegal in your country. This bot is created as a hobby project and is not used by the creator on any basis. If you intend to use this code for any purposes, you assume all legal responsibility.

The bot helps you download music from streaming services like **Spotify, Soundcloud, YouTube, and YouTube Music**. All you need to do is send a link to the track on any of the above services. You can also send a search request and the bot will give you search results from YouTube.

The bot uses the **[song.link](https://song.link/)** service to retrieve the YouTube track link if the original link is from a different music service. Additionally, the bot uses the **[pytube module](https://github.com/pytube/pytube/tree/master)** to download the audio from YouTube.

The bot is multilingual, currently it supports two languages: **Ukrainian and English**. You can modify the messages in the `messages.json` file.
### Sneak Peek

|                   Demo #1                    |                   Demo #2                    |
|:--------------------------------------------:|:--------------------------------------------:|
| ![image](https://i.ibb.co/yS6cyJg/image.png) | ![image](https://i.ibb.co/RQL0x7t/image.png) |

### Getting Started
Before you can run the bot, ensure that you have the following prerequisites installed on your system:

1. **Python and pip**: If you don't have Python and pip installed, you can download and install them from the official Python website: **[Python Downloads](https://www.python.org/downloads/)**.

2. **Docker**: Make sure you have Docker installed. You can download and install Docker from the official Docker website: **[Docker Installation](https://docs.docker.com/get-docker/)**.

To get started, copy the repository and follow these steps to configure your `.env` file:

1. **Token Configuration**: Obtain your unique token by following these steps:
   - Visit **[Telegram's BotFather](https://t.me/BotFather)** to create your bot (you can read more about tokens and bots in general **[here](https://core.telegram.org/bots)**).
   - Copy the generated token and replace `TOKEN=YOUR_TOKEN_HERE` with your actual token.

2. **Database Configuration**: Configure your PostgreSQL database settings:
   - Set `POSTGRES_USER` to your PostgreSQL username.
   - Set `POSTGRES_PASSWORD` to your PostgreSQL password.
   - Set `POSTGRES_DB` to the desired name for your database.

Your `.env` file should look like this:

```plaintext
TOKEN=5904225100:AAE85tP1MbUY-KeJ3qZvPyjPPYvFROEqMDI
POSTGRES_USER=admin
POSTGRES_PASSWORD=HHDofCI*192c
POSTGRES_DB=database
```
After configuring your `.env` file, execute these commands to launch the bot:

``` bash
pip install -r requirements.txt
set -a && source .env && set +a
docker-compose up
alembic upgrade head
python3 app.py
```

Now you're all set to download the audio files. But remember about **copyright**, appreciate other people's work. Please support the artists by buying their music.
