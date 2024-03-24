from outline_generator import generate_outline
from termcolor import colored
from depth_v2 import expand_outline

api_key = "your_api_key"
outline = generate_outline(api_key)
print("Generated Outline:")
print(outline)
print("\n")
print(colored("Outline Generation Completed!", "green"))

print(colored("Expanding Outline...", "blue"))

expanded_outline = expand_outline(api_key, outline)
final_outline = expanded_outline["final_outline"]
character_cards = expanded_outline["character_cards"]
character_plotlines = expanded_outline["character_plotlines"]
expansion_messages = expanded_outline["messages"]
chapters_and_scenes = expanded_outline["chapters_and_scenes"]

print(colored("Expanded Outline:", "green"))
print(final_outline)

print(colored("Character Cards:", "green"))
print(character_cards)

print(colored("Character Plotlines:", "green"))
print(character_plotlines)

print(colored("Expansion Messages:", "green"))
print(expansion_messages)

print(colored("Chapters and Scenes:", "green"))
print(chapters_and_scenes)

print(colored("Outline Expansion Completed!", "blue"))