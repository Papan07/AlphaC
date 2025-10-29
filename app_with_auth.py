from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure Gemini
gemini_client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        # Generate bot response
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        
        bot_message = response.candidates[0].content.parts[0].text
        
        return jsonify({'response': bot_message})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)