from openai import OpenAI
import json
import os
from tqdm import tqdm
from utils import parse_response, save_json
from quality_checker import QualityChecker
from dotenv import load_dotenv

# Tracking cost
total_tokens_used = 0
total_cost_usd = 0

load_dotenv()
client = OpenAI()

TOPICS = ["Astronomy", "Physics", "Computer Science", "Mathematics", "History"]
N_SAMPLES = 10
SAVE_DIR = "data"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------------------
# Core Functions
# ---------------------

def generate_instruction_answer(topic):
    """
    Generate a single instruction-answer pair for a given topic using OpenAI Chat API.
    """
    system_prompt = f"""
    You are an AI assistant creating instruction-answer pairs for fine-tuning LLMs.
    Topic: {topic}
    Generate a meaningful instruction and a detailed, accurate answer.
    Format:
    Instruction: <instruction>
    Answer: <answer>
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Generate one instruction-answer pair."}
            ],
            temperature=0.7,
            max_tokens=500
        )

        content = response.choices[0].message.content
        # ---Track Cost---
        total_tokens = response.usage.total_tokens
        cost = (total_tokens / 1000) * 0.09  # Assuming $0.09 per 1k tokens
        global total_tokens_used, total_cost_usd
        total_tokens_used += total_tokens
        total_cost_usd += cost
        print(f" Total tokens used: {total_tokens_used} | Estimated cost: ${total_cost_usd:.4f}")

        return parse_response(content)

    except Exception as e:
        print(f"Error during generation: {e}")
        return None

def generate_dataset(topic, n_samples, quality_checker):
    """
    Generate and save dataset for one topic with quality checking.
    """
    filename = f"instructions_{topic.lower().replace(' ', '_')}.json"
    save_path = os.path.join(SAVE_DIR, filename)
    dataset = []

    print(f"\nGenerating {n_samples} samples for topic: {topic}")

    for _ in tqdm(range(n_samples)):
        sample = generate_instruction_answer(topic)
        if sample:
            quality_passed = quality_checker.check(sample)
            if quality_passed:
                dataset.append(sample)

    save_json(dataset, save_path)
    print(f"Saved {len(dataset)} high-quality samples to {save_path}")

# ---------------------
# Main
# ---------------------

def main():
    quality_checker = QualityChecker(min_answer_words=30)
    for topic in TOPICS:
        generate_dataset(topic, N_SAMPLES, quality_checker)

if __name__ == "__main__":
    main()
