import discord
import os
import random
import re
import dotenv
from revChatGPT.revChatGPT import Chatbot

dotenv.load_dotenv()



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

MALE = os.environ['MALE'].lower() == 'true'
display_name = os.environ.get('DISPLAY_NAME')

opts = {}

chatgpt_token = os.environ.get('CHATGPT_TOKEN')
chance_of_response = float(os.environ.get('CHANCE')) or 0.05

if chatgpt_token is not None and chatgpt_token != '':
    opts['session_token'] = chatgpt_token

chatbot = Chatbot(opts)

@client.event
async def on_ready():
    global display_name
    if display_name is None:
        display_name = client.user.display_name
    print(f'ChaosBot is ready to act as {display_name}!')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.channel.type not in (discord.ChannelType.text, discord.ChannelType.public_thread, discord.ChannelType.private):
        return

    n = random.random()
    if n < chance_of_response:
        print('miss:', n)
        return

    async with message.channel.typing():
        history = message.channel.history(limit=10)

        prompt = ''

        async for msg in history:
            name = display_name if msg.author == client.user else msg.author.display_name

            prompt = (
                name + ': {start}' + 
                msg.clean_content + '{end}\n' + 
                prompt
            )

        prompt = (
            f"{os.environ.get('DESCRIPTION') or ''} " +
 
            f"The following paragraph is a conversation between other people in an online chat room and {display_name} is about to suddenly interrupt them." +
            f"Because {display_name} is in a online chat room, {'he' if MALE else 'she'} should be responding to them informally. " +
            f"Start {'his' if MALE else 'her'} message with " +
            '{start} and end with {end}.\n\n' +
            prompt +
            display_name + ': '
        )

        print(prompt)

        response = chatbot.get_chat_response(prompt, output="text")
        
        if not response['message']:
            print('no message:', response)
            return
        
        m = re.search('{start}([\s\S]*){end}', response['message'])

        if not m:
            print('didnt detect message:', response)
            return

    await msg.channel.send(m.groups()[0])


client.run(os.environ['TOKEN'])