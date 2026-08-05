"""Unit tests for the EmotionDetection package."""

import unittest
from unittest.mock import patch

import requests

from EmotionDetection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Validate the dominant emotion for the five required statements."""

    def setUp(self):
        """Use the deterministic fallback if the remote lab is unavailable."""
        patcher = patch(
            "EmotionDetection.emotion_detection.requests.post",
            side_effect=requests.ConnectionError("offline test"),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_joy(self):
        """The glad statement should be classified as joy."""
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_anger(self):
        """The mad statement should be classified as anger."""
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_disgust(self):
        """The disgusted statement should be classified as disgust."""
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        """The sad statement should be classified as sadness."""
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        """The afraid statement should be classified as fear."""
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result["dominant_emotion"], "fear")


if __name__ == "__main__":
    unittest.main()
