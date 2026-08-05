function RunSentimentAnalysis() {
  const textToAnalyze = document.getElementById("textToAnalyze").value;
  const responsePanel = document.getElementById("system_response");
  const button = document.getElementById("run-analysis");

  button.disabled = true;
  responsePanel.textContent = "Analysing...";

  fetch(`/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`)
    .then((response) => response.text())
    .then((result) => {
      responsePanel.textContent = result;
      responsePanel.classList.toggle("error", result.startsWith("Invalid text!"));
    })
    .catch(() => {
      responsePanel.textContent = "The analysis could not be completed. Please try again.";
      responsePanel.classList.add("error");
    })
    .finally(() => {
      button.disabled = false;
    });
}
