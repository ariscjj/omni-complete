import os
from dotenv import load_dotenv
load_dotenv()
# from groq import Groq

# client = Groq(
    # This is the default and can be omitted
    # api_key=os.environ.get("GROQ_API_KEY"),
    # max_retries=2,
# )

from config import Config 

def prompt_json(prompt: str):
    config = Config(prompt=prompt) 
    return config  
    # chat_completion = client.chat.completions.create(
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt,
    #         }
    #     ],
    #     stream=False,
    #     model="gpt-4o",
    #     # model="llama3-8b-8192",
    #     response_format={
    #         "type": "json_object",
    #     },
    # )
    # return chat_completion.choices[0].message.content
