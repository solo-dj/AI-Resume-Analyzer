import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful personal assistant."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"Error: {str(e)}"
