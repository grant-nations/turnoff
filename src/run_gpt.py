import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# TODO: 
# check the length of the prompt and the response to make sure it's not too long
