# CALLBACK | An Recall Open Source Clone
#
# CAUTION!
# NOT SAFE TO USE! THIS SCRIPT DOES NOT ENCRYPT ANY STORED DATA.

import os
import threading
import time
import numpy as np
from datetime import datetime
from PIL import Image, ImageGrab, ImageChops
import pytesseract
import sqlite3
import re
import nltk
from pynput import mouse, keyboard

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'Path\\to\\tesseract.exe'

# Download NLTK data
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

download_nltk_data()

def clean_extracted_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9.,;:!?\'"\s]', '', text)
    text = text.lower()
    text = '\n'.join([line for line in text.split('\n') if line.strip() != ''])
    return text

def tokenize_text(text):
    tokens = nltk.word_tokenize(text)
    stop_words_en = set(nltk.corpus.stopwords.words('english'))
    stop_words_pt = set(nltk.corpus.stopwords.words('portuguese'))
    stop_words = stop_words_en.union(stop_words_pt)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return filtered_tokens

# Save screenshot and data to database
def save_screenshot(image, text, tokens):
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d_%H-%M-%S")
    screenshots_path = os.path.join(str(now.year), str(now.month), str(now.day))
    os.makedirs(screenshots_path, exist_ok=True)
    screenshot_filename = f'{formatted_now}.png'
    screenshot_save_path = os.path.join(screenshots_path, screenshot_filename)

    image_compressed = image.convert('RGB', palette=Image.ADAPTIVE, colors=8)
    image_compressed.save(screenshot_save_path, optimize=True, quality=50)

    conn = sqlite3.connect('screenshots.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS screenshots (
        id INTEGER PRIMARY KEY,
        image_path TEXT,
        text TEXT,
        tokens TEXT
    )
    ''')

    cursor.execute("INSERT INTO screenshots (image_path, text, tokens) VALUES (?, ?, ?)", 
                   (screenshot_save_path, text, ' '.join(tokens)))
    conn.commit()
    conn.close()

# Save and process screenshot
def capture_screen(screenshot):
    raw_text = pytesseract.image_to_string(screenshot, lang='eng+por')
    cleaned_text = clean_extracted_text(raw_text)
    tokens = tokenize_text(cleaned_text)
    save_screenshot(screenshot, cleaned_text, tokens)
    print("Text extracted and stored successfully!")

# Compare previous and current screenshot
def images_are_different(img1, img2, threshold=1):
    diff = ImageChops.difference(img1, img2)
    np_diff = np.array(diff)
    return np.sum(np_diff) > threshold

previous_screenshot = ImageGrab.grab()
screenshot_interval = 1  #  Screenshot interval in seconds
monitoring = False
monitoring_lock = threading.Lock()

# Detect changes on the screen
def monitor_screen():
    global previous_screenshot, monitoring
    with monitoring_lock:
        if monitoring:
            return
        monitoring = True

    while True:
        current_screenshot = ImageGrab.grab()
        if images_are_different(previous_screenshot, current_screenshot):
            capture_screen(current_screenshot)
            previous_screenshot = current_screenshot
            break

        time.sleep(screenshot_interval)

    with monitoring_lock:
        monitoring = False

# Function for monitoring mouse clicks and keystrokes
def on_click(x, y, button, pressed):
    if pressed:
        threading.Thread(target=monitor_screen).start()

def on_press(key):
    threading.Thread(target=monitor_screen).start()

mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press)

mouse_listener.start()
keyboard_listener.start()

# Keep the script running
mouse_listener.join()
keyboard_listener.join()