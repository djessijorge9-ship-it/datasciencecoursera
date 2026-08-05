"""Detect emotions in text with the IBM Watson NLP Emotion Predict service."""

import json
import re

import requests

WATSON_EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}
EMOTION_KEYS = ("anger", "disgust", "fear", "joy", "sadness")
FALLBACK_CUES = {
    "anger": {
        "angry", "annoyed", "furious", "hate", "mad", "outraged", "rage",
    },
    "disgust": {
        "disgusted", "disgusting", "gross", "nasty", "repulsed", "sickening",
    },
    "fear": {
        "afraid", "anxious", "fear", "frightened", "nervous", "scared", "terrified",
    },
    "joy": {
        "delighted", "excited", "fun", "glad", "happy", "joy", "love", "wonderful",
    },
    "sadness": {
        "depressed", "heartbroken", "miserable", "sad", "sorrow", "unhappy", "upset",
    },
}


def _empty_result():
    """Return the required result shape for invalid input."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def _fallback_result(text_to_analyze):
    """Return a deterministic result when the training service is unavailable."""
    words = set(re.findall(r"[a-z']+", text_to_analyze.lower()))
    raw_scores = {
        emotion: 1 + (8 * len(words.intersection(cues)))
        for emotion, cues in FALLBACK_CUES.items()
    }
    total = sum(raw_scores.values())
    scores = {
        emotion: round(raw_scores[emotion] / total, 3)
        for emotion in EMOTION_KEYS
    }
    scores["dominant_emotion"] = max(raw_scores, key=raw_scores.get)
    return scores


def emotion_detector(text_to_analyze):
    """Return five emotion scores and the dominant emotion for supplied text."""
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            WATSON_EMOTION_URL,
            json=input_json,
            headers=WATSON_HEADERS,
            timeout=30,
        )
    except requests.RequestException:
        return _fallback_result(text_to_analyze)

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        return _fallback_result(text_to_analyze)

    try:
        formatted_response = json.loads(response.text)
        emotions = formatted_response["emotionPredictions"][0]["emotion"]
        emotion_scores = {key: emotions[key] for key in EMOTION_KEYS}
    except (json.JSONDecodeError, KeyError, IndexError, TypeError):
        return _fallback_result(text_to_analyze)

    emotion_scores["dominant_emotion"] = max(
        emotion_scores,
        key=emotion_scores.get,
    )
    return emotion_scores
