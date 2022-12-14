# ChaosBot
A discord bot that acts as a character and sends a message from ChatGPT's 'API' randomly.

## Setup

Run `install.sh` or the following commands:

```bash
# Create new environment (optional)
python3 -m venv chaosbot
source chaosbot/bin/activate

# Install dependencies
pip3 install --upgrade discord
pip3 install --upgrade python-dotnet
pip3 install --upgrade revChatGPT
python3 -m playwright install
```

Create an .env file with the following keys:

```
TOKEN=<discord_token>
CHATGPT_TOKEN=[optional chatgpt session token]
MALE=<true/false>
DISPLAY_NAME=[optional display name override, uses bot display name as default]
DESCRIPTION[optional description about the character your bot is roleplaying as]
```

Run it
```bash
python3 main.py
```

This code is only tested on Arch Linux, and probably won't work after ChatGPT closes their open preview.
