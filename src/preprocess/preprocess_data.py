import os
import json
import pandas as pd
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the paths to your data directories relative to the script location
data_dirs = [
    '../../data/raw/movie-corpus/',
    '../../data/raw/EmotionLines/friends/',
    '../../data/raw/dailydialog/',
    '../../data/raw/Synthetic_Persona_Chat/',
    '../../data/raw/topical_chat/'
]

def load_data():
    data = []
    for dir in data_dirs:
        logger.info(f"Checking directory: {dir}")
        if not os.path.exists(dir):
            logger.error(f"Directory not found: {dir}")
            continue
        for file_name in os.listdir(dir):
            if file_name.startswith('.'):
                logger.info(f"Skipping hidden file: {file_name}")
                continue
            if file_name.endswith('.json') or file_name.endswith('.csv'):
                file_path = os.path.join(dir, file_name)
                try:
                    if file_name.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            logger.info(f"Loading JSON file: {file_path}")
                            data.extend(json.load(f))
                    elif file_name.endswith('.csv'):
                        logger.info(f"Loading CSV file: {file_path}")
                        data.extend(pd.read_csv(file_path).to_dict('records'))
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {e}")
                    continue
    return data

def clean_text(text):
    """Clean text by lowering case and removing special characters."""
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove special characters
    return text

def clean_data(data):
    """Clean the dataset."""
    cleaned_data = []
    for record in data:
        logger.info(f"Original record: {record}")
        if isinstance(record, dict):
            cleaned_record = {k: clean_text(v) for k, v in record.items()}
            logger.info(f"Cleaned record: {cleaned_record}")
            cleaned_data.append(cleaned_record)
        else:
            logger.warning(f"Skipping non-dict record: {record}")
    return cleaned_data

def preprocess():
    data = load_data()
    logger.info(f"Loaded data count: {len(data)}")
    cleaned_data = clean_data(data)
    logger.info(f"Cleaned data count: {len(cleaned_data)}")
    # Save the cleaned data for later use
    os.makedirs('../../data/processed/', exist_ok=True)
    with open('../../data/processed/cleaned_data.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False)
    logger.info("Data cleaning complete. Cleaned data saved.")

if __name__ == "__main__":
    preprocess()
