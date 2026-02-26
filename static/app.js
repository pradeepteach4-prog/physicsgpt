const questionEl = document.getElementById('question');
const examEl = document.getElementById('exam');
const levelEl = document.getElementById('level');
const answerBtn = document.getElementById('answerBtn');
const speakBtn = document.getElementById('speakBtn');
const stopBtn = document.getElementById('stopBtn');
const statusEl = document.getElementById('status');
const answerEl = document.getElementById('answer');

let latestAnswer = '';

async function generateAnswer() {
  const question = questionEl.value.trim();
  if (!question) {
    statusEl.textContent = 'Please type a physics question first.';
    return;
  }

  statusEl.textContent = 'Generating answer...';
  answerBtn.disabled = true;

  try {
    const response = await fetch('/api/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question,
        exam: examEl.value,
        level: levelEl.value,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Unknown server error');
    }

    latestAnswer = data.answer;
    answerEl.textContent = latestAnswer;
    speakBtn.disabled = false;
    statusEl.textContent = 'Answer ready. Click "Speak Answer" to hear it.';
  } catch (error) {
    statusEl.textContent = `Error: ${error.message}`;
  } finally {
    answerBtn.disabled = false;
  }
}

function speakAnswer() {
  if (!latestAnswer) return;

  if (!('speechSynthesis' in window)) {
    statusEl.textContent = 'Speech synthesis is not supported in this browser.';
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(latestAnswer);
  utterance.rate = 1;
  utterance.pitch = 1;

  utterance.onstart = () => {
    statusEl.textContent = 'Speaking...';
    stopBtn.disabled = false;
  };

  utterance.onend = () => {
    statusEl.textContent = 'Finished speaking.';
    stopBtn.disabled = true;
  };

  utterance.onerror = () => {
    statusEl.textContent = 'Speech playback failed.';
    stopBtn.disabled = true;
  };

  window.speechSynthesis.speak(utterance);
}

function stopSpeaking() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    statusEl.textContent = 'Speech stopped.';
  }
  stopBtn.disabled = true;
}

answerBtn.addEventListener('click', generateAnswer);
speakBtn.addEventListener('click', speakAnswer);
stopBtn.addEventListener('click', stopSpeaking);
