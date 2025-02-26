from google import genai
from dotenv import load_dotenv  
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save
import requests
import base64
load_dotenv()   

class Router:
    def __init__(self):
        self.audio_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.cloudflare_account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.cloudflare_api_key = os.getenv("CLOUDFLARE_API_KEY")

    def generate_dialogue(self, prompt: str):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt)
            return response.text
        except Exception as e:
            return f"generate_dialogue(): {e}"
    
    def generate_image(self, prompt: str, filename: str):
        url = f"https://api.cloudflare.com/client/v4/accounts/{self.cloudflare_account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        
        headers = {"Authorization": f"Bearer {self.cloudflare_api_key}"}
        payload = {"prompt": prompt}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            imgdata = base64.b64decode(response.json().get("result").get("image"))
            with open(filename, 'wb') as f:
                f.write(imgdata)
            return filename
        except Exception as e:
            return f"generate_image(): {e}"

    def generate_audio(self, prompt: str, filename: str):
        
        audio = self.audio_client.text_to_speech.convert(
                text=prompt,
                voice_id="JBFqnCBsd6RMkjVDRZzb", 
                model_id="eleven_flash_v2",
                output_format="mp3_44100_128",
        )
        """audio_bytes = b''.join(list(audio))
            audio_segment = AudioSegment.from_file(BytesIO(audio_bytes), format="mp3")
            audio_segment.export(filename, format="mp3")"""
        # this got resolved from some github issue discussion
        save(audio, filename)
        return filename
        


