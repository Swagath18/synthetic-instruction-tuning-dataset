import json
import os

def parse_response(content):
    """
    Parses OpenAI generated text into instruction-answer dictionary.
    """
    try:
        instruction = content.split("Instruction:")[1].split("Answer:")[0].strip()
        answer = content.split("Answer:")[1].strip()
        return {"instruction": instruction, "input": "", "output": answer}
    except Exception as e:
        print(f"Parsing error: {e}\nContent was:\n{content}")
        return None

def save_json(data, path):
    """
    Saves a list of dictionaries into a JSON file.
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
