# AI Emotion Detector

This project is a Flask web application that analyses English text with the IBM Watson NLP Emotion Predict service. It returns confidence scores for anger, disgust, fear, joy, and sadness, together with the dominant emotion.

The application was completed for the Coursera **Python Project for AI & Application Development** final project.

## Project structure

```text
EmotionDetection/
  __init__.py
  emotion_detection.py
static/
  mywebscript.js
  style.css
templates/
  index.html
server.py
test_emotion_detection.py
requirements.txt
```

## Run locally

```bash
python -m pip install -r requirements.txt
python server.py
```

Open `http://localhost:5000` in a browser.

## Test and analyse

```bash
python -m unittest test_emotion_detection.py -v
pylint server.py
```

The Watson service is the primary analyser. A small deterministic fallback keeps the demonstration and tests usable if the training endpoint is temporarily unavailable.

## Author

Djessi Jorge
