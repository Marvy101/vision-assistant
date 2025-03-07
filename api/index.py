from flask import Flask, request
from main import process_file

app = Flask(__name__)

API_KEY = 'wearewinningthiscompetition'

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'

@app.route('/vision', methods=['POST'])
def upload_file():
    # Check API key
    if request.headers.get('key') != API_KEY:
        return {'error': 'Invalid API key'}, 401

    if 'image' not in request.files:
        return {'error': 'No image file provided'}, 400
    
    file = request.files['image']
    if file.filename == '':
        return {'error': 'No selected file'}, 400
    
    # Get past_context from form data if provided
    past_context = request.form.get('past_context', None)
    
    if file:
        try:
            # Process the file using the function from main.py
            result = process_file(file, past_context)
            return result
        except Exception as e:
            return {'error': str(e)}, 500
        
if __name__ == '__main__':
    app.run(debug=True)