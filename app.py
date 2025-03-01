from flask import Flask, request, jsonify, render_template
import logging
import PyPDF2
import difflib

app = Flask(__name__)

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# קריאת תוכן ה-PDF ושמירתו במשתנה
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
    except Exception as e:
        logger.error(f"שגיאה בקריאת ה-PDF: {e}")
    print("🔍 טקסט מה-PDF:", pdf_text[:1000])  # מציג את 1000 התווים הראשונים של ה-PDF
    return text.lower()

pdf_text = extract_text_from_pdf("תולדות האומנות - רנסאנס.pdf")

def find_best_match(question):
    """ מחפש התאמות לשאלה בטקסט מתוך ה-PDF """
    sentences = pdf_text.split(". ")  # מפצל את ה-PDF למשפטים
    matches = difflib.get_close_matches(question.lower(), sentences, n=3, cutoff=0.4)
    
    if matches:
        return matches[0]  # מחזיר את ההתאמה הכי קרובה
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
            return jsonify({'error': 'שאלה נדרשת'}), 400
            
        answer = find_best_match(question)
        return jsonify({'answer': answer})
    
    except Exception as e:
        logger.error(f"שגיאה בשרת: {str(e)}")
        return jsonify({'error': f'שגיאת שרת: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
