from flask import Flask, request, jsonify, render_template
import logging
import PyPDF2
from difflib import get_close_matches

app = Flask(__name__)

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# קריאת ה-PDF ושמירתו במשתנה
pdf_path = "תולדות האומנות - רנסאנס.pdf"

def read_pdf(pdf_path):
    """קורא את ה-PDF ושומר את התוכן בטקסט"""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.lower()  # להקל על חיפושים לא תלויי אותיות גדולות/קטנות

pdf_content = read_pdf(pdf_path)

def find_best_match(question):
    """מוצא את הקטעים שהכי דומים לשאלה שנשאלה"""
    sentences = pdf_content.split("\n")
    matches = get_close_matches(question.lower(), sentences, n=3, cutoff=0.5)
    
    if matches:
        return matches[0]  # מחזיר את ההתאמה הכי טובה
    else:
        return "אין לי את המידע הזה בתוך ה-PDF"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def get_answer():
    try:
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({'error': 'No question provided'}), 400
            
        answer = find_best_match(question)
        return jsonify({'answer': answer})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
