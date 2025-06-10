
# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types

client = genai.Client(api_key="AIzaSyBA2Rc3Lns11CuGC6cflzhSn54CQbek5jo")

def userMsg(message):
    inputted_msg = str(input(""))
    return inputted_msg

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a chatbot in a To-Do application, similar to Apple reminders, and you are there to answer any questions the user has. This can be about the application, or just general questions"),
    contents=[userMsg()]
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        temperature=0
    )
)
print(response.text)