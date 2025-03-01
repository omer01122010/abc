from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)

# הגדרת לוגים
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# תוכן ה-PDF (דוגמה)
pdf_content = """
Bible = Old Testament + New Testament
New Testament: 4 Gospels written by Evangelists: Matthew, Mark, Luke, John.
"""

def check_answer(question, options):
    """בודק את השאלה מול מאגר המידע"""
    question = question.lower()
    
    if any(term in question for term in ["מי כתב את הבשורות", "who wrote the gospels"]):
        evangelists = ["matthew", "mark", "luke", "john", "מתי", "מרקוס", "לוקאס", "יוחנן"]
        for i, option in enumerate(options):
            if any(evangelist in option.lower() for evangelist in evangelists):
                return chr(1488 + i) + ". " + option  
    return "אין לי את המידע הזה בתוך ה-PDF"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def get_answer():
    try:
        data = request.json
        question = data.get('question', '')
        options = data.get('options', [])
        
        if not question or len(options) < 4:
            return jsonify({'error': 'Question and at least 4 options are required'}), 400
            
        answer = check_answer(question, options)
        return jsonify({'answer': answer})
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
