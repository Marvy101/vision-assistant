from flask import Flask, request, send_file
from main import process_file, process_text_to_speech
import tempfile
import os

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
            :root {
                --primary-color: #2563eb;
                --secondary-color: #1e40af;
                --success-color: #16a34a;
                --code-bg: #1e293b;
                --code-color: #e2e8f0;
                --border-radius: 8px;
            }
            
            body {
                font-family: system-ui, -apple-system, sans-serif;
                line-height: 1.6;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
                color: #1a1a1a;
                background-color: #f8fafc;
            }

            h1, h2, h3, h4 {
                color: #0f172a;
                margin-top: 2em;
            }

            h1 {
                font-size: 2.5em;
                text-align: center;
                color: var(--primary-color);
                margin-bottom: 1.5em;
            }

            .endpoint {
                background-color: white;
                padding: 2em;
                border-radius: var(--border-radius);
                margin: 20px 0;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
                border: 1px solid #e5e7eb;
            }

            .method {
                background-color: #f97316;
                color: white;
                font-weight: 600;
                padding: 0.3em 0.8em;
                border-radius: 4px;
                font-size: 0.9em;
            }

            .url {
                color: var(--primary-color);
                font-family: 'Menlo', monospace;
                font-weight: 500;
            }

            .parameter {
                margin-left: 20px;
                background-color: #f8fafc;
                padding: 1em;
                border-radius: var(--border-radius);
                border: 1px solid #e5e7eb;
            }

            .parameter strong {
                color: var(--secondary-color);
            }

            .copy-wrapper {
                position: relative;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .copy-button {
                background-color: #e5e7eb;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 0.8em;
                transition: background-color 0.2s;
            }

            .copy-button:hover {
                background-color: #d1d5db;
            }

            code {
                background-color: var(--code-bg);
                color: var(--code-color);
                padding: 0.3em 0.5em;
                border-radius: 4px;
                font-family: 'Menlo', monospace;
                font-size: 0.9em;
            }

            pre code {
                display: block;
                padding: 1em;
                overflow-x: auto;
                line-height: 1.5;
                border-radius: var(--border-radius);
            }

            .api-key {
                background-color: #f0fdf4;
                padding: 1.5em;
                border-radius: var(--border-radius);
                margin: 1em 0;
                border: 1px solid #bbf7d0;
            }

            .api-key code {
                background-color: #dcfce7;
                color: var(--success-color);
            }

            .error-list {
                list-style: none;
                padding: 0;
            }

            .error-list li {
                padding: 0.5em 1em;
                margin-bottom: 0.5em;
                background-color: #fee2e2;
                border-radius: 4px;
                border-left: 4px solid #ef4444;
            }

            .notes-list {
                list-style: none;
                padding: 0;
            }

            .notes-list li {
                padding: 0.5em 1em;
                margin-bottom: 0.5em;
                background-color: #e0f2fe;
                border-radius: 4px;
                border-left: 4px solid var(--primary-color);
            }
        </style>
        <script>
            function copyToClipboard(text) {
                navigator.clipboard.writeText(text).then(() => {
                    const button = event.target;
                    const originalText = button.textContent;
                    button.textContent = 'Copied!';
                    setTimeout(() => {
                        button.textContent = originalText;
                    }, 2000);
                });
            }
        </script>
    </head>
    <body>
        <h1>Vision Assistant API Documentation</h1>
        
        <h2>Base URL</h2>
        <div class="api-key">
            <div class="copy-wrapper">
                <p><strong>Base URL:</strong> <code>https://vision-assistant-sepia.vercel.app/</code></p>
                <button class="copy-button" onclick="copyToClipboard('https://vision-assistant-sepia.vercel.app/')">Copy URL</button>
            </div>
        </div>

        <h2>Authentication</h2>
        <div class="api-key">
            <div class="copy-wrapper">
                <p><strong>API Key:</strong> <code>wearewinningthiscompetition</code></p>
                <button class="copy-button" onclick="copyToClipboard('wearewinningthiscompetition')">Copy Key</button>
            </div>
            <div class="copy-wrapper">
                <p>Include this key in the request headers as: <code>key: wearewinningthiscompetition</code></p>
                <button class="copy-button" onclick="copyToClipboard('key: wearewinningthiscompetition')">Copy Header</button>
            </div>
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
            <div class="copy-wrapper">
                <pre><code>curl -X POST \\
    -H "key: wearewinningthiscompetition" \\
    -F "image=@path/to/your/image.jpg" \\
    -F "past_context=I am about to cross the road what should I look out for?" \\
    https://vision-assistant-sepia.vercel.app/vision</code></pre>
                <button class="copy-button" onclick="copyToClipboard('curl -X POST \\\n    -H \"key: wearewinningthiscompetition\" \\\n    -F \"image=@path/to/your/image.jpg\" \\\n    -F \"past_context=I am about to cross the road what should I look out for?\" \\\n    https://vision-assistant-sepia.vercel.app/vision')">Copy cURL</button>
            </div>

            <h4>Response Format:</h4>
            <div class="copy-wrapper">
                <pre><code>{
    "description": "Detailed description of what the person is seeing",
    "read_out": "Optional transcribed text if present in the image"
}</code></pre>
                <button class="copy-button" onclick="copyToClipboard('{\n    \"description\": \"Detailed description of what the person is seeing\",\n    \"read_out\": \"Optional transcribed text if present in the image\"\n}')">Copy JSON</button>
            </div>
        </div>

        <h2>Error Responses</h2>
        <div class="endpoint">
            <ul class="error-list">
                <li><strong>401:</strong> Invalid API key</li>
                <li><strong>400:</strong> No image file provided or empty file</li>
                <li><strong>500:</strong> Server error during processing</li>
            </ul>
        </div>

        <h2>Notes</h2>
        <ul class="notes-list">
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
        
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    # Check API key
    if request.headers.get('key') != API_KEY:
        return {'error': 'Invalid API key'}, 401

    # Get text and voice from request
    data = request.get_json()
    if not data or 'text' not in data:
        return {'error': 'No text provided'}, 400
    
    text = data['text']
    voice = data.get('voice', 'alloy')  # Default to alloy if no voice specified

    # Process the request
    audio_data, status_code = process_text_to_speech(text, voice)
    
    # If there was an error, return it
    if status_code != 200:
        return audio_data, status_code

    try:
        # Create a temporary file for the speech
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            # Write the audio data to the file
            temp_file.write(audio_data)
            temp_file.flush()
            
            # Send the file back to the client
            return send_file(
                temp_file.name,
                mimetype='audio/mpeg',
                as_attachment=True,
                download_name='speech.mp3'
            )
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_file.name)
        except:
            pass

if __name__ == '__main__':
    app.run(debug=True)