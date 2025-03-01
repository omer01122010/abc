function submitQuestion() {
    const question = document.getElementById('question').value;
    const options = Array.from(document.getElementsByClassName('option'))
                        .map(input => input.value)
                        .filter(value => value !== ''); // מסנן מסיחים ריקים

    if (!question || options.length < 4) {
        document.getElementById('statusMessage').innerText = 'אנא הכנס שאלה ומינימום 4 מסיחים!';
        return;
    }

    // מציג אנימציית טעינה
    const answerDiv = document.getElementById('answer');
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    answerDiv.innerHTML = '<div class="loading"></div>';
    document.getElementById('statusMessage').innerText = '';

    // שולח בקשה לשרת
    fetch('/answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, options })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('שגיאה בחיבור לשרת');
        }
        return response.json();
    })
    .then(data => {
        answerDiv.innerText = data.answer;
        submitBtn.disabled = false;
    })
    .catch(error => {
        console.error('שגיאה:', error);
        answerDiv.innerText = '';
        document.getElementById('statusMessage').innerText = 'שגיאה בחיבור לשרת. אנא נסה שנית מאוחר יותר.';
        submitBtn.disabled = false;
    });
}
