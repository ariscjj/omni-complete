import os
from dotenv import load_dotenv
from groq import Groq

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


# Construct the path to the .env file located in the parent directory
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Load environment variables from the .env file
load_dotenv(dotenv_path)
# Load environment variables from .env file
load_dotenv(dotenv_path)

# Print the contents of the .env file for verification
with open(dotenv_path, 'r') as f:
    print("ENV file contents:")
    print(f.read())
load_dotenv()


# Print all environment variables to check if GROQ_API_KEY is loaded
print("All environment variables after loading .env:")
print(dict(os.environ))  # Convert to dict for better readability

# Access the specific environment variable
api_key = os.getenv("GROQ_API_KEY")
print(f"Loaded API Key: {api_key}")
with open('.env', 'r') as f:
    print("ENV file")
    print(os.environ.get("GROQ_API_KEY"))
    print(f.read())

# print("environment", os.environ)
api_key = os.environ.get("GROQ_API_KEY") 
print("API1", api_key)

client = Groq( api_key=os.environ.get("GROQ_API_KEY"), max_retries=2)

# from config import Config 
def prompt_json(prompt: str):
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
        model="gpt-4o",
        # model="llama3-8b-8192",
        response_format={
            "type": "json_object",
        },
    )
    return chat_completion.choices[0].message.content

GROQ_API_KEY = "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"
