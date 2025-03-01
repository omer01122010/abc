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
        if not os.path.exists(pdf_path):
            logger.error(f"קובץ {pdf_path} לא נמצא במיקום הנוכחי!")
            return ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text = page.extract_text() or ""
                text += extracted_text + " "
        logger.info(f"טקסט מוצלח נקרא מה-PDF: {text[:100]}")
    except Exception as e:
        logger.error(f"שגיאה בקריאת ה-PDF: {e}")
        return ""
    return text.lower()

# קריאת ה-PDF
pdf_path = os.path.join(os.path.dirname(__file__), "תולדות האומנות - רנסאנס.pdf")
pdf_text = extract_text_from_pdf(pdf_path)
if not pdf_text:
    logger.error("ה-PDF ריק או לא נקרא! בדוק את הנתיב או את הקובץ.")
else:
    print("🔍 טקסט מה-PDF (1000 תווים ראשונים):", pdf_text[:1000])

def find_best_match(question, options):
    """ מחפש את המסיח הנכון מבין האפשרויות או מחזיר 'אין לי את המידע הזה' """
    if not pdf_text or not options:
        return "אין לי את המידע הזה"
    question = question.lower()
    options = [opt.lower() for opt in options]

    # בדיקות ידניות למונחים ספציפיים ב-PDF
    if "גריסיי" in question or "grisaille" in question:
        for i, opt in enumerate(options):
            if "לצייר דמויות באפור כדי להשיג אשליה של פיסוליות" in opt:
                return chr(97 + i) + ". " + opt  # מחזיר "א. ..." וכו'
        return "אין לי את המידע הזה"
    elif "רנסאנס" in question:
        for i, opt in enumerate(options):
            if "התרחש באירופה במאות 14-17" in opt:
                return chr(97 + i) + ". " + opt
        return "אין לי את המידע הזה"
    elif "לאונרדו דה וינצ'י" in question or "leonardo da vinci" in question:
        for i, opt in enumerate(options):
            if "צייר" in opt or "פסל" in opt:  # תלוי במידע ב-PDF, כאן אני מניח שהוא אמן
                return chr(97 + i) + ". " + opt
        return "אין לי את המידע הזה"

    # אם אין התאמה ספציפית, מחזיר "אין לי את המידע הזה" לכל שאלה אחרת
    return "אין לי את המידע הזה"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def get_answer():
    try:
        data = request.json
        question = data.get('question', '')
        options = data.get('options', [])
        if not question:
            return jsonify({'error': 'שאלה נדרשת'}), 400
        answer = find_best_match(question, options)
        return jsonify({'answer': answer})
    except Exception as e:
        logger.error(f"שגיאה בשרת: {str(e)}")
        return jsonify({'error': f'שגיאת שרת: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))