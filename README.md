# Netfly Subtitle Converter

A subtitle overlay tool that converts the subtitles from Japanese Language ( currently hardcoded ) to English and displays the translated subtitles while the video is being played. 
Please note that this is not a real time translation tool. Users need to upload ScreenCapture of the video files with subtitles visible to make this script work. 
Only subtitles are overlayed in real time. This tool uses JavaScript to synchronize custom subtitles with the video player and Python to process subtitle data with OCR and cloud technologies.

## Features
- Displays custom subtitles with timing synchronization on Netflix videos.
- Uses Google Vision OCR for text recognition.
- Stores subtitle data on AWS S3 for easy access and retrieval.
- Customizable font style, color, and background for better readability.

## Tech Stack
- **Python**: Processes subtitle data, extracts text with OCR, and uploads it to AWS S3.
- **AWS S3**: Cloud storage for subtitle files, making them easily accessible for the JavaScript overlay.
- **Google Cloud Vision**: Optical Character Recognition (OCR) for extracting subtitle text from images.
- **AWS Translate**: Translating the text from Japanese Language to English.
- **JavaScript**: Core logic for subtitle timing and display.

## How It Works
1. **Subtitle Processing (Python & OCR)**:
   - Subtitle images are processed using Python and Google Cloud Vision OCR.
   - Text is extracted and formatted into JSON with start and end times.
   - JSON files are stored in AWS S3.

2. **JavaScript Overlay**:
   - A JavaScript script overlays the custom subtitles on Netflix by fetching the JSON subtitle file from S3.
   - Uses `setTimeout` to display and hide subtitles at the appropriate times.

## JSON Subtitle Format
Subtitles are stored in JSON format with each entry containing `start_time`, `end_time`, and `translated_text`:

```json
[
  {
    "start_time": 1,
    "end_time": 5,
    "translated_text": "Hello, welcome!"
  },
  {
    "start_time": 6,
    "end_time": 10,
    "translated_text": "Let's get started."
  }
]
```
## Setup
1. You should have the screen capture of the anime for which you need the subtitles to be translated in real time.
2. Please have your own Google Cloud Vision API Key ready. Also please be ready with your own AWS Access Key and AWS Secret Access Key as we will need to access AWS resources like S3 and AWS Translate.
3. This has been tested on Netflix. When you screen record something on Netflix, the entire background becomes black and only subtitles are visible. This is good for us since extracting text from Images becomes easier without a lot of pre processing.
4. Clone the repo and store the video file in your root directory from where you are running the main.py.

## Known Limitations
1. Syncing Accuracy: Subtitle timing may vary slightly due to network or browser performance.
2. Manual Loading: Script must be loaded manually on Netflix each time.

## Working Demo / Screenshot
<img width="1190" alt="image" src="https://github.com/user-attachments/assets/d3687896-4ba6-47e4-9a09-023e98e9fef3">
<img width="1193" alt="image" src="https://github.com/user-attachments/assets/3f4ba0db-ab3a-4129-97ef-1bf9f98e0b34">

## Contributions
Contributions are always welcome. Please feel free to open new issues or raise a Pull Request for new features or bug fixes.
