#!/bin/bash
python3 -m venv chaosbot
source chaosbot/bin/activate


pip3 install --upgrade discord
pip3 install --upgrade python-dotnet
pip3 install --upgrade revChatGPT
python3 -m playwright install