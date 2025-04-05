from elevenlabs.client import ElevenLabs
from elevenlabs import play

client = ElevenLabs(
  api_key= 'sk_de508afc864e3c4d78fd799a0624ce253c7f60701e595e0b', 
)
voice = "Charlie"
request = "Hi this is me"
audio = client.generate(
    text=request,
    voice=voice,
    model="eleven_monolingual_v1"
)
play(audio)

