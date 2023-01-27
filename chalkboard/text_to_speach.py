"""Chat GPT"""

import pyttsx3

engine = pyttsx3.init()

# Set the rate at which the text is spoken
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-20)

# Set the volume of the speech
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+0.5)

# Set the voice to be used
voices = engine.getProperty('voices')

# selected = [
#     "diego",
#     "tessa",
#     "Victoria",
# ]

selected = [
    # "alice",
    # "alva",
    # "amelie",
    # "anna",
    # "carmit",
    # "damayanti",
    # "daniel",
    # "diego",
    # "ellen",
    # "fiona",
    # "Fred",
    # "ioana",
    # "joana",
    # "jorge",
    # "juan",
    # "kanya",
    # "karen",
    # "kyoko",
    # "laura",
    # "lekha",
    # "luca",
    # "luciana",
    # "maged",
    # "mariska",
    # "meijia",
    # "melina",
    # "milena",
    # "moira",
    # "monica",
    # "nora",
    # "paulina",
    # "rishi",
    # "samantha",
    # "sara",
    # "satu",
    # "sinji",
    # "tessa",
    # "thomas",
    # "tingting",
    # "veena",
    "Victoria",
    # "xander",
    # "yelda",
    # "yuna",
    # "yuri",
    # "zosia",
    # "zuzana",
 ]

text = """
It was a dark and stormy night. The wind was howling and the rain was pounding against the windows. Sarah huddled under her blankets, trying to block out the noise. She had always been afraid of storms, and this one seemed particularly intense.
As she lay there, she heard a faint tapping at her window. At first, she thought it was just the rain, but the sound persisted. She slowly sat up and peered through the window, but she couldn't see anything in the darkness.
The tapping continued, and Sarah couldn't shake the feeling that someone - or something - was out there, trying to get in. She pulled the blankets up to her chin and closed her eyes, praying that the storm would pass quickly.
But the tapping only grew louder, and Sarah knew she couldn't ignore it any longer. She gathered all of her courage and slowly made her way to the window. As she pulled back the curtains, a pair of glowing eyes stared back at her from the darkness. Sarah let out a blood-curdling scream as the creature lunged towards her.
I hope that wasn't too creepy for you! If you have any other requests, let me know.
"""

for voice in voices:
    name = voice.id.split('.')[-1]
    if name not in selected:
        continue

    print(name)
    engine.setProperty('voice', voice.id)

    # Speak the text
    # engine.say(f"Hello")
    engine.say(text)
    # Start the speech

engine.runAndWait()

