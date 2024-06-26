import os
from dotenv import load_dotenv
from groq import Groq
import time
# Construct the path to the .env file located in the parent directory
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Load environment variables from .env file
load_dotenv(dotenv_path)
client = Groq( api_key=os.environ.get("GROQ_API_KEY"), max_retries=2)

# from config import Config 
def prompt_flag(prompt: str):
    # for openAI 
    # config = Config(prompt=prompt) 
    # return config  

    # for Groq 
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        stream=False,
        # model="gpt-4o",
        model="llama3-8b-8192",
        response_format={
            "type": "json_object",
        },
    )

    return chat_completion.choices[0].message.content

