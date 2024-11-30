import os
import json
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths to the preprocessed data
preprocessed_data_path = '../../data/processed/cleaned_data.json'
cleaned_output_path = '../../data/processed/cleaned_data_no_missing.json'


def load_preprocessed_data(file_path):
    """Load the preprocessed data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def review_data(data):
    """Review the data by providing basic statistics."""
    if isinstance(data, list) and data:
        first_record = data[0]
        logger.info(f"First record: {first_record}")

        if isinstance(first_record, dict):
            df = pd.DataFrame(data)
            logger.info(f"Dataframe shape: {df.shape}")

            if not df.empty:
                logger.info("Basic Statistics:")
                logger.info(df.describe(include='all'))
                logger.info("Missing values per column:")
                logger.info(df.isnull().sum())
                logger.info("Unique values per column:")
                logger.info(df.nunique())
            else:
                logger.warning("Dataframe is empty.")

            return df
        else:
            logger.error("The data records are not in dictionary format.")
    else:
        logger.error("The preprocessed data is not in the expected format (list of dictionaries).")

    return None


def remove_missing_data(df):
    """Remove rows with missing values in crucial columns."""
    df_cleaned = df.dropna(subset=['dialog', 'act', 'emotion'])
    logger.info(f"Removed rows with missing values. New dataframe shape: {df_cleaned.shape}")
    return df_cleaned


def save_cleaned_data(df, output_path):
    """Save the cleaned data to a JSON file."""
    df.to_json(output_path, orient='records', lines=True, force_ascii=False)
    logger.info(f"Cleaned data saved at: {output_path}")


def main():
    data = load_preprocessed_data(preprocessed_data_path)
    df = review_data(data)

    if df is not None and not df.empty:
        df_cleaned = remove_missing_data(df)
        save_cleaned_data(df_cleaned, cleaned_output_path)
        # Proceed with consolidation if needed
        dataframes = [df_cleaned]
        consolidated_df = pd.concat(dataframes, ignore_index=True)
        consolidated_output_path = '../../data/consolidated/consolidated_data_no_missing.csv'
        consolidated_df.to_csv(consolidated_output_path, index=False)
        logger.info(f"Consolidated data saved at: {consolidated_output_path}")


if __name__ == "__main__":
    main()
