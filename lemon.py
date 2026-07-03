import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)

try:
    with open("system_prompt.txt", "r", encoding="utf-8") as file:
        SYSTEM_PROMPT= file.read().strip()
except FileNotFoundError:
    SYSTEM_PROMPT= "You are a helpful assistant."

def tts(text, voice_path=None):

    if voice_path is None:
        resp = requests.post(
            "https://api.boson.ai/v1/audio/speech",
            headers={"Authorization": f"Bearer {os.environ['BOSON_API_KEY']}"},
            json={
                "model": "higgs-tts-3",
                "input": text,
            },
        )
    else:
        with open(voice_path, "rb") as ref_audio:
            resp = requests.post(
                "https://api.boson.ai/v1/audio/speech",
                headers={"Authorization": f"Bearer {os.environ['BOSON_API_KEY']}"},
                data={
                    "model": "higgs-tts-3",
                    "input": text,
                    #"ref_text": "Transcript of the reference clip.",
                },
                files={"ref_audio": ref_audio},
            )

    resp.raise_for_status()
    with open("out.mp3", "wb") as f:
        f.write(resp.content)

def gemini(text):
    client = genai.Client()

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT
    )

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=text,
        config=config
    )

    return response.text

def talk(text_in):
    ai_response = gemini(text_in)
    tts(ai_response, voice_path="simple_rick.wav")

    return ai_response

talk("What are you made of?")