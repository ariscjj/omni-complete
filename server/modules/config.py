from openai import AsyncAzureOpenAI, AsyncOpenAI, AzureOpenAI
from typing import List
from src.core.exceptions import ConfigError
import openai
import backoff
import os
import dotenv
import json
import logging

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

class Config:
    """
    Configuration class for managing various API keys and clients.
    """


    ACTION_AGENT_AZURE_API_KEY = os.environ.get("ACTION_AGENT_AZURE_API_KEY")
    AZURE_3_5_KEY = os.environ.get("AZURE_3_5_KEY")
    ORGANIZATION_OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
    client_gpt4 = AsyncAzureOpenAI(
            api_key=ACTION_AGENT_AZURE_API_KEY,
            api_version="2023-10-01-preview",
            azure_endpoint = "https://action-agents.openai.azure.com/"
    )
    client_gpt3 = AsyncAzureOpenAI(
            api_key=AZURE_3_5_KEY,
            api_version="2023-10-01-preview",
            azure_endpoint="https://action-agents2.openai.azure.com/"
            )
    client_gpt4o = AsyncOpenAI(
        api_key=ORGANIZATION_OPENAI_KEY
    )
    client_model_3 = "agent-api-35-2"
    client_model_4 = "agent-api" #test
    client_model_gpt4o = "gpt-4o"

    
    @backoff.on_exception(backoff.expo, openai.RateLimitError)
    async def generate_response(self, prompt: str, json_output: bool, key: str | List[str], model="gpt-4"):
        """
        Generates a response using the Azure OpenAI client based on a given prompt.

        Args:
            prompt (str): The input prompt to generate a response for.
            json_output (bool): Flag to determine if output should be in JSON format.
            key (str): Key to extract specific data from the JSON response, if applicable.

        Returns:
            str: The generated response. If json_output is True, returns the specific data extracted using the provided key from the JSON response.
        """
        try:
            if model == 'gpt-4':
                client = self.client_gpt4
                model = self.client_model_4
            elif model == "gpt-4o":
                client = self.client_gpt4o
                model = self.client_model_gpt4o
            else:
                client = self.client_gpt3
                model = self.client_model_3
                
            response = await client.chat.completions.create(
                    model=model,
                    stream=False,
                    response_format={"type": "json_object"} if json_output else None,
                    messages=[{"role": "system", "content": prompt}],
                )
            output = response.choices[0].message.content
            print("\n\n****output:", output)
            if json_output:
                output_dic = json.loads(output)
                if isinstance(key, str):
                    output = output_dic.copy()[key]
                elif isinstance(key, list):
                    output = output_dic
            return output
        except Exception as e:
            logger.error("FAILED TO GENERATE RESPONSE FROM OPENAI", e)
            raise ConfigError(str(e))
