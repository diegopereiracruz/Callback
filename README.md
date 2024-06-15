# CALLBACK | An Open Source Clone of Microsoft's Recall

[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)]()

## Introduction

CALLBACK is an open-source recreation of Microsoft's recently announced Recall feature. Recall captures screenshots of every action a user performs on their computer and saves them in a local database. This serves as a memory bank, enabling users to search and retrieve past activities to remember website names, file locations, and more. This project is in its early stages and is intended for educational purposes only.

⚠️ **Warning**: This program does NOT protect stored data with any encryption! Use it only for study purposes.

## Features

- **Screenshot Capture**: Automatically captures screenshots of user actions.
- **Text Extraction**: Extracts text from screenshots using OCR (Optical Character Recognition).
- **Tokenization**: Tokenizes extracted text for efficient searching.
- **Search Functionality**: Allows users to search for past screenshots based on keywords.
- **Local Database Storage**: Saves screenshots and metadata in a local SQLite database.

## Installation

### Prerequisites

- Python 3.x
- Tesseract OCR
- Required Python packages listed in `requirements.txt`

### Setup (Windows only at the moment)

1. Clone the repository:
    ```bash
    git clone https://github.com/diegopereiracruz/Callback.git
    cd Callback
    ```

2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) is installed and its executable path is correctly set in `callback.py`:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r'Path\\to\\tesseract.exe'
    ```

## Usage

1. Run the `callback.py` script to start capturing screenshots and monitoring user actions:
    ```bash
    python callback.py
    ```

2. To search for screenshots based on keywords, run `callback_search.py` with the desired keyword:
    ```bash
    python callback_search.py
    ```

### Example

- **Capture and Process Screenshots**:
    ```python
    # Within callback.py
    mouse_listener.start()
    keyboard_listener.start()
    ```

- **Search for Captured Screenshots**:
    ```python
    # Within callback_search.py
    keyword = "python"
    image_paths = search_images(keyword)
    for path in image_paths:
        print(path)
    ```

## Limitations and Future Improvements

- **Data Security**: Currently, there is no encryption for stored data. This is a significant security risk and should be addressed before using the software for any sensitive purposes.
- **Performance**: The script may impact system performance due to continuous screenshot capturing.
- **Feature Completeness**: This project is a basic implementation and lacks many advanced features that could enhance usability and functionality.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## Acknowledgements

- Microsoft for the concept of Recall.
- The open-source community for providing the tools and libraries used in this project.

