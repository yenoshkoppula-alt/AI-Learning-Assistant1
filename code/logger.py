import os
import csv
from datetime import datetime

# Path configuration
DATA_DIR = "data"
LOG_FILE = os.path.join(DATA_DIR, "emotion_logs.csv")

def init_logger():
    """
    Initializes the logger directory and CSV file.
    Creates headers: Timestamp, User Input, Emotion, Confidence, AI Response
    """
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    # Create CSV file with headers if it doesn't exist or is empty
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "User Input", "Emotion", "Confidence", "AI Response"])
        print(f"Initialized CSV database: {LOG_FILE}")

def log_interaction(user_input, emotion, confidence, ai_response):
    """
    Appends a single interaction record to the CSV log.
    """
    # Ensure initialized
    init_logger()
    
    timestamp = datetime.now().isoformat()
    
    try:
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, user_input, emotion, confidence, ai_response])
        print(f"Successfully logged interaction for emotion: {emotion}")
    except Exception as e:
        print(f"Error logging interaction: {e}")