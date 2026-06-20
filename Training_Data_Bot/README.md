# Training Data Bot

## Overview

This project automates the process of converting documents into structured datasets for machine learning and LLM fine-tuning. It supports multiple input sources, generates training examples, evaluates dataset quality, and exports the final dataset in commonly used formats.

The project demonstrates document processing, data preparation, and dataset generation workflows used in AI applications.

## Features

* Document loading from PDFs, text files, folders, and URLs
* Automated text preprocessing and chunking
* Training data generation for multiple tasks
* Quality evaluation and filtering
* Dataset export in JSON, JSONL, and CSV formats
* Modular and extensible pipeline design

## Tech Stack

* Python
* AsyncIO
* PDF Processing Libraries
* Web Scraping Utilities
* Data Processing Tools
* JSON and CSV Export Utilities

## How It Works

1. Documents are collected from supported sources.
2. Text is cleaned and divided into smaller chunks.
3. Training examples are generated for different tasks.
4. Dataset quality is evaluated and filtered.
5. The final dataset is exported in the selected format.

## Project Structure

```text
training_data_bot/
│
├── bot.py
├── models.py
├── sources/
├── preprocessing/
├── tasks/
├── evaluation/
├── storage/
├── core/
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd training-data-bot

pip install -r requirements.txt
```

## Run the Project

```bash
python run_example.py
```

Generated datasets will be saved in the output directory.

## Example Use Cases

* Creating datasets for chatbot training
* Building question-answering datasets
* Document summarization dataset generation
* Classification dataset preparation
* Fine-tuning data preparation for LLMs

## Learning Outcomes

Through this project, I learned:

* Data preprocessing techniques
* Document ingestion pipelines
* Dataset generation workflows
* Quality evaluation methods
* Asynchronous Python programming
* Modular software design

## Future Improvements

* Additional task generation templates
* Advanced quality evaluation metrics
* Support for more document formats
* Cloud storage integration
* Interactive user interface

## License

This project is based on open-source code released under the MIT License.
Original copyright belongs to the respective author.
I have used this project for learning, documentation, and portfolio-building purposes.
