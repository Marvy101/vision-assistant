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

@app.route('/vision-docs')
def vision_docs():
    docs = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vision Assistant API Documentation</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .endpoint {
                background-color: #f5f5f5;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .method {
                color: #e67e22;
                font-weight: bold;
            }
            .url {
                color: #2980b9;
            }
            .parameter {
                margin-left: 20px;
            }
            code {
                background-color: #f0f0f0;
                padding: 2px 5px;
                border-radius: 3px;
            }
            .api-key {
                background-color: #e8f5e9;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <h1>Vision Assistant API Documentation</h1>
        
        <h2>Authentication</h2>
        <div class="api-key">
            <p><strong>API Key:</strong> <code>wearewinningthiscompetition</code></p>
            <p>Include this key in the request headers as: <code>key: wearewinningthiscompetition</code></p>
        </div>

        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <h3><span class="method">POST</span> <span class="url">/vision</span></h3>
            <p>Process an image and get a detailed description suitable for visually impaired users.</p>
            
            <h4>Request</h4>
            <p><strong>Content-Type:</strong> multipart/form-data</p>
            
            <h4>Parameters:</h4>
            <div class="parameter">
                <p><strong>image</strong> (required)<br>
                The image file to be processed</p>
                
                <p><strong>past_context</strong> (optional)<br>
                Previous context or specific questions to consider when describing the image</p>
            </div>

            <h4>Example Request using cURL:</h4>
            <pre><code>curl -X POST \\
    -H "key: wearewinningthiscompetition" \\
    -F "image=@path/to/your/image.jpg" \\
    -F "past_context=I am about to cross the road what should I look out for?" \\
    http://your-server/vision</code></pre>

            <h4>Response Format:</h4>
            <pre><code>{
    "description": "Detailed description of what the person is seeing",
    "read_out": "Optional transcribed text if present in the image"
}</code></pre>
        </div>

        <h2>Error Responses</h2>
        <div class="endpoint">
            <ul>
                <li><strong>401:</strong> Invalid API key</li>
                <li><strong>400:</strong> No image file provided or empty file</li>
                <li><strong>500:</strong> Server error during processing</li>
            </ul>
        </div>

        <h2>Notes</h2>
        <ul>
            <li>The API is designed to provide detailed descriptions for visually impaired users</li>
            <li>Images are processed using advanced AI to generate natural, context-aware descriptions</li>
            <li>When providing past_context, the description will be tailored to address specific concerns or questions</li>
            <li>Text in images will be transcribed when it's crucial to understanding the content</li>
        </ul>
    </body>
    </html>
    """
    return docs

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