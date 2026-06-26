const I18N = {
  en: {
    app_title: "Fake News Detector",
    app_desc: "Select an image and text on the page, right-click, and choose 'Analyze Fake News'.",
    analyzing: "Analyzing...",
    confidence: "Confidence",
    score_sim: "Similarity",
    score_txt: "Text Suspicious",
    score_img: "Image Manipulation",
    reasons: "Reasons:",
    feedback_prompt: "Is this correct?",
    correct: "Yes",
    incorrect: "No",
    thanks: "Thanks for your feedback!",
    result_real: "Real News",
    result_fake: "Fake News",
    result_suspicious: "Suspicious",
    level_high: "High",
    level_med: "Medium",
    level_low: "Low"
  },
  vi: {
    app_title: "Trợ lý Kiểm tin",
    app_desc: "Bôi đen văn bản và click chuột phải vào ảnh, chọn 'Analyze Fake News'.",
    analyzing: "Đang phân tích...",
    confidence: "Độ tin cậy",
    score_sim: "Khớp Ảnh-Chữ",
    score_txt: "Từ ngữ giật tít",
    score_img: "Ảnh chỉnh sửa",
    reasons: "Lý do:",
    feedback_prompt: "Kết quả này có đúng không?",
    correct: "Đúng",
    incorrect: "Sai",
    thanks: "Cảm ơn đóng góp của bạn!",
    result_real: "Tin thật",
    result_fake: "Tin giả",
    result_suspicious: "Đáng ngờ",
    level_high: "Cao",
    level_med: "Trung bình",
    level_low: "Thấp"
  }
};

let currentLang = 'en';

function applyLang() {
  const dict = I18N[currentLang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) el.textContent = dict[key];
  });
  
  document.getElementById('lang-toggle').textContent = currentLang === 'en' ? 'VI' : 'EN';
  
  // Re-render UI if data exists
  chrome.storage.local.get(['analysisResult'], (data) => {
    if (data.analysisResult) updateUI(data);
  });
}

function formatLevel(score, isInverted = false) {
  // If isInverted is true (for similarity): higher score = better (Low suspicion)
  // If false (for text/img): higher score = High suspicion
  let value = score;
  if (isInverted) value = 1 - score; 

  const dict = I18N[currentLang];
  if (value > 0.6) return `${dict.level_high} (${Math.round(score*100)}%)`;
  if (value > 0.3) return `${dict.level_med} (${Math.round(score*100)}%)`;
  return `${dict.level_low} (${Math.round(score*100)}%)`;
}

function formatResult(resName) {
  const dict = I18N[currentLang];
  if (resName.toLowerCase() === 'real') return dict.result_real;
  if (resName.toLowerCase() === 'fake') return dict.result_fake;
  return dict.result_suspicious;
}

function updateUI(data) {
  const loading = document.getElementById('loading');
  const resultContainer = document.getElementById('result-container');
  const errorContainer = document.getElementById('error-container');

  loading.classList.add('hidden');
  resultContainer.classList.add('hidden');
  errorContainer.classList.add('hidden');
  document.getElementById('feedback-thanks').classList.add('hidden');

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
    badge.textContent = formatResult(res.result);
    badge.className = 'badge ' + res.result.toLowerCase();

    // Tags
    const tagsContainer = document.getElementById('tags-container');
    tagsContainer.innerHTML = '';
    if (res.tags) {
      res.tags.forEach(tag => {
        const span = document.createElement('span');
        span.className = 'tag';
        span.textContent = tag;
        tagsContainer.appendChild(span);
      });
    }

    document.getElementById('confidence-number').textContent = res.confidence;
    document.getElementById('score-sim').textContent = formatLevel(res.scores.similarity, true);
    document.getElementById('score-text').textContent = formatLevel(res.scores.text_suspicious);
    document.getElementById('score-img').textContent = formatLevel(res.scores.image_manipulation);

    const ul = document.getElementById('reasons-list');
    ul.innerHTML = ''; 
    res.reasons.forEach(r => {
      const li = document.createElement('li');
      li.textContent = r;
      ul.appendChild(li);
    });
  }
}

function sendFeedback(isCorrect) {
  chrome.storage.local.get(['analysisRequestData'], (data) => {
    if (!data.analysisRequestData) return;
    
    fetch("http://localhost:8000/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        image_url: data.analysisRequestData.image_url,
        text: data.analysisRequestData.text,
        is_correct: isCorrect,
        user_feedback: isCorrect ? "Correct" : "Incorrect"
      })
    }).then(() => {
      document.getElementById('feedback-thanks').classList.remove('hidden');
    }).catch(console.error);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  applyLang();

  document.getElementById('lang-toggle').addEventListener('click', () => {
    currentLang = currentLang === 'en' ? 'vi' : 'en';
    applyLang();
  });

  document.getElementById('btn-correct').addEventListener('click', () => sendFeedback(true));
  document.getElementById('btn-incorrect').addEventListener('click', () => sendFeedback(false));

  chrome.storage.local.get(['analysisResult', 'analysisError', 'isAnalyzing'], updateUI);

  chrome.storage.onChanged.addListener((changes, namespace) => {
    if (namespace === 'local') {
      chrome.storage.local.get(['analysisResult', 'analysisError', 'isAnalyzing'], updateUI);
    }
  });
});
