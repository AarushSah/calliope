import anthropic
import json
from termcolor import colored
import re
import datetime as dt

def output(text):
    print(text)

def get_output_text(text):
    if "<output>" in text and "</output>" in text:
        return text.split("<output>")[1].split("</output>")[0]
    else:
        return text

def structure_outline(client, messages):
    response = message(client, messages, "Please structure the rough outline into different acts, with a clear beginning, middle, and end. Provide the structured outline within <output> tags. Make sure it has all of the information and context, and is very detailed and well-organized. Think of it as a detailed table of contents for the story.")
    return get_output_text(response)

def develop_characters(client, messages, structured_outline):
    response = message(client, messages, f"Using the structured outline below, please list all the characters mentioned in the story. Provide a brief description of each character within <output> tags. Within the output tags, each character should be wrapped in <character> tags with their name and a brief description.\n\n{structured_outline}")
    return get_output_text(response)

def describe_character_actions(client, messages, character_info):
    response = message(client, messages, f"<function_calls> <invoke> <tool_name>describe_character_actions</tool_name> <parameters> <character_info>{character_info}</character_info> </parameters> </invoke> </function_calls>", stop_sequence="</function_calls>")
    return get_output_text(response)

def develop_ending(client, messages, structured_outline, character_info, character_actions):
    response = message(client, messages, f"Using the structured outline, character information, and character actions:\n\n{structured_outline}\n\n{character_info}\n\n{character_actions}\n\nPlease develop a satisfying and cohesive ending for the story. Provide the ending within <output> tags.")
    return get_output_text(response)

def generate_character_cards(client, messages, structured_outline, character_info):
    response = message(client, messages, f"Using the final story outline and character information:\n\n{structured_outline}\n\n{character_info}\n\nPlease create detailed character cards for each character mentioned in the story. Include their name, age, occupation, appearance, personality traits, motivations, and any other relevant details. Provide the character cards within <output> tags.")
    return get_output_text(response)

def generate_chapters_and_scenes(client, messages, structured_outline):
    response = message(client, messages, f"Now, you will fully outline the book. Use the function calling tool to generate a detailed outline, with at LEAST 20 chapters. Make sure it's coherent and thematically correct, and reads well. <function_calls> <invoke> <tool_name>generate_chapters_and_scenes</tool_name> <parameters> <structured_outline>{structured_outline}</structured_outline> </parameters> </invoke> </function_calls>", stop_sequence="</function_calls>")
    return get_output_text(response)

def message(client, messages, prompt, system="You are a story development assistant. Your task is to help the user expand and develop their story outline, whether it is to create detailed character profiles, and provide a final comprehensive outline. Follow the user's instructions carefully and provide the requested information within <output> tags. Only do what the user asks for. Make sure to be extremely detailed and think step by step within <thinking> tags.", stop_sequence=None):
    messages.append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    )
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=4000,
        temperature=0,
        system=system,
        messages=messages,
        stop_sequences=[stop_sequence] if stop_sequence else None
    )
    messages.append(
        {
            "role": "assistant",
            "content": message.content[0].text
        }
    )
    return message.content[0].text

def expand_outline(api_key, rough_outline):
    client = anthropic.Anthropic(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Here is a rough outline for a story:\n\n{rough_outline}\n\nPlease help me expand and develop this outline."
                }
            ]
        },
        {
            "role": "assistant",
            "content": "Sure! I will do so in a detailed way that structures my output. I will think in a detailed way within <thinking> tags, and give my final response within <output> tags. Let's get started!"
        }
    ]
    structured_outline = structure_outline(client, messages)
    output(colored("Structured Outline:", "blue"))
    output(structured_outline)
    output("\n")
    character_info = develop_characters(client, messages, structured_outline)
    output(colored("Character Information:", "blue"))
    output(character_info)
    output("\n")
    character_actions = describe_character_actions(client, messages, character_info)
    output(colored("Character Actions:", "blue"))
    output(character_actions)
    output("\n")
    ending = develop_ending(client, messages, structured_outline, character_info, character_actions)
    output(colored("Ending:", "blue"))
    output(ending)
    output("\n")
    character_cards = generate_character_cards(client, messages, structured_outline, character_info)
    output(colored("Character Cards:", "blue"))
    output(character_cards)
    output("\n")
    chapters_and_scenes = generate_chapters_and_scenes(client, messages, structured_outline)
    output(colored("Chapters and Scenes:", "blue"))
    output(chapters_and_scenes)
    output("\n")
    final_outline = f"<final_outline>\n{structured_outline}\n</final_outline>"
    character_cards = f"<character_cards>\n{character_cards}\n</character_cards>"
    character_plotlines = f"<character_plotlines>\n{character_actions}\n</character_plotlines>"
    chapters_and_scenes = f"<chapters_and_scenes>\n{chapters_and_scenes}\n</chapters_and_scenes>"
    output(colored("Final Outline:", "green"))
    output(final_outline)
    output("\n")
    output(colored("Character Cards:", "green"))
    output(character_cards)
    output("\n")
    output(colored("Character Plotlines:", "green"))
    output(character_plotlines)
    output("\n")
    output(colored("Chapters and Scenes:", "green"))
    output(chapters_and_scenes)
    output("\n")
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"./dumps/depth_{timestamp}.json", "w") as file:
        json.dump(messages, file, indent=4)
    return {
        "final_outline": final_outline,
        "character_cards": character_cards,
        "character_plotlines": character_plotlines,
        "chapters_and_scenes": chapters_and_scenes,
        "messages": messages
    }

if __name__ == "__main__":
    api_key = "your_api_key"
    rough_outline = "<outline>\n\nPart 1: The Village\n- Introduce the peasant girl, her humble life, and hint at her dark \"gift\"\n- The new samurai recruit is sent to keep order in her rural village \n- Despite class differences, he is intrigued by the mysterious peasant girl\n- A tragic event occurs that forces the girl to reveal her ability to see deaths\n\nPart 2: The Outcast Samurai\n- The disillusioned samurai is cast out by his clan after an outburst of violence\n- Wandering to survive, he crosses paths with the peasant girl using her powers\n- Initially wants nothing to do with her, but is drawn into her world\n- Begrudgingly takes her under his wing to train her abilities \n\nPart 3: Forbidden Love\n- The peasant girl and samurai recruit's feelings deepen into a forbidden romance\n- This causes tensions with the recruit's samurai superiors and rivals\n- The outcast samurai tries to warn the girl of the dangers of defying class roles\n\nPart 4: Shogunate Betrayal  \n- The recruit is tasked with infiltrating a rival samurai faction \n- He and the peasant girl get caught in the middle of an escalating conflict\n- The shogunate's corruption and cruelty is fully revealed \n\nPart 5: Reckoning\n- The outcast samurai's training allows the peasant girl to master her abilities\n- She foresees a potential future that could prevent further bloodshed\n- At great personal cost, she and the samurai recruit take a stand against injustice\n\n</outline>"
    expanded_outline = expand_outline(api_key, rough_outline)
    # output("Expanded Outline:")
    # output(expanded_outline)