# Synthetic Instruction-Tuning Dataset Generator

This project generates high-quality synthetic instruction-answer datasets for fine-tuning Large Language Models (LLMs).

It features automatic rule-based quality checking to ensure dataset usefulness and relevance.

---

## Features
- Multi-topic generation (Astronomy, Physics, Computer Science, Mathematics, History)
- Instruction-Answer formatting
- Quality filtering based on length, structure, and relevance
- Live tracking of token usage and cost
- Professional modular structure ready for scaling

## Project Structure
```
synthetic-instruction-tuning-dataset/
├── data/                   # Generated JSON instruction-answer datasets
├── reports/                # Logs for quality control failures
├── generate_data.py        # Main generator script
├── quality_checker.py      # Rule-based quality checker
├── utils.py                # Utilities (parsing, saving)
├── requirements.txt        # Required Python packages
├── README.md               # This documentation
├── .gitignore              # Git ignore rules
└── .env                    # Private API
```


## Running the Project

1. Install requirements:

    ```bash
    pip install -r requirements.txt

2. Set your OpenAI API Key:

    Create a .env file in project root:
    ```bash
    OPENAI_API_KEY=your-api-key-here

3. Run the generator:

    ```bash
    python generate_data.py

##  Output
High-quality instruction-answer pairs saved as .json files inside /data/

Failed or low-quality samples logged into /reports/quality_failures.txt

## Sample JSON entry:
```
{
  "instruction": "Describe the life cycle of a star like the Sun.",
  "input": "",
  "output": "A star like the Sun forms from a molecular cloud, enters the main sequence phase, expands into a red giant, and ends as a white dwarf."
}
```

## Future Enhancements
Scaling to async/multi-threaded generation for larger datasets

Adding automatic adversarial filtering

Difficulty level-based instruction generation (easy, medium, hard)