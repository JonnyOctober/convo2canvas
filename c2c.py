import discord
from discord.ext import commands
import aiohttp
import base64
from io import BytesIO
import openai
from config import DISCORD_TOKEN, OPENAI_API_KEY,TARGET_CHANNEL_ID,GPT_INSTRUCTIONS

# Create a new bot instance with intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

TARGET_CHANNEL_ID = TARGET_CHANNEL_ID # Replace this with the channel ID of the channel you want to monitor
TOKEN = DISCORD_TOKEN # Replace this with your Discord token
openai.api_key = OPENAI_API_KEY # Replace this with your OpenAI API key

async def generate_image(prompt, steps=None):
    if steps is None:
        steps = 40

    url = "http://localhost:7860/sdapi/v1/txt2img"  # Update this with your local API endpoint
    payload = {#You can change the width and height of the image here, or modify other parameters of the image generation. 
        "prompt": prompt, 
        "steps": steps,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
    } #there are many more parameters that you can utilize via Automatic1111

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                response_json = await response.json()
                print(f"Response JSON: {response_json}")
                image_data = response_json['images'][-1]
                image_data = image_data.split("base64,")[-1]
                image_bytes = base64.b64decode(image_data)
                return image_bytes
            else:
                print(f"Error: {response.status} - {await response.text()}")
                return None

async def generate_gpt_response(prompt):
    model_engine = "gpt-3.5-turbo"
    chat_messages = [                   #You can change the parameters of the prompt here.
        {"role": "system", "content": GPT_INSTRUCTIONS},
        {"role": "user", "content": prompt}
    ]

    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=chat_messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )

    message = response['choices'][0]['message']['content']
    return message.strip()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"Message received in channel {message.channel.id}: {message.content}")

    if message.channel.id == TARGET_CHANNEL_ID:
        # author_id = message.author.id

        gpt_response = await generate_gpt_response(message.content)
        image_bytes = await generate_image(gpt_response)
        if image_bytes:
            
            # Place the payload code here to modify the image if needed

            # Send the generated image
            generated_image = discord.File(BytesIO(image_bytes), filename="generated_image.png")
            await message.reply(file=generated_image)

client.run(TOKEN)
