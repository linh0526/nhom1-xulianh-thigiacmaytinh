document.addEventListener('DOMContentLoaded', () => {
  // Check if we have analysis result in local storage
  chrome.storage.local.get(['analysisResult', 'analysisError', 'isAnalyzing'], (data) => {
    const loading = document.getElementById('loading');
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');

    if (data.isAnalyzing) {
      loading.classList.remove('hidden');
      return;
    }

    if (data.analysisError) {
      errorContainer.classList.remove('hidden');
      document.getElementById('error-message').textContent = data.analysisError;
      return;
    }

    if (data.analysisResult) {
      const res = data.analysisResult;
      resultContainer.classList.remove('hidden');

      const badge = document.getElementById('result-badge');
      badge.textContent = res.result;
      badge.className = 'badge ' + res.result.toLowerCase();

      document.getElementById('confidence-text').textContent = 'Confidence: ' + res.confidence + '%';
      document.getElementById('score-sim').textContent = res.scores.similarity;
      document.getElementById('score-text').textContent = res.scores.text_suspicious;
      document.getElementById('score-img').textContent = res.scores.image_manipulation;

      const ul = document.getElementById('reasons-list');
      res.reasons.forEach(r => {
        const li = document.createElement('li');
        li.textContent = r;
        ul.appendChild(li);
      });
    }
  });
});
