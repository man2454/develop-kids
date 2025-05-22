# Quest of Knowledge

A Python-based educational game for children aged 5-7.

## Setup and Installation

### Prerequisites
- Python 3 (ensure it's added to your system's PATH)

### Dependencies
This game uses the following Python libraries:
  - `pygame`: For graphics, sound, and game mechanics.
  - `pyttsx3`: For text-to-speech functionality.

You can install them using pip:
  ```bash
  pip install pygame pyttsx3
  ```

**Note on Text-to-Speech (TTS) engines:** `pyttsx3` relies on text-to-speech engines available on your operating system.
  - **Windows:** Should work out of the box using SAPI5.
  - **macOS:** Should work out of the box using NSSpeechSynthesizer.
  - **Linux:** May require installing a TTS engine like `espeak` or `festival`. If you encounter issues with TTS on Linux, try installing `espeak`:
    ```bash
    sudo apt-get update && sudo apt-get install espeak
    ```

## How to Play
1. Navigate to the project's root directory in your terminal.
2. Run the game using the command: `python src/main.py`

**Objective:** Answer 20 questions correctly to complete the Quest of Knowledge. Be careful! Wrong answers will reduce your HP. If your HP reaches 0, the game is over.
