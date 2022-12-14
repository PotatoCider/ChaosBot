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

opts = {}

chatgpt_token = os.environ.get('CHATGPT_TOKEN')

if chatgpt_token is not None and chatgpt_token != '':
    opts['session_token'] = chatgpt_token

chatbot = Chatbot(opts)

@client.event
async def on_ready():
    print(f'ChaosBot is ready!')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if message.channel.type not in (discord.ChannelType.text, discord.ChannelType.public_thread, discord.ChannelType.private):
        return

    n = random.randrange(100)
    if n != 42:
        print('miss:', n)
        return

    await message.channel.typing()

    history = message.channel.history(limit=10)

    prompt = ''

    async for msg in history:
        prompt = (
            msg.author.display_name + ': {start}' + 
            msg.clean_content + '{end}\n' + 
            prompt
        )

    prompt = (
        'The person ChaosBot in this conversation should only respond once, start its message with {start} and end with {end}. ' +
        'The following is a conversation in Discord chatroom.\n\n' +
        prompt +
        'ChaosBot: '
    )

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