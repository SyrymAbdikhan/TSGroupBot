
# TS Group Bot

![python](https://img.shields.io/badge/python-v3.11.2-blue.svg?logo=python&logoColor=yellow) ![telethon](https://img.shields.io/badge/telethon-v1.24.0-blue.svg?logo=telegram) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

This bot was specially designed for TS (Telecommunication Systems) group chat in Telegram. The idea of the bot is to get the information from a university's LMS (Learning Management System), process it and present to the user in readable and interactive way.

## Features

- Tag everyone in the group
- Get deadlines from moodle in mini app
- Create and Manage queues

## Commands

- `/start`: Greet the user
- `/call`: Tag all members of the group
- `/deadlines`: Shows the deadlines in mini app
- `/newq`: Creates new queue
- `/settoken`: Sets moodle token to handle deadlines
- `/help`: Sends bot usage information

## Requirements

- Python v3.12.7
- Telethon v1.24.0
- asyncpg v0.27.0
- SQLAlchemy v2.0.4

## Installation

1. Clone this repository

    ```
    $ git clone https://github.com/SyrymAbdikhan/TSGroupBot.git
    $ cd TSGroupBot
    ```

2. Rename the file `.env.dist` to `.env` and replace the placeholders with required data.

- Create a new bot on Telegram by talking to the [BotFather](https://t.me/BotFather), and obtain the `BOT_TOKEN`.

- Go to the [Telegram Core](https://my.telegram.org/), and login to obtain the `API_HASH` and the `API_ID`.

3. Create a virtual environment and install required dependencies.

    ```
    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

4. Run the bot using `python -m bot`

- To run the bot with Docker `sudo docker compose up -d --build`

## Note

- Bot requires external database to connect to, and uses `web` docker network.
- Bot requires link to the website for mini app to show deadlines. Repo can be found [here](https://github.com/SyrymAbdikhan/TSGroup_MiniApp).
