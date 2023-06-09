from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()

# Retrieve the values from the environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_CHANNEL_ID = #Discord channel ID where you want the bot to interact 
GPT_INSTRUCTIONS = "Based on the following text, generate a simple prompt description for image generation that represents the concept of the text. The response should be at least 10 and no more than 30 words and not include punctuation, any names or proper nouns, and should not include any language related to generating an image, only describe the scene. Prioritize for creativity and abstraction, describing the emotion of the text over the literal scene. Do not describe a human or individual, describe a scene. Prioritize outdoors and city street scenes. Do not specify Visual element, incorporate it into the output. begin each output with \"!generate\". NEVER use “.” Or “,” or \":\" in your response."
                    #You can get very creative with the instructions here  





