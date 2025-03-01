from flask import Flask, request, jsonify, render_template
import logging
import PyPDF2
import difflib
import os

app = Flask(__name__, static_folder='static', template_folder='templates')

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# קריאת תוכן ה-PDF ושמירתו במשתנה
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        # ודא שהנתיב תקין ביחס למיקום הקובץ
        if not os.path.exists(pdf_path):
            logger.error(f"קובץ {pdf_path} לא נמצא במיקום הנוכחי!")
            return ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text = page.extract_text() or ""
                text += extracted_text + " "
        logger.info(f"טקסט מוצלח נקרא מה-PDF: {text[:100]}")  # לוג קצר לבדיקה
    except Exception as e:
        logger.error(f"שגיאה בקריאת ה-PDF: {e}")
        return ""
    return text.lower()

# קריאת ה-PDF - עדכן את הנתיב אם צריך
pdf_path = "תולדות האומנות - רנסאנס.pdf"
pdf_text = extract_text_from_pdf(pdf_path)
if not pdf_text:
    logger.error("ה-PDF ריק או לא נקרא! בדוק את הנתיב או את הקובץ.")
else:
    print("🔍 טקסט מה-PDF (1000 תווים ראשונים):", pdf_text[:1000])  # בדיקה מלאה, מרווח תקין

def find_best_match(question):
    """ מחפש התאמות לשאלה בטקסט מתוך ה-PDF """
    if not pdf_text:
        return "אין לי את המידע הזה בתוך ה-PDF"
    sentences = [s for s in pdf_text.split(". ") if s.strip()]  # מפצל למשפטים תקינים
    matches = difflib.get_close_matches(question.lower(), sentences, n=3, cutoff=0.3)  # cutoff נמוך יותר
    if matches:
        return matches[0]
    # בדיקות ידניות לדוגמה (אפשר להוסיף לפי התוכן)
    if "רנסאנס" in question.lower():
        return "הרנסאנס התרחש באירופה במאות 14-17."
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
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))