from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64

load_dotenv()

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Optimized for speed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    image_data = data.get('image')
    
    contents = []
    
    if image_data:
        # Remove data URL prefix
        image_base64 = image_data.split(',')[1]
        contents.append({
            'parts': [
                {'text': user_message or 'What do you see in this image?'},
                {'inline_data': {
                    'mime_type': 'image/jpeg',
                    'data': image_base64
                }}
            ]
        })
        model = "gemini-2.5-flash"
    else:
        contents = user_message
        model = "gemini-2.5-flash"
    
    # Generate bot response
    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(contents)
    
    return jsonify({'response': response.candidates[0].content.parts[0].text})

if __name__ == '__main__':
    app.run(debug=False, threaded=True)