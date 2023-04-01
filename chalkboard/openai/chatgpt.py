
import openai

from pathlib import Path

openai.api_key = Path("./api_key").read_text()

# model = "chatbot"
model = "text-davinci-003"

prompt = "give me a detailed story of a boy in a forest that discovers a sentient machine"
completion = openai.Completion.create(engine=model, prompt=prompt, max_tokens=2048, n=1, stop=None, temperature=0.7)
message = completion.choices[0].text
print(message)
