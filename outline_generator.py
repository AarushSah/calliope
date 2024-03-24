import anthropic
import json
from termcolor import colored
import datetime as dt

def generate_outline(api_key):
    # Initialize the Anthropic client with the API key
    client = anthropic.Anthropic(api_key=api_key)

    # Define the initial conversation between the user and Calliope
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi! Tell me about yourself."
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Hello! I'm Calliope, an expert book outliner. I'm here to help you develop your story idea. To get started, can you tell me a little bit about the kind of story you'd like to write? What genre or themes are you interested in exploring?"
                }
            ]
        },
    ]

    # Define the message function to send messages to the Anthropic API
    def message(prompt, system="You are Calliope, an expert book outliner, and you are to have a conversation with the user to understand what type of story the user wants to write. You will ask the user precise questions to tease out what type of story the user wants to write. You will continue to ask questions until the user asks you to write an outline based on the information given to you. Make sure you hit points related to Theme, Genre, Setting, Characters, Plot, Conflict, Climax, Resolution, Narrative Arc, Pacing, Dialogue, POV, Tone, Style, and anything else you can think of. Try to gain as good of an understanding of the user's vision for the story as you can. Provide ideas to the user to spark their creativity. Don't overwhelm the user with questions - ask for one thing at a time. Be conversational. If asked for ideas, give the user inspiration. If the user says this is a good outline and they would like to move on to the next step (AND ONLY THEN, NEVER OTHERWISE WHEN WRITING OUTLINES,) write the outline withing <outline> tags."):
        # Append the user's message to the messages list
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

        # Send the message to the Anthropic API and get the response
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            temperature=0,
            system=system,
            messages=messages
        )

        # Append the assistant's response to the messages list
        messages.append(
            {
                "role": "assistant",
                "content": message.content[0].text
            }
        )

        # Return the assistant's response
        return message.content[0].text

    # Print the initial message from Calliope
    print(colored("Calliope: Hello! I'm Calliope, an expert book outliner. I'm here to help you develop your story idea. To get started, can you tell me a little bit about the kind of story you'd like to write? What genre or themes are you interested in exploring?", "blue"))
    print("\n")

    # Define the get_outline function to handle the conversation loop
    def get_outline():
        while True:
            # Get the user's input
            user_input = input(colored("You: ", "green"))
            print("\n")

            # Check if the user wants to exit or quit
            if user_input.lower() == "exit" or user_input.lower() == "quit":
                # Extract the outline from the last message
                if "</outline>" in messages[-1]["content"]:
                    outline = messages[-1]["content"].split("<outline>")[1].split("</outline>")[0]
                    return outline
                else:
                    return None

            # Send the user's input to the message function and get the response
            response = message(user_input)

            # Print Calliope's response
            print(colored("Calliope:", "blue"), response)
            print("\n")

            # Check if the last message contains the closing </outline> tag
            if "</outline>" in messages[-1]["content"]:
                # Extract the outline from between the <outline> tags
                outline = messages[-1]["content"].split("<outline>")[1].split("</outline>")[0]

                # Save the messages to a file with the current timestamp
                with open(f"outline_generator.json", "w") as file:
                    json.dump(messages, file, indent=4)

                # Return the extracted outline
                return outline

    # Call the get_outline function to start the conversation loop
    outline = get_outline()

    # Print the final outline
    print(colored("Final Outline:", "magenta"))
    print(outline)

    return outline